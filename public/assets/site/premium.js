/* The approved EVIA loop is live media, with a static fallback and native playback. */
(() => {
  const scene = document.querySelector('.premium-home .scene');
  const video = scene?.querySelector('.scene-video');
  if (!video) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width:760px)');
  let visible = !('IntersectionObserver' in window);
  let attempt = 0;
  let failedSource = '';
  const canPlay = () => visible && !document.hidden && !reduced.matches && !navigator.connection?.saveData;
  async function playback() {
    const request = ++attempt;
    const allowed = canPlay();
    scene.classList.toggle('effects-paused', !allowed);
    if (!allowed) { video.pause(); return; }
    const source = new URL(mobile.matches ? video.dataset.mobile : video.dataset.desktop, location.href).href;
    if (failedSource === source) return;
    if (video.getAttribute('src') !== source) {
      scene.classList.remove('is-playing');
      video.src = source;
    }
    try {
      await video.play();
      if (request !== attempt || !canPlay()) { if (!canPlay()) video.pause(); return; }
      scene.classList.add('is-playing');
    } catch { /* The approved poster stays visible when autoplay is unavailable. */ }
  }
  video.addEventListener('error', () => {
    failedSource = video.getAttribute('src');
    scene.classList.remove('is-playing');
    video.pause();
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches) scene.classList.remove('is-playing');
    playback();
  });
  mobile.addEventListener('change', playback);
  navigator.connection?.addEventListener('change', playback);
  document.addEventListener('visibilitychange', playback);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    playback();
  }).observe(scene);
  playback();
})();

/* The services carousel moves only when the visitor chooses. */
(() => {
  const rail = document.getElementById('home-services-rail');
  if (!rail) return;
  const prev = document.getElementById('home-services-prev');
  const next = document.getElementById('home-services-next');
  const status = document.getElementById('home-services-position');
  const cards = [...rail.children];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const relativeLeft = card => card.getBoundingClientRect().left - rail.getBoundingClientRect().left + rail.scrollLeft - rail.clientLeft;
  const update = () => {
    const end = rail.scrollWidth - rail.clientWidth;
    prev.disabled = rail.scrollLeft <= 2;
    next.disabled = rail.scrollLeft >= end - 2;
    const index = cards.reduce((best, card, i) => Math.abs(relativeLeft(card) - rail.scrollLeft) < Math.abs(relativeLeft(cards[best]) - rail.scrollLeft) ? i : best, 0);
    status.textContent = `${index + 1} de ${cards.length}`;
  };
  const move = direction => {
    const gap = parseFloat(getComputedStyle(rail).columnGap) || 0;
    const step = cards[0].getBoundingClientRect().width + gap;
    rail.scrollBy({left: direction * step, behavior: reduced.matches ? 'instant' : 'smooth'});
  };
  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  rail.addEventListener('scroll', update, {passive:true});
  rail.addEventListener('keydown', event => {
    if (event.target !== rail) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {event.preventDefault();move(event.key === 'ArrowRight' ? 1 : -1);}
    if (event.key === 'Home' || event.key === 'End') {event.preventDefault();rail.scrollTo({left:event.key === 'Home' ? 0 : rail.scrollWidth,behavior:reduced.matches ? 'instant' : 'smooth'});}
  });
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(rail);
  window.addEventListener('resize', update);
  update();
})();
