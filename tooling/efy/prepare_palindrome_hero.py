"""Create a forward/reverse hero loop with eased, identical end poses."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
source = Path(os.environ.get('EFY_HERO_SOURCE', '/workspace/output/efy-evia-interacciones-movil-20261029'))
output = Path(os.environ.get('EFY_HERO_OUTPUT', '/workspace/output/efy-evia-bucle-suave-20261030'))
frames = output / 'frames'
frames.mkdir(parents=True, exist_ok=True)

# Slow only the turnarounds; retain the original pace through each selection.
count = 300
velocity = []
for i in range(count):
    p = min(1, i / 18, (count - 1 - i) / 18)
    velocity.append(p * p * (3 - 2 * p))
distance = [0.0]
for value in velocity[1:]:
    distance.append(distance[-1] + value)
forward = [round(287 * value / distance[-1]) for value in distance]
timeline = forward + forward[::-1]
assert timeline == timeline[::-1]
assert timeline[0] == timeline[-1] == 0
assert timeline[299] == timeline[300] == 287
for i, frame in enumerate(timeline):
    target = frames / f'{i:04d}.jpg'
    target.unlink(missing_ok=True)
    target.symlink_to(source / 'frames' / f'{frame:04d}.jpg')
(output / 'timeline.json').write_text(json.dumps(timeline))

for stem, size, crf in [
    ('evia-bucle-suave-20261030', 'scale=1280:720', '22'),
    ('evia-bucle-suave-mobile-20261030', 'crop=648:720:iw*0.45:0,scale=720:800', '23'),
]:
    target = root / 'public/assets' / stem
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-framerate', '24', '-i', str(frames / '%04d.jpg'),
                    '-frames:v', str(len(timeline)), '-vf', size + ',setsar=1',
                    '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', crf,
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    str(target.with_suffix('.mp4'))], check=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-i', str(target.with_suffix('.mp4')), '-frames:v', '1',
                    '-quality', '86', str(target.with_suffix('.webp'))], check=True)
    print(stem, '25 seconds', target.with_suffix('.mp4').stat().st_size, flush=True)
