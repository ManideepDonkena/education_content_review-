"""Record final acceptance evidence and package editable source, excluding caches."""
import json,re,hashlib,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent
probe=json.loads((R/'output/media_probe.json').read_text())
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert v['width']==1920 and v['height']==1080 and int(v['nb_frames'])==36000
assert v['r_frame_rate']=='30/1' and a['sample_rate']=='48000'
assert len(probe['chapters'])==10 and abs(float(probe['format']['duration'])-1200)<.034
assert any(s['codec_type']=='subtitle' for s in probe['streams'])
assert 'Exported and decoded complete' in (R/'export.log').read_text()
audits=[json.loads(p.read_text()) for p in sorted((R/'output').glob('chapter_*_audit.json'))]
assert len(audits)==10
assert sum(len(j['bounds']) for j in audits)==40
assert not any(b['bounds_violations'] for j in audits for b in j['bounds'])
def sec(s):
    h,m,z=s.split(':');return int(h)*3600+int(m)*60+float(z)
caps=re.findall(r'(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})',(R/'output/captions.vtt').read_text())
prev=0
for start,end in caps:
    start,end=sec(start),sec(end);assert start>=prev-.002 and start<end<=1200;prev=end
assert len(caps)==274
levels=(R/'output/audio_levels.txt').read_text()
maximum=float(re.search(r'max_volume: ([-\d.]+) dB',levels)[1]);assert maximum<0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((R/'build_manifest.json').read_text())
manifest['source_sha256']={name:sha(R/name) for name in manifest['source_sha256']}
manifest['video_sha256']=sha(R/'output/pythagoras_20min.mp4')
(R/'build_manifest.json').write_text(json.dumps(manifest,indent=2))
report={'status':'technical_checks_passed','duration_seconds':float(probe['format']['duration']),'video_frames':36000,'resolution':[1920,1080],'fps':30,'audio_codec':a['codec_name'],'audio_sample_rate':48000,'audio_max_dbfs':maximum,'captions':len(caps),'chapters':10,'full_ffmpeg_decode':'passed','beat_end_bounds_checks':40,'bounds_violations':0,'animation_anchors':sum(len(j['cues']) for j in audits),'mathematical_checks':'passed; see math_checks.json and render_geometry_checks.json','visual_review':'120 preview samples and120 final-resolution chapter samples reviewed; repaired angle-motion sample inspected separately','review_limits':['Not every frame visually inspected','Sentence-based synchronization; within-sentence positions estimated','No teacher approval, learner study or continuous human listening review'],'video_sha256':manifest['video_sha256']}
(R/'output/final_checks.json').write_text(json.dumps(report,indent=2))
with zipfile.ZipFile(R/'output/editable_lesson_source.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in R.rglob('*'):
        rel=p.relative_to(R)
        if any(x in rel.parts for x in ['.tts','models','media','media_rest','audio','__pycache__','frames']):continue
        if p.is_file() and p.suffix in ['.py','.json','.md','.html','.vtt','.txt']:
            z.write(p,rel)
print(json.dumps(report,indent=2))
