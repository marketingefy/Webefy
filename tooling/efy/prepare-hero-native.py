from pathlib import Path
import cv2,numpy as np,json,argparse,subprocess
from scipy import ndimage
from PIL import Image,ImageFilter,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True);(out/'raw').mkdir(exist_ok=True);cv2.setNumThreads(2)
source=ROOT/'tooling/efy/media/evia-native-magica-20261110.mp4'
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(source),'-vf','scale=832:624','-threads','2','-q:v','2','-start_number','0','-y',str(out/'raw/%04d.jpg')],check=True)
raw=sorted((out/'raw').glob('*.jpg'));grays=[cv2.imread(str(p),0)for p in raw]
anchors={0:[455,386],24:[347,282],72:[381,299],120:[589,316],168:[617,343],192:[455,386]}
track=np.zeros((len(raw),2),dtype=np.float32)
for lo,hi in zip(list(anchors)[:-1],list(anchors)[1:]):
 f=[np.array(anchors[lo],np.float32)];b=[np.array(anchors[hi],np.float32)]
 for i in range(lo,hi):
  p,ok,_=cv2.calcOpticalFlowPyrLK(grays[i],grays[i+1],f[-1].reshape(1,1,2),None,winSize=(31,31),maxLevel=3);f.append(p[0,0]if ok[0,0]else f[-1])
 for i in range(hi,lo,-1):
  p,ok,_=cv2.calcOpticalFlowPyrLK(grays[i],grays[i-1],b[-1].reshape(1,1,2),None,winSize=(31,31),maxLevel=3);b.append(p[0,0]if ok[0,0]else b[-1])
 for k in range(hi-lo+1):
  u=k/(hi-lo);track[lo+k]=f[k]*(1-u)+b[hi-lo-k]*u
# Dense native chroma masks preserve dark visor and bronze/glass instead of removing them.
masks=[];bounds=[]
for p in raw:
 a=np.asarray(Image.open(p)).astype(float);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2];fg=~((g>105)&(g>1.23*r)&(g>1.23*b));fg=ndimage.binary_closing(fg,iterations=1);lab,_=ndimage.label(fg);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();y,x=np.nonzero(mask);assert min(x.min(),831-x.max(),y.min(),623-y.max())>10,'Native character clipped';masks.append(mask);bounds.append([int(x.min()),int(y.min()),int(x.max()),int(y.max())])
bounds=np.array(bounds);crop=[max(0,int(bounds[:,0].min())-12),max(0,int(bounds[:,1].min())-12),min(832,int(bounds[:,2].max())+13),min(624,int(bounds[:,3].max())+13)];x0,y0,x1,y1=crop;scale=min(880/(x1-x0),720/(y1-y0));w=round((x1-x0)*scale);h=round((y1-y0)*scale);px=400+(880-w)//2;py=(720-h)//2
logical=np.column_stack((px+(track[:,0]-x0)*scale,py+(track[:,1]-y0)*scale));(out/'finger-track.json').write_text(json.dumps(logical.tolist()));(out/'geometry.json').write_text(json.dumps({'crop_832':crop,'logical':[px,py,w,h],'native_bounds':bounds.tolist()}))
frames=out/'base-frames';frames.mkdir(exist_ok=True);cap=cv2.VideoCapture(str(source))
for i,mask in enumerate(masks):
 ok,bgr=cap.read();assert ok;rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB);r,gc,b=[rgb[:,:,k].astype(float)for k in range(3)];green=(gc>105)&(gc>1.23*r)&(gc>1.23*b);lab,_=ndimage.label(~green);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();alpha=np.asarray(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.55))).copy();alpha[green]=0;rgba=np.dstack((rgb,alpha));edge=(alpha>0)&(alpha<250);rgba[:,:,1][edge]=np.minimum(rgba[:,:,1][edge],np.maximum(rgba[:,:,0][edge],rgba[:,:,2][edge])*1.04).astype('uint8');rgba[alpha==0,:3]=0;crop2=tuple(v*2 for v in crop);sprite=Image.fromarray(rgba).crop(crop2).resize((w*3//2,h*3//2),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(1920,1080));canvas.alpha_composite(sprite,(px*3//2,py*3//2));canvas.save(frames/f'{i:04d}.png',compress_level=2)

 if i%48==0:print('Prepared native full silhouette',i,flush=True)
cap.release();print('Complete source + tracked fingertips',len(masks),crop,[px,py,w,h],flush=True)
# Diagnostic markers on every half second for a visual check of the light anchor.
board=Image.new('RGB',(1152,648),'#080e1d');d=ImageDraw.Draw(board)
for k,i in enumerate(range(0,len(raw),12)):
 if k>=16:break
 im=Image.open(raw[i]).convert('RGB');q=ImageDraw.Draw(im);x,y=track[i];q.ellipse((x-6,y-6,x+6,y+6),outline='white',width=2);im=im.resize((288,216));board.paste(im,(k%4*288,k//4*162));d.text((k%4*288+5,k//4*162+5),str(i),fill='white')
board.save(out/'finger-review.jpg')

from pathlib import Path
import numpy as np,cv2,json
from scipy.signal import savgol_filter
out=args.out.resolve();g=json.loads((out/'geometry.json').read_text());track=np.array(json.loads((out/'finger-track.json').read_text()));x0,y0,x1,y1=g['crop_832'];px,py,w,h=g['logical'];sx=w/(x1-x0);sy=h/(y1-y0);raw=np.column_stack(((track[:,0]-px)/sx+x0,(track[:,1]-py)/sy+y0));raw=savgol_filter(raw,7,2,axis=0);distances=[]
for i,p in enumerate(sorted((out/'raw').glob('*.jpg'))):
 rgb=cv2.cvtColor(cv2.imread(str(p)),cv2.COLOR_BGR2RGB).astype(float);r,gc,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2];warm=(r>100)&(gc>65)&(r>gc*.94)&(r>b*1.04)
 x,y=raw[i];cx,cy=round(x),round(y)
 if not warm[cy,cx]:
  left=max(0,cx-28);right=min(832,cx+29);top=max(0,cy-28);bottom=min(624,cy+29);ys,xs=np.nonzero(warm[top:bottom,left:right]);ds=(xs+left-x)**2+(ys+top-y)**2
  if len(ds):k=ds.argmin();raw[i]=[xs[k]+left,ys[k]+top];distances.append(float(np.sqrt(ds[k])))
logical=np.column_stack((px+(raw[:,0]-x0)*sx,py+(raw[:,1]-y0)*sy));(out/'finger-track.json').write_text(json.dumps(logical.tolist()));print('Anchored light to warm glove pixels, max snap',max(distances));print('activation tips',[logical[round(t*24)].round(1).tolist()for t in [1.35,3.9,6.35]])
