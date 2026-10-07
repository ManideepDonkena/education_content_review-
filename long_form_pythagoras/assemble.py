"""Join ten rendered chapters and mux measured narration, captions and chapters."""
import json, subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
def run(args):subprocess.run(args,check=True)
def main():
    timeline=json.loads((R/'timeline.json').read_text())
    clips=[]
    for n in range(1,11):
        matches=[p for root in [R/'media/videos',R/'media_rest/videos'] for p in root.glob(f'*/1080p30/C{n:02}.mp4')]
        assert len(matches)==1,(n,matches)
        clips.append(matches[0])
    cat=R/'output/concat.txt'
    cat.write_text(''.join("file '"+str(p.resolve()).replace("'","'\\''")+"'\n" for p in clips))
    meta=[';FFMETADATA1','title=The geometry of a shortcut','artist=Original educational lesson; synthetic narration']
    for n in range(1,11):
        ts=[t for t in timeline if t['chapter']==n]
        meta+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(ts[0]['start']*1000)}",f"END={round((ts[-1]['start']+ts[-1]['duration'])*1000)}",f"title={ts[0]['chapter_title']}"]
    (R/'output/chapters.ffmeta').write_text('\n'.join(meta))
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(cat),'-i',str(R/'audio/narration.wav'),'-i',str(R/'output/captions.vtt'),'-i',str(R/'output/chapters.ffmeta'),'-map','0:v:0','-map','1:a:0','-map','2:s:0','-map_metadata','3','-map_chapters','3','-c:v','copy','-af','loudnorm=I=-18:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','192k','-c:s','mov_text','-metadata:s:s:0','language=eng','-t','1200','-movflags','+faststart',str(R/'output/pythagoras_20min.mp4')])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(R/'output/pythagoras_20min.mp4')]))
    (R/'output/media_probe.json').write_text(json.dumps(probe,indent=2))
    assert abs(float(probe['format']['duration'])-1200)<.1
    v=next(x for x in probe['streams'] if x['codec_type']=='video')
    assert (v['width'],v['height'])==(1920,1080)
    assert len(probe['chapters'])==10
    run(['ffmpeg','-v','error','-i',str(R/'output/pythagoras_20min.mp4'),'-f','null','-'])
    print('Exported and decoded complete 20-minute 1080p video')
if __name__=='__main__':main()
