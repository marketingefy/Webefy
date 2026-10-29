"""Encode the corrected suit and matching hologram rotations for review, not publish."""
from pathlib import Path
import subprocess
import os

root = Path(__file__).resolve().parents[2]
output = Path(os.environ.get('EFY_HERO_OUTPUT','/workspace/output/efy-evia-traje-giro-20261029'))
source = output / 'composicion-12s.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                '-framerate','24','-i',str(output/'frames/%04d.jpg'),'-frames:v','288',
                '-an','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',
                '-movflags','+faststart',str(source)],check=True)
for stem, size, crf in [
    ('evia-gestos-fluidos-20261029','scale=1280:720','22'),
    ('evia-gestos-fluidos-mobile-20261029','crop=648:720:iw*0.45:0,scale=720:800','23'),
]:
    target = root/'public/assets'/stem
    graph = (f'[0:v]fps=24,trim=duration=12,{size},setsar=1,split=2[b][h];'
             '[b]trim=start=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[body];'
             '[h]trim=duration=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[head];'
             '[body][head]xfade=transition=fade:duration=0.5:offset=11,format=yuv420p[loop]')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
                    '-filter_complex',graph,'-map','[loop]','-an','-c:v','libx264',
                    '-preset','slow','-crf',crf,'-movflags','+faststart',str(target.with_suffix('.mp4'))],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(target.with_suffix('.mp4')),
                    '-frames:v','1','-quality','86',str(target.with_suffix('.webp'))],check=True)
    print(stem, target.with_suffix('.mp4').stat().st_size,flush=True)
