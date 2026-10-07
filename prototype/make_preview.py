"""Extract review frames from the exported video, including tile motion."""
from pathlib import Path
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
shots=ROOT/'output/frames'
shots.mkdir(exist_ok=True)
timeline=json.loads((ROOT/'timeline.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
canvas=Image.new('RGB',(1280,3*278),'#101a2b')
for i,seg in enumerate(timeline):
    t=seg['start']+min(seg['duration']-1,5.7)
    file=shots/f"{i+1:02}_{seg['id']}.jpg"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(ROOT/'output/like_terms.mp4'),'-frames:v','1',str(file)],check=True)
    im=Image.open(file).resize((426,240))
    x=(i%3)*426;y=(i//3)*278
    canvas.paste(im,(x,y))
    ImageDraw.Draw(canvas).text((x+10,y+247),f"{seg['id']} / {t:.1f}s",font=font,fill='white')
canvas.save(ROOT/'output/contact_sheet.jpg')
Image.open(shots/'04_combine.jpg').save(ROOT/'output/poster.jpg')
for t in [23.0,23.8,24.4]:
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(ROOT/'output/like_terms.mp4'),'-frames:v','1',str(shots/f'motion_{t}.jpg')],check=True)
print('Saved nine scene frames, three motion frames, poster, and contact sheet.')
