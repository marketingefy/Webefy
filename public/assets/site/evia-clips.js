/* Each decorative film loads only when visible; its poster is always available. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-evia-clip]').forEach(figure => {
    const video = figure.querySelector('video');
    if (!video) return;
    let visible = !('IntersectionObserver' in window), failed = false, attempt = 0;
    const allowed = () => visible && !failed && !document.hidden && !reduced.matches && !navigator.connection?.saveData;
    async function playback() {
      const current = ++attempt;
      if (!allowed()) { video.pause(); if (reduced.matches) figure.classList.remove('is-playing'); return; }
      if (!video.getAttribute('src')) video.src = video.dataset.source;
      try {
        await video.play();
        if (current === attempt && allowed()) figure.classList.add('is-playing');
        else if (!allowed()) video.pause();
      } catch { figure.classList.remove('is-playing'); }
    }
    video.addEventListener('error', () => {
      failed = true; video.pause(); figure.classList.remove('is-playing');
    });
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting; playback();
    }, {threshold:.08}).observe(figure);
    document.addEventListener('visibilitychange', playback);
    reduced.addEventListener('change', playback);
    navigator.connection?.addEventListener('change', playback);
    playback();
  });
})();
