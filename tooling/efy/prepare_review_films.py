"""Prepare the three review-only films; never publishes or touches another checkout."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('module', choices=['inicio', 'conocenos', 'resenas'])
parser.add_argument('source', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
duration = 10 if args.module == 'inicio' else 8
if args.module == 'inicio':
    variants = [
        (root/'public/assets/evia-premium-consistent-preview', 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720', '22'),
        (root/'public/assets/evia-premium-consistent-preview-mobile', 'crop=trunc(ih*0.9/2)*2:ih:iw*0.384:0,scale=720:800', '23'),
    ]
else:
    variants = [(root/('public/assets/site/evia-conocenos-corporativo-20261029' if args.module == 'conocenos' else f'public/assets/site/evia-{args.module}-preview'),
                 'scale=720:960:force_original_aspect_ratio=decrease,pad=720:960:(ow-iw)/2:(oh-ih)/2:color=0x080e1d', '22')]
for stem, sizing, quality in variants:
    graph = (
        f'[0:v]fps=24,trim=duration={duration},{sizing},setsar=1,split=2[body][head];'
        '[body]trim=start=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[forward];'
        '[head]trim=duration=0.5,setpts=PTS-STARTPTS,fps=24,settb=AVTB[start];'
        f'[forward][start]xfade=transition=fade:duration=0.5:offset={duration-1},format=yuv420p[loop]'
    )
    movie = stem.with_suffix('.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(args.source),
                    '-filter_complex',graph,'-map','[loop]','-an','-c:v','libx264','-preset','slow',
                    '-crf',quality,'-movflags','+faststart',str(movie)],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(movie),
                    '-frames:v','1','-quality','86',str(stem.with_suffix('.webp'))],check=True)
    print(movie.name,movie.stat().st_size,flush=True)
