/* megamenu.js: propuesta de menu con mega menu. Solo la carga opcion-megamenu.html; reutiliza NAV/iconos de nav.js.
   Barra superior = logo + boton de menu; al abrir, panel a pantalla completa con todos los enlaces. */
(function(){
  const bar = document.getElementById('megaHeader');
  if(!bar || !window.ASOC_NAV) return;
  const ICONS = window.ASOC_ICONS, NAV = window.ASOC_NAV, C = (window.ASOC && window.ASOC.contact) || {};
  const FILL = {play:1, whatsapp:1, facebook:1, instagram:1, linkedin:1};
  const svg = (n) => '<svg viewBox="0 0 24 24"' + (FILL[n] ? ' class="fill"' : '') + '>' + (ICONS[n] || '') + '</svg>';
  const page = document.body.dataset.page || 'index';

  /* ---------- contenido: los 8 enlaces principales + texto de cada panel ---------- */
  const META = {
    inicio:    {i:'home',        blurb:'Conoce ASOCLICPER: unimos a las clínicas de cirugía plástica, estética y reconstructiva de Colombia en torno a la excelencia y la seguridad del paciente.'},
    nosotros:  {i:'users',       blurb:'Nuestro propósito, meta, política de calidad y valores, y la Junta Directiva que lidera la Asociación.'},
    clinicas:  {i:'map-pin',     blurb:'Una red de 17 clínicas habilitadas y con cirujanos plásticos acreditados, en 8 departamentos del país.'},
    aliados:   {i:'briefcase',   blurb:'Conecta tu marca con la red de clínicas: patrocinios, eventos, podcast y alianzas comerciales.'},
    turismo:   {i:'plane',       blurb:'Clínicas certificadas y una guía paso a paso para operarte en Colombia con seguridad.'},
    seguridad: {i:'shield-check',blurb:'Verifica tu clínica, aprende a reconocer señales de alerta y escucha nuestro podcast sobre cirugía segura.'},
    noticias:  {i:'news',        blurb:'Novedades del sector, comunicados y contenidos para aprender sobre cirugía plástica segura.'},
    contacto:  {i:'mail',        blurb:'¿Quieres asociarte, verificar una clínica o proponer una alianza? Escríbenos y te respondemos.'}
  };
  const items = [{k:'inicio', t:'Inicio', href:'index.html'}]
    .concat(NAV.map(n => ({k:n.k, t:n.t, href:n.href, sub:n.sub, keys:n.keys})))
    .concat([{k:'contacto', t:'Contacto', href:'contacto.html', sub:[
      {i:'whatsapp', t:'WhatsApp', d:C.phone || '(+57) 315 307 54 63', href:C.wa || 'https://wa.me/573153075463'},
      {i:'mail', t:'Correo electrónico', d:C.mail || 'info@asoclicper.com.co', href:'mailto:' + (C.mail || 'info@asoclicper.com.co')},
      {i:'map-pin', t:'Oficina en Cali', d:'Torres de la 50 · Ofic. 216', href:'contacto.html'}]}]);
  const isCurrent = (it) => it.k === page || (it.keys && it.keys.indexOf(page) > -1);
  const CTA_LABEL = {inicio:'Ir al inicio', nosotros:'Conocer a ASOCLICPER', noticias:'Ver todas las noticias'};

  /* ---------- barra superior (logo + boton de menu) ---------- */
  bar.innerHTML =
    '<div class="wrap">' +
      '<a class="logo" href="index.html"><img src="images/logo-color.svg" alt="Asoclicper"></a>' +
      '<button class="mega-toggle" id="megaToggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="mega" data-magnetic>' +
        '<span class="mt-label">Menú</span><span class="mt-icon" aria-hidden="true"><i></i><i></i><i></i></span>' +
      '</button>' +
    '</div>';

  /* ---------- panel a pantalla completa ---------- */
  const li = items.map((it, n) =>
    '<li class="m-item' + (isCurrent(it) ? ' is-current' : '') + '" data-i="' + n + '" style="--d:' + n + '">' +
      '<div class="m-row"><a class="m-link" href="' + it.href + '"><span class="m-num">' + String(n + 1).padStart(2, '0') + '</span><span>' + it.t + '</span>' +
        '<span class="m-arr" aria-hidden="true"><svg viewBox="0 0 24 24">' + ICONS['arrow-up-right'] + '</svg></span></a>' +
        (it.sub ? '<button class="m-exp" type="button" aria-label="Mostrar enlaces de ' + it.t + '" aria-expanded="false"><svg viewBox="0 0 24 24">' + ICONS.chevron + '</svg></button>' : '') +
      '</div>' +
      (it.sub ? '<div class="m-sub">' + it.sub.map(s => '<a href="' + s.href + '"' + (/^https?:/.test(s.href) ? ' target="_blank" rel="noopener"' : '') + '><span><b style="font-weight:600">' + s.t + '</b><small>' + s.d + '</small></span></a>').join('') + '</div>' : '') +
    '</li>').join('');

  const panels = items.map((it, n) => {
    const m = META[it.k] || {i:'star', blurb:''};
    const body = it.sub
      ? '<div class="m-cards">' + it.sub.map(s => '<a class="m-card" href="' + s.href + '"' + (/^https?:/.test(s.href) ? ' target="_blank" rel="noopener"' : '') + '><span class="mi">' + svg(s.i) + '</span><span><b>' + s.t + '</b><small>' + s.d + '</small></span><span class="go">' + svg('arrow-up-right') + '</span></a>').join('') + '</div>' +
        (it.k !== 'contacto' ? '<a class="m-all" href="' + it.href + '">Ver toda la sección ' + svg('arrow-right') + '</a>' : '')
      : '<div class="m-hero"><span class="mi">' + svg(m.i) + '</span><p>' + m.blurb + '</p></div><a class="m-all" href="' + it.href + '">' + (CTA_LABEL[it.k] || 'Ir a ' + it.t) + ' ' + svg('arrow-right') + '</a>';
    return '<div class="m-panel" data-i="' + n + '"><div class="pk">' + String(n + 1).padStart(2, '0') + ' · ' + it.t + '</div><h3>' + it.t + '</h3>' + (it.sub ? '<p class="pd">' + m.blurb + '</p>' : '') + body + '</div>';
  }).join('');

  const mega = document.createElement('div');
  mega.className = 'mega'; mega.id = 'mega'; mega.setAttribute('role', 'dialog'); mega.setAttribute('aria-modal', 'true'); mega.setAttribute('aria-label', 'Menú principal'); mega.setAttribute('aria-hidden', 'true');
  mega.innerHTML =
    '<div class="mega-bg" aria-hidden="true"><span class="mb1"></span><span class="mb2"></span><span class="mb3"></span><span class="mb4"></span><span class="mg"></span></div>' +
    '<div class="wrap mega-top">' +
      '<a class="mega-logo" href="index.html"><img src="images/logo-blanco.svg" alt="Asoclicper"></a>' +
      '<div class="mega-top-r">' +
        '<div class="m-lang" role="group" aria-label="Idioma"><span class="gl" aria-hidden="true">' + svg('globe') + '</span>' +
          '<a class="is-on" href="#" data-lang="es-CO" lang="es-CO" hreflang="es-CO" aria-current="true" title="Español (Colombia)">ES</a>' +
          '<a href="#" data-lang="en-US" lang="en-US" hreflang="en-US" title="English (US) · próximamente">EN</a></div>' +
        '<a class="btn btn-ghost" href="contacto.html">Contacto</a><a class="btn btn-primary" href="ser-asociado.html">Ser Asociado</a>' +
        '<button class="mega-close" id="megaClose" type="button" aria-label="Cerrar menú"><svg viewBox="0 0 24 24">' + ICONS.x + '</svg></button></div>' +
    '</div>' +
    '<div class="wrap mega-body">' +
      '<nav class="mega-nav" aria-label="Menú principal"><ol>' + li + '</ol></nav>' +
      '<div class="mega-panels">' + panels + '</div>' +
      '<aside class="mega-side">' +
        '<a class="m-feat" href="seguridad-del-paciente.html#verifica"><span class="go">' + svg('arrow-up-right') + '</span><small>Para pacientes</small><b>Verifica tu clínica</b><span class="d">Confirma si tu clínica hace parte de ASOCLICPER antes de operarte.</span></a>' +
        '<a class="m-doc" href="asoclicper-documental.html"><span class="mi">' + svg('file') + '</span><span><b>Asoclicper Documental</b><small>Documentos legales para consulta</small></span></a>' +
        '<div class="m-contact"><h4>Contacto</h4>' +
          '<a href="https://www.google.com/maps/search/?api=1&query=Carrera+50+%23+9B-20+Cali" target="_blank" rel="noopener">' + svg('map-pin') + '<span>' + (C.address || 'Carrera 50 # 9B - 20, Edif. Torres de la 50, Ofic. 216, Santiago de Cali, Colombia') + '</span></a>' +
          '<a href="tel:' + (C.tel || '+573153075463') + '">' + svg('phone') + '<span>' + (C.phone || '(+57) 315 307 54 63') + '</span></a>' +
          '<a href="mailto:' + (C.mail || 'info@asoclicper.com.co') + '">' + svg('mail') + '<span>' + (C.mail || 'info@asoclicper.com.co') + '</span></a>' +
          '<div class="m-social"><a href="' + (C.fb || '#') + '" target="_blank" rel="noopener" aria-label="Facebook">' + svg('facebook') + '</a><a href="' + (C.ig || '#') + '" target="_blank" rel="noopener" aria-label="Instagram">' + svg('instagram') + '</a><a href="' + (C.li || '#') + '" target="_blank" rel="noopener" aria-label="LinkedIn">' + svg('linkedin') + '</a></div>' +
        '</div>' +
      '</aside>' +
    '</div>' +
    '<div class="wrap mega-foot"><span>© 2026 ASOCLICPER · Asociación Colombiana de Clínicas de Cirugía Plástica, Estética y Reconstructiva</span>' +
      '<span><a href="asoclicper-documental.html">Asoclicper Documental</a> · <a href="transparencia.html#aviso">Aviso de privacidad</a><span class="keys"> · pulsa<kbd>Esc</kbd>para cerrar</span></span></div>';
  document.body.appendChild(mega);

  /* ---------- comportamiento ---------- */
  const toggle = document.getElementById('megaToggle'), closeBtn = document.getElementById('megaClose');
  const lis = Array.from(mega.querySelectorAll('.m-item')), pans = Array.from(mega.querySelectorAll('.m-panel'));
  let open = false;

  function activate(n){
    lis.forEach((el, i) => el.classList.toggle('is-active', i === n));
    pans.forEach((el, i) => el.classList.toggle('is-active', i === n));
  }
  // panel inicial: la seccion actual si tiene submenu; si no, "Clinicas Asociadas"
  const firstSub = items.findIndex(it => it.sub && isCurrent(it));
  const defaultPanel = firstSub > -1 ? firstSub : items.findIndex(it => it.k === 'clinicas');
  activate(defaultPanel);

  lis.forEach((el, n) => {
    el.addEventListener('mouseenter', () => activate(n));
    el.addEventListener('focusin', () => activate(n));
    const exp = el.querySelector('.m-exp');
    if(exp) exp.addEventListener('click', () => { const on = !el.classList.contains('is-exp'); lis.forEach(x => x.classList.remove('is-exp')); el.classList.toggle('is-exp', on); exp.setAttribute('aria-expanded', on ? 'true' : 'false'); });
  });

  function setOrigin(){
    const r = toggle.getBoundingClientRect();
    mega.style.setProperty('--mx', (r.left + r.width - 24) + 'px');
    mega.style.setProperty('--my', (r.top + r.height / 2) + 'px');
  }
  function openMenu(){
    if(open) return; open = true; setOrigin();
    mega.classList.add('is-open'); mega.setAttribute('aria-hidden', 'false');
    toggle.setAttribute('aria-expanded', 'true'); document.documentElement.classList.add('mega-lock');
    mega.scrollTop = 0; setTimeout(() => closeBtn.focus({preventScroll:true}), 450);
  }
  function closeMenu(){
    if(!open) return; open = false; setOrigin();
    mega.classList.remove('is-open'); mega.setAttribute('aria-hidden', 'true');
    toggle.setAttribute('aria-expanded', 'false'); document.documentElement.classList.remove('mega-lock');
    toggle.focus({preventScroll:true});
  }
  toggle.addEventListener('click', openMenu);
  closeBtn.addEventListener('click', closeMenu);
  // al elegir un enlace de la misma pagina (ancla) se cierra; los demas navegan
  mega.addEventListener('click', (e) => { const a = e.target.closest('a[href]'); if(a && !a.dataset.lang && !e.defaultPrevented){ const h = a.getAttribute('href'); if(h.charAt(0) === '#' || /^(mailto|tel):/.test(h)) closeMenu(); } });
  document.addEventListener('keydown', (e) => {
    if(!open) return;
    if(e.key === 'Escape'){ closeMenu(); return; }
    if(e.key !== 'Tab') return;
    const f = Array.from(mega.querySelectorAll('a[href],button')).filter(el => el.offsetParent !== null && !el.closest('.m-panel:not(.is-active)'));
    if(!f.length) return;
    const first = f[0], last = f[f.length - 1];
    if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
    else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
  });
  window.addEventListener('resize', () => { if(open) setOrigin(); });

  /* estado de scroll de la barra */
  function onScroll(){ bar.classList.toggle('scrolled', window.scrollY > 40); }
  document.addEventListener('scroll', onScroll, {passive:true}); onScroll();
})();
