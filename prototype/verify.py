"""Check the rendered lesson's timing, equations, audio, and visual boundaries."""
from pathlib import Path
import array
import json
import math
import subprocess
import sys
import wave
import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    video = ROOT / "output" / "like_terms.mp4"
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)
    ]))
    streams = {s["codec_type"]: s for s in probe["streams"]}
    assert "video" in streams and "audio" in streams
    assert streams["video"]["width"] == 1280 and streams["video"]["height"] == 720
    assert streams["video"]["pix_fmt"] == "yuv420p"
    assert streams["video"]["avg_frame_rate"] == "30/1"
    timeline = json.loads((ROOT / "timeline.json").read_text())
    expected = sum(s["duration"] for s in timeline)
    actual = float(probe["format"]["duration"])
    assert 60 <= actual <= 90
    assert abs(expected - actual) <= 0.15, (expected, actual)
    assert abs(float(streams['video']['duration']) - float(streams['audio']['duration'])) <= 0.2
    boundaries = json.loads((ROOT / "output" / "layout_checks.json").read_text())
    assert len(boundaries) == len(timeline) == 9
    for declared, rendered in zip(timeline, boundaries):
        assert declared["id"] == rendered["scene"]
        assert abs(declared["start"] - rendered["start"]) <= 0.07
    x,a,b = sp.symbols("x a b", real=True)
    expressions = [
        (2*x**2+3*x**2,5*x**2),
        (a*x**2+b*x**2,(a+b)*x**2),
        (x**2*x**2,x**4),
        (4*x**2+2*x**2,6*x**2)
    ]
    assert all(sp.simplify(left-right) == 0 for left,right in expressions)
    audio_checks=[]
    for segment in timeline:
        with wave.open(str(ROOT/'audio'/f"{segment['id']}.wav")) as wav:
            assert wav.getsampwidth()==2
            samples=array.array('h',wav.readframes(wav.getnframes()))
            if sys.byteorder != 'little': samples.byteswap()
        peak=max(abs(x) for x in samples)
        rms=math.sqrt(sum(x*x for x in samples)/len(samples))
        assert rms>100, 'Missing or effectively silent narration'
        assert peak<32767, 'Clipped narration samples'
        audio_checks.append({'scene':segment['id'],'peak':peak,'rms':round(rms,1)})
    # Decode the complete final artifact, not only the source narration.
    subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
    result={
        'status':'passed', 'duration_seconds':actual,'resolution':'1280x720',
        'fps':30,'video_codec':streams['video']['codec_name'],
        'audio_codec':streams['audio']['codec_name'],
        'scenes':9,'equation_identities_checked':len(expressions),
        'timing_and_boundary_checks':'passed','full_media_decode':'passed',
        'audio_signal_checks':audio_checks,
        'limitations':['Synthetic narration; human listening review pending.',
                       'Teacher approval and learner testing pending.',
                       'Boundary checks do not replace visual inspection.']
    }
    (ROOT/'output'/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='audio_signal_checks'},indent=2))


if __name__=='__main__':
    main()
