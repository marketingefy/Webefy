"""Check the moving alpha cutouts, not just the existence of a video element.
Run locally with ffmpeg, ffprobe, numpy, scipy and Pillow installed.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import numpy as np
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--old',action='store_true',help='Reproduce the missing backpack/suit contours in the previous exports')
parser.add_argument('--previous',action='store_true',help='Reproduce missing table surfaces in the first contour correction')
args=parser.parse_args()
hero=ROOT/'public/assets'/('evia-cinema-fullhd-20261109.mp4' if args.old else 'evia-cinema-contorno-20261110.mp4' if args.previous else 'evia-cinema-integro-20261110.mp4')
contact=ROOT/'public/assets'/('evia-contacto-alpha-20261109.mp4' if args.old else 'evia-contacto-completo-20261110.mp4')

def metadata(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames:format=duration','-of','json',str(path)]))

def read_frames(path,width,height,fps=3):
 process=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vf',f'fps={fps}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
 try:
  while True:
   data=process.stdout.read(width*height*3)
   if not data:break
   assert len(data)==width*height*3,'Incomplete video frame'
   yield np.frombuffer(data,dtype='uint8').reshape(height,width,3)
 finally:
  process.stdout.close();process.wait()

h=metadata(hero);assert h['streams'][0]['nb_frames']=='600' and float(h['format']['duration'])==25
first=subprocess.check_output(['ffmpeg','-v','error','-i',str(hero),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
frame=np.frombuffer(first,dtype='uint8').reshape(1080,3840,3)
# The original backpack is visible here, but the old matte discarded it.
alpha=float(frame[307,1920+1716,0])/255
print('Hero backpack opacity:',round(alpha,3))
assert alpha>.93,'Visible backpack surface was removed by alpha'
c=metadata(contact);assert c['streams'][0]['nb_frames']=='360' and float(c['format']['duration'])==15
worst=0;count=0
for f in read_frames(contact,1440,960):
 rgb=f[:,:720].astype(float);a=f[:,720:,0].astype(float)/255;r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 warm=(r>85)&(r>g*.94)&(r>b*.88);warm=ndimage.binary_opening(warm,iterations=3);labels,_=ndimage.label(warm);sizes=np.bincount(labels.ravel());sizes[0]=0;body=labels==sizes.argmax()
 loss=float((body&(a<.5)).sum())/max(1,body.sum());worst=max(worst,loss);count+=1
 assert np.mean(a[:70,:])<.01,'Exterior video border must stay transparent'
print('Contact poses checked:',count,'worst lost warm suit area:',round(worst*100,3),'%')
assert worst<.0035,'Moving suit/helmet edges were removed by alpha'
print('PASS: preserved suit contours and complete forward/reverse loops')

# A visible point alone did not catch missing glass/rim patches or partial CSS-mask
# rasterization. Inspect interior areas of all surfaces in every encoded frame.
regions={
 'helmet/visor':(1000,90,70,105), 'torso':(1030,260,80,115),
 'left-leg':(985,555,30,80), 'right-leg':(1100,555,30,80),
 'table-glass':(700,412,400,60), 'table-rim':(480,470,700,25),
 'table-pedestal':(665,550,270,90),
}
process=subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(hero),
 '-vf','crop=1920:1080:1920:0,scale=1280:720','-f','rawvideo','-pix_fmt','gray','pipe:1'],stdout=subprocess.PIPE)
worst={name:0 for name in regions};frames=0
try:
 while True:
  data=process.stdout.read(1280*720)
  if not data:break
  assert len(data)==1280*720,'Incomplete alpha frame'
  a=np.frombuffer(data,dtype='uint8').reshape(720,1280)
  for name,(x,y,w,h) in regions.items():
   loss=float(np.mean(a[y:y+h,x:x+w]<235));worst[name]=max(worst[name],loss)
  assert np.mean(a[:,:350])<1,'The room must remain transparent'
  frames+=1
finally:
 process.stdout.close();process.wait()
print('Hero full-loop frames:',frames,'worst lost interior areas:',worst)
assert frames==600
assert max(worst.values())<.002,'Helmet, suit or continuous table surface disappeared during the loop'
print('PASS: every frame preserves all seven opaque surface regions')
