(() => {
  const nav = document.querySelector('#site-nav');
  if (!nav) return;

  const desktop = matchMedia('(min-width:1181px) and (hover:hover) and (pointer:fine)');
  const entries = [...nav.querySelectorAll('.nav-item')].flatMap(item => {
    const link = item.querySelector('.nav-link[aria-controls]');
    const panel = link && document.getElementById(link.getAttribute('aria-controls'));
    const toggle = item.querySelector('.nav-submenu-toggle');
    return panel?.matches('.nav-preview') && item.contains(panel) ? [{ item, link, panel, toggle }] : [];
  });
  if (!entries.length) return;

  let opened = null;
  let leaveTimer;
  let restoringFocus = null;

  function markCurrentSelection() {
    const normalizePath = path => path.replace(/\/index\.html$/, '/').replace(/\/siniestros\.html$/, '/reportar-siniestro.html');
    const path = normalizePath(location.pathname);
    const links = [...nav.querySelectorAll('.nav-preview-link')];
    const category = document.querySelector('[data-service-category][aria-pressed="true"]');
    const hash = location.hash.startsWith('#seguro-') ? location.hash : category ? (category.id ? '#' + category.id : '') : location.hash;
    const destinations = links.map(link => ({ link, url: new URL(link.href, location.href) }));
    const matchesSection = hash && destinations.some(({ url }) => normalizePath(url.pathname) === path && url.hash === hash);
    destinations.forEach(({ link, url }) => {
      const requestedType = url.searchParams.get('tipo');
      const currentType = document.querySelector('#lookup-type')?.value || new URLSearchParams(location.search).get('tipo');
      const selected = normalizePath(url.pathname) === path && (!requestedType || requestedType === currentType) && (matchesSection ? url.hash === hash : !url.hash);
      if (selected) link.setAttribute('aria-current', matchesSection ? 'location' : 'page');
      else link.removeAttribute('aria-current');
    });
  }
  markCurrentSelection();
  window.addEventListener('hashchange', markCurrentSelection);
  document.querySelector('#lookup-type')?.addEventListener('change', markCurrentSelection);
  document.addEventListener('click', event => {
    if (event.target.closest('[data-service-category]')) markCurrentSelection();
  });

  function cancelLeave() {
    clearTimeout(leaveTimer);
    leaveTimer = undefined;
  }

  function close() {
    cancelLeave();
    if (!opened) return;
    opened.link.setAttribute('aria-expanded', 'false');
    opened.toggle?.setAttribute('aria-expanded', 'false');
    opened.panel.hidden = true;
    opened.item.classList.remove('is-preview-open');
    opened = null;
  }

  function open(entry, trigger = entry.link, force = false) {
    if (!desktop.matches && !force) return;
    markCurrentSelection();
    cancelLeave();
    if (opened === entry) return;
    close();
    opened = entry;
    entry.returnFocus = trigger;
    entry.link.setAttribute('aria-expanded', 'true');
    entry.toggle?.setAttribute('aria-expanded', 'true');
    entry.panel.hidden = false;
    entry.item.classList.add('is-preview-open');
  }

  entries.forEach(entry => {
    // Hidden panels remain out of the reading and keyboard order on touch screens.
    entry.link.setAttribute('aria-expanded', 'false');
    entry.toggle?.setAttribute('aria-expanded', 'false');
    entry.toggle?.addEventListener('click', () => {
      if (opened === entry) close();
      else open(entry, entry.toggle, true);
    });
    if (entry.link.tagName === 'BUTTON') entry.link.addEventListener('click', () => {
      if (opened === entry) close();
      else open(entry, entry.link, true);
    });
    entry.link.addEventListener('keydown', event => {
      if (event.key !== 'ArrowDown') return;
      event.preventDefault();
      open(entry, entry.link, true);
      entry.panel.querySelector('a')?.focus();
    });
    entry.panel.addEventListener('click', event => {
      if (event.target.closest('a')) {
        close();
        nav.classList.remove('is-open');
        document.querySelector('.menu-toggle')?.setAttribute('aria-expanded', 'false');
      }
    });
    entry.panel.hidden = true;
    entry.item.classList.remove('is-preview-open');

    entry.item.addEventListener('pointerenter', event => {
      if (entry.link.tagName !== 'BUTTON' && event.pointerType !== 'touch') open(entry);
    });
    entry.item.addEventListener('pointerleave', () => {
      if (opened !== entry) return;
      cancelLeave();
      leaveTimer = setTimeout(() => {
        if (opened === entry && !entry.item.contains(document.activeElement)) close();
      }, 100);
    });
    entry.item.addEventListener('focusin', event => {
      if (entry.link.tagName !== 'BUTTON' && event.target !== restoringFocus) open(entry);
    });
    entry.item.addEventListener('focusout', event => {
      // relatedTarget identifies the next focus before the browser blurs the old link.
      if (opened === entry && !entry.item.contains(event.relatedTarget)) close();
    });
  });

  document.addEventListener('pointerdown', event => {
    if (opened && !opened.item.contains(event.target)) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || !opened) return;
    // A modal owns its keyboard interaction, even during a focus transition.
    if (event.target.closest?.('dialog[open]')) return;
    event.preventDefault();
    event.stopPropagation();
    const link = opened.returnFocus || opened.link;
    close();
    restoringFocus = link;
    link.focus({ preventScroll: true });
    restoringFocus = null;
  }, true);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) close();
  });
  if (desktop.addEventListener) desktop.addEventListener('change', close);
  else desktop.addListener(close);
})();
