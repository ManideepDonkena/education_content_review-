import json, subprocess, sys
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
profile=sys.argv[1] if len(sys.argv)>1 else '480p30'
timeline=json.loads((R/'timeline.json').read_text())
out=R/'output'/'frames';out.mkdir(exist_ok=True)
for n in ([int(sys.argv[2])] if len(sys.argv)>2 else range(1,11)):
    matches=[p for root in [R/'media/videos',R/'media_rest/videos'] for p in root.glob(f'*/{profile}/C{n:02}.mp4')]
    if not matches:continue
    ts=[t for t in timeline if t['chapter']==n];origin=ts[0]['start'];thumbs=[]
    for t in ts:
        for fraction in [.25,.6,.93]:
            local=t['start']-origin+fraction*t['duration']
            p=out/f"{profile}_C{n:02}_beat{t['id']}_{int(fraction*100)}.jpg"
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(local),'-i',str(matches[0]),'-frames:v','1','-q:v','2',str(p)],check=True)
            im=Image.open(p).convert('RGB');im.thumbnail((380,214))
            card=Image.new('RGB',(380,240),'#111e31');card.paste(im,(0,24));ImageDraw.Draw(card).text((8,5),f"Beat {t['id']}  |  lesson {int(t['start']+fraction*t['duration'])//60:02}:{int(t['start']+fraction*t['duration'])%60:02}",fill='white');thumbs.append(card)
    sheet=Image.new('RGB',(1140,960),'#0b1220')
    for ix,im in enumerate(thumbs):sheet.paste(im,((ix%3)*380,(ix//3)*240))
    sheet.save(R/'output'/f'{profile}_chapter_{n:02}.jpg',quality=90)
    print('Chapter',n,flush=True)
