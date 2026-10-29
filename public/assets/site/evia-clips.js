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

(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('[data-count]').forEach(counter=>{
  const end=Number(counter.dataset.count);let started=false;
  const reveal=()=>{if(started)return;started=true;counter.closest('.experience-section')?.classList.add('is-visible');if(reduced.matches){counter.textContent=String(end);return;}const start=performance.now();const tick=now=>{const t=Math.min((now-start)/1500,1);counter.textContent=String(Math.round(end*(1-(1-t)**3)));if(t<1&&!reduced.matches)requestAnimationFrame(tick);else counter.textContent=String(end);};requestAnimationFrame(tick);};
  if('IntersectionObserver' in window&&!reduced.matches){const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){reveal();observer.disconnect();}},{threshold:.35});observer.observe(counter);}else reveal();
 });
})();
