(() => {
  const form = document.querySelector('#lookup-form');
  if (!form) return;

  const type = document.querySelector('#lookup-type');
  const methods = [...form.querySelectorAll('input[name="lookup-method"]')];
  const cedula = document.querySelector('#lookup-cedula');
  const plate = document.querySelector('#lookup-plate');
  const result = document.querySelector('#lookup-result');
  const summary = document.querySelector('#lookup-summary');
  const email = document.querySelector('#lookup-email');
  const status = document.querySelector('#lookup-status');
  const recipient = 'siniestros@efyseguros.com';
  const topics = {
    vehicular: 'siniestro vehicular',
    siniestro: 'otro siniestro',
    reembolso: 'reembolso'
  };

  function resetResult() {
    result.hidden = true;
    summary.value = '';
    email.href = 'mailto:' + recipient;
    if (status) status.textContent = '';
  }

  function normalizedPlate() {
    return plate.value.toUpperCase().replace(/[\s-]/g, '');
  }

  function validatePlate() {
    const value = normalizedPlate();
    const valid = /^[A-Z0-9]{5,8}$/.test(value) && /[A-Z]/.test(value) && /[0-9]/.test(value);
    plate.setCustomValidity(!plate.disabled && plate.value !== '' && !valid
      ? 'Escribe una placa de 5 a 8 letras y números, con al menos una letra y un número. Por ejemplo: ABC-1234.'
      : '');
  }

  function updateLookup() {
    const vehicular = type.value === 'vehicular';
    document.querySelector('#lookup-plate-option').hidden = !vehicular;
    if (!vehicular) methods.find(method => method.value === 'cedula').checked = true;
    const byPlate = vehicular && methods.some(method => method.value === 'placa' && method.checked);
    document.querySelector('#lookup-cedula-field').hidden = byPlate;
    document.querySelector('#lookup-plate-field').hidden = !byPlate;
    cedula.disabled = byPlate;
    cedula.required = !byPlate;
    plate.disabled = !byPlate;
    plate.required = byPlate;
    validatePlate();
    resetResult();
  }

  type.addEventListener('change', updateLookup);
  methods.forEach(method => method.addEventListener('change', updateLookup));
  cedula.addEventListener('input', resetResult);
  plate.addEventListener('input', () => {
    validatePlate();
    resetResult();
  });

  form.addEventListener('submit', event => {
    event.preventDefault();
    validatePlate();
    if (!form.reportValidity()) return;

    const byPlate = !plate.disabled;
    const identifier = byPlate ? normalizedPlate() : cedula.value;
    if (byPlate) plate.value = identifier;
    const topic = topics[type.value];
    if (!topic) return;

    const body = 'Hola, equipo de Efy:\n\n'
      + 'Quisiera consultar sobre mi ' + topic + '.\n'
      + (byPlate ? 'Placa del vehículo: ' : 'Cédula: ') + identifier + '\n\n'
      + 'Por favor, indíquenme cómo consultar el avance de mi caso y qué información necesitan para verificar mi identidad.\n\n'
      + 'Gracias.';
    summary.value = body;
    email.href = 'mailto:' + recipient
      + '?subject=' + encodeURIComponent('Consulta de ' + topic + ' · Efy Seguros')
      + '&body=' + encodeURIComponent(body);
    result.hidden = false;
    if (status) status.textContent = 'Consulta preparada. Revisa el resumen y abre tu correo para enviarla.';
  });

  updateLookup();
  // Identifiers stay in this page. Preparing the draft makes no request, stores
  // nothing and sends no email; only the visitor can open and send their draft.
})();
