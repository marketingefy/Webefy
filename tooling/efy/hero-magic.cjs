/* Deterministic, restrained fingertip light. Composited into the film offline. */
(function(root){
 const events=[{at:1.35,icon:0},{at:3.9,icon:1},{at:6.35,icon:2}];
 const palette=['#f8f9ff','#a8dcff','#f7a5ce'];
 const random=n=>{const x=Math.sin(n*12.9898+78.233)*43758.5453;return x-Math.floor(x);};
 function star(ctx,x,y,r,angle,color,alpha){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha=alpha;ctx.fillStyle=color;ctx.shadowColor=color;ctx.shadowBlur=6;ctx.beginPath();for(let i=0;i<8;i++){const a=i*Math.PI/4-Math.PI/2,d=i%2?r*.22:r;i?ctx.lineTo(Math.cos(a)*d,Math.sin(a)*d):ctx.moveTo(Math.cos(a)*d,Math.sin(a)*d);}ctx.closePath();ctx.fill();ctx.restore();}
 function draw(ctx,t,fingerAt,targets){ctx.clearRect(0,0,1280,720);let count=0;const point=fingerAt(t);const globalFade=Math.min(1,Math.max(0,t/.3),Math.max(0,(8-t)/.3));
  ctx.save();ctx.globalAlpha=globalFade;const halo=ctx.createRadialGradient(point[0],point[1],0,point[0],point[1],27);halo.addColorStop(0,'#ffffffee');halo.addColorStop(.12,'#e5f5ffcc');halo.addColorStop(.4,'#a8dcff55');halo.addColorStop(.75,'#f25c9d20');halo.addColorStop(1,'#f25c9d00');ctx.fillStyle=halo;ctx.fillRect(point[0]-27,point[1]-27,54,54);ctx.restore();
  for(let j=0;j<events.length;j++){const event=events[j],target=targets[event.icon],energy=Math.exp(-Math.pow((t-event.at)/.4,2));
   if(energy>.02){star(ctx,point[0],point[1],7+7*energy,t*.8,'#ffffff',.95*energy*globalFade);ctx.save();ctx.strokeStyle='#e3edff';ctx.shadowColor='#b2dfff';ctx.shadowBlur=7;ctx.globalAlpha=.38*energy*globalFade;ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(...point);ctx.quadraticCurveTo((point[0]+target[0])/2,Math.min(point[1],target[1])-24,...target);ctx.stroke();ctx.restore();}
   for(let k=0;k<16;k++){const born=event.at-.16+k*.035,u=(t-born)/(.42+.22*random(k+31*j));if(u<0||u>1)continue;const origin=fingerAt(born),angle=random(k+73*j)*Math.PI*2,distance=(28+42*random(k+9+53*j))*(1-Math.pow(1-u,2)),x=origin[0]+Math.cos(angle)*distance,y=origin[1]+Math.sin(angle)*distance-15*u*u;star(ctx,x,y,2.8+2.5*random(k+19*j),u*1.3,palette[k%3],Math.pow(1-u,1.3)*globalFade);count++;}
  }
  return {particles:count,finger:point};
 }
 const api={events,draw};root.EFY_HERO_MAGIC=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
