/* Render all three selections with the same normalized response, on the real film. */
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const {once}=require('node:events');
const root=path.resolve(__dirname,'../..');
const renderRoot=path.resolve(process.argv.find(a=>a.startsWith('--out='))?.slice(6)||path.join(root,'output/hero-magic'));const output=path.join(renderRoot,'hero');
const samples=process.argv.includes('--samples');
const full=process.argv.includes('--render')||samples;
const server=http.createServer(async(req,res)=>{try{
 const route=new URL(req.url,'http://localhost').pathname;
 const files={'/':path.join(__dirname,'hero-magic-compositor.html'),'/magic.js':path.join(__dirname,'hero-magic.cjs'),'/finger-track.json':path.join(renderRoot,'finger-track.json'),'/font.woff2':path.join(root,'public/assets/fonts/ibm-plex-sans-latin-500-normal.woff2'),'/iconos.png':path.join(__dirname,'media/hero-holograms.png')};const file=route.startsWith('/base/')?path.join(path.join(renderRoot,'base-frames'),path.basename(route)):files[route];if(!file){res.writeHead(404);return res.end();}
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
 if(samples){for(const t of [0,1.35,3.9,6.35]){await page.evaluate(t=>window.drawFrame(t),t);await page.screenshot({path:output+'/sample-'+t+'.png',omitBackground:true});}return;}
 await page.evaluate(()=>{window.onlyOverlay=true;document.querySelector('#native-base').style.visibility='hidden';});await fs.mkdir(output+'/overlays',{recursive:true});
 for(let frame=0;frame<193;frame++){
  await page.evaluate(t=>window.drawFrame(t),frame/24);
  await page.screenshot({path:output+'/overlays/'+String(frame).padStart(4,'0')+'.png',omitBackground:true});
  if(frame%48===0)console.log('Rendered',frame,'/288');
 }
 console.log('PASS: native-motion fingertip effects rendered');
}finally{await browser?.close();server.close();}})().catch(e=>{console.error(e.message);process.exitCode=1});
