/* instagram.js: carrusel de publicaciones de Instagram.
   Lee un JSON (por defecto assets/instagram.json) y pinta el carrusel dentro de [data-ig-feed].
   La fuente es intercambiable sin tocar el diseno: puede ser un archivo estatico generado por una tarea programada
   que consulta la API oficial de Instagram, o la URL JSON de un servicio de feed (ver _build/instagram/README.md).

   Formato del JSON:
   { "profile": {"username": "asoclicper", "url": "https://www.instagram.com/asoclicper/"},
     "posts": [ {"id", "type": "IMAGE|VIDEO|CAROUSEL_ALBUM", "image": "ruta o URL", "permalink", "caption", "timestamp"} ] }  */
(function(){
  const $ = (s, r) => (r || document).querySelector(s);
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = (t) => (t || '').toString().replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
  const TYPE = {
    VIDEO: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
    CAROUSEL_ALBUM: '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 4H7a3 3 0 00-3 3v9"/></svg>'
  };
  const LABEL = {VIDEO: 'Video', CAROUSEL_ALBUM: 'Carrusel de imágenes', IMAGE: 'Imagen'};

  document.querySelectorAll('[data-ig-feed]').forEach(init);

  function init(root){
    const track = $('.ig-track', root), bar = $('.ig-bar span', root);
    const section = root.closest('section') || document;
    const prev = $('[data-ig="prev"]', section), next = $('[data-ig="next"]', section);
    const limit = parseInt(root.dataset.limit || '10', 10);
    root.classList.add('is-loading');

    fetch(root.dataset.src || 'assets/instagram.json', {cache: 'no-cache'})
      .then(r => { if(!r.ok) throw new Error(r.status); return r.json(); })
      .then(build)
      .catch(fail);

    function fail(){
      root.classList.remove('is-loading');
      const url = root.dataset.profile || 'https://www.instagram.com/asoclicper/';
      track.innerHTML = '<div class="ig-fallback"><span>Mira nuestras publicaciones más recientes en Instagram.</span><a class="btn btn-primary btn-sm" href="' + esc(url) + '" target="_blank" rel="noopener">Ir a @asoclicper</a></div>';
      [prev, next].forEach(b => b && (b.disabled = true));
      if(bar) bar.parentElement.hidden = true;
    }

    function build(data){
      const user = (data.profile && data.profile.username) || 'asoclicper';
      const posts = (data.posts || []).filter(p => p.image).slice(0, limit);
      if(!posts.length) return fail();
      track.innerHTML = posts.map((p, i) => {
        const type = p.type || 'IMAGE';
        const cap = (p.caption || '').trim();
        const alt = (LABEL[type] || 'Publicación') + ' de @' + user + (cap ? ': ' + cap.slice(0, 110) : '');
        return '<a class="ig-item rv" style="--d:' + (Math.min(i, 5) * .07) + 's" href="' + esc(p.permalink || (data.profile && data.profile.url) || '#') + '" target="_blank" rel="noopener" draggable="false" aria-label="' + esc(alt + '. Abrir en Instagram') + '">' +
          '<img src="' + esc(p.image) + '" alt="" width="560" height="700" loading="' + (i < 5 ? 'eager' : 'lazy') + '" decoding="async" draggable="false">' +
          (TYPE[type] ? '<span class="ig-type" title="' + esc(LABEL[type]) + '">' + TYPE[type] + '</span>' : '') +
          '<div class="ig-cap">' + (cap ? '<p>' + esc(cap) + '</p>' : '') + '<span>' + window.asocIcon('instagram') + ' Ver en Instagram</span></div></a>';
      }).join('');
      root.classList.remove('is-loading');
      if(window.asocReveal) window.asocReveal(root);
      wire();
    }

    function wire(){
      const items = Array.from(track.children);
      const step = () => { const a = items[0], b = items[1]; return (b ? b.offsetLeft - a.offsetLeft : a.offsetWidth + 16); };
      const perPage = () => Math.max(1, Math.floor((track.clientWidth + 16) / step() + .01));
      const max = () => track.scrollWidth - track.clientWidth;
      let raf = 0;
      function sync(){
        raf = 0;
        const m = max(), x = track.scrollLeft;
        if(prev) prev.disabled = x <= 2;
        if(next) next.disabled = x >= m - 2;
        if(bar){
          const w = Math.min(1, track.clientWidth / track.scrollWidth);
          bar.style.width = (w * 100).toFixed(2) + '%';
          bar.style.transform = 'translateX(' + (m > 0 ? (x / m) * (1 / w - 1) * 100 : 0).toFixed(2) + '%)';
        }
      }
      const queue = () => { if(!raf) raf = requestAnimationFrame(sync); };
      track.addEventListener('scroll', queue, {passive: true});
      window.addEventListener('resize', queue, {passive: true});
      window.addEventListener('load', queue);
      if(window.ResizeObserver){ const ro = new ResizeObserver(queue); ro.observe(track); ro.observe(items[items.length - 1]); }
      sync();

      const go = (dir) => track.scrollBy({left: dir * step() * perPage(), behavior: reduce ? 'auto' : 'smooth'});
      if(prev) prev.addEventListener('click', () => go(-1));
      if(next) next.addEventListener('click', () => go(1));
      track.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowRight'){ e.preventDefault(); go(1); }
        else if(e.key === 'ArrowLeft'){ e.preventDefault(); go(-1); }
      });

      /* arrastrar con el mouse (en tactil el scroll nativo ya funciona) */
      let down = false, sx = 0, sl = 0, moved = 0;
      track.addEventListener('pointerdown', (e) => {
        if(e.pointerType !== 'mouse' || e.button !== 0) return;
        down = true; moved = 0; sx = e.clientX; sl = track.scrollLeft;
      });
      window.addEventListener('pointermove', (e) => {
        if(!down) return;
        const dx = e.clientX - sx;
        moved = Math.max(moved, Math.abs(dx));
        if(moved > 5){ track.classList.add('is-drag'); track.scrollLeft = sl - dx; }
      });
      const end = () => {
        if(!down) return;
        down = false;
        if(track.classList.contains('is-drag')){
          // al soltar se recupera el ajuste por tarjeta; se vuelve a la tarjeta mas cercana
          const target = Math.round(track.scrollLeft / step()) * step();
          track.classList.remove('is-drag');
          track.scrollTo({left: target, behavior: reduce ? 'auto' : 'smooth'});
        }
      };
      window.addEventListener('pointerup', end);
      window.addEventListener('pointercancel', end);
      track.addEventListener('click', (e) => { if(moved > 5){ e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
    }
  }
})();
