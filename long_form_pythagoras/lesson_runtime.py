"""Measured narration timing and shared visual style for generated Manim scenes."""
from manim import *
from pathlib import Path
import json, math, re

ROOT=Path(__file__).resolve().parent
BG='#0B1220'; INK='#F3F5F7'; MUTED='#A9B6CA'; TEAL='#57D6BF'; GOLD='#FFD17C'; PINK='#F08CA9'; GRID='#29394F'
config.background_color=BG

def txt(s,size=28,color=INK):
    return Text(s,font='Lato',font_size=size,color=color)

def eq(s,size=42,color=INK):
    return MathTex(s,font_size=size,color=color)

def fit(m,width=6.5,height=4.7,center=(-2.8,-.1,0)):
    factor=min(1,width/max(m.width,.001),height/max(m.height,.001))
    m.scale(factor).move_to(center)
    return m

class LessonScene(Scene):
    def chapter(self,n):
        self.chapter_number=n
        self.timeline={t['id']:t for t in json.loads((ROOT/'timeline.json').read_text())}
        self.lesson=json.loads((ROOT/'lesson.json').read_text())
        ch=self.lesson['chapters'][n-1]
        self.chapter_start=self.timeline[ch['beats'][0]['id']]['start']
        self.records=[];self.cue_records=[]
        title=txt(ch['title'],34)
        if title.width>11.7:title.scale_to_fit_width(11.7)
        title.move_to([-6.45,2.94,0],aligned_edge=LEFT)
        eyebrow=txt('THE GEOMETRY OF A SHORTCUT',16,TEAL).move_to([-6.45,3.53,0],aligned_edge=LEFT)
        number=txt(f'{n:02} / 10',18,MUTED).move_to([6.12,3.5,0])
        self.chrome=VGroup(title,eyebrow,number,Line([-6.45,2.45,0],[6.45,2.45,0],color=GRID),Line([-6.45,-2.7,0],[6.45,-2.7,0],color=GRID))
        self.add(self.chrome)
        self.panel=VGroup()
    def begin(self,beat_id):
        self.current=self.timeline[str(beat_id).zfill(2)]
        self.beat_start=self.current['start']-self.chapter_start
        self.until(self.beat_start)
    def until(self,t):
        delta=t-self.renderer.time
        if delta>1/config.frame_rate:
            self.wait(round(delta*config.frame_rate)/config.frame_rate)
    def cue(self,phrase,*animations,run_time=1.2):
        norm=lambda s:re.sub(r'[^a-z0-9 ]','',s.lower())
        needle=norm(phrase);offset=None
        for sentence in self.current['sentences']:
            hay=norm(sentence['text'])
            if needle in hay:
                pos=hay.index(needle)
                offset=sentence['start']+sentence['duration']*len(hay[:pos].split())/max(1,len(hay.split()))
                break
        if offset is None: raise ValueError(f'Cue not found in beat {self.current["id"]}: {phrase}')
        target=self.beat_start+offset
        self.cue_records.append({'beat':self.current['id'],'phrase':phrase,'target':target,'actual_before_wait':self.renderer.time})
        self.until(target)
        if animations:self.play(*animations,run_time=run_time)
    def panel_to(self,*items):
        new=VGroup(*items).arrange(DOWN,buff=.4,aligned_edge=LEFT)
        fit(new,5.15,4.3,(3.7,-.05,0))
        old=self.panel;self.panel=new
        # Remove old writing before revealing new writing; crossfading both creates
        # a brief but unreadable overlap even when endpoint layouts are correct.
        return Succession(FadeOut(old),FadeIn(new))
    def finish(self):
        target=self.beat_start+self.current['duration']
        if self.renderer.time>target+.05:raise ValueError(f'Beat overrun {self.current["id"]}: {self.renderer.time-target}')
        self.until(target)
        violations=[]
        for m in self.mobjects:
            if m is self.chrome:continue
            if m.width<.001 and m.height<.001:continue
            box=[float(m.get_left()[0]),float(m.get_right()[0]),float(m.get_bottom()[1]),float(m.get_top()[1])]
            if box[0]<-6.8 or box[1]>6.8 or box[2]<-2.65 or box[3]>2.4:
                violations.append({'type':type(m).__name__,'bbox':box})
        self.records.append({'beat':self.current['id'],'time':self.renderer.time,'bounds_violations':violations})
    def done(self):
        (ROOT/'output'/f'chapter_{self.chapter_number:02}_audit.json').write_text(json.dumps({'bounds':self.records,'cues':self.cue_records},indent=2))
