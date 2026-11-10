from pathlib import Path
import subprocess,json,argparse
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
out=args.out.resolve();hero=out/'hero';loop=hero/'loop';loop.mkdir(exist_ok=True)
assert all((hero/'frames'/f'{i:04d}.png').is_file() for i in range(288)), 'Render all frames before encoding'
for i,index in enumerate(json.loads((ROOT/'tooling/efy/hero-gesture-timeline.json').read_text())):
 p=loop/f'{i:04d}.png'
 if not p.exists():p.symlink_to(hero/'frames'/f'{index:04d}.png')
subprocess.run(['ffmpeg','-v','error','-threads','2','-framerate','24','-i',str(loop/'%04d.png'),'-filter_complex_threads','2','-filter_complex','[0:v]split[r][a];[r]format=rgb24[rgb];[a]alphaextract,format=rgb24[alpha];[rgb][alpha]hstack=inputs=2,format=yuv420p[v]','-map','[v]','-c:v','libx264','-threads','2','-preset','fast','-crf','16','-movflags','+faststart','-y',str(ROOT/'public/assets/evia-cinema-gestos-20261110.mp4')],check=True)
Image.open(hero/'frames/0000.png').crop((600,0,1920,1080)).save(str(ROOT/'public/assets/evia-cinema-gestos-20261110.png'))
subprocess.run(['ffmpeg','-v','error','-threads','2','-framerate','24','-i',str(loop/'%04d.png'),'-f','lavfi','-i','color=c=0x080e1d:s=1920x1080:r=24:d=25','-filter_complex_threads','2','-filter_complex','[1:v][0:v]overlay=shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-c:v','libx264','-threads','2','-preset','fast','-crf','18','-movflags','+faststart','-y',str(out/'EVIA-gestos-sincronizados.mp4')],check=True)
print('Hero from native transparent PNG: 600 frames, 25 seconds, no per-frame segmentation',flush=True)
