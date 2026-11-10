/* Shared by the offline transparent-film renderer and its motion checks. */
(function(root){
 const selections=[{name:'Vehículo',start:1,dx:-14,dy:5,angle:-.13,gaze:-.018},{name:'Hogar',start:4,dx:22,dy:6,angle:-.21,gaze:-.012},{name:'Salud',start:7,dx:50,dy:8,angle:-.28,gaze:.012}];
 const rest={name:'reposo',dx:0,dy:0,angle:0,gaze:0};
 // Retain the pointing pose between icons; never snap back up between selections.
 const keyframes=[[0,rest,0],[.5,rest,0],[2.25,selections[0],1],[3.15,selections[0],.86],[5.25,selections[1],1],[6.15,selections[1],.86],[8.25,selections[2],1],[9.3,selections[2],.86],[11.8,rest,0],[12,rest,0]];
 function at(t){let active=null,energy=0;for(const s of selections){const p=Math.max(0,Math.min(1,(t-s.start)/2.5)),e=Math.pow(Math.sin(Math.PI*p),.75);if(e>energy){energy=e;active=s;}}
  const i=Math.max(0,keyframes.findIndex((k,j)=>j<keyframes.length-1&&t>=k[0]&&t<=keyframes[j+1][0]));const a=keyframes[i],b=keyframes[i+1],p=Math.max(0,Math.min(1,(t-a[0])/(b[0]-a[0]))),u=(1-Math.cos(Math.PI*p))*.5;
  const value=k=>a[1][k]*a[2]*(1-u)+b[1][k]*b[2]*u,angle=value('angle'),dx=value('dx'),dy=value('dy'),c=Math.cos(angle),n=Math.sin(angle);
  return {name:active?.name||'transición',energy,angle,dx,dy,gaze:value('gaze'),nod:3*energy,finger:[930+c*(-140)-n*19+dx,285+n*(-140)+c*19+dy],palm:[930+c*(-86)-n*22+dx,285+n*(-86)+c*22+dy]};
 }
 const api={at,selections};root.EFY_HERO_GESTURE=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
