(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const experience = document.querySelector('.experience-section');
  let countersStarted = false;
  function revealExperience() {
    experience.classList.add('is-visible');
    if (countersStarted) return;
    countersStarted = true;
    if (reduced.matches) return;
    experience.querySelectorAll('[data-count]').forEach(counter => {
      const end = Number(counter.dataset.count);
      const start = performance.now();
      const animate = now => {
        const progress = Math.min((now - start) / 850, 1);
        counter.textContent = String(Math.round(end * (1 - (1 - progress) ** 3)));
        if (progress < 1 && !reduced.matches) requestAnimationFrame(animate);
        else counter.textContent = String(end);
      };
      requestAnimationFrame(animate);
    });
  }
  if ('IntersectionObserver' in window && !reduced.matches) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        revealExperience();
        observer.disconnect();
      }
    }, {threshold:0.2});
    observer.observe(experience);
  } else revealExperience();

  const portrait = document.querySelector('.evia-motion');
  if (!portrait) return;
  const video = portrait.querySelector('video');
  let visible = false, failed = false;
  const playbackAllowed = () => visible && !failed && !document.hidden && !reduced.matches && !navigator.connection?.saveData;
  function playback() {
    if (!playbackAllowed()) {
      video.pause();
      return;
    }
    if (!video.getAttribute('src')) video.src = video.dataset.source;
    video.play().catch(() => portrait.classList.remove('is-playing'));
  }
  video.addEventListener('playing', () => portrait.classList.add('is-playing'));
  video.addEventListener('error', () => { failed = true; portrait.classList.remove('is-playing'); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      playback();
    }, {threshold:0.15}).observe(portrait);
  } else {
    visible = true;
    playback();
  }
  document.addEventListener('visibilitychange', playback);
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      revealExperience();
      portrait.classList.remove('is-playing');
    }
    playback();
  });
})();
