/* post.js: comportamiento del single post de Noticias
   progreso de lectura, indice con seccion activa, compartir, visor de imagenes, video diferido y paralaje de la portada */
(function(){
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EN = document.documentElement.lang === 'en';
  const T = EN
    ? {copied:'Link copied', close:'Close', prev:'Previous image', next:'Next image', of:'of', video:'Video player'}
    : {copied:'Enlace copiado', close:'Cerrar', prev:'Imagen anterior', next:'Imagen siguiente', of:'de', video:'Reproductor de video'};
  const prose = $('.prose');

  /* ---------- progreso de lectura ---------- */
  const bar = $('#progress');
  let ticking = false;
  function paint(){
    ticking = false;
    if(!bar || !prose) return;
    const r = prose.getBoundingClientRect();
    const vh = window.innerHeight;
    // empieza cuando el texto entra al 70% de la pantalla y llega a 100% cuando su final pasa el 60%
    const done = Math.min(1, Math.max(0, (vh * .7 - r.top) / (r.height + vh * .1)));
    bar.style.transform = 'scaleX(' + done.toFixed(4) + ')';
  }
  const onScroll = () => { if(!ticking){ ticking = true; requestAnimationFrame(paint); } };
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll, {passive:true});
  paint();

  /* ---------- revelado de bloques del articulo ---------- */
  if(prose){
    Array.from(prose.children).forEach((el, i) => {
      if(i === 0 || el.tagName === 'P' && !el.classList.contains('pbtn')) return;
      if(el.classList.contains('pgal')) return;
      el.classList.add('rv');
    });
    $$('.post-end, .about-box').forEach(el => el.classList.add('rv'));
    if(window.asocReveal) window.asocReveal(document);
  }
  const gio = 'IntersectionObserver' in window && !reduce ? new IntersectionObserver((es) => {
    es.forEach(e => { if(e.isIntersecting){ e.target.classList.add('in'); gio.unobserve(e.target); } });
  }, {threshold:.12, rootMargin:'0px 0px -6% 0px'}) : null;
  $$('.pgal').forEach(g => {
    $$('a', g).forEach((a, i) => a.style.setProperty('--d', (Math.min(i, 8) * .07) + 's'));
    if(gio) gio.observe(g); else g.classList.add('in');
  });

  /* ---------- indice: seccion activa ---------- */
  const toc = $('.toc');
  if(toc){
    // en pantallas chicas el indice arranca plegado; en escritorio siempre abierto
    const mq = window.matchMedia('(min-width:1101px)');
    toc.open = mq.matches;
    const sync = (e) => { if(e.matches) toc.open = true; };
    if(mq.addEventListener) mq.addEventListener('change', sync); else if(mq.addListener) mq.addListener(sync);
    const links = $$('a[data-h]', toc);
    const map = links.map(a => ({a, li: a.parentElement, el: document.getElementById(a.dataset.h)})).filter(x => x.el);
    links.forEach(a => a.addEventListener('click', (e) => {
      const el = document.getElementById(a.dataset.h);
      if(!el) return;
      e.preventDefault();
      el.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block:'start'});
      // con <base href="../"> un '#id' suelto se resuelve contra la raiz del sitio: se usa la ruta completa de la pagina
      history.replaceState(null, '', location.pathname + location.search + '#' + a.dataset.h);
    }));
    if(map.length && 'IntersectionObserver' in window){
      let current = null;
      const set = (x) => { if(current === x) return; current = x; map.forEach(m => m.li.classList.toggle('is-on', m === x)); };
      const spy = () => {
        let hit = null;
        const line = window.innerHeight * .28;
        map.forEach(m => { if(m.el.getBoundingClientRect().top <= line) hit = m; });
        set(hit);
      };
      window.addEventListener('scroll', () => requestAnimationFrame(spy), {passive:true});
      spy();
    }
  }

  /* ---------- compartir ---------- */
  const url = location.href.split('#')[0];
  const ttl = (document.title || '').replace(/\s*\|\s*ASOCLICPER\s*$/i, '');
  const nets = {
    whatsapp: 'https://wa.me/?text=' + encodeURIComponent(ttl + ' ' + url),
    facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url),
    linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url),
    x: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(ttl) + '&url=' + encodeURIComponent(url),
    mail: 'mailto:?subject=' + encodeURIComponent(ttl) + '&body=' + encodeURIComponent(url)
  };
  $$('[data-net]').forEach(a => { a.href = nets[a.dataset.net]; });
  let toastT = 0, toast = null;
  function say(msg){
    if(!toast){
      toast = document.createElement('div'); toast.className = 'post-toast'; toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.innerHTML = window.asocIcon('check') + msg;
    toast.classList.add('is-on');
    clearTimeout(toastT);
    toastT = setTimeout(() => toast.classList.remove('is-on'), 2200);
  }
  function copy(){
    const done = () => say(T.copied);
    if(navigator.clipboard && window.isSecureContext){
      navigator.clipboard.writeText(url).then(done, fallback);
    } else fallback();
    function fallback(){
      const t = document.createElement('textarea'); t.value = url; t.setAttribute('readonly', '');
      t.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0';
      document.body.appendChild(t); t.select();
      try{ document.execCommand('copy'); done(); }catch(e){}
      t.remove();
    }
  }
  $$('[data-act="copy"]').forEach(b => b.addEventListener('click', copy));
  if(navigator.share){
    $$('[data-act="native"]').forEach(b => {
      b.hidden = false;
      b.addEventListener('click', () => navigator.share({title: ttl, url}).catch(() => {}));
    });
  }

  /* ---------- video diferido ---------- */
  $$('.pvid').forEach(fig => {
    const btn = $('.pvid-btn', fig);
    if(!btn) return;
    btn.addEventListener('click', () => {
      if(fig.classList.contains('is-on')) return;
      const id = fig.dataset.yt;
      const box = document.createElement('div');
      box.className = 'pvid-box';
      box.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1" title="' + T.video + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      fig.classList.add('is-on');
      fig.replaceChild(box, btn);
    });
  });

  /* ---------- visor de imagenes ---------- */
  const items = $$('a.lb-i');
  if(items.length){
    let box = null, img, num, cap, group = [], idx = 0, last = null, x0 = null;
    const ico = {
      x:'<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
      l:'<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
      r:'<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
    };
    function build(){
      box = document.createElement('div');
      box.className = 'lb';
      box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
      box.innerHTML =
        '<button type="button" class="lb-btn lb-x" aria-label="' + T.close + '">' + ico.x + '</button>' +
        '<button type="button" class="lb-btn lb-p" aria-label="' + T.prev + '">' + ico.l + '</button>' +
        '<figure class="lb-fig"><img class="lb-img" alt=""></figure>' +
        '<button type="button" class="lb-btn lb-nx" aria-label="' + T.next + '">' + ico.r + '</button>' +
        '<div class="lb-bar"><span class="n"></span><span class="c"></span></div>';
      document.body.appendChild(box);
      img = $('.lb-img', box); num = $('.n', box); cap = $('.c', box);
      box.addEventListener('click', (e) => {
        if(e.target.closest('.lb-x') || e.target === box || e.target.classList.contains('lb-fig')) close();
        else if(e.target.closest('.lb-p')) go(-1);
        else if(e.target.closest('.lb-nx')) go(1);
      });
      box.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, {passive:true});
      box.addEventListener('touchend', (e) => {
        if(x0 === null) return;
        const dx = e.changedTouches[0].clientX - x0; x0 = null;
        if(Math.abs(dx) > 50) go(dx < 0 ? 1 : -1);
      });
    }
    function show(i, swap){
      idx = (i + group.length) % group.length;
      const a = group[idx], th = $('img', a);
      const apply = () => {
        img.src = a.href;
        img.alt = th ? th.alt : '';
        num.textContent = (idx + 1) + ' ' + T.of + ' ' + group.length;
        cap.textContent = '';
        img.classList.remove('is-swap');
      };
      if(swap && !reduce){ img.classList.add('is-swap'); setTimeout(apply, 160); } else apply();
      // precarga de vecinas
      [1, -1].forEach(d => { if(group.length > 1){ const n = group[(idx + d + group.length) % group.length]; (new Image()).src = n.href; } });
    }
    function go(d){ if(group.length > 1) show(idx + d, true); }
    function open(a){
      if(!box) build();
      last = document.activeElement;
      group = items.filter(x => x.dataset.lb === a.dataset.lb);
      box.classList.toggle('is-single', group.length < 2);
      box.classList.add('is-open');
      document.documentElement.style.overflow = 'hidden';
      show(group.indexOf(a), false);
      $('.lb-x', box).focus({preventScroll:true});
    }
    function close(){
      if(!box || !box.classList.contains('is-open')) return;
      box.classList.remove('is-open');
      document.documentElement.style.overflow = '';
      img.removeAttribute('src');
      if(last && last.focus) last.focus({preventScroll:true});
    }
    items.forEach(a => a.addEventListener('click', (e) => {
      if(e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); open(a);
    }));
    document.addEventListener('keydown', (e) => {
      if(!box || !box.classList.contains('is-open')) return;
      if(e.key === 'Escape') close();
      else if(e.key === 'ArrowRight') go(1);
      else if(e.key === 'ArrowLeft') go(-1);
    });
  }

  /* ---------- paralaje de la portada ---------- */
  const frame = $('.pc-frame:not(.is-contain):not(.is-brand)');
  if(frame && !reduce && 'IntersectionObserver' in window){
    let live = false, raf = 0;
    const upd = () => {
      raf = 0;
      const r = frame.getBoundingClientRect(), vh = window.innerHeight;
      const p = (r.top + r.height / 2 - vh / 2) / vh;
      frame.style.setProperty('--py', Math.max(-14, Math.min(14, p * -26)).toFixed(1) + 'px');
    };
    const sch = () => { if(live && !raf) raf = requestAnimationFrame(upd); };
    new IntersectionObserver((es) => { live = es[0].isIntersecting; sch(); }, {rootMargin:'120px'}).observe(frame);
    window.addEventListener('scroll', sch, {passive:true});
    upd();
  }
})();
