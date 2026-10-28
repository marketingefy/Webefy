/* Guided quotes stay on this device until the visitor opens and sends WhatsApp. */
(() => {
  'use strict';
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const revealTargets = document.querySelectorAll('.protection-heading,.protection-card,.business-card,.client-action,.section-heading,.editorial-link');
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.08 });
    revealTargets.forEach(element => {
      element.classList.add('motion-reveal');
      observer.observe(element);
    });
    const showAll = () => {
      if (!reducedMotion.matches) return;
      observer.disconnect();
      revealTargets.forEach(element => element.classList.add('is-revealed'));
    };
    reducedMotion.addEventListener('change', showAll);
  }

  const form = document.getElementById('quote-form');
  if (!form) return;
  const contacts = JSON.parse(document.getElementById('contact-data').textContent);
  const branch = document.getElementById('quote-branch');
  const goal = document.getElementById('quote-goal');
  const notes = document.getElementById('quote-notes');
  const summary = document.getElementById('quote-summary');
  const advisor = document.getElementById('quote-advisor');
  const steps = [...form.querySelectorAll('[data-quote-step]')];
  const back = document.getElementById('quote-back');
  const next = document.getElementById('quote-next');
  const whatsapp = document.getElementById('quote-whatsapp');
  const copyStatus = document.getElementById('quote-copy-status');
  let current = 0;
  // Custom validation only applies to the current step; hidden fields cannot trap focus.
  form.noValidate = true;
  contacts.whatsapp.forEach((contact, index) => {
    const option = document.createElement('option');
    option.value = String(index);
    option.textContent = `Comercial · ${contact.label}`;
    advisor.append(option);
  });
  const selected = new URLSearchParams(location.search).get('ramo');
  if ([...branch.options].some(option => option.value === selected)) branch.value = selected;

  function updateSummary() {
    summary.value = `Solicitud de cotización desde la web de Efy\n\nRamo: ${branch.selectedOptions[0].textContent}\nPrioridad: ${goal.value}${notes.value.trim() ? `\nMi consulta: ${notes.value.trim()}` : ''}`;
    const contact = contacts.whatsapp[Number(advisor.value)] || contacts.whatsapp[0];
    const url = new URL(contact.url);
    const greeting = url.searchParams.get('text');
    url.searchParams.set('text', `${greeting}\n\n${summary.value}`);
    whatsapp.href = url.href;
  }
  function showStep(index, focus = true) {
    current = index;
    steps.forEach((step, i) => {
      step.hidden = i !== index;
      step.disabled = i !== index;
    });
    document.getElementById('quote-progress').value = index + 1;
    document.getElementById('quote-step-label').textContent = `Paso ${index + 1} de 3 · ${['Tu seguro', 'Tu prioridad', 'Tu resumen'][index]}`;
    back.hidden = index === 0;
    next.hidden = index === 2;
    copyStatus.textContent = '';
    if (index === 2) updateSummary();
    if (focus) {
      steps[index].querySelector('legend').focus({ preventScroll: true });
      const bounds = form.getBoundingClientRect();
      if (bounds.top < 24 || bounds.top > innerHeight / 2) {
        form.closest('.quote-workspace').scrollIntoView({ block: 'start', behavior: reducedMotion.matches ? 'instant' : 'smooth' });
      }
    }
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (current === 2) return;
    const invalid = [...steps[current].querySelectorAll('input,select,textarea')].find(field => !field.checkValidity());
    if (invalid) { invalid.reportValidity(); return; }
    showStep(current + 1);
  });
  back.addEventListener('click', () => showStep(Math.max(0, current - 1)));
  advisor.addEventListener('change', updateSummary);
  document.getElementById('quote-copy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(summary.value);
      copyStatus.textContent = 'Resumen copiado. Puedes compartirlo con tu asesor.';
    } catch {
      summary.focus(); summary.select();
      copyStatus.textContent = 'Seleccionamos el resumen para que puedas copiarlo.';
    }
  });
  showStep(0, false);
  form.hidden = false;
})();
