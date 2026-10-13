/* Manual service catalogue: filters and accessible horizontal navigation. */
(() => {
  'use strict';

  const initialize = () => {
    const rail = document.getElementById('service-rail');
    if (!rail) return;

    const cards = [...rail.querySelectorAll('.service-card')];
    const categories = [...document.querySelectorAll('[data-service-category]')];
    const previous = document.getElementById('service-prev');
    const next = document.getElementById('service-next');
    const position = document.getElementById('service-position');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let pendingFrame = 0;

    const visibleCards = () => cards.filter(card => !card.hidden);
    const maximumScroll = () => Math.max(0, rail.scrollWidth - rail.clientWidth);

    const updatePosition = () => {
      pendingFrame = 0;
      const shown = visibleCards();
      const current = Math.max(0, rail.scrollLeft);
      const maximum = maximumScroll();
      if (previous) previous.disabled = current <= 1;
      if (next) next.disabled = current >= maximum - 1;
      if (!position) return;

      const bounds = rail.getBoundingClientRect();
      const left = bounds.left + rail.clientLeft;
      const right = left + rail.clientWidth;
      const inView = shown.reduce((indices, card, index) => {
        const item = card.getBoundingClientRect();
        if (item.right > left + 2 && item.left < right - 2) indices.push(index + 1);
        return indices;
      }, []);
      const first = inView[0] || (shown.length ? 1 : 0);
      const last = inView[inView.length - 1] || first;
      const range = first === last ? String(first) : `${first}–${last}`;
      const message = shown.length
        ? `${range} de ${shown.length} ${shown.length === 1 ? 'seguro' : 'seguros'}`
        : 'No hay seguros en esta categoría.';
      // Avoid repeatedly announcing the same range while a swipe is settling.
      if (position.textContent !== message) position.textContent = message;
    };

    const schedulePosition = () => {
      if (!pendingFrame) pendingFrame = requestAnimationFrame(updatePosition);
    };

    const scrollTo = (left, behavior = 'instant') => {
      rail.scrollTo({ left: Math.max(0, Math.min(maximumScroll(), left)), behavior });
      schedulePosition();
    };

    const selectCategory = category => {
      if (!categories.some(button => button.dataset.serviceCategory === category)) return;
      categories.forEach(button => {
        button.setAttribute('aria-pressed', String(button.dataset.serviceCategory === category));
      });
      cards.forEach(card => { card.hidden = category !== 'Todas' && card.dataset.serviceGroup !== category; });
      scrollTo(0);
    };

    const move = (direction, behavior) => {
      const shown = visibleCards();
      if (!shown.length) return;
      const first = shown[0].getBoundingClientRect();
      const step = shown.length > 1
        ? shown[1].getBoundingClientRect().left - first.left
        : first.width;
      scrollTo(rail.scrollLeft + direction * step, behavior);
    };

    const buttonBehavior = () => reducedMotion.matches ? 'instant' : 'smooth';
    previous?.addEventListener('click', () => move(-1, buttonBehavior()));
    next?.addEventListener('click', () => move(1, buttonBehavior()));
    categories.forEach(button => {
      button.addEventListener('click', () => selectCategory(button.dataset.serviceCategory));
    });
    rail.addEventListener('scroll', schedulePosition, { passive: true });
    rail.addEventListener('keydown', event => {
      // Leave native links, disclosure controls and other focused children alone.
      if (event.target !== rail) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        move(event.key === 'ArrowLeft' ? -1 : 1, 'instant');
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault();
        scrollTo(event.key === 'Home' ? 0 : maximumScroll());
      }
    });

    const applyHash = () => {
      let id;
      try { id = decodeURIComponent(window.location.hash.slice(1)); }
      catch { return; }
      if (!id) return;
      const category = categories.find(button => button.id === id);
      if (category) {
        selectCategory(category.dataset.serviceCategory);
        return;
      }
      const card = cards.find(item => item.id === id);
      if (!card) return;
      selectCategory(card.dataset.serviceGroup);
      const railBounds = rail.getBoundingClientRect();
      scrollTo(rail.scrollLeft + card.getBoundingClientRect().left - railBounds.left - rail.clientLeft);
    };
    window.addEventListener('hashchange', applyHash);

    if ('ResizeObserver' in window) new ResizeObserver(schedulePosition).observe(rail);
    else window.addEventListener('resize', schedulePosition, { passive: true });
    // Apply an initial fragment once; a slow page load must not reset a later choice.
    applyHash();
    window.addEventListener('load', schedulePosition, { once: true });
    schedulePosition();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
