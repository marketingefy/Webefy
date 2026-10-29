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
