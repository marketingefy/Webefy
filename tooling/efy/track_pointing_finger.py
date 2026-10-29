"""Track the left-facing cream glove in the locked, approved EVIA composition."""
from pathlib import Path
import json,subprocess,os
import numpy as np
from scipy import ndimage
from scipy.signal import savgol_filter
out=Path(os.environ['EFY_HERO_OUTPUT'])
raw=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out/'base.mp4'),'-vf','fps=24,scale=1280:720,crop=300:180:680:210','-frames:v','288','-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,180,300,3)
points=[]
for frame in frames:
 r,g,b=frame.astype(np.float32).transpose(2,0,1)
 mask=(r>105)&(g>85)&(b>60)&(r>g*.92)&(r-g<80)&(g>b*.75)&(r>b*.88)
 mask=ndimage.binary_opening(mask,iterations=1)
 labels,count=ndimage.label(mask);sizes=np.bincount(labels.ravel());sizes[0]=0
 selected=labels==sizes.argmax();ys,xs=np.where(selected)
 if not len(xs):points.append(points[-1] if points else [830,300]);continue
 left=np.percentile(xs,1);edge=xs<=left+3
 points.append([float(np.median(xs[edge])+680-2),float(np.median(ys[edge])+210)])
points=np.asarray(points)
points=ndimage.median_filter(points,size=(3,1))
points=savgol_filter(points,9,2,axis=0)
(out/'finger-track.json').write_text(json.dumps(points.round(2).tolist()))
print('Tracked',len(points),'frames; range:',points.min(axis=0),points.max(axis=0))
