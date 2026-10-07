"""Synthesize sentence clips, then calibrate speech and pauses to exactly 1200 s."""
import json, re, hashlib, subprocess, math
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as rt
from kokoro_onnx import Kokoro
R=Path(__file__).resolve().parent
def stamp(t):
    ms=round(t*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
    return f'{h:02}:{m:02}:{s:02}.{ms:03}'
def main():
    lesson=json.loads((R/'lesson.json').read_text())
    opts=rt.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
    session=rt.InferenceSession(str(R/'models/kokoro-v1.0.onnx'),sess_options=opts,providers=['CPUExecutionProvider'])
    k=Kokoro.from_session(session,str(R/'models/voices-v1.0.bin'))
    beats=[];total=0
    for chapter in lesson['chapters']:
        for b in chapter['beats']:
            sentences=re.split(r'(?<=[.!?])\s+',b['narration'].strip())
            clips=[]
            for i,sentence in enumerate(sentences):
                h=hashlib.sha256(('af_heart|0.85|'+sentence).encode()).hexdigest()[:12]
                p=R/'audio'/f'raw_{h}.wav'
                if not p.exists():
                    a,sr=k.create(sentence,voice='af_heart',speed=.85,lang='en-us')
                    sf.write(p,a,sr)
                info=sf.info(p)
                clips.append({'text':sentence,'file':str(p),'raw_duration':info.duration})
                total+=info.duration
            beats.append({**b,'chapter':chapter['id'],'chapter_title':chapter['title'],'sentences':clips})
            print('Synthesized',b['id'],round(sum(c['raw_duration'] for c in clips),2),flush=True)
    # Each beat has an audio lead and closing visual hold; questions add explicit thinking time.
    fixed=sum(.5+.6+b['thinking_pause_seconds'] for b in beats)
    factor=total/(1200-fixed)
    assert .70<factor<1.25, f'Pacing needs editorial adjustment, atempo={factor}'
    sr=24000; output=[];cursor=0.;vtt=['WEBVTT',''];timeline=[]
    for b in beats:
        start=cursor;parts=[np.zeros(round(.5*sr),dtype=np.float32)];local=.5;sentences=[]
        for c in b['sentences']:
            dest=R/'audio'/('paced_'+Path(c['file']).name)
            subprocess.run(['ffmpeg','-v','error','-y','-i',c['file'],'-af',f'atempo={factor:.9f}','-ar',str(sr),str(dest)],check=True)
            a,_=sf.read(dest,dtype='float32');d=len(a)/sr
            sentences.append({'text':c['text'],'start':local,'duration':d})
            vtt += [f'{stamp(start+local)} --> {stamp(start+local+d)}',c['text'],'']
            parts.append(a);local+=d
        tail=.6+b['thinking_pause_seconds'];local+=tail
        # Frame alignment prevents accumulated rounding drift across chapters.
        nframes=math.ceil(local*30);duration=nframes/30
        spoken=np.concatenate(parts)
        needed=round(duration*sr)-len(spoken)
        assert needed>=0
        a=np.concatenate([spoken,np.zeros(needed,dtype=np.float32)])
        sf.write(R/'audio'/f"beat_{b['id']}.wav",a,sr)
        output.append(a);cursor+=duration
        timeline.append({'id':b['id'],'chapter':b['chapter'],'chapter_title':b['chapter_title'],'start':start,'duration':duration,'speech_end':sentences[-1]['start']+sentences[-1]['duration'],'sentences':sentences,'thinking_pause_seconds':b['thinking_pause_seconds']})
    # ffmpeg atempo can shorten clips slightly. Allocate the small residual evenly as visual holds.
    residual=1200-cursor
    if abs(residual)>15: raise ValueError(f'Unexpected timing drift {residual}')
    frames=round(residual*30)
    # Rebuild beat lengths exactly; never trim speech or a requested thinking pause.
    for i in range(abs(frames)):
        ix=i%len(timeline);delta=(1 if frames>0 else -1)/30
        timeline[ix]['duration']+=delta
    cursor=0;out=[];vtt=['WEBVTT','']
    for t,a in zip(timeline,output):
        t['start']=cursor;n=round(t['duration']*sr)
        assert t['duration']>=t['speech_end']+t['thinking_pause_seconds']+.1
        a=np.pad(a,(0,max(0,n-len(a))))[:n];out.append(a)
        sf.write(R/'audio'/f"beat_{t['id']}.wav",a,sr)
        for s in t['sentences']:vtt += [f"{stamp(cursor+s['start'])} --> {stamp(cursor+s['start']+s['duration'])}",s['text'],'']
        cursor+=t['duration']
    audio=np.concatenate(out)
    assert len(audio)==1200*sr
    sf.write(R/'audio/narration.wav',audio,sr)
    (R/'timeline.json').write_text(json.dumps(timeline,indent=2))
    (R/'output/captions.vtt').write_text('\n'.join(vtt))
    (R/'audio_report.json').write_text(json.dumps({'voice':'Kokoro af_heart','synthesis_speed':.85,'atempo':factor,'raw_speech_seconds':total,'final_duration':len(audio)/sr,'sentence_count':sum(len(t['sentences']) for t in timeline),'word_count':sum(len(b['narration'].split()) for b in beats),'peak':float(np.max(np.abs(audio))),'rms':float(np.sqrt(np.mean(audio**2))),'sync':'Measured sentence boundaries; within-sentence visual cues use word-position estimates.'},indent=2))
    print('Complete',len(audio)/sr,'seconds; tempo factor',factor,flush=True)
if __name__=='__main__':main()
