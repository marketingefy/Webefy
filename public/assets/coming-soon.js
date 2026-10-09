(() => {
  const scene = document.querySelector('.scene');
  const video = document.querySelector('.scene-video');
  const control = document.querySelector('.motion-control');
  const label = control.querySelector('span');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 760px)');
  const connection = navigator.connection;
  let wantsMotion = !reducedMotion.matches && !connection?.saveData;
  let inView = true;
  let failed = false;
  let playAttempt = 0;
  control.hidden = false;

  function updateControl() {
    const playing = !video.paused && !failed;
    control.setAttribute('aria-pressed', String(playing));
    label.textContent = playing ? 'Pausar escena' : 'Reproducir escena';
  }

  function loadSource() {
    if (video.getAttribute('src')) return;
    video.src = mobile.matches ? 'assets/evia-workshop-loop-mobile.mp4' : 'assets/evia-workshop-loop.mp4';
    video.muted = true;
  }

  async function syncPlayback() {
    const attempt = ++playAttempt;
    if (!wantsMotion || document.hidden || !inView || failed) {
      video.pause();
      updateControl();
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
    updateControl();
  }

  control.addEventListener('click', () => {
    if (failed) {
      failed = false;
      video.removeAttribute('src');
      video.load();
    }
    wantsMotion = video.paused;
    syncPlayback();
  });
  video.addEventListener('play', updateControl);
  video.addEventListener('pause', updateControl);
  video.addEventListener('error', () => {
    failed = true;
    video.pause();
    scene.classList.remove('is-ready');
    updateControl();
  });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      wantsMotion = false;
      scene.classList.remove('is-ready');
      syncPlayback();
    }
  });
  connection?.addEventListener('change', () => {
    if (connection.saveData) {
      wantsMotion = false;
      syncPlayback();
    }
  });
  document.addEventListener('visibilitychange', syncPlayback);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      inView = entries[0].isIntersecting;
      syncPlayback();
    }, { threshold: 0 }).observe(scene);
  }
  syncPlayback();
})();
