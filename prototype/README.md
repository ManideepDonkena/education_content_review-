# First narrated prototype for like terms

This prototype turns the prepared lesson into an approximately 79-second English teaching clip. It shows a square of area x², two and three equal tiles combining into five, the distributive law, the difference between addition and multiplication, and a short practice question.

## Watch and review

- [Teaching video](output/like_terms.mp4)
- [Local player with chapter links](review.html)
- [Caption file](output/like_terms.srt)
- [Editable Manim scene](like_terms.py)
- [Narration script](narration.json)
- [Measured scene timings](timeline.json)
- [Validation record](output/validation.json)

The narration is synthetic draft English, generated locally using Flite. A teacher's review of the explanation, pronunciation, and classroom pacing is still required. No teacher or student approval is claimed. This is the short first milestone; the full lesson and its five-problem sequence remain in the [lesson draft](../examples/like_terms_lesson.md).

## Build

Run commands from this directory. Python 3.10, FFmpeg with the Flite filter, Cairo/Pango development libraries, LaTeX, dvisvgm, and the Lato font were available on the build machine. The system Python also provides SymPy for `verify.py` and Pillow for `make_preview.py`; install those in your chosen verification environment when rebuilding elsewhere. Manim is pinned in the project environment. See the [official installation guide](https://docs.manim.community/en/stable/installation/uv.html) for platform prerequisites.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
python3 build_audio.py
.venv/bin/python -m manim -r 1280,720 --fps 30 --media_dir media like_terms.py LikeTerms
python3 export_video.py
python3 verify.py
python3 make_preview.py
```

The exact installed Python dependencies are recorded in `requirements.lock.txt`. A build log is retained in `output/render.log`. Generated media caches and the virtual environment are excluded by the local `.gitignore`.

To use teacher recordings, replace the mono PCM WAV files in `audio/`, update the corresponding narration text, and run `python3 build_audio.py --reuse-audio`. Re-render the video so scene durations follow the actual recordings. Audio begins 0.4 seconds after each scene boundary. Increase the hold duration for additional student thinking time.

## Correctness and design checks

The area illustration assumes x > 0. The distributive identity is valid for every real x, as stated in the video. Tile labels and side lengths remain unchanged while regrouping. Golden coefficients and teal variable parts are reinforced by words and equations. The practice answer is revealed after a thinking pause.

Automated checks cover tile geometry, content boundaries, equation identities, timing, decoded audio, and media streams. Rendered sample frames are also inspected. These checks support prototype review; they do not establish learner effectiveness or replace teacher listening and review.

## Questions for the teacher review

1. Can a student explain why the exponent stays unchanged?
2. Is the shift from positive side lengths to the general algebraic identity clear?
3. Are the symbols, voice, captions, and animation pace easy to follow?
4. Does the multiplication comparison clarify the operation without distracting?
5. Can the student answer the final question and explain the answer independently?

Record the scene, issue, and requested change before extending this into the full lesson.
