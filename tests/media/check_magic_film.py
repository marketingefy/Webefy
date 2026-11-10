"""Compare the coded film with the complete, moving native source silhouettes."""
from pathlib import Path
import subprocess,numpy as np,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];ref=np.load(ROOT/'tooling/efy/media/evia-magic-reference.npz');timeline=ref['timeline'];shape=tuple(ref['shape']);masks=np.unpackbits(ref['packed'],axis=1)[:,:shape[0]*shape[1]].reshape((-1,*shape)).astype(bool)
p=subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(ROOT/'public/assets/evia-cinema-magica-20261110.mp4'),'-vf','crop=1920:1080:1920:0,scale=1280:720','-pix_fmt','gray','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE);count=0;worst=0;first=None;last=None
try:
 while True:
  data=p.stdout.read(1280*720)
  if not data:break
  a=np.frombuffer(data,dtype='uint8').reshape(shape);mask=masks[timeline[count]];loss=float(np.mean(a[mask]<235));worst=max(worst,loss);assert loss<.001,f'Frame {count} lost source silhouette';assert np.max(a[:,:350])<10
  if first is None:first=a.copy()
  last=a.copy();count+=1
finally:p.stdout.close();p.wait()
assert count==384;assert np.abs(first.astype(float)-last.astype(float)).mean()<.1
im=Image.open(ROOT/'public/assets/evia-contacto-movil-alpha-20261110.webp');assert im.info['background']==(0,0,0,0);assert im.n_frames==180
for i in range(im.n_frames):
 im.seek(i);a=np.asarray(im.convert('RGBA'))[:,:,3];assert max(a[0,0],a[0,-1],a[-1,0],a[-1,-1])==0,f'Mobile animation frame {i} has an opaque background'
print(json.dumps({'native_hero_frames':count,'worst_lost_source_area':worst,'contact_native_rgba_frames':im.n_frames,'contact_background':'transparent'}))
print('PASS: complete moving astronaut/table, seamless loop and transparent mobile animation')

# Foreground alpha can be intact while green backing remains in a real arm gap.
p=subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(ROOT/'public/assets/evia-cinema-magica-20261110.mp4'),'-vf','fps=6,scale=2560:720','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE)
residue=0;samples=0
try:
 while True:
  data=p.stdout.read(2560*720*3)
  if not data:break
  f=np.frombuffer(data,dtype='uint8').reshape(720,2560,3);rgb=f[:,:1280].astype(float);a=f[:,1280:,0];r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2];n=int(((a>235)&(g>120)&(g>r*1.3)&(g>b*1.3)).sum());residue=max(residue,n);samples+=1
finally:p.stdout.close();p.wait()
assert residue<4,f'Chroma green backing leaked into the opaque scene ({residue} pixels)'
print(json.dumps({'color_frames_checked':samples,'largest_green_background_residue_px':residue}))
