(() => {
  const scene = document.querySelector('.scene');
  const video = document.querySelector('.scene-video');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 760px)');
  const connection = navigator.connection;
  let wantsMotion = !reducedMotion.matches && !connection?.saveData;
  let inView = true;
  let failed = false;
  let playAttempt = 0;

  function loadSource() {
    if (video.getAttribute('src')) return;
    video.src = mobile.matches ? 'assets/evia-workshop-loop-mobile.mp4?v=evia-wide-restored-20261009' : 'assets/evia-workshop-loop.mp4?v=evia-wide-restored-20261009';
    video.muted = true;
  }

  async function syncPlayback() {
    const attempt = ++playAttempt;
    if (!wantsMotion || document.hidden || !inView || failed) {
      video.pause();
      return;
    }
    loadSource();
    try {
      await video.play();
      if (attempt !== playAttempt || !wantsMotion || document.hidden || !inView) {
        if (!wantsMotion || document.hidden || !inView) video.pause();
        return;
      }
      scene.classList.add('is-ready');
    } catch {
      // The illustration stays visible if autoplay is unavailable.
    }
  }

  video.addEventListener('error', () => {
    failed = true;
    video.pause();
    scene.classList.remove('is-ready');
  });
  function updateMotionPreference() {
    wantsMotion = !reducedMotion.matches && !connection?.saveData;
    if (!wantsMotion) scene.classList.remove('is-ready');
    syncPlayback();
  }
  reducedMotion.addEventListener('change', updateMotionPreference);
  connection?.addEventListener('change', updateMotionPreference);
  document.addEventListener('visibilitychange', syncPlayback);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      inView = entries[0].isIntersecting;
      syncPlayback();
    }, { threshold: 0 }).observe(scene);
  }
  syncPlayback();
})();
