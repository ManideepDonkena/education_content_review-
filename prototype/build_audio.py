"""Generate local draft English narration, measured timings, and caption files.

Uses FFmpeg's installed Flite filter. No network or paid speech service is used.
Replace audio/*.wav with reviewed recordings and rerun with --reuse-audio to
recalculate the animation timing and captions around those recordings.
"""
from pathlib import Path
import argparse
import json
import subprocess
import textwrap
import wave

ROOT = Path(__file__).resolve().parent


def stamp(seconds, separator=","):
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, ms = divmod(ms, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}{separator}{ms:03}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse-audio", action="store_true")
    args = parser.parse_args()
    (ROOT / "audio").mkdir(exist_ok=True)
    (ROOT / "output").mkdir(exist_ok=True)
    segments = json.loads((ROOT / "narration.json").read_text())
    timeline, captions, vtt = [], [], ["WEBVTT\n"]
    elapsed = 0.0
    for number, seg in enumerate(segments, 1):
        txt = ROOT / "audio" / f"{seg['id']}.txt"
        wav = txt.with_suffix(".wav")
        txt.write_text(seg["text"])
        if not args.reuse_audio:
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", f"flite=textfile={txt}:voice=slt",
                "-af", "atempo=0.94", "-ar", "48000", "-ac", "1", str(wav)
            ], check=True)
        with wave.open(str(wav)) as audio:
            duration = audio.getnframes() / audio.getframerate()
        # Round each scene length to a frame boundary to avoid cumulative drift.
        frames = __import__("math").ceil((0.4 + duration + seg["hold"]) * 30)
        scene_duration = frames / 30
        entry = dict(seg, start=elapsed, audio_start=elapsed + 0.4,
                     audio_duration=duration, duration=scene_duration)
        timeline.append(entry)
        cap = "\n".join(textwrap.wrap(seg["text"], width=67))
        captions.append(f"{number}\n{stamp(elapsed+0.4)} --> {stamp(elapsed+0.4+duration)}\n{cap}\n")
        vtt.append(f"{stamp(elapsed+0.4,'.')} --> {stamp(elapsed+0.4+duration,'.')}\n{cap}\n")
        elapsed += scene_duration
    (ROOT / "timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")
    (ROOT / "output" / "like_terms.srt").write_text("\n".join(captions))
    (ROOT / "output" / "like_terms.vtt").write_text("\n".join(vtt))
    print(f"Generated {len(segments)} narration segments; video duration {elapsed:.2f}s")


if __name__ == "__main__":
    main()
