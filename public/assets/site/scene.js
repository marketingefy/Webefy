/* Light layers follow the original poster's cover crop; EVIA stays still. */
(() => {
  const scene = document.querySelector('.workshop');
  const effects = scene?.querySelector('.scene-effects');
  if (!effects) return;
  const image = scene.querySelector('img');
  const mobile = matchMedia('(max-width:760px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true;
  function align() {
    const width = mobile.matches ? 720 : 1280;
    const height = mobile.matches ? 800 : 720;
    const scale = Math.max(scene.clientWidth / width, scene.clientHeight / height);
    const position = getComputedStyle(image).objectPosition.split(' ').map(parseFloat);
    const left = (scene.clientWidth - width * scale) * position[0] / 100;
    const top = (scene.clientHeight - height * scale) * position[1] / 100;
    effects.style.setProperty('--scene-width', `${width}px`);
    effects.style.setProperty('--scene-height', `${height}px`);
    effects.style.setProperty('--scene-transform', `translate(${left}px,${top}px) scale(${scale})`);
    scene.classList.add('effects-aligned');
  }
  function activity() {
    scene.classList.toggle('effects-paused', reduced.matches || document.hidden || !visible || Boolean(navigator.connection?.saveData));
  }
  new ResizeObserver(align).observe(scene);
  mobile.addEventListener('change', align);
  reduced.addEventListener('change', activity);
  navigator.connection?.addEventListener('change', activity);
  document.addEventListener('visibilitychange', activity);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {visible = entries[0].isIntersecting; activity();}).observe(scene);
  align(); activity();
})();
