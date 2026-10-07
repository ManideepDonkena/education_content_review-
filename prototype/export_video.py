"""Export a fast-start H.264/AAC MP4 with audio padded to the video duration."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
source=ROOT/'media/videos/like_terms/720p30/LikeTerms.mp4'
duration=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
    '-show_entries','stream=duration','-of','default=nw=1:nk=1',str(source)],text=True).strip()
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
    '-c:v','copy','-af','apad','-c:a','aac','-b:a','160k','-t',duration,
    '-movflags','+faststart',str(ROOT/'output/like_terms.mp4')],check=True)
print(f'Exported {duration}s MP4')
