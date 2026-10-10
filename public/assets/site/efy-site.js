(() => {
  document.documentElement.classList.add('js');
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const faq = JSON.parse(document.querySelector('#faq-data').textContent);
  const contacts = JSON.parse(document.querySelector('#contact-data').textContent);
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
  // Glass is the approved shared design; old simulation links can still open it directly.
  const glassPreview = new URLSearchParams(location.search).get('evia') === 'cristal';
  dialog.classList.add('is-glass');
  if (glassPreview) {
    document.querySelectorAll('a[href]').forEach(link => {
      const url = new URL(link.href, location.href);
      if (url.origin === location.origin && url.pathname.endsWith('.html')) {
        url.searchParams.set('evia', 'cristal');
        link.href = url.href;
      }
    });
  }
  const messages = document.querySelector('#chat-messages');
  const input = document.querySelector('#chat-input');
  const fab = document.querySelector('.chat-fab');
  const previewVersion = document.querySelector('meta[name="efy-site-version"]')?.content;
  function siteLink(path) {
    if (!previewVersion) return path;
    const url = new URL(path, location.href);
    url.searchParams.set('v', previewVersion);
    if (glassPreview) url.searchParams.set('evia', 'cristal');
    return url.href;
  }
  let lastTrigger;
  const businessMenus = {
    inicio: {
      text: 'Hola, soy EVIA, tu asistente virtual de Efy. ¿En qué puedo ayudarte?',
      options: [
        { menu: 'cotizar', label: 'Solicitar una cotización' },
        { menu: 'poliza', label: 'Dudas sobre mi póliza' },
        { menu: 'asistencia', label: 'Siniestros y asistencia' },
        { faq: 'contacto', label: 'Hablar con un asesor' }
      ]
    },
    cotizar: {
      faq: 'cotizar',
      options: [
        { href: 'servicios.html#seguro-vehiculos', label: 'Seguro de vehículos' },
        { href: 'servicios.html#seguro-hogar', label: 'Seguro de hogar' },
        { href: 'servicios.html#seguro-pymes', label: 'Seguro para pymes' },
        { href: 'servicios.html', label: 'Explorar todos los seguros' },
        { faq: 'contacto', label: 'Hablar con un asesor' }
      ]
    },
    poliza: {
      text: 'Te ayudo a entender los conceptos de tu póliza. ¿Qué te gustaría revisar?',
      options: [
        { faq: 'vigencia', label: 'Vigencia de la póliza' },
        { faq: 'cobertura', label: 'Entender las coberturas' },
        { faq: 'deducible', label: 'Entender el deducible' },
        { faq: 'renovar', label: 'Renovar mi seguro' },
        { faq: 'contacto', label: 'Consultar con un asesor' }
      ]
    },
    asistencia: {
      text: 'Encuentra el siguiente paso para tu caso. Si hay una emergencia en Ecuador, llama al 911.',
      options: [
        { href: 'reportar-siniestro.html', label: 'Reportar un siniestro' },
        { href: 'consultas.html', label: 'Estado de siniestros y reembolsos' },
        { faq: 'reembolso-documentos', label: 'Preparar un reembolso' },
        { href: 'lineas-asistencia.html', label: 'Asistencia de mi aseguradora' }
      ]
    }
  };
  const messageClock = new Intl.DateTimeFormat('es-EC', { hour: '2-digit', minute: '2-digit', hour12: false });
  function stampMessage(entry) {
    if (entry.querySelector('.chat-message-time')) return;
    const now = new Date();
    const time = document.createElement('time');
    time.className = 'chat-message-time';
    time.dateTime = now.toISOString();
    time.textContent = messageClock.format(now);
    time.setAttribute('aria-label', `Hora del mensaje: ${time.textContent}`);
    entry.append(time);
  }
  function appendBusinessOptions(entry, options) {
    const list = document.createElement('div');
    list.className = 'chat-business-options';
    list.setAttribute('aria-label', 'Opciones de atención');
    options.forEach((option, index) => {
      const action = document.createElement(option.href ? 'a' : 'button');
      if (option.href) action.href = siteLink(option.href);
      else {
        action.type = 'button';
        if (option.menu) action.dataset.chatMenu = option.menu;
        else action.dataset.chatFaq = option.faq;
      }
      const number = document.createElement('span');
      number.className = 'chat-option-number';
      number.textContent = String(index + 1).padStart(2, '0');
      number.setAttribute('aria-hidden', 'true');
      const label = document.createElement('span');
      label.textContent = option.label;
      const arrow = document.createElement('span');
      arrow.className = 'chat-option-arrow';
      arrow.textContent = '›';
      arrow.setAttribute('aria-hidden', 'true');
      action.append(number, label, arrow);
      list.append(action);
    });
    entry.classList.add('chat-menu-message');
    entry.insertBefore(list, entry.querySelector('.chat-message-time'));
    messages.scrollTop = messages.scrollHeight;
  }
  const intents = [
    ['estado', ['estado', 'reembolso', 'seguimiento de siniestro', 'seguimiento de mi siniestro']],
    ['lineas', ['lineas de asistencia', 'linea de asistencia', 'telefono de asistencia', 'asistencia vehicular', 'asistencia medica']],
    ['resenas', ['resena', 'opinion', 'testimonio', 'valoracion', 'experiencias de clientes']],
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
    if (/contact|comunicar|whatsapp|telefono|llamar|hablar con/.test(cleaned) && contacts.providers.some(provider => (` ${cleaned.replace(/[^a-z0-9]+/g, ' ')} `).includes(` ${normalize(provider).replace(/[^a-z0-9]+/g, ' ')} `))) {
      const lines = faq.find(item => item.id === 'lineas');
      return { text: lines.answer, id: 'lineas' };
    }
    const padded = ` ${cleaned.replace(/[^a-z0-9]+/g, ' ')} `;
    const researched = faq.map(item => ({item, score: Math.max(0, ...(item.aliases || []).map(alias => padded.includes(` ${normalize(alias)} `) ? alias.length : 0))})).sort((a,b) => b.score - a.score)[0];
    if (researched?.score > 0) return { text: researched.item.answer, id: researched.item.id };
    if (/contacta|contacto|comunicar|whatsapp|hablar con (efy|un asesor|una persona|el equipo|comercial)|asesor comercial/.test(cleaned)) {
      const contact = faq.find(item => item.id === 'contacto');
      return { text: contact.answer, id: 'contacto' };
    }
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
    if (faqId === 'contacto') {
      const actions = document.createElement('div');
      actions.className = 'chat-contact-actions';
      contacts.whatsapp.forEach(contact => {
        const action = document.createElement('a');
        action.href = contact.url;
        action.className = 'chat-whatsapp';
        action.textContent = `WhatsApp comercial · ${contact.label}`;
        actions.append(action);
      });
      entry.append(actions);
    }
    if (faqId) {
      const source = faq.find(item => item.id === faqId)?.source;
      if (source?.url) {
        const sourceLink = document.createElement('a');
        sourceLink.href = source.url;
        sourceLink.textContent = `Fuente: ${source.label}`;
        sourceLink.className = 'chat-source';
        entry.append(sourceLink);
      }
      const link = document.createElement('a');
      link.href = siteLink(`ayuda.html#faq-${faqId}`);
      link.textContent = 'Ver en el centro de ayuda →';
      entry.append(link);
      if (faqId === 'siniestro') {
        const reportLink = document.createElement('a');
        reportLink.href = siteLink('reportar-siniestro.html');
        reportLink.textContent = 'Reportar en Asistencia →';
        entry.append(reportLink);
      }
      if (faqId === 'servicios') {
        const servicesLink = document.createElement('a');
        servicesLink.href = siteLink('servicios.html#catalogo');
        servicesLink.textContent = 'Explorar Servicios →';
        entry.append(servicesLink);
      }
      if (faqId === 'socios') {
        const partnersLink = document.createElement('a');
        partnersLink.href = siteLink('socios.html');
        partnersLink.textContent = 'Ver Socios estratégicos →';
        entry.append(partnersLink);
      }
      if (faqId === 'resenas') {
        const reviewsLink = document.createElement('a');
        reviewsLink.href = siteLink('resenas.html');
        reviewsLink.textContent = 'Ver Reseñas →';
        entry.append(reviewsLink);
      }
      if (faqId === 'estado' || faqId === 'lineas') {
        const assistanceLink = document.createElement('a');
        assistanceLink.href = siteLink(faqId === 'estado' ? 'consultas.html' : 'lineas-asistencia.html');
        assistanceLink.textContent = faqId === 'estado' ? 'Consultar por mi caso →' : 'Ver líneas de asistencia →';
        entry.append(assistanceLink);
      }
    }
    stampMessage(entry);
    messages.append(entry);
    messages.scrollTop = messages.scrollHeight;
    return entry;
  }
  function submitQuestion(question, { focusInput = true } = {}) {
    const text = question.trim().slice(0, 400);
    if (!text) return;
    addMessage(text, 'user');
    const answer = answerFor(text);
    addMessage(answer.text, 'bot', answer.id);
    input.value = '';
    if (focusInput) input.focus();
  }
  function openChat(trigger) {
    lastTrigger = trigger;
    stampMessage(messages.querySelector('.chat-message'));
    if (!dialog.open) dialog.showModal();
    fab.setAttribute('aria-expanded', 'true');
    document.querySelector('#close-chat').focus({ preventScroll: true });
  }
  document.querySelectorAll('[data-open-chat]').forEach(trigger => {
    trigger.addEventListener('click', () => openChat(trigger));
  });
  document.querySelectorAll('[data-chat-question]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      openChat(trigger);
      submitQuestion(trigger.dataset.chatQuestion, { focusInput: false });
    });
  });
  messages.addEventListener('click', event => {
    const action = event.target.closest('button[data-chat-menu],button[data-chat-faq]');
    if (!action || !messages.contains(action)) return;
    if (action.dataset.chatFaq) {
      const item = faq.find(item => item.id === action.dataset.chatFaq);
      if (item) submitQuestion(item.question, { focusInput: false });
      return;
    }
    const menu = businessMenus[action.dataset.chatMenu];
    if (!menu) return;
    addMessage(action.children[1].textContent, 'user');
    const item = menu.faq ? faq.find(item => item.id === menu.faq) : null;
    const entry = addMessage(item?.answer || menu.text, 'bot', item?.id);
    appendBusinessOptions(entry, menu.options);
  });
  document.querySelector('#chat-menu-toggle')?.addEventListener('click', () => {
    addMessage('Ver opciones', 'user');
    const entry = addMessage('¿En qué puedo ayudarte?', 'bot');
    appendBusinessOptions(entry, businessMenus.inicio.options);
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
  appendBusinessOptions(messages.querySelector('.chat-message'), businessMenus.inicio.options);

  const search = document.querySelector('#faq-search');
  function providerDirectory(inputId, itemSelector, countId, emptyId) {
    const input = document.querySelector(inputId);
    if (!input) return;
    const items = [...document.querySelectorAll(itemSelector)];
    function filter() {
      const query = normalize(input.value);
      let count = 0;
      items.forEach(item => {
        item.hidden = !normalize(item.dataset.provider).includes(query);
        if (!item.hidden) count++;
      });
      document.querySelector(countId).textContent = `${count} ${count === 1 ? 'socio encontrado' : 'socios encontrados'}`;
      document.querySelector(emptyId).hidden = count !== 0;
    }
    input.addEventListener('input', filter);
    filter();
  }
  providerDirectory('#partner-search', '.partner-card', '#partner-count', '#partner-empty');
  providerDirectory('#assistance-search', '.assistance-card', '#assistance-count', '#assistance-empty');
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
      document.querySelector('#consult-whatsapp').href = contacts.whatsapp[0].url + '?text=' + encodeURIComponent(summary.value);
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

  const reviewRail = document.querySelector('.review-demo-rail');
  if (reviewRail) {
    const previous = document.querySelector('.review-prev');
    const next = document.querySelector('.review-next');
    const position = document.querySelector('.review-position');
    const stride = () => reviewRail.firstElementChild.getBoundingClientRect().width + parseFloat(getComputedStyle(reviewRail).columnGap);
    function updateReviews() {
      const start = Math.round(reviewRail.scrollLeft / stride()) + 1;
      const visible = Math.max(1, Math.floor((reviewRail.clientWidth + 24) / stride()));
      const label = `${start}–${Math.min(start + visible - 1, reviewRail.children.length)} de ${reviewRail.children.length} ejemplos`;
      if (position.textContent !== label) position.textContent = label;
      previous.disabled = reviewRail.scrollLeft <= 2;
      next.disabled = reviewRail.scrollLeft >= reviewRail.scrollWidth - reviewRail.clientWidth - 2;
    }
    function moveReviews(direction) {
      reviewRail.scrollBy({left: direction * stride(), behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    }
    previous.addEventListener('click', () => moveReviews(-1));
    next.addEventListener('click', () => moveReviews(1));
    reviewRail.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        moveReviews(event.key === 'ArrowRight' ? 1 : -1);
      }
    });
    reviewRail.addEventListener('scroll', updateReviews, {passive:true});
    new ResizeObserver(updateReviews).observe(reviewRail);
    updateReviews();
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
  if (glassPreview) openChat(fab);
})();
