(() => {
  const form = document.querySelector('#claim-form');
  const steps = [...form.querySelectorAll('.claim-step')];
  const progress = [...document.querySelectorAll('.claim-progress li')];
  const availability = document.querySelector('#claim-availability');
  const errorBox = document.querySelector('#claim-error');
  const send = document.querySelector('#claim-send');
  const files = document.querySelector('#claim-files');
  const endpoint = 'api/siniestros.php';
  let current = 0, config, requestId, sending = false, receipt;
  form.noValidate = true;
  const field = name => name === 'attachments' ? files : form.elements.namedItem(name);
  const todayParts = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Guayaquil', year:'numeric', month:'2-digit', day:'2-digit' }).formatToParts(new Date());
  const part = type => todayParts.find(item => item.type === type).value;
  field('event_date').max = `${part('year')}-${part('month')}-${part('day')}`;
  function showError(message) { errorBox.textContent = message; errorBox.hidden = false; }
  function showStep(index, focus = true) {
    current = index;
    steps.forEach((step, i) => step.hidden = i !== index);
    progress.forEach((item, i) => i === index ? item.setAttribute('aria-current', 'step') : item.removeAttribute('aria-current'));
    if (index === 2) review();
    if (focus) { const legend = steps[index].querySelector('legend'); legend.tabIndex = -1; legend.focus(); }
  }
  function validateStep(index) {
    const controls = [...steps[index].querySelectorAll('input,select,textarea')];
    controls.forEach(control => {
      control.setCustomValidity('');
      control.removeAttribute('aria-invalid');
      if (control.name === 'name' && control.value.trim().length < 2) control.setCustomValidity('Escribe tu nombre y apellido.');
      if (control.name === 'phone' && (!/^\+?[0-9 ()-]+$/.test(control.value.trim()) || control.value.replace(/\D/g,'').length < 7 || control.value.replace(/\D/g,'').length > 15)) control.setCustomValidity('Escribe un teléfono válido.');
      if (control.name === 'description' && control.value.trim().length < 20) control.setCustomValidity('Describe lo ocurrido con al menos 20 caracteres.');
      if (control.name === 'location' && !control.value.trim()) control.setCustomValidity('Indica el lugar del evento.');
    });
    if (index === 1) validateFiles();
    const invalid = controls.find(control => !control.checkValidity());
    if (invalid) { invalid.setAttribute('aria-invalid','true'); invalid.reportValidity(); return false; }
    return true;
  }
  function validateFiles() {
    const bounds = config?.limits || {max_files:3,file_bytes:2097152,total_bytes:6291456};
    const list = [...files.files];
    let message = '';
    if (list.length > bounds.max_files) message = `Adjunta como máximo ${bounds.max_files} archivos.`;
    else if (list.some(file => !['image/jpeg','image/png','image/webp','application/pdf'].includes(file.type))) message = 'Usa fotos JPG, PNG o WebP, o documentos PDF.';
    else if (list.some(file => file.size === 0 || file.size > bounds.file_bytes)) message = 'Revisa que cada archivo tenga contenido y no supere el tamaño permitido.';
    else if (list.reduce((total,file) => total + file.size,0) > bounds.total_bytes) message = 'Los archivos superan el tamaño total permitido.';
    files.setCustomValidity(message);
    const target = document.querySelector('#claim-file-list');
    target.replaceChildren();
    list.forEach(file => {
      const row = document.createElement('li'), name = document.createElement('span'), size = document.createElement('span');
      name.textContent = file.name; size.textContent = `${(file.size / 1048576).toFixed(2)} MB`;
      row.append(name,size); target.append(row);
    });
    return !message;
  }
  function review() {
    const container = document.querySelector('#claim-review');
    container.replaceChildren();
    const labels = [['name','Nombre'],['phone','Teléfono'],['email','Correo'],['insurer','Aseguradora'],['policy','Póliza'],['event_type','Evento'],['event_date','Fecha'],['event_time','Hora de Quito'],['location','Lugar'],['description','Descripción']];
    const add = (label,value) => { const row=document.createElement('div'), term=document.createElement('dt'), detail=document.createElement('dd'); term.textContent=label; detail.textContent=value || 'No indicado'; row.append(term,detail); container.append(row); };
    labels.forEach(([name,label]) => add(label,field(name).value.trim()));
    add('Adjuntos', [...files.files].map(file=>file.name).join('\n') || 'Sin adjuntos');
  }
  async function loadConfig() {
    const response = await fetch(endpoint, {credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(12000)});
    const data = await response.json();
    if (!response.ok || !data.ok || !data.ready || data.recipient !== 'siniestros@efyseguros.com' || !data.csrf) throw Error('El envío no está disponible. Puedes escribir a siniestros@efyseguros.com.');
    config = data;
    send.disabled = false;
    availability.hidden = true;
    document.querySelector('#claim-file-hint').textContent = `Hasta ${data.limits.max_files} archivos JPG, PNG, WebP o PDF. Máximo ${(data.limits.file_bytes / 1048576).toFixed(1)} MB por archivo y ${(data.limits.total_bytes / 1048576).toFixed(1)} MB en total.`;
    validateFiles();
  }
  form.querySelectorAll('[data-claim-next]').forEach(button => button.addEventListener('click',()=>{errorBox.hidden=true;if(validateStep(current))showStep(current+1);}));
  form.querySelectorAll('[data-claim-back]').forEach(button => button.addEventListener('click',()=>{errorBox.hidden=true;showStep(current-1);}));
  form.addEventListener('input',event=>{requestId=undefined;event.target.setCustomValidity?.('');event.target.removeAttribute('aria-invalid');});
  files.addEventListener('change',()=>{requestId=undefined;validateFiles();});
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(sending)return;
    errorBox.hidden=true;
    for(let i=0;i<steps.length;i++){
      showStep(i,false);
      if(!validateStep(i))return;
    }
    showStep(2,false);
    if(!config){showError('El envío no está disponible. Puedes escribir a siniestros@efyseguros.com.');return;}
    requestId ||= crypto.randomUUID();
    const body = new FormData(form);
    body.append('csrf',config.csrf);
    body.append('request_id',requestId);
    sending=true;
    steps.forEach(step=>step.disabled=true);
    send.disabled=true;
    const original=send.innerHTML;
    send.textContent='Enviando reporte…';
    try{
      const submit=()=>fetch(endpoint,{method:'POST',credentials:'same-origin',body,signal:AbortSignal.timeout(45000)});
      let response=await submit();
      let data=await response.json();
      if(response.status===419){await loadConfig();body.set('csrf',config.csrf);response=await submit();data=await response.json();}
      if(!response.ok || !data.ok){
        steps.forEach(step=>step.disabled=false);
        if(data.errors){
          const first=Object.keys(data.errors)[0];
          Object.entries(data.errors).forEach(([name,message])=>{const control=field(name);control?.setCustomValidity(message);control?.setAttribute('aria-invalid','true');});
          const control=field(first);
          if(control){showStep(Number(control.closest('.claim-step').dataset.step));control.reportValidity();}
        }
        showError(data.message || 'No pudimos completar el envío. Conserva los datos y vuelve a intentarlo.');
        return;
      }
      receipt={...data,summary:[...document.querySelectorAll('#claim-review>div')].map(row=>`${row.querySelector('dt').textContent}: ${row.querySelector('dd').textContent}`).join('\n')};
      form.hidden=true;
      document.querySelector('.claim-progress').hidden=true;
      document.querySelector('#claim-reference').textContent=data.reference;
      const stamp=new Date(data.received_at);
      document.querySelector('#claim-received-at').textContent=`Fecha de envío: ${new Intl.DateTimeFormat('es-EC',{dateStyle:'long',timeStyle:'short',timeZone:'America/Guayaquil'}).format(stamp)} · hora de Quito`;
      const success=document.querySelector('#claim-success');success.hidden=false;
      const title=document.querySelector('#claim-success-title');title.tabIndex=-1;title.focus();
    }catch{
      showError('No pudimos confirmar la respuesta del servidor. Puedes volver a intentarlo sin cambiar los datos: conservaremos el mismo intento para evitar un reporte duplicado. También puedes escribir a siniestros@efyseguros.com.');
    }finally{
      sending=false;
      steps.forEach(step=>step.disabled=false);
      send.disabled=!config;
      send.innerHTML=original;
    }
  });
  document.querySelector('#claim-download').addEventListener('click',()=>{
    if(!receipt)return;
    const text=`COMPROBANTE DE ENVÍO A EFY\nReferencia: ${receipt.reference}\nFecha: ${receipt.received_at}\nDestinatario: ${receipt.recipient}\n\n${receipt.summary}\n\nEl servidor aceptó el envío al correo de Efy. Esta referencia no confirma cobertura ni sustituye el aviso exigido por la aseguradora. Los adjuntos se enviaron por correo y no están incluidos en este comprobante.`;
    const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
    const link=document.createElement('a');link.href=url;link.download=`${receipt.reference.replace(/[^A-Z0-9-]/g,'')}.txt`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  showStep(0,false);
  loadConfig().catch(error=>{availability.textContent=error.message==='El envío no está disponible. Puedes escribir a siniestros@efyseguros.com.'?error.message:'No pudimos comprobar el envío. Actualiza la página o escribe a siniestros@efyseguros.com.';});
})();
