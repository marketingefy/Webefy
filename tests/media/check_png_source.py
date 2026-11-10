"""Check every encoded frame against the complete regenerated PNG silhouette."""
from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2]
png=Image.open(ROOT/'public/assets/evia-inicio-png-20261110.png').resize((880,720),Image.Resampling.LANCZOS)
reference=np.zeros((720,1280),dtype='uint8');reference[:,400:]=np.asarray(png)[:,:,3]
# Exclude only a narrow boundary where antialiasing and a <=5px hand gesture vary.
core=ndimage.binary_erosion(reference>250,iterations=8)
assert core.sum()>180000,'Reference must contain the entire character and console'
path=ROOT/'public/assets/evia-cinema-png-20261110.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(path),'-vf','crop=1920:1080:1920:0,scale=1280:720','-f','rawvideo','-pix_fmt','gray','pipe:1'],stdout=subprocess.PIPE)
frames=0;worst=0;first=None;last=None
try:
 while True:
  data=p.stdout.read(1280*720)
  if not data:break
  assert len(data)==1280*720
  a=np.frombuffer(data,dtype='uint8').reshape(720,1280)
  loss=float(np.mean(a[core]<235));worst=max(worst,loss)
  assert loss<.0005,f'Frame {frames}: part of the source PNG became transparent ({loss:.3%})'
  assert np.max(a[:,:350])<10,'The original room/background must not return'
  if first is None:first=a.copy()
  last=a.copy();frames+=1
finally:p.stdout.close();p.wait()
assert frames==600
assert np.abs(first.astype(float)-last.astype(float)).mean()<.1,'The loop must return to the same silhouette'
print(json.dumps({'frames':frames,'source_interior_pixels_checked_per_frame':int(core.sum()),'worst_missing_source_area':worst,'loop_seam_alpha_mean_difference':float(np.abs(first.astype(float)-last.astype(float)).mean())}))
print('PASS: original PNG helmet, visor, gloves, backpack, suit, boots, glass, rim and pedestal stay opaque throughout the loop')

service=ROOT/'public/assets/evia-servicios-escudo-20261110.mp4'
p=subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(service),'-vf','crop=810:1080:810:0','-f','rawvideo','-pix_fmt','gray','pipe:1'],stdout=subprocess.PIPE)
frames=0;min_margin=1080;worst_hole=0;first=None;last=None
try:
 while True:
  data=p.stdout.read(810*1080)
  if not data:break
  assert len(data)==810*1080
  a=np.frombuffer(data,dtype='uint8').reshape(1080,810);body=a>180
  y,x=np.nonzero(body);margin=min(x.min(),809-x.max(),y.min(),1079-y.max());min_margin=min(min_margin,int(margin))
  assert margin>30,f'Services frame {frames}: helmet or boots touch the video edge'
  holes=ndimage.binary_fill_holes(body)&~body;labels,_=ndimage.label(holes);sizes=np.bincount(labels.ravel());sizes[0]=0
  largest=int(sizes.max());worst_hole=max(worst_hole,largest)
  assert largest<12,f'Services frame {frames}: transparent hole inside visor, suit or shield'
  if first is None:first=a.copy()
  last=a.copy();frames+=1
finally:p.stdout.close();p.wait()
assert frames==240
assert np.abs(first.astype(float)-last.astype(float)).mean()<.1
print(json.dumps({'services_frames':frames,'minimum_safe_margin_px':min_margin,'largest_internal_transparent_hole_px':worst_hole}))
print('PASS: complete transparent shield film, safe helmet/boot margins and seamless return')
