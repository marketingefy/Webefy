(() => {
  const form = document.querySelector('#error-form');
  if (!form) return;
  const result = document.querySelector('#error-result');
  const summary = document.querySelector('#error-summary');
  const status = document.querySelector('#error-status');
  const pageField = document.querySelector('#error-page');
  const description = document.querySelector('#error-description');
  form.addEventListener('input', () => {
    result.hidden = true;
    pageField.setCustomValidity('');
    description.setCustomValidity('');
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    pageField.setCustomValidity(pageField.value.trim() ? '' : 'Indica la página donde ocurrió el error.');
    description.setCustomValidity(description.value.trim().length >= 10 ? '' : 'Describe el error con al menos 10 caracteres.');
    if (!form.reportValidity()) return;
    summary.value = `Reporte de error de la web de Efy\n\nPágina o apartado: ${pageField.value.trim()}\nProblema: ${document.querySelector('#error-type').value}\nDispositivo o navegador: ${document.querySelector('#error-device').value.trim() || 'No indicado'}\n\nQué ocurrió:\n${description.value.trim()}`;
    document.querySelector('#error-email').href = `mailto:${form.dataset.recipient}?subject=${encodeURIComponent('Error en la web de Efy')}&body=${encodeURIComponent(summary.value)}`;
    status.textContent = 'El reporte está preparado. Envía el mensaje desde tu aplicación de correo; la web no lo ha enviado.';
    result.hidden = false;
    summary.focus();
  });
  document.querySelector('#error-copy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(summary.value);
      status.textContent = 'Reporte copiado. Pégalo en un correo a ' + form.dataset.recipient + ' y envíalo.';
    } catch {
      summary.focus();
      summary.select();
      status.textContent = 'Seleccionamos el reporte. Cópialo y envíalo a ' + form.dataset.recipient + '.';
    }
  });
})();
