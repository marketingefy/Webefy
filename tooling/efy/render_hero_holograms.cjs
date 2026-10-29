/* Render all three selections with the same normalized rotation, on the real film. */
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const {once}=require('node:events');
const root=path.resolve(__dirname,'../..');
const output=process.env.EFY_HERO_OUTPUT || '/workspace/output/efy-evia-traje-giro-20261029';
const full=process.argv.includes('--render');
const server=http.createServer(async(req,res)=>{try{
 const route=new URL(req.url,'http://localhost').pathname;
 const file=route==='/'?path.join(__dirname,'hero-holograms.html'):route==='/font.woff2'?path.join(root,'public/assets/fonts/ibm-plex-sans-latin-500-normal.woff2'):path.join(output,path.basename(route));
 const content=await fs.readFile(file);const mime={'.html':'text/html; charset=utf-8','.woff2':'font/woff2','.jpg':'image/jpeg','.png':'image/png','.mp4':'video/mp4'}[path.extname(file)];
 const range=req.headers.range?.match(/bytes=(\d+)-(\d*)/);
 if(range){const start=+range[1],end=range[2]?Math.min(+range[2],content.length-1):content.length-1;res.writeHead(206,{'Content-Type':mime,'Content-Range':'bytes '+start+'-'+end+'/'+content.length,'Content-Length':end-start+1,'Accept-Ranges':'bytes'});res.end(content.subarray(start,end+1));}
 else{res.writeHead(200,{'Content-Type':mime||'application/octet-stream','Content-Length':content.length});res.end(content);}
}catch{res.writeHead(404);res.end();}});
(async()=>{let browser;try{
 server.listen(0,'127.0.0.1');await once(server,'listening');
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1280,height:720}});
 await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'domcontentloaded'});
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
 if(!full){await page.screenshot({path:output+'/composicion-inicial.png'});console.log('Composición inicial lista');return;}
 await fs.mkdir(output+'/frames',{recursive:true});
 for(let frame=0;frame<288;frame++){
  await page.evaluate(t=>window.drawFrame(t),frame/24);
  await page.screenshot({path:output+'/frames/'+String(frame).padStart(4,'0')+'.jpg',type:'jpeg',quality:95});
  if(frame%48===0)console.log('Rendered',frame,'/288');
 }
 // Compare actual computed 3D transforms, rather than just source values.
 const rotations=[];
 for(let i=0;i<3;i++){
  const matrices=[];
  for(const phase of [.25,.5,.75]){await page.evaluate(t=>window.setHologramTime(t),[1,4,7][i]+phase*2.5);matrices.push(await page.locator('.turner').nth(i).evaluate(e=>Array.from(new DOMMatrix(getComputedStyle(e).transform).toFloat64Array(),v=>Math.round(v*1e6)/1e6||0)));}
  rotations.push(matrices);
 }
 const assert=require('node:assert/strict');assert.deepEqual(rotations[0],rotations[1]);assert.deepEqual(rotations[1],rotations[2]);
 console.log('PASS: Vehículo, Hogar y Salud renderizan los mismos giros en los tres puntos de control.');
}finally{await browser?.close();server.close();}})().catch(e=>{console.error(e.message);process.exitCode=1});
