"""Optimize the approved EVIA portrait video for Conócenos, with a matching poster."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path)
args = parser.parse_args()
assets = Path(__file__).resolve().parents[1] / 'public' / 'assets' / 'site'
output = assets / 'evia-about-loop.mp4'
graph = (
    '[0:v]fps=24,scale=720:960:force_original_aspect_ratio=increase,'
    'crop=720:960,setsar=1,split=2[forward][source];'
    '[source]reverse[backward];'
    '[forward][backward]concat=n=2:v=1:a=0,format=yuv420p[loop]'
)
subprocess.run([
    'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(args.source),
    '-filter_complex', graph, '-map', '[loop]', '-an', '-c:v', 'libx264',
    '-preset', 'slow', '-crf', '23', '-movflags', '+faststart', str(output),
], check=True)
subprocess.run([
    'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(output),
    '-frames:v', '1', '-quality', '86', str(assets / 'evia-about-poster.webp'),
], check=True)
print('EVIA portrait loop:', output.stat().st_size, 'bytes')
