/* site.js: comportamiento comun de las paginas internas (sin dependencias externas) */
(function(){
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(pointer: fine)').matches;
  const ic = (n, c) => window.asocIcon(n, c);
  const norm = (t) => (t || '').toString().normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const esc = (t) => (t || '').toString().replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));

  /* ---------- reveals ---------- */
  const io = 'IntersectionObserver' in window ? new IntersectionObserver((es) => {
    es.forEach(e => { if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  }, {threshold:.08, rootMargin:'0px 0px -6% 0px'}) : null;
  function reveal(root){
    $$('.rv:not([data-rv-on])', root).forEach((el) => {
      el.setAttribute('data-rv-on', '1');
      if(el.dataset.d) el.style.setProperty('--d', el.dataset.d + 's');
      if(io && !reduce) io.observe(el); else el.classList.add('in');
    });
    $$('.stagger:not([data-st-on])', root).forEach((wrap) => {
      if(!wrap.children.length) return;
      wrap.setAttribute('data-st-on', '1');
      Array.from(wrap.children).forEach((c, i) => { c.classList.add('rv'); c.style.setProperty('--d', (i * .08) + 's'); });
      reveal(wrap);
    });
  }
  window.asocReveal = reveal;

  /* ---------- contadores ---------- */
  const cio = 'IntersectionObserver' in window ? new IntersectionObserver((es) => {
    es.forEach(e => {
      if(!e.isIntersecting) return;
      cio.unobserve(e.target);
      const el = e.target, target = parseFloat(el.dataset.count), pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
      if(reduce){ el.textContent = pre + target.toLocaleString('es-CO') + suf; return; }
      const t0 = performance.now(), dur = 1600;
      (function tick(now){
        const p = Math.min(1, (now - t0) / dur), v = target * (1 - Math.pow(1 - p, 3));
        el.textContent = pre + Math.floor(v).toLocaleString('es-CO') + suf;
        if(p < 1) requestAnimationFrame(tick);
      })(t0);
    });
  }, {threshold:.4}) : null;
  function counters(root){ $$('[data-count]:not([data-c-on])', root).forEach(el => { el.setAttribute('data-c-on', '1'); if(cio) cio.observe(el); else el.textContent = (el.dataset.prefix || '') + el.dataset.count; }); }

  /* ---------- cursor, magnetico y spotlight ---------- */
  if(fine && !reduce){
    document.documentElement.classList.add('has-cursor');
    const dot = document.createElement('div'); dot.className = 'cursor-dot';
    const ring = document.createElement('div'); ring.className = 'cursor-ring';
    document.body.append(dot, ring);
    let mx = -100, my = -100, rx = -100, ry = -100;
    window.addEventListener('mousemove', (e) => { mx = e.clientX; my = e.clientY; dot.style.left = mx + 'px'; dot.style.top = my + 'px'; }, {passive:true});
    (function loop(){ rx += (mx - rx) * .2; ry += (my - ry) * .2; ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; requestAnimationFrame(loop); })();
    document.addEventListener('mousedown', () => ring.classList.add('is-down'));
    document.addEventListener('mouseup', () => ring.classList.remove('is-down'));
    const HOVER = 'a,button,input,select,textarea,label.check,.chip,.tab,.clinic-card,.acc-head,.vf-opt,.card,.spot';
    document.addEventListener('mouseover', (e) => { if(e.target.closest && e.target.closest(HOVER)) ring.classList.add('is-hover'); });
    document.addEventListener('mouseout', (e) => { if(e.target.closest && e.target.closest(HOVER)) ring.classList.remove('is-hover'); });

    /* magnetico */
    document.addEventListener('mousemove', (e) => {
      const b = e.target.closest && e.target.closest('.btn-primary,.btn-dark,[data-magnetic]');
      if(!b) return;
      const r = b.getBoundingClientRect();
      b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * .3) + 'px,' + ((e.clientY - r.top - r.height / 2) * .4) + 'px)';
    }, {passive:true});
    document.addEventListener('mouseout', (e) => { const b = e.target.closest && e.target.closest('.btn-primary,.btn-dark,[data-magnetic]'); if(b && !b.contains(e.relatedTarget)) b.style.transform = ''; });

    /* spotlight de borde */
    const spots = new Set();
    const sio = new IntersectionObserver((es) => es.forEach(e => e.isIntersecting ? spots.add(e.target) : spots.delete(e.target)), {rootMargin:'200px'});
    const watchSpots = (root) => $$('.spot:not([data-sp-on])', root).forEach(el => { el.setAttribute('data-sp-on', '1'); sio.observe(el); });
    window.asocSpots = watchSpots;
    let pending = false, px = 0, py = 0;
    document.addEventListener('mousemove', (e) => {
      px = e.clientX; py = e.clientY;
      if(pending) return; pending = true;
      requestAnimationFrame(() => { pending = false; spots.forEach(el => { const r = el.getBoundingClientRect(); el.style.setProperty('--sx', (px - r.left) + 'px'); el.style.setProperty('--sy', (py - r.top) + 'px'); }); });
    }, {passive:true});
  } else { window.asocSpots = () => {}; }

  /* ---------- fab de contacto ---------- */
  (function(){
    if($('#fab')) return;
    const C = (window.ASOC && window.ASOC.contact) || {wa:'https://wa.me/573153075463'};
    const wrap = document.createElement('div');
    wrap.innerHTML =
      '<button type="button" class="fab" id="fab" aria-haspopup="dialog" aria-expanded="false" aria-controls="fabPopup" data-magnetic><span class="fab-icon" aria-hidden="true">' + '<svg viewBox="0 0 24 24" fill="currentColor">' + window.ASOC_ICONS.whatsapp + '</svg></span><span class="fab-label">Hablar con un experto</span></button>' +
      '<div class="fab-popup" id="fabPopup" role="dialog" aria-modal="false" aria-label="Contacto"><button type="button" class="fab-popup-close" id="fabPopupClose" aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<span class="fab-popup-avatar"><img src="images/icon-color.svg" alt=""></span><p class="fab-popup-title">Equipo Asoclicper</p><p class="fab-popup-message">¿Tienes dudas sobre tu clínica o quieres asociarte? Escríbenos y te respondemos directo por WhatsApp.</p>' +
      '<a href="' + C.wa + '" target="_blank" rel="noopener" class="fab-popup-cta" data-magnetic><svg viewBox="0 0 24 24">' + window.ASOC_ICONS.whatsapp + '</svg>Escribir por WhatsApp</a></div>';
    document.body.append(...wrap.children);
    const fab = $('#fab'), pop = $('#fabPopup');
    const open = (v) => { fab.setAttribute('aria-expanded', v); fab.classList.toggle('is-hidden', v); pop.classList.toggle('is-open', v); };
    fab.addEventListener('click', () => open(true));
    $('#fabPopupClose').addEventListener('click', () => open(false));
    document.addEventListener('click', (e) => { if(pop.classList.contains('is-open') && !pop.contains(e.target) && !fab.contains(e.target)) open(false); });
    document.addEventListener('keydown', (e) => { if(e.key === 'Escape') open(false); });
    const vis = () => fab.classList.toggle('is-visible', window.scrollY > window.innerHeight * .5);
    window.addEventListener('scroll', vis, {passive:true}); vis();
  })();

  /* ---------- tabs y acordeones genericos ---------- */
  function initTabs(root){
    $$('[data-tabs]:not([data-t-on])', root).forEach((wrap) => {
      wrap.setAttribute('data-t-on', '1');
      const scope = wrap.dataset.target ? $(wrap.dataset.target) : (wrap.querySelector('.tab-panel') ? wrap : wrap.parentElement);
      const tabs = $$('.tab', wrap), panels = $$('.tab-panel', scope);
      const set = (k) => { tabs.forEach(t => t.classList.toggle('is-on', t.dataset.tab === k)); panels.forEach(p => p.classList.toggle('is-on', p.dataset.panel === k)); };
      tabs.forEach(t => t.addEventListener('click', () => { set(t.dataset.tab); if(t.dataset.hash) history.replaceState(null, '', '#' + t.dataset.tab); }));
      const h = location.hash.slice(1);
      if(h && tabs.some(t => t.dataset.tab === h)) set(h); else if(tabs[0]) set(tabs[0].dataset.tab);
      window.addEventListener('hashchange', () => { const k = location.hash.slice(1); if(tabs.some(t => t.dataset.tab === k)) set(k); });
    });
  }
  function initAcc(root){
    $$('.acc:not([data-a-on])', root).forEach((acc) => {
      acc.setAttribute('data-a-on', '1');
      $$('.acc-item', acc).forEach((it) => {
        const head = $('.acc-head', it), body = $('.acc-body', it);
        head.addEventListener('click', () => {
          const open = !it.classList.contains('is-open');
          if(acc.dataset.single !== undefined) $$('.acc-item.is-open', acc).forEach(o => { if(o !== it){ o.classList.remove('is-open'); $('.acc-body', o).style.maxHeight = null; } });
          it.classList.toggle('is-open', open);
          body.style.maxHeight = open ? body.scrollHeight + 'px' : null;
        });
      });
    });
  }

  /* ---------- modal de clinica ---------- */
  let modal;
  function getModal(){
    if(modal) return modal;
    modal = document.createElement('div'); modal.className = 'modal'; modal.innerHTML = '<div class="modal-box" role="dialog" aria-modal="true"><button class="modal-close" aria-label="Cerrar">' + '✕' + '</button><div class="modal-in"></div></div>';
    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => { if(e.target === modal || e.target.closest('.modal-close')) closeModal(); });
    document.addEventListener('keydown', (e) => { if(e.key === 'Escape') closeModal(); });
    return modal;
  }
  function closeModal(){ if(modal){ modal.classList.remove('is-open'); document.documentElement.style.overflow = ''; if(/^#clinica-/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search); } }
  function openClinic(id){
    const c = window.ASOC.clinics.find(x => x.id === id); if(!c) return;
    const m = getModal();
    const fact = (i, l, v) => v ? '<div class="md-fact">' + ic(i) + '<div><small>' + l + '</small>' + v + '</div></div>' : '';
    const link = (u, t) => '<a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(t || u.replace(/^https?:\/\//, '').replace(/\/$/, '')) + '</a>';
    const maps = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(c.name + ' ' + c.addr + ' ' + c.city);
    $('.modal-in', m).innerHTML =
      '<div class="md-head"><div class="lg"><img src="' + c.logo + '" alt="' + esc(c.name) + '"></div><div><h3>' + esc(c.name) + '</h3><div class="where">' + ic('map-pin') + esc(c.city) + ', ' + esc(c.dept) + '</div>' +
      '<div class="cc-badges" style="position:static;margin-top:12px;">' + (c.iso ? '<span class="badge iso">' + ic('award') + ' ISO 9001</span>' : '') + (c.intl ? '<span class="badge intl">' + ic('globe') + ' Pacientes internacionales</span>' : '') + '<span class="badge">' + ic('shield-check') + ' Clínica asociada</span></div></div></div>' +
      '<div class="md-body"><p class="desc">' + esc(c.desc) + '</p><div class="md-facts">' +
        fact('map-pin', 'Dirección', '<b>' + esc(c.addr) + '</b>') + fact('phone', 'Teléfono', '<b>' + esc(c.phone) + '</b>') +
        fact('mail', 'Correo', c.mail ? link('mailto:' + c.mail, c.mail) : '') + fact('globe', 'Sitio web', c.web ? link(c.web) : '') + fact('users', 'Dirección / gerencia', c.mgr ? '<b>' + esc(c.mgr) + '</b>' : '') +
      '</div>' + (c.services ? '<div class="md-services"><h4>Servicios y capacidad</h4><div class="chips">' + c.services.map(s => '<span class="chip" style="cursor:default">' + esc(s) + '</span>').join('') + '</div></div>' : '') +
      '<div class="md-actions">' + (c.web ? '<a class="btn btn-primary" href="' + esc(c.web) + '" target="_blank" rel="noopener">Visitar sitio web ' + ic('external') + '</a>' : '') +
        (c.wa ? '<a class="btn btn-ghost-dark" href="' + esc(c.wa) + '" target="_blank" rel="noopener">' + ic('whatsapp') + ' WhatsApp internacional</a>' : '') +
        '<a class="btn btn-ghost-dark" href="' + maps + '" target="_blank" rel="noopener">' + ic('map-pin') + ' Cómo llegar</a></div></div>';
    m.classList.add('is-open'); document.documentElement.style.overflow = 'hidden';
    if(location.hash !== '#clinica-' + id) history.replaceState(null, '', '#clinica-' + id);
  }
  window.asocOpenClinic = openClinic;
  function checkHash(){ const m = /^#clinica-(.+)$/.exec(location.hash); if(m) openClinic(m[1]); }

  /* ---------- directorio de clinicas ---------- */
  function initDirectory(root){
    const all = window.ASOC.clinics, mode = root.dataset.mode || 'full';
    const depts = Array.from(new Set(all.map(c => c.dept)));
    depts.sort((a, b) => all.filter(c => c.dept === b).length - all.filter(c => c.dept === a).length);
    const state = {q:'', dept:'', flag:''};
    root.innerHTML =
      '<div class="filter-bar"><label class="search">' + ic('search') + '<input type="search" placeholder="Busca por clínica, ciudad o departamento…" aria-label="Buscar clínica"></label></div>' +
      '<div class="chips" data-dept style="margin-bottom:' + (mode === 'turismo' ? '14' : '34') + 'px;"></div>' +
      (mode === 'turismo' ? '<div class="chips" data-flag style="margin-bottom:34px;"></div>' : '') +
      '<div class="clinic-grid"></div>';
    const grid = $('.clinic-grid', root), input = $('input', root);
    const dChips = $('[data-dept]', root), fChips = $('[data-flag]', root);
    dChips.innerHTML = '<button class="chip is-on" data-v="">Todas <span class="n">' + all.length + '</span></button>' + depts.map(d => '<button class="chip" data-v="' + esc(d) + '">' + esc(d) + ' <span class="n">' + all.filter(c => c.dept === d).length + '</span></button>').join('');
    if(fChips) fChips.innerHTML = '<button class="chip is-on" data-v="">Todas las clínicas</button><button class="chip" data-v="iso">' + ic('award') + ' Certificadas ISO 9001 <span class="n">' + all.filter(c => c.iso).length + '</span></button><button class="chip" data-v="intl">' + ic('globe') + ' Atienden pacientes internacionales <span class="n">' + all.filter(c => c.intl).length + '</span></button>';
    grid.innerHTML = all.map(c =>
      '<button class="clinic-card rv" data-id="' + c.id + '" data-s="' + esc(norm([c.name, c.city, c.dept].join(' '))) + '"><div class="cc-logo"><img src="' + c.logo + '" alt="' + esc(c.name) + '" loading="lazy"><div class="cc-badges">' + (c.iso ? '<span class="badge iso">ISO 9001</span>' : '') + (c.intl ? '<span class="badge intl">Internacional</span>' : '') + '</div></div>' +
      '<div class="cc-body"><h3>' + esc(c.name) + '</h3><div class="where">' + ic('map-pin') + esc(c.city) + ', ' + esc(c.dept) + '</div><p>' + esc(c.blurb) + '</p><span class="cc-more">Ver ficha completa ' + ic('arrow-right') + '</span></div></button>').join('') +
      '<div class="empty" hidden>No encontramos clínicas con ese criterio. Prueba con otra ciudad o escríbenos por WhatsApp.</div>';
    const cards = $$('.clinic-card', grid), empty = $('.empty', grid);
    function apply(){
      let n = 0;
      cards.forEach((el, i) => {
        const c = all[i];
        const ok = (!state.q || el.dataset.s.indexOf(norm(state.q)) > -1) && (!state.dept || c.dept === state.dept) && (!state.flag || c[state.flag]);
        el.classList.toggle('is-hidden', !ok); if(ok) n++;
      });
      empty.hidden = n > 0;
    }
    input.addEventListener('input', () => { state.q = input.value.trim(); apply(); });
    dChips.addEventListener('click', (e) => { const b = e.target.closest('.chip'); if(!b) return; state.dept = b.dataset.v; $$('.chip', dChips).forEach(x => x.classList.toggle('is-on', x === b)); apply(); });
    if(fChips) fChips.addEventListener('click', (e) => { const b = e.target.closest('.chip'); if(!b) return; state.flag = b.dataset.v; $$('.chip', fChips).forEach(x => x.classList.toggle('is-on', x === b)); apply(); });
    grid.addEventListener('click', (e) => { const b = e.target.closest('.clinic-card'); if(b) openClinic(b.dataset.id); });
    asocFillIcons(root); reveal(root);
    cards.forEach((c, i) => c.style.setProperty('--d', Math.min(i, 8) * .05 + 's'));
  }

  /* ---------- verifica tu clinica ---------- */
  function initVerify(root){
    const all = window.ASOC.clinics;
    root.innerHTML =
      '<div><span class="eyebrow">Verifica tu clínica</span><h3>¿Tu clínica hace parte de ASOCLICPER?</h3><p class="sub">Escribe el nombre de la clínica o la ciudad. Solo las clínicas habilitadas y con cirujanos plásticos acreditados hacen parte de nuestra red de 17 asociadas.</p></div>' +
      '<div class="vf-box"><div class="vf-input">' + ic('search') + '<input type="search" placeholder="Ej: Corpus, San Fernando, Medellín…" aria-label="Nombre de la clínica" autocomplete="off"></div><div class="vf-list"></div><div class="vf-result"></div></div>';
    const input = $('input', root), list = $('.vf-list', root), res = $('.vf-result', root);
    function show(kind, html, iconName){ res.className = 'vf-result ' + kind; res.innerHTML = ic(iconName) + '<div>' + html + '</div>'; }
    function choose(c){
      list.innerHTML = ''; input.value = c.name;
      show('ok', '<b>Sí: ' + esc(c.name) + ' es una clínica asociada a ASOCLICPER</b><span>' + esc(c.city) + ', ' + esc(c.dept) + '. Cumple con los estándares de calidad y seguridad de la red. <a class="link-arrow" style="display:inline-flex;margin-top:6px;" href="clinicas-asociadas.html#clinica-' + c.id + '">Ver ficha completa ' + ic('arrow-right') + '</a></span>', 'check');
    }
    input.addEventListener('input', () => {
      const q = norm(input.value.trim()); res.className = 'vf-result';
      if(q.length < 2){ list.innerHTML = ''; return; }
      const hits = all.filter(c => norm([c.name, c.city, c.dept].join(' ')).indexOf(q) > -1).slice(0, 5);
      list.innerHTML = hits.map(c => '<button class="vf-opt" data-id="' + c.id + '"><img src="' + c.logo + '" alt=""><span><b>' + esc(c.name) + '</b><small>' + esc(c.city) + ', ' + esc(c.dept) + '</small></span></button>').join('');
      if(!hits.length) show('no', '<b>No encontramos «' + esc(input.value.trim()) + '» entre las 17 clínicas asociadas</b><span>Eso no la descalifica ni la valida: verifica su habilitación y que el cirujano esté adscrito a la Sociedad Colombiana de Cirugía Plástica, y consúltanos por WhatsApp antes de decidir.</span>', 'alert');
    });
    list.addEventListener('click', (e) => { const b = e.target.closest('.vf-opt'); if(b) choose(all.find(c => c.id === b.dataset.id)); });
    asocFillIcons(root);
  }

  /* ---------- formularios (demo sin backend) ---------- */
  function initForms(root){
    $$('form[data-form]:not([data-f-on])', root).forEach((form) => {
      form.setAttribute('data-f-on', '1');
      form.addEventListener('submit', (e) => {
        e.preventDefault(); let ok = true;
        $$('.field', form).forEach((f) => {
          const inp = $('input,select,textarea', f); if(!inp || !inp.required) return;
          const bad = !inp.value.trim() || (inp.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value));
          f.classList.toggle('is-bad', bad); if(bad) ok = false;
        });
        const chk = $('input[type=checkbox][required]', form);
        if(chk && !chk.checked){ ok = false; chk.closest('.check').style.color = '#c9403a'; } else if(chk) chk.closest('.check').style.color = '';
        if(!ok){ const f = $('.is-bad', form); if(f) f.scrollIntoView({block:'center', behavior:'smooth'}); return; }
        const shell = form.closest('.form-shell') || form.parentElement;
        form.style.display = 'none'; const okBox = $('.form-ok', shell); if(okBox){ okBox.classList.add('is-on'); okBox.scrollIntoView({block:'center', behavior:'smooth'}); }
      });
      $$('.field input,.field select,.field textarea', form).forEach(i => i.addEventListener('input', () => i.closest('.field').classList.remove('is-bad')));
    });
  }

  function boot(root){
    asocFillIcons(root); initTabs(root); initAcc(root); initForms(root);
    $$('[data-clinic-directory]:not([data-d-on])', root).forEach(el => { el.setAttribute('data-d-on', '1'); initDirectory(el); });
    $$('[data-verify]:not([data-v-on])', root).forEach(el => { el.setAttribute('data-v-on', '1'); initVerify(el); });
    reveal(root); counters(root); window.asocSpots(root);
  }
  window.asocBoot = boot;
  boot(document);
  checkHash(); window.addEventListener('hashchange', checkHash);
  window.ASOC_UI = {openClinic, norm, esc, ic};
})();
