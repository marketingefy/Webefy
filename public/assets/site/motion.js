/* Entrance choreography inspired by the owner's reference. No scroll interception. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if (!Element.prototype.animate) return;
  const active = new Set();
  function animate(element, frames, options = {}) {
    if (!element || reduced.matches || document.hidden) return;
    const animation = element.animate(frames, {
      duration: 850, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards', ...options
    });
    active.add(animation);
    const done = () => active.delete(animation);
    animation.finished.then(done, done);
  }
  function rise(element, delay = 0, distance = 38) {
    animate(element, [
      { opacity: 0, transform: `translateY(${distance}px)`, clipPath: 'inset(0 0 12% 0)' },
      { opacity: 1, transform: 'translateY(0)', clipPath: 'inset(0)' }
    ], { delay });
  }
  const title = document.querySelector('h1');
  // Preserve the original inline wording and breaks, including screen-reader text.
  if (title && !reduced.matches) {
    const lines = [];
    let line = document.createElement('span');
    line.className = 'entrance-line';
    [...title.childNodes].forEach(node => {
      if (node.nodeName === 'BR') {
        lines.push(line, node);
        line = document.createElement('span');
        line.className = 'entrance-line';
      } else line.append(node);
    });
    lines.push(line);
    title.replaceChildren(...lines);
    title.querySelectorAll('.entrance-line').forEach((element, i) => rise(element, 160 + i * 140, 55));
  }
  if (scrollY < 80 && !location.hash) {
    rise(document.querySelector('.header-inner'), 0, -16);
    const intro = title?.closest('section');
    rise(intro?.querySelector('.eyebrow'), 80, 18);
    rise(intro?.querySelector('.hero-lead,.large-copy,.intro-copy'), 470, 26);
    rise(intro?.querySelector('.actions'), 600, 24);
    animate(document.querySelector('.workshop'), [
      { clipPath: 'inset(5% 0 20% 9% round 36px)', opacity: .15 },
      { clipPath: 'inset(0% round 0px)', opacity: 1 }
    ], { duration: 1400 });
  }
  const targets = document.querySelectorAll('.section-heading,.protection-heading,.protection-card,.service-card,.business-card,.client-action,.editorial-link,.partner-card,.assistance-option,.review-demo-card,.contact-department,.guide-grid>div,.about-story>div');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting);
      visible.forEach((entry, index) => {
        observer.unobserve(entry.target);
        if (reduced.matches || entry.target.getBoundingClientRect().bottom < 0) return;
        // Small groups reveal together; long carousels do not accrue long delays.
        rise(entry.target, (index % 3) * 110, matchMedia('(max-width:760px)').matches ? 30 : 52);
      });
    }, { threshold: .08 });
    targets.forEach(element => observer.observe(element));
  }
  reduced.addEventListener('change', () => {
    if (reduced.matches) active.forEach(animation => animation.cancel());
  });
  document.addEventListener('visibilitychange', () => {
    active.forEach(animation => document.hidden ? animation.pause() : animation.play());
  });
  // Keyboard navigation always reveals a focused control immediately.
  document.addEventListener('focusin', event => {
    active.forEach(animation => {
      const element = animation.effect?.target;
      if (element?.contains(event.target)) animation.finish();
    });
  });
})();
