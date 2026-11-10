/* Render all three selections with the same normalized response, on the real film. */
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const {once}=require('node:events');
const root=path.resolve(__dirname,'../..');
const output=path.join(path.resolve(process.argv.find(a=>a.startsWith('--out='))?.slice(6)||path.join(root,'output/hero-gesture')),'hero');
const samples=process.argv.includes('--samples');
const full=process.argv.includes('--render')||samples;
const server=http.createServer(async(req,res)=>{try{
 const route=new URL(req.url,'http://localhost').pathname;
 const files={'/':path.join(__dirname,'hero-gesture-compositor.html'),'/gesture.js':path.join(__dirname,'hero-gesture.cjs'),'/evia-png.png':path.join(root,'public/assets/evia-inicio-png-20261110.png'),'/font.woff2':path.join(root,'public/assets/fonts/ibm-plex-sans-latin-500-normal.woff2'),'/iconos.png':path.join(__dirname,'media/hero-holograms.png')};
 const file=files[route];if(!file){res.writeHead(404);return res.end();}
 const content=await fs.readFile(file);const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.cjs':'text/javascript','.woff2':'font/woff2','.jpg':'image/jpeg','.png':'image/png','.mp4':'video/mp4'}[path.extname(file)];
 const range=req.headers.range?.match(/bytes=(\d+)-(\d*)/);
 if(range){const start=+range[1],end=range[2]?Math.min(+range[2],content.length-1):content.length-1;res.writeHead(206,{'Content-Type':mime,'Content-Range':'bytes '+start+'-'+end+'/'+content.length,'Content-Length':end-start+1,'Accept-Ranges':'bytes'});res.end(content.subarray(start,end+1));}
 else{res.writeHead(200,{'Content-Type':mime||'application/octet-stream','Content-Length':content.length});res.end(content);}
}catch{res.writeHead(404);res.end();}});
(async()=>{let browser;try{
 await fs.mkdir(output,{recursive:true});server.listen(0,'127.0.0.1');await once(server,'listening');
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1920,height:1080}});
 await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'domcontentloaded'});
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
 if(!full){await page.screenshot({path:output+'/composicion-inicial.png'});console.log('Composición inicial lista');return;}
 if(samples){for(const t of [0,2.25,5.25,8.25]){await page.evaluate(t=>window.drawFrame(t),t);await page.screenshot({path:output+'/sample-'+t+'.png',omitBackground:true});}return;}
 await fs.mkdir(output+'/frames',{recursive:true});
 for(let frame=0;frame<288;frame++){
  await page.evaluate(t=>window.drawFrame(t),frame/24);
  await page.screenshot({path:output+'/frames/'+String(frame).padStart(4,'0')+'.png',omitBackground:true});
  if(frame%48===0)console.log('Rendered',frame,'/288');
 }
 // Compare actual computed transforms, rather than just source values.
 const responses=[];
 for(let i=0;i<3;i++){
  const matrices=[];
  for(const phase of [.25,.5,.75]){await page.evaluate(t=>window.setHologramTime(t),[1,4,7][i]+phase*2.5);matrices.push(await page.locator('.turner').nth(i).evaluate(e=>Array.from(new DOMMatrix(getComputedStyle(e).transform).toFloat64Array(),v=>Math.round(v*1e6)/1e6||0)));}
  responses.push(matrices);
 }
 const assert=require('node:assert/strict');assert.deepEqual(responses[0],responses[1]);assert.deepEqual(responses[1],responses[2]);
 console.log('PASS: Vehículo, Hogar y Salud renderizan la misma respuesta en los tres puntos de control.');
}finally{await browser?.close();server.close();}})().catch(e=>{console.error(e.message);process.exitCode=1});
