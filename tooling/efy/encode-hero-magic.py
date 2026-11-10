from pathlib import Path
import subprocess,json,math,argparse
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();out=args.out.resolve();frames=out/'frames';frames.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-threads','2','-framerate','24','-i',str(out/'base-frames/%04d.png'),'-framerate','24','-i',str(out/'hero/overlays/%04d.png'),'-filter_complex_threads','2','-filter_complex','[0:v][1:v]overlay=shortest=1:format=auto,format=rgba[v]','-map','[v]','-frames:v','193','-c:v','png','-threads','2','-compression_level','2','-start_number','0','-y',str(frames/'%04d.png')],check=True)
forward=[round((i/191-.5*math.sin(2*math.pi*i/191)/(2*math.pi))*192)for i in range(192)];timeline=forward+forward[::-1];(out/'timeline.json').write_text(json.dumps(timeline));loop=out/'loop';loop.mkdir(exist_ok=True)
for i,index in enumerate(timeline):
 p=loop/f'{i:04d}.png'
 if not p.exists():p.symlink_to(frames/f'{index:04d}.png')
print('193 complete native poses with anchored magic; 384-frame forward/reverse loop',flush=True)
subprocess.run(['ffmpeg','-v','error','-threads','2','-framerate','24','-i',str(loop/'%04d.png'),'-filter_complex_threads','2','-filter_complex','[0:v]split[r][a];[r]format=rgb24[rgb];[a]alphaextract,format=rgb24[alpha];[rgb][alpha]hstack=inputs=2,format=yuv420p[v]','-map','[v]','-c:v','libx264','-threads','2','-preset','fast','-crf','16','-movflags','+faststart','-y',str(ROOT/'public/assets/evia-cinema-magica-20261110.mp4')],check=True)
Image.open(frames/'0000.png').crop((600,0,1920,1080)).save(str(ROOT/'public/assets/evia-cinema-magica-20261110.png'))
subprocess.run(['ffmpeg','-v','error','-threads','2','-framerate','24','-i',str(loop/'%04d.png'),'-f','lavfi','-i','color=c=0x080e1d:s=1920x1080:r=24:d=16','-filter_complex_threads','2','-filter_complex','[1:v][0:v]overlay=shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-c:v','libx264','-threads','2','-preset','fast','-crf','18','-movflags','+faststart','-y',str(out/'EVIA-varita-de-luz.mp4')],check=True)
print('Dynamic hero, transparent poster and normal magic preview ready',flush=True)
