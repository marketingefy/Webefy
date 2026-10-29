"""Build a self-contained visual preview, without hosting or publishing the site."""
import base64
import os
import json
import mimetypes
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[2] / 'public'
output = Path(os.environ.get('EFY_PREVIEW_OUTPUT','/workspace/output/efy-evia-dedo-luz-20261029'))
assets, identifiers = {}, {}


def asset_reference(value, parent):
    parts = urlsplit(value)
    if parts.scheme or value.startswith('#'):
        return value
    path = (root / unquote(parts.path).lstrip('/') if parts.path.startswith('/')
            else parent / unquote(parts.path)).resolve()
    if not path.is_relative_to(root / 'assets') or not path.is_file():
        return value
    if path not in identifiers:
        identifier = str(len(identifiers))
        identifiers[path] = identifier
        mime = {'.woff2':'font/woff2','.js':'text/javascript','.css':'text/css',
                '.webp':'image/webp','.svg':'image/svg+xml','.mp4':'video/mp4'}.get(path.suffix)
        mime = mime or mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        if path.suffix in ('.css', '.js'):
            text = path.read_text()
            if path.suffix == '.css':
                text = re.sub(r'url\(([\"\']?)([^)\"\']+)\1\)',
                              lambda m: 'url("' + asset_reference(m[2], path.parent) + '")', text)
            else:
                # The file preview keeps each module's URL/query available to its UI.
                text = re.sub(r'(?<![\w$.])(?:window\.)?location\.(href|pathname|search|hash|origin)',
                              r'window.EFY_PREVIEW_URL.\1', text)
            assets[identifier] = {'type':mime, 'text':text}
        else:
            assets[identifier] = 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()
    return 'efy-asset:' + identifiers[path]


pages = {}
for path in sorted(root.glob('*.html')):
    html = path.read_text()
    html = re.sub(r'\b(src|href|data-source|data-desktop|data-mobile)="([^"]+)"',
                  lambda m: m[1] + '="' + asset_reference(m[2], path.parent) + '"', html)
    def srcset(match):
        values = []
        for candidate in match[1].split(','):
            item = candidate.strip().split()
            values.append(asset_reference(item[0], path.parent) + (' ' + ' '.join(item[1:]) if len(item)>1 else ''))
        return 'srcset="' + ', '.join(values) + '"'
    html = re.sub(r'srcset="([^"]+)"',srcset,html)
    pages[path.name] = html


def safe_json(data):
    return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')


template = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Efy · Vista previa privada</title><style>
*{box-sizing:border-box}body{margin:0;background:#dfe5f0;font-family:Arial,sans-serif;color:#17233d}.preview-toolbar{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:12px 20px;background:#fff;border-bottom:1px solid #c6d0e5;min-height:68px}.preview-info strong{font-size:13px;display:block}.preview-info small{display:block;font-size:11px;color:#61718b;margin-top:4px}.preview-actions{display:flex;align-items:center;gap:8px}.preview-actions select,.preview-actions button{font:inherit;font-size:12px;min-height:38px;padding:8px 11px;border:1px solid #b8c6df;border-radius:9px;background:white;color:#17233d;cursor:pointer}.preview-actions button[aria-pressed=true]{background:#17233d;color:#fff}.preview-shell{width:100%;margin:auto;background:#080e1d;transition:max-width 250ms ease;max-width:1800px}.preview-shell.is-phone{max-width:390px;box-shadow:0 8px 55px #17233d33}.preview-shell iframe{display:block;width:100%;height:calc(100dvh - 69px);border:0;background:#080e1d}.preview-toolbar :focus-visible{outline:3px solid #ce005e;outline-offset:3px}@media(max-width:600px){.preview-toolbar{padding:10px 12px;gap:8px;align-items:start;min-height:90px}.preview-info{max-width:150px}.preview-info strong{font-size:12px}.preview-info small{font-size:10px;line-height:1.35}.preview-actions{flex-wrap:wrap;justify-content:end;max-width:190px;gap:5px}.preview-actions select{width:100%;min-height:30px;padding:5px 7px}.preview-actions button{min-height:29px;font-size:10px;padding:5px 9px}.preview-shell iframe{height:calc(100dvh - 90px)}}@media(prefers-reduced-motion:reduce){.preview-shell{transition:none}}
</style></head><body><header class="preview-toolbar"><div class="preview-info"><strong>Vista previa · Sin publicar</strong><small>Revisión de diseño. Los formularios no envían información.</small></div><div class="preview-actions"><select id="preview-page" aria-label="Elegir módulo"><option value="index.html">Inicio</option><option value="nosotros.html">Conócenos</option><option value="socios.html">Aliados</option><option value="contactos.html">Contacto</option><option value="resenas.html">Reseñas</option><option value="servicios.html">Servicios</option><option value="asistencia.html">Asistencias</option><option value="ayuda.html">Ayuda</option></select><button type="button" id="desktop" aria-pressed="true">Computadora</button><button type="button" id="phone" aria-pressed="false">Celular</button></div></header><main class="preview-shell" id="preview-shell"><iframe id="preview-frame" title="Propuesta de Efy Seguros" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe></main><script>
const PAGES=__PAGES__, ASSETS=__ASSETS__, CACHE={};
const frame=document.getElementById('preview-frame'), chooser=document.getElementById('preview-page');
function getAsset(id){if(CACHE[id])return CACHE[id];const item=ASSETS[id];if(typeof item==='string')return CACHE[id]=item;const text=item.text.replace(/efy-asset:(\\d+)/g,(_,key)=>getAsset(key));return CACHE[id]='data:'+item.type+';base64,'+btoa(unescape(encodeURIComponent(text)));}
function navigate(route){
 const url=new URL(route,'https://www.efyseguros.com/');const file=url.pathname.split('/').pop()||'index.html';if(!PAGES[file])return;
 const selected=[...chooser.options].find(o=>o.value===file);if(selected)chooser.value=file;
 document.title='Vista previa · '+(selected?.textContent||'Efy Seguros');
 const setup='window.EFY_PREVIEW_URL=new URL('+JSON.stringify(url.href)+');window.fetch=async function(input){const value=String(input?.url||input);if(value.startsWith("data:"))return new Response("");return new Response(JSON.stringify({ok:false,ready:false,error:"PREVIEW_MODE"}),{status:503,headers:{"Content-Type":"application/json"}});};history.replaceState=history.pushState=function(state,title,value){if(value)window.EFY_PREVIEW_URL=new URL(value,window.EFY_PREVIEW_URL.href);};document.addEventListener("submit",e=>e.preventDefault(),true);document.addEventListener("click",function(e){const a=e.target.closest("a[href]");if(!a)return;const target=new URL(a.getAttribute("href"),window.EFY_PREVIEW_URL.href);if(target.origin==="https://www.efyseguros.com"&&(target.pathname.endsWith(".html")||target.pathname.endsWith("/"))){e.preventDefault();parent.postMessage({type:"efy-preview-navigate",route:target.href},"*");}else if(!target.protocol.startsWith("data")){a.target="_blank";a.rel="noopener noreferrer";}},true);';
 let html=PAGES[file].replace(/efy-asset:(\\d+)/g,(_,id)=>getAsset(id));
 html=html.replace('<head>','<head><base href="https://www.efyseguros.com/'+file+'"><script>'+setup+'<\\/script>');
 frame.onload=()=>{if(url.hash){const target=frame.contentDocument.getElementById(decodeURIComponent(url.hash.slice(1)));target?.scrollIntoView({behavior:'instant'});}};
 frame.srcdoc=html;
}
window.addEventListener('message',event=>{if(event.source===frame.contentWindow&&event.data?.type==='efy-preview-navigate')navigate(event.data.route);});
chooser.addEventListener('change',()=>navigate(chooser.value));
for(const [id,phone] of [['phone',true],['desktop',false]])document.getElementById(id).addEventListener('click',()=>{document.getElementById('preview-shell').classList.toggle('is-phone',phone);document.getElementById('phone').setAttribute('aria-pressed',String(phone));document.getElementById('desktop').setAttribute('aria-pressed',String(!phone));});
navigate('index.html');
</script></body></html>'''
html=template.replace('__PAGES__',safe_json(pages)).replace('__ASSETS__',safe_json(assets))
output.mkdir(parents=True,exist_ok=True)
destination=output/'Efy-vista-previa-interactiva.html'
destination.write_text(html)
print(destination,len(html.encode()),'bytes;',len(pages),'módulos;',len(assets),'recursos integrados')
