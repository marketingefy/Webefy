(() => {
  document.documentElement.classList.add('js');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const faq = JSON.parse(document.querySelector('#faq-data').textContent);
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  menu.addEventListener('click', () => {
    const opened = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(opened));
    nav.classList.toggle('is-open', opened);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      menu.setAttribute('aria-expanded', 'false');
      menu.focus();
    }
  });

  // The guide uses the site's published FAQ, with no API calls or saved conversations.
  const dialog = document.querySelector('#evia-dialog');
  const messages = document.querySelector('#chat-messages');
  const input = document.querySelector('#chat-input');
  const fab = document.querySelector('.chat-fab');
  let lastTrigger;
  const intents = [
    ['socios', ['socios', 'aliados', 'aseguradoras trabajan', 'aseguradoras trabaja', 'aseguradoras tienen', 'aseguradoras cuentan', 'con que aseguradora']],
    ['servicios', ['servicio', 'seguros ofrecen', 'seguros tienen', 'seguros cuentan', 'tipos de seguros', 'catalogo', 'ramos']],
    ['deducible', ['deducible', 'deducibles', 'franquicia']],
    ['exclusiones', ['exclusion', 'exclusiones', 'no cubre', 'no cubierto']],
    ['cobertura', ['cobertura', 'coberturas', 'cubre', 'proteccion']],
    ['renovar', ['renovar', 'renovacion', 'vencimiento', 'vence']],
    ['siniestro', ['siniestro', 'accidente', 'emergencia', 'choque', 'reclamo', 'robo']],
    ['documentos', ['asistencia', 'telefono de aseguradora']],
    ['ubicacion', ['donde', 'ubicacion', 'direccion', 'quito', 'ciudad']],
    ['contacto', ['contactar', 'contacto', 'whatsapp', 'correo', 'telefono', 'horario']],
    ['cotizar', ['cotizar', 'cotizacion', 'precio', 'costo', 'cuesta', 'documentos', 'requisitos']],
    ['elegir', ['elegir', 'empiezo', 'comparar', 'necesito un seguro']],
    ['evia', ['evia', 'quien eres', 'como funciona', 'inteligencia artificial', 'eres ia', 'eres un bot']]
  ];
  function answerFor(question) {
    const cleaned = normalize(question);
    const exact = faq.find(item => normalize(item.question) === cleaned);
    if (exact) return { text: exact.answer, id: exact.id };
    if (/^(hola|buenas|buenos dias|buenas tardes|buenas noches|hey)[!.\s]*$/.test(cleaned)) return { text: 'Hola. Puedo ayudarte con conceptos de seguros y preguntas frecuentes de Efy. ¿Quieres conocer qué es una cobertura, un deducible o cómo preparar una consulta?' };
    if (/^(gracias|muchas gracias|perfecto|listo)[!.\s]*$/.test(cleaned)) return { text: 'Con gusto. Puedes seguir preguntando o revisar el centro de ayuda.' };
    if (/mi poliza|mi cobertura|me cubre|estoy cubierto|numero de poliza|numero de cedula/.test(cleaned)) return { text: 'No puedo consultar una póliza ni confirmar si un evento particular está cubierto. Revisa las condiciones de tu contrato y consulta a tu aseguradora por su canal oficial.', id: 'cobertura' };
    const intent = intents.find(([, words]) => words.some(word => cleaned.includes(word)));
    if (intent) {
      const item = faq.find(item => item.id === intent[0]);
      return { text: item.answer, id: item.id };
    }
    const tokens = cleaned.split(/\W+/).filter(token => token.length > 3 && !['quiero','puedo','tengo','sobre','saber','seguro','seguros','necesito','pregunta'].includes(token));
    const scored = faq.map(item => ({ item, score: tokens.filter(token => normalize(item.question).includes(token)).length })).sort((a,b) => b.score - a.score);
    if (scored[0]?.score >= 2) return { text: scored[0].item.answer, id: scored[0].item.id };
    return { text: 'No tengo una respuesta confirmada para esa pregunta. Esta guía puede orientarte sobre coberturas, deducibles, exclusiones, renovaciones o cómo preparar una consulta. Para condiciones de un seguro específico, revisa la póliza y consulta a la aseguradora.' };
  }
  function addMessage(text, author, faqId) {
    const entry = document.createElement('div');
    entry.className = `chat-message ${author}`;
    const name = document.createElement('span');
    name.textContent = author === 'user' ? 'Tú' : 'EVIA';
    const body = document.createElement('p');
    body.textContent = text;
    entry.append(name, body);
    if (faqId) {
      const link = document.createElement('a');
      link.href = `ayuda.html#faq-${faqId}`;
      link.textContent = 'Ver en el centro de ayuda →';
      entry.append(link);
      if (faqId === 'siniestro') {
        const reportLink = document.createElement('a');
        reportLink.href = 'siniestros.html';
        reportLink.textContent = 'Ir al módulo Siniestros →';
        entry.append(reportLink);
      }
      if (faqId === 'servicios') {
        const servicesLink = document.createElement('a');
        servicesLink.href = 'servicios.html#catalogo';
        servicesLink.textContent = 'Explorar Servicios →';
        entry.append(servicesLink);
      }
      if (faqId === 'socios') {
        const partnersLink = document.createElement('a');
        partnersLink.href = 'socios.html';
        partnersLink.textContent = 'Ver Socios estratégicos →';
        entry.append(partnersLink);
      }
    }
    messages.append(entry);
    messages.scrollTop = messages.scrollHeight;
  }
  function submitQuestion(question) {
    const text = question.trim().slice(0, 400);
    if (!text) return;
    addMessage(text, 'user');
    const answer = answerFor(text);
    addMessage(answer.text, 'bot', answer.id);
    input.value = '';
    input.focus();
  }
  function openChat(trigger) {
    lastTrigger = trigger;
    if (!dialog.open) dialog.showModal();
    fab.setAttribute('aria-expanded', 'true');
    input.focus();
  }
  document.querySelectorAll('[data-open-chat]').forEach(trigger => {
    trigger.addEventListener('click', () => openChat(trigger));
  });
  document.querySelectorAll('[data-chat-question]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      openChat(trigger);
      submitQuestion(trigger.dataset.chatQuestion);
    });
  });
  document.querySelector('#close-chat').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    fab.setAttribute('aria-expanded', 'false');
    lastTrigger?.focus();
  });
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  document.querySelector('#chat-form').addEventListener('submit', event => {
    event.preventDefault();
    submitQuestion(input.value);
  });

  const search = document.querySelector('#faq-search');
  if (search) {
    const filters = [...document.querySelectorAll('[data-category].filter-button')];
    const items = [...document.querySelectorAll('.faq-item')];
    const clear = document.querySelector('#clear-search');
    let category = 'Todas';
    function filterQuestions() {
      const query = normalize(search.value);
      let count = 0;
      items.forEach(item => {
        const show = (category === 'Todas' || item.dataset.category === category) && normalize(item.textContent).includes(query);
        item.hidden = !show;
        if (show) count++;
      });
      clear.hidden = !search.value;
      document.querySelector('#no-results').hidden = count !== 0;
      document.querySelector('#search-status').textContent = `${count} ${count === 1 ? 'pregunta encontrada' : 'preguntas encontradas'}`;
    }
    search.addEventListener('input', filterQuestions);
    search.closest('form').addEventListener('submit', event => { event.preventDefault(); filterQuestions(); });
    clear.addEventListener('click', () => { search.value = ''; filterQuestions(); search.focus(); });
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.category;
      filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
      filterQuestions();
    }));
    if (location.hash) {
      const target = document.getElementById(location.hash.slice(1));
      if (target?.classList.contains('faq-item')) target.open = true;
    }
  }

  const consult = document.querySelector('#consult-form');
  if (consult) {
    const summary = document.querySelector('#consult-summary');
    const status = document.querySelector('#copy-status');
    consult.addEventListener('input', () => { document.querySelector('#consult-result').hidden = true; status.textContent = ''; });
    consult.addEventListener('submit', event => {
      event.preventDefault();
      const question = document.querySelector('#consult-question').value.trim();
      const questionField = document.querySelector('#consult-question');
      questionField.setCustomValidity(question ? '' : 'Escribe tu pregunta para preparar la consulta.');
      if (!consult.reportValidity()) return;
      summary.value = `Consulta para Efy Seguros\nTema: ${document.querySelector('#consult-topic').value}\n\n${question}`;
      document.querySelector('#consult-result').hidden = false;
      status.textContent = 'Resumen preparado. No se ha enviado al equipo de Efy.';
      summary.focus();
    });
    document.querySelector('#consult-question').addEventListener('input', event => event.target.setCustomValidity(''));
    document.querySelector('#copy-consult').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(summary.value);
        status.textContent = 'Consulta copiada. Puedes pegarla en tu próxima conversación.';
      } catch {
        summary.focus();
        summary.select();
        status.textContent = 'Seleccionamos el resumen. Usa la opción Copiar de tu dispositivo.';
      }
    });
  }

  const video = document.querySelector('.workshop-video');
  if (video) {
    const scene = document.querySelector('.workshop');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const mobile = matchMedia('(max-width:760px)');
    let visible = true;
    let failed = false;
    let attempt = 0;
    const canPlay = () => !reduced.matches && !navigator.connection?.saveData && !document.hidden && visible && !failed;
    async function playback() {
      const request = ++attempt;
      if (!canPlay()) { video.pause(); return; }
      if (!video.getAttribute('src')) video.src = mobile.matches ? '../assets/evia-workshop-loop-mobile.mp4?v=evia-wide-restored-20261009' : '../assets/evia-workshop-loop.mp4?v=evia-wide-restored-20261009';
      try {
        await video.play();
        if (request !== attempt || !canPlay()) { if (!canPlay()) video.pause(); return; }
        scene.classList.add('is-ready');
      } catch { /* Keep the poster when autoplay is unavailable. */ }
    }
    const preferenceChanged = () => { if (reduced.matches || navigator.connection?.saveData) scene.classList.remove('is-ready'); playback(); };
    video.addEventListener('error', () => { failed = true; scene.classList.remove('is-ready'); video.pause(); });
    reduced.addEventListener('change', preferenceChanged);
    navigator.connection?.addEventListener('change', preferenceChanged);
    document.addEventListener('visibilitychange', playback);
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { visible = entries[0].isIntersecting; playback(); }).observe(scene);
    playback();
  }
})();
