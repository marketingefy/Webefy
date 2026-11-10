const assert=require('node:assert/strict');
const {at}=require('../../tooling/efy/hero-gesture.cjs');
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
const rest=at(0),poses=[2.25,5.25,8.25].map(at);
for(const p of poses){assert.ok(distance(p.finger,rest.finger)>25,'Each selection must visibly move the hand');assert.ok(p.energy>.99,'Pointing and icon activation must coincide');}
assert.ok(distance(poses[0].finger,poses[1].finger)>20);assert.ok(distance(poses[1].finger,poses[2].finger)>20);
for(const t of [3.5,6.5])assert.ok(distance(at(t).finger,rest.finger)>15,'Retain a continuous pointing pose between icons');
for(let t=0;t<11.99;t+=1/24)assert.ok(distance(at(t).finger,at(t+1/24).finger)<3,'No sudden hand jumps');
assert.ok(distance(rest.finger,at(11.99).finger)<.01,'End in the starting pose for a seamless loop');
console.log('PASS: three visible, synchronized gestures with continuous transitions and a seamless return');
