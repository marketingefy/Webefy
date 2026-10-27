(() => {
  'use strict';
  const form = document.querySelector('#coverage-form');
  if (!form) return;

  const endpoint = '/nueva/api/coberturas.php';
  const workspace = document.querySelector('.coverage-workspace');
  const cooperative = document.querySelector('#coverage-cooperative');
  const confirmation = document.querySelector('#coverage-confirm');
  const cooperativeCard = document.querySelector('#coverage-cooperative-card');
  const queryFields = document.querySelector('#coverage-query-fields');
  const cedula = document.querySelector('#coverage-cedula');
  const consent = document.querySelector('#coverage-consent');
  const submit = document.querySelector('#coverage-submit');
  const retry = document.querySelector('#coverage-retry');
  const status = document.querySelector('#coverage-status');
  const results = document.querySelector('#coverage-results');
  const records = document.querySelector('#coverage-records');
  const summary = document.querySelector('#coverage-summary');
  const queryDate = document.querySelector('#coverage-query-date');
  const clear = document.querySelector('#coverage-clear');
  const pendingNote = document.querySelector('#coverage-pending');
  let csrf = '';
  let ready = false;
  let busy = false;
  let selectionVersion = 0;

  function message(text, error = false) {
    status.textContent = text;
    status.classList.toggle('is-error', error);
  }

  function update() {
    const confirmed = cooperative.value === 'coopartamos' && confirmation.checked;
    cooperativeCard.hidden = cooperative.value !== 'coopartamos';
    confirmation.disabled = cooperative.value !== 'coopartamos' || busy;
    queryFields.disabled = !confirmed || !ready || busy;
    submit.disabled = !confirmed || !ready || busy;
    cooperative.disabled = busy;
    retry.disabled = busy;
    clear.disabled = busy;
    workspace.setAttribute('aria-busy', String(busy));
  }

  function clearResult() {
    records.replaceChildren();
    summary.textContent = '';
    queryDate.textContent = '';
    results.hidden = true;
  }

  async function request(options = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 22000);
    try {
      const response = await fetch(endpoint, {
        credentials: 'same-origin', cache: 'no-store', signal: controller.signal,
        headers: { Accept: 'application/json', ...(options.body ? { 'Content-Type': 'application/json' } : {}) },
        ...options
      });
      let data;
      try { data = await response.json(); }
      catch { throw new Error('invalid-response'); }
      return { response, data };
    } finally { clearTimeout(timer); }
  }

  async function loadConfiguration() {
    busy = true;
    ready = false;
    csrf = '';
    message('Comprobando disponibilidad de la consulta…');
    update();
    try {
      const { response, data } = await request();
      ready = response.ok && data?.ok === true && data.ready === true && typeof data.csrf === 'string' && data.csrf.length > 0;
      csrf = ready ? data.csrf : '';
      message(ready ? 'Consulta disponible. Selecciona tu cooperativa para continuar.' : 'La consulta no está disponible en este momento. Puedes contactar al equipo operativo de Efy.', !ready);
    } catch {
      message('No pudimos conectar con la consulta. Inténtalo de nuevo o contacta al equipo operativo de Efy.', true);
    } finally {
      busy = false;
      retry.hidden = ready;
      update();
    }
  }

  function text(value, limit = 160) {
    return typeof value === 'string' && value.length <= limit && value.trim() ? value.trim() : null;
  }

  function displayDate(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(value)) return 'No informada';
    const day = value.slice(0, 10);
    const parsed = new Date(day + 'T12:00:00Z');
    if (Number.isNaN(parsed.valueOf()) || parsed.toISOString().slice(0, 10) !== day) return 'No informada';
    return new Intl.DateTimeFormat('es-EC', { day: '2-digit', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(parsed);
  }

  function validResult(data) {
    return data?.ok === true && typeof data.encontrado === 'boolean' &&
      Array.isArray(data.registros) && data.registros.length <= 100 &&
      Array.isArray(data.fuentes_pendientes) && data.fuentes_pendientes.every(source => ['PRIVILEGIO', 'PROASSISLIFE'].includes(source)) &&
      data.encontrado === (data.registros.length > 0) &&
      data.registros.every(record => record && typeof record === 'object' && text(record.aseguradora) && text(record.estado));
  }

  function render(data) {
    clearResult();
    const pendingNames = data.fuentes_pendientes.map(source => ({ PRIVILEGIO: 'Privilegio', PROASSISLIFE: 'Proassislife' })[source]);
    pendingNote.hidden = pendingNames.length === 0;
    if (pendingNames.length) {
      pendingNote.querySelector('strong').textContent = 'Información pendiente: ' + pendingNames.join(' y ');
      pendingNote.querySelector('p').textContent = 'Estas carteras aún no están incorporadas. Si no encuentras tu registro, contacta a Efy para revisarlo.';
    }
    summary.textContent = data.encontrado
      ? 'Estos son los registros encontrados en la cartera consultada. Revisa la aseguradora y el estado de cada contrato.'
      : 'No encontramos coincidencias en las carteras consultadas. Esto no confirma que no tengas seguro.' + (pendingNames.length ? ' La información de ' + pendingNames.join(' y ') + ' está pendiente de incorporación.' : ' Contacta a Efy para verificar tu registro.');
    data.registros.forEach(record => {
      const card = document.createElement('article');
      card.className = 'coverage-record';
      const title = document.createElement('h3');
      title.textContent = text(record.aseguradora);
      const details = document.createElement('dl');
      const rows = [
        ['Contrato', text(record.contrato) || 'No informado'],
        ['Estado', ({ VIGENTE: 'Vigente', POR_INICIAR: 'Por iniciar', VENCIDA: 'Vencida', NO_DETERMINADA: 'No determinada' })[record.estado] || text(record.estado)],
        ['Desde', displayDate(record.vigencia_inicio)],
        ['Hasta', displayDate(record.vigencia_fin)]
      ];
      rows.forEach(([label, value]) => {
        const row = document.createElement('div');
        const term = document.createElement('dt');
        const description = document.createElement('dd');
        term.textContent = label;
        description.textContent = value;
        row.append(term, description);
        details.append(row);
      });
      card.append(title, details);
      records.append(card);
    });
    if (text(data.fecha_consulta)) queryDate.textContent = 'Fecha de consulta: ' + displayDate(data.fecha_consulta);
    results.hidden = false;
    results.focus({ preventScroll: true });
    results.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest' });
  }

  cooperative.addEventListener('change', () => {
    selectionVersion++;
    confirmation.checked = false;
    cedula.value = '';
    consent.checked = false;
    clearResult();
    update();
  });
  confirmation.addEventListener('change', () => {
    selectionVersion++;
    clearResult();
    update();
  });
  cedula.addEventListener('input', () => {
    cedula.setCustomValidity('');
    clearResult();
  });
  retry.addEventListener('click', loadConfiguration);
  clear.addEventListener('click', () => {
    form.reset();
    clearResult();
    cedula.setCustomValidity('');
    message(ready ? 'Consulta disponible. Selecciona tu cooperativa para continuar.' : 'La consulta no está disponible en este momento.', !ready);
    update();
    cooperative.focus();
  });

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!ready || busy || cooperative.value !== 'coopartamos' || !confirmation.checked) return;
    cedula.setCustomValidity(/^\d{10}$/.test(cedula.value) ? '' : 'Ingresa los 10 dígitos de tu cédula, sin espacios ni guiones.');
    if (!form.reportValidity() || !consent.checked) return;
    clearResult();
    const version = selectionVersion;
    const body = JSON.stringify({ cooperativa: cooperative.value, cedula: cedula.value, consent: true, csrf });
    busy = true;
    message('Consultando tu registro…');
    update();
    try {
      const { response, data } = await request({ method: 'POST', body });
      if (version !== selectionVersion) return;
      if (response.status === 419) {
        ready = false;
        csrf = '';
        retry.hidden = false;
        message('La sesión de consulta venció. Pulsa «Reintentar conexión» y vuelve a consultar.', true);
      } else if (response.status === 429) {
        message('Se alcanzó el límite de consultas. Espera unos minutos antes de intentarlo de nuevo o contacta al equipo operativo de Efy.', true);
      } else if (response.status === 422) {
        message('Revisa tu cédula y la autorización antes de volver a consultar.', true);
      } else if (!response.ok || !validResult(data)) {
        message('No pudimos completar la consulta. Inténtalo de nuevo o contacta al equipo operativo de Efy. Este error no confirma ausencia de cobertura.', true);
      } else {
        message('Consulta completada.');
        render(data);
      }
    } catch (error) {
      message(error.name === 'AbortError'
        ? 'La consulta tardó más de lo esperado. Vuelve a intentarlo. No se ha podido confirmar tu cobertura.'
        : 'No pudimos completar la consulta. Revisa tu conexión e inténtalo de nuevo. No se ha podido confirmar tu cobertura.', true);
    } finally {
      busy = false;
      update();
    }
  });

  window.addEventListener('pagehide', () => { cedula.value = ''; consent.checked = false; clearResult(); });
  update();
  loadConfiguration();
})();
