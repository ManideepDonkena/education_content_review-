"""A deterministic Manim lesson: identical quantities combine by distributivity.

Run build_audio.py first. Timings are measured from audio, not estimated.
"""
from pathlib import Path
import json
import textwrap
from manim import *

ROOT = Path(__file__).resolve().parent
BG = "#101A2B"
INK = "#F4F4EF"
MUTED = "#A9B8CB"
TEAL = "#65D7C0"
GOLD = "#FFCA7A"
LINE = "#2B3C55"
config.background_color = BG
config.frame_rate = 30


def label(text, size=24, color=INK):
    return Text(text, font="Lato", font_size=size, color=color)


def formula(*parts, size=46):
    m = MathTex(*parts, font_size=size, color=INK)
    m.set_color_by_tex("x^2", TEAL, substring=False)
    return m


def tile(point):
    square = Square(side_length=1.05, stroke_color=TEAL, stroke_width=2,
                    fill_color=TEAL, fill_opacity=0.13)
    area = formula("x^2", size=35)
    return VGroup(square, area).move_to(point)


class LikeTerms(Scene):
    def construct(self):
        self.timeline = json.loads((ROOT / "timeline.json").read_text())
        self.safe_records = []
        self.content = VGroup()
        self.subtitle = VGroup()
        self.header = label("MATH  /  CONCEPT 01", 17, TEAL).to_corner(UL, buff=0.55)
        self.heading = label("Why like terms combine", 36).next_to(self.header, DOWN, aligned_edge=LEFT, buff=0.23)
        self.topline = Line([-6.55, 2.48, 0], [6.55, 2.48, 0], color=LINE)
        self.footer = Line([-6.55, -2.48, 0], [6.55, -2.48, 0], color=LINE)
        self.page = label("01 / 09", 17, MUTED).to_corner(UR, buff=0.55)
        self.add(self.header, self.heading, self.topline, self.footer, self.page)

        self.begin(0)
        q = formula("2", "x^2", "+", "3", "x^2", "=", "?", size=66).move_to([0, 0.5, 0])
        q[0].set_color(GOLD); q[3].set_color(GOLD)
        prompt = label("What changes?  What stays the same?", 26, MUTED).move_to([0, -0.8, 0])
        self.play(Write(q), FadeIn(prompt, shift=UP*0.15), run_time=1.4)
        self.content = VGroup(q, prompt)
        self.finish()

        self.begin(1, clear=True)
        square = Square(side_length=1.7, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.13).move_to([-2, 0.25, 0])
        inside = formula("x^2", size=54).move_to(square)
        side = formula("x", size=36).next_to(square, LEFT, buff=0.2)
        bottom = formula("x", size=36).next_to(square, DOWN, buff=0.2)
        explain = VGroup(label("ONE IDENTICAL TILE", 20, TEAL), formula(r"\text{area} = x \times x = x^2", size=42), label("For the area picture, x > 0.", 23, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([2.25, 0.2, 0])
        self.play(Create(square), Write(inside), FadeIn(side), FadeIn(bottom), run_time=1.3)
        self.play(FadeIn(explain), run_time=0.7)
        self.content = VGroup(square, inside, side, bottom, explain)
        self.finish()

        self.begin(2, clear=True)
        self.tiles = VGroup(*[tile([p, 0.35, 0]) for p in [-4.35, -3.05, 0.75, 2.05, 3.35]])
        self.left = formula("2", "x^2").move_to([-3.7, -1.05, 0]); self.left[0].set_color(GOLD)
        self.right = formula("3", "x^2").move_to([2.05, -1.05, 0]); self.right[0].set_color(GOLD)
        self.plus = formula("+", size=52).move_to([-1.2, 0.35, 0])
        self.note = label("Same area. Same variable part.", 23, MUTED).move_to([0, 1.6, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.15) for t in self.tiles], lag_ratio=0.15), FadeIn(self.left), FadeIn(self.right), FadeIn(self.plus), FadeIn(self.note), run_time=2)
        self.content = VGroup(self.tiles, self.left, self.right, self.plus, self.note)
        self.finish()

        self.begin(3)
        self.play(FadeOut(self.left), FadeOut(self.right), FadeOut(self.plus), run_time=0.5)
        self.content.remove(self.left, self.right, self.plus)
        self.play(*[t.animate.move_to([x, 0.35, 0]) for t, x in zip(self.tiles, [-2.6,-1.3,0,1.3,2.6])], run_time=2.0)
        result = formula("5", "x^2", size=55).move_to([0,-1.05,0]); result[0].set_color(GOLD)
        self.play(Write(result), run_time=0.7)
        self.content.add(result)
        assert len(self.tiles)==5
        assert all(abs(t[0].width-1.05)<1e-6 and abs(t[0].height-1.05)<1e-6 for t in self.tiles)
        self.finish()

        self.begin(4, clear=True)
        first = formula("2", "x^2", "+", "3", "x^2", size=55).move_to([0,1.35,0])
        second = formula("=", "(2+3)", "x^2", size=55).move_to([0,0.15,0])
        third = formula("=", "5", "x^2", size=55).move_to([0,-1.05,0])
        first[0].set_color(GOLD); first[3].set_color(GOLD); second[1].set_color(GOLD); third[1].set_color(GOLD)
        self.play(Write(first), run_time=0.8)
        self.wait(1)
        self.play(Write(second), run_time=0.9)
        self.wait(1)
        self.play(Write(third), run_time=0.8)
        self.content = VGroup(first,second,third)
        self.finish()

        self.begin(5, clear=True)
        law = formula("a", "x^2", "+", "b", "x^2", "=", "(a+b)", "x^2", size=49).move_to([0,0.8,0])
        for i in [0,3,6]: law[i].set_color(GOLD)
        name = label("THE DISTRIBUTIVE LAW", 20, TEAL).move_to([0,1.9,0])
        rule1 = label("Add the coefficients.", 30, GOLD).move_to([0,-0.3,0])
        rule2 = label("Keep the shared variable part.", 30, TEAL).move_to([0,-0.95,0])
        domain = label("This identity holds for every real x.", 21, MUTED).move_to([0,-1.85,0])
        self.play(FadeIn(name), Write(law), FadeIn(rule1), FadeIn(rule2), FadeIn(domain), run_time=1.7)
        self.content=VGroup(name,law,rule1,rule2,domain)
        self.finish()

        self.begin(6, clear=True)
        left = VGroup(label("ADDITION",21,TEAL),formula("2x^2 + 3x^2 = 5x^2",size=41),label("Count identical quantities.",23,MUTED)).arrange(DOWN,buff=0.4).move_to([-3.35,0.35,0])
        right = VGroup(label("MULTIPLICATION",21,GOLD),formula(r"x^2 \times x^2 = x^4",size=41),label("Multiply the powers.",23,MUTED)).arrange(DOWN,buff=0.4).move_to([3.25,0.35,0])
        divider=Line([0,1.5,0],[0,-1.1,0],color=LINE)
        note=label("The operation matters.",28,INK).move_to([0,-1.8,0])
        self.play(FadeIn(left),Create(divider),run_time=0.8)
        self.wait(2)
        self.play(FadeIn(right),FadeIn(note),run_time=0.8)
        self.content=VGroup(left,right,divider,note)
        self.finish()

        self.begin(7, clear=True)
        title=label("YOUR TURN",21,TEAL).move_to([0,1.8,0])
        question=formula("4", "x^2", "+", "2", "x^2", "=", "?",size=64).move_to([0,0.45,0])
        question[0].set_color(GOLD);question[3].set_color(GOLD)
        prompt=label("Explain what changes and what stays the same.",25,MUTED).move_to([0,-0.8,0])
        pause=label("Pause the video to think.",22,TEAL).move_to([0,-1.65,0])
        self.play(FadeIn(title),Write(question),FadeIn(prompt),FadeIn(pause),run_time=1.3)
        self.content=VGroup(title,question,prompt,pause)
        self.finish()

        self.begin(8, clear=True)
        answer=formula("4", "x^2", "+", "2", "x^2", "=", "6", "x^2",size=61).move_to([0,0.65,0])
        for i in [0,3,6]:answer[i].set_color(GOLD)
        rule=label("Same variable part. Add the coefficients.",29,INK).move_to([0,-0.6,0])
        sub=label("4 + 2 = 6     |     x² stays x²",25,TEAL).move_to([0,-1.45,0])
        self.play(Write(answer),FadeIn(rule),FadeIn(sub),run_time=1.4)
        self.content=VGroup(answer,rule,sub)
        self.finish()
        (ROOT/'output'/'layout_checks.json').write_text(json.dumps(self.safe_records,indent=2)+'\n')

    def begin(self,index,clear=False):
        segment=self.timeline[index]
        self.segment_start=self.time
        self.segment=segment
        # Scene boundaries are continuous; a short visual transition precedes speech.
        if clear:
            # Content children were individually introduced by animations. Clear
            # the scene rather than removing a wrapper that was never added.
            self.clear()
            self.add(self.header,self.heading,self.topline,self.footer)
        self.remove(self.subtitle,self.page)
        self.page=label(f"{index+1:02} / 09",17,MUTED).to_corner(UR,buff=0.55)
        lines=textwrap.wrap(segment['text'],width=72)
        self.subtitle=VGroup(*[label(line,20,INK) for line in lines]).arrange(DOWN,buff=0.10).move_to([0,-3.13,0])
        self.add(self.subtitle,self.page)
        self.add_sound(str(ROOT/'audio'/f"{segment['id']}.wav"),time_offset=0.4)

    def finish(self):
        for item in self.content:
            assert item.get_left()[0] >= -6.6, (self.segment['id'],'left boundary')
            assert item.get_right()[0] <= 6.6, (self.segment['id'],'right boundary')
            assert item.get_top()[1] <= 2.42, (self.segment['id'],'top boundary')
            assert item.get_bottom()[1] >= -2.4, (self.segment['id'],'subtitle overlap')
        assert self.subtitle.width <= 13.1
        assert self.subtitle.get_bottom()[1] >= -3.85
        self.safe_records.append({'scene':self.segment['id'],'boundary_checks':'passed','start':round(self.segment_start,3)})
        remaining=self.segment['duration']-(self.time-self.segment_start)
        assert remaining>=0, (self.segment['id'],'animation exceeds narration slot')
        if remaining > 0:
            # A tiny fraction of a frame avoids floor-rounding off the final
            # frame when a nominal integer frame count is represented in float.
            self.wait((round(remaining*30)+0.01)/30)
