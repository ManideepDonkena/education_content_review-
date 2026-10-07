"""Export the editable narrative, storyboard and local chapter player."""
import json, html
from pathlib import Path
R=Path(__file__).resolve().parent
def main():
    lesson=json.loads((R/'lesson.json').read_text()); ts=json.loads((R/'timeline.json').read_text()); times={t['id']:t for t in ts}
    def fmt(t):return f'{int(t)//60:02}:{int(t)%60:02}'
    narrative=['# '+lesson['title'],'','Original premium-model draft, reviewed and rendered by the coding agent. Synthetic English narration.','']
    board=['# Narrative storyboard and visualization script','','Timings below are measured from synthesized audio; within-sentence action timing is approximate.','']
    buttons=[]
    for ch in lesson['chapters']:
        start=times[ch['beats'][0]['id']]['start'];title=ch['title']
        narrative += [f"## {fmt(start)} — {title}",'']
        buttons.append(f'<button data-time="{start}"><span>{fmt(start)}</span> {html.escape(title)}</button>')
        for b in ch['beats']:
            t=times[b['id']]
            narrative += [b['narration'],'']
            if b['thinking_pause_seconds']:narrative += [f"[Thinking pause: {b['thinking_pause_seconds']} seconds]",'']
            board += [f"## Beat {b['id']} · {fmt(t['start'])}–{fmt(t['start']+t['duration'])}",'',f"**Teaching purpose:** {b['check']}",'',f"**Narration:** {b['narration']}",'',f"**Rendered visualization:** {b['visual']}",'',f"**Reference equation:** `{b['equation']}`",'',f"**Thinking pause:** {b['thinking_pause_seconds']} seconds.",'']
            audit_path=R/'output'/f"chapter_{ch['id']:02}_audit.json"
            if audit_path.exists():
                cues=[q for q in json.loads(audit_path.read_text())['cues'] if q['beat']==b['id']]
                board += ['**Animation anchors in the narration:**','']
                for q in cues:board += [f"- {fmt(start+max(q['target'],q['actual_before_wait']))}: {q['phrase']}"]
                board += ['']
    (R/'narrative.md').write_text('\n'.join(narrative));(R/'storyboard.md').write_text('\n'.join(board))
    (R/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The geometry of a shortcut</title><style>body{margin:0;background:#0b1220;color:#f3f5f7;font:17px system-ui}main{max-width:1300px;margin:auto;padding:28px}h1{font-size:34px;margin:8px 0}p{color:#a9b6ca;line-height:1.5}.layout{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:20px}video{width:100%;background:#000;border-radius:12px}button{display:block;width:100%;text-align:left;padding:13px;border:1px solid #29394f;background:#111e31;color:#f3f5f7;border-radius:7px;margin-bottom:7px;cursor:pointer}button:hover{border-color:#57d6bf}button span{color:#57d6bf;font-variant-numeric:tabular-nums;margin-right:8px}a{color:#57d6bf}video::cue{font:24px sans-serif;background:#0b1220e8}small{color:#a9b6ca}@media(max-width:850px){.layout{grid-template-columns:1fr}}</style><main><small>ORIGINAL EXPLANATORY LESSON · 20 MINUTES</small><h1>The geometry of a shortcut</h1><p>Why the Pythagorean theorem works — from a route across a floor to an area proof, worked examples and your own reasoning.</p><div class="layout"><section><video id="lesson" controls preload="metadata"><source src="output/pythagoras_20min.mp4" type="video/mp4"><track default kind="captions" src="output/captions.vtt" srclang="en" label="English"></video><p><a href="output/pythagoras_20min.mp4" download>Download video</a> · <a href="narrative.md">Narrative</a> · <a href="storyboard.md">Storyboard</a> · <a href="research/teacher_comparison.md">Ten source explanations</a></p><small>Neutral synthetic voice. Mathematical and technical checks are documented separately; teacher and learner evaluation remains pending.</small></section><nav>'''+''.join(buttons)+'''</nav></div></main><script>const video=document.getElementById('lesson');document.querySelectorAll('button[data-time]').forEach(b=>b.onclick=()=>{video.currentTime=Number(b.dataset.time);video.play()});</script></html>''')
    print('Narrative, storyboard and player exported')
if __name__=='__main__':main()
