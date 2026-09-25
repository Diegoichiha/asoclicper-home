/* nav.js: iconos + header/footer compartidos (todas las paginas, incluido el home) */
(function(){
  const ICONS = {
    'arrow-right':'<path d="M5 12h14M13 5l7 7-7 7"/>',
    'arrow-up-right':'<path d="M7 17L17 7M8 7h9v9"/>',
    check:'<path d="M20 6L9 17l-5-5"/>',
    x:'<path d="M18 6L6 18M6 6l12 12"/>',
    plus:'<path d="M12 5v14M5 12h14"/>',
    search:'<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/>',
    'map-pin':'<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0116 0z"/><circle cx="12" cy="10" r="3"/>',
    phone:'<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/>',
    mail:'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>',
    shield:'<path d="M12 22s8-4.5 8-11V5l-8-3-8 3v6c0 6.5 8 11 8 11z"/>',
    'shield-check':'<path d="M12 22s8-4.5 8-11V5l-8-3-8 3v6c0 6.5 8 11 8 11z"/><path d="M9 12l2 2 4-4"/>',
    users:'<path d="M17 21v-2a4 4 0 00-4-4H7a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>',
    star:'<path d="M12 2l3 7 7 .6-5.3 4.6L18 22l-6-3.8L6 22l1.3-7.8L2 9.6 9 9z"/>',
    globe:'<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"/>',
    plane:'<path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    calendar:'<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    file:'<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    download:'<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    chevron:'<path d="M6 9l6 6 6-6"/>',
    mic:'<path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/><path d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"/>',
    alert:'<path d="M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0zM12 9v4M12 17h.01"/>',
    scale:'<path d="M12 3v18M5 21h14M3 7h18M6 7l-3 8a4 4 0 006 0zM18 7l-3 8a4 4 0 006 0z"/>',
    megaphone:'<path d="M3 11v2a1 1 0 001 1h2l5 4V6L6 10H4a1 1 0 00-1 1zM15 8a5 5 0 010 8M18 5a9 9 0 010 14"/>',
    link:'<path d="M10 13a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1M14 11a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
    building:'<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    chart:'<path d="M3 3v18h18M7 14l4-4 3 3 5-6"/>',
    clipboard:'<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2M9 14l2 2 4-4"/>',
    lock:'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
    heart:'<path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l1 1.1L12 21.2l7.8-7.7 1-1.1a5.5 5.5 0 000-7.8z"/>',
    external:'<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/>',
    dollar:'<path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>',
    award:'<circle cx="12" cy="8" r="6"/><path d="M15.5 13.5L17 22l-5-3-5 3 1.5-8.5"/>',
    clock:'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    home:'<path d="M3 11l9-8 9 8v10a1 1 0 01-1 1h-5v-7H9v7H4a1 1 0 01-1-1z"/>',
    briefcase:'<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>',
    news:'<path d="M4 4h13a2 2 0 012 2v14H6a2 2 0 01-2-2zM19 8h1a1 1 0 011 1v9a2 2 0 01-2 2M8 8h7M8 12h7M8 16h4"/>',
    play:'<path d="M8 5v14l11-7z"/>',
    whatsapp:'<path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.3c-.25.7-1.45 1.35-2 1.4-.53.06-1.02.28-3.4-.72-2.9-1.2-4.75-4.1-4.9-4.3-.14-.2-1.16-1.55-1.16-2.95 0-1.4.73-2.1 1-2.4.25-.27.55-.34.73-.34h.52c.17 0 .4-.06.6.47.25.6.83 2.05.9 2.2.07.15.12.33.02.53-.1.2-.15.32-.3.5-.14.16-.3.36-.44.49-.14.13-.3.28-.13.56.17.28.75 1.24 1.62 2 1.12 1 2.05 1.32 2.33 1.47.28.15.44.13.6-.08.17-.2.7-.82.9-1.1.18-.28.37-.23.62-.14.25.1 1.6.75 1.88.9.28.13.46.2.53.3.07.13.07.7-.18 1.4z"/>',
    facebook:'<path d="M13.5 21v-7.5H16l.5-3H13.5V8.3c0-.87.24-1.46 1.5-1.46H16.6V4.14C16.3 4.1 15.3 4 14.1 4c-2.4 0-4 1.47-4 4.16V10.5H7.6v3h2.5V21h3.4z"/>',
    instagram:'<path d="M12 2.2c2.7 0 3 0 4.1.06 2.7.12 3.9 1.36 4.1 4.1.05 1.1.06 1.4.06 4.1s0 3-.06 4.1c-.12 2.7-1.36 3.94-4.1 4.06-1.1.05-1.4.06-4.1.06s-3 0-4.1-.06c-2.74-.12-3.94-1.36-4.06-4.06C3.78 15 3.77 14.7 3.77 12s0-3 .06-4.1C4 5.2 5.2 4 7.9 3.86 9 3.8 9.3 3.8 12 3.8zm0 4.05a5.75 5.75 0 100 11.5 5.75 5.75 0 000-11.5zm0 9.5a3.75 3.75 0 110-7.5 3.75 3.75 0 010 7.5zm5.9-9.7a1.35 1.35 0 11-2.7 0 1.35 1.35 0 012.7 0z"/>',
    linkedin:'<path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21H17v-5.4c0-1.3-.02-2.96-1.8-2.96-1.8 0-2.08 1.4-2.08 2.86V21H9z"/>'
  };
  const FILL = {play:1,whatsapp:1,facebook:1,instagram:1,linkedin:1};
  const svg = (n) => '<svg viewBox="0 0 24 24"' + (FILL[n] ? ' class="fill"' : '') + '>' + (ICONS[n] || '') + '</svg>';
  window.ASOC_ICONS = ICONS;
  window.asocIcon = (n, cls) => '<span class="ico ' + (cls || '') + '">' + svg(n) + '</span>';
  window.asocFillIcons = (root) => (root || document).querySelectorAll('[data-i]:not([data-i-done])').forEach(el => {
    el.classList.add('ico'); el.setAttribute('data-i-done', '1'); el.innerHTML = svg(el.dataset.i);
  });
  const ni = (n) => '<span class="nav-ico">' + svg(n) + '</span>';

  const NAV = [
    { k:'nosotros', t:'Nosotros', href:'nosotros.html' },
    { k:'clinicas', t:'Clínicas Asociadas', href:'clinicas-asociadas.html', keys:['clinicas','beneficios','ser-asociado'], sub:[
      { i:'map-pin', t:'Directorio de las 17 clínicas', d:'Encuentra y verifica tu clínica', href:'clinicas-asociadas.html' },
      { i:'star', t:'Beneficios de asociarte', d:'Incluye calculadora de ahorro', href:'beneficios.html' },
      { i:'clipboard', t:'Ser Asociado', d:'Requisitos y pre-solicitud de afiliación', href:'ser-asociado.html' } ] },
    { k:'aliados', t:'Aliados Comerciales', href:'aliados.html', sub:[
      { i:'megaphone', t:'Paquetes de patrocinio', d:'Stands, banners y podcast', href:'aliados.html#paquetes' },
      { i:'briefcase', t:'Contacto comercial B2B', d:'Hablemos de tu marca', href:'aliados.html#b2b' },
      { i:'link', t:'Perfiles de aliados', d:'Quiénes ya caminan con nosotros', href:'aliados.html#perfiles' } ] },
    { k:'turismo', t:'Turismo Médico', href:'turismo-medico.html', sub:[
      { i:'award', t:'Directorio de clínicas certificadas', d:'Clínicas habilitadas y con ISO 9001', href:'turismo-medico.html#directorio' },
      { i:'plane', t:'Guía de viaje paso a paso', d:'Prepara tu cirugía con seguridad', href:'turismo-medico.html#guia' } ] },
    { k:'seguridad', t:'Seguridad del Paciente', href:'seguridad-del-paciente.html', sub:[
      { i:'search', t:'Verifica tu clínica', d:'Buscador de clínicas asociadas', href:'seguridad-del-paciente.html#verifica' },
      { i:'alert', t:'Señales de alerta', d:'Cómo reconocer clínicas ilegales', href:'seguridad-del-paciente.html#alertas' },
      { i:'mic', t:'Podcast «Bajo el Bisturí»', d:'Conversaciones sobre cirugía segura', href:'seguridad-del-paciente.html#podcast' } ] },
    { k:'noticias', t:'Noticias', href:'noticias.html' }
  ];
  const page = document.body.dataset.page || 'index';
  const isActive = (it) => it.k === page || (it.keys && it.keys.indexOf(page) > -1);

  const header = document.getElementById('siteHeader');
  if(header){
    header.innerHTML =
      '<div class="wrap">' +
        '<a class="logo" href="index.html"><img src="images/logo-color.svg" alt="Asoclicper"></a>' +
        '<nav class="mainnav" aria-label="Principal">' + NAV.map(it =>
          '<div class="nav-item' + (it.sub ? ' has-drop' : '') + (isActive(it) ? ' is-active' : '') + '">' +
            '<a class="nav-link" href="' + it.href + '">' + it.t + (it.sub ? '<svg class="caret" viewBox="0 0 24 24">' + ICONS.chevron + '</svg>' : '') + '</a>' +
            (it.sub ? '<div class="nav-drop">' + it.sub.map(s => '<a href="' + s.href + '"><span class="di">' + ni(s.i) + '</span><span><b>' + s.t + '</b><small>' + s.d + '</small></span></a>').join('') + '</div>' : '') +
          '</div>').join('') + '</nav>' +
        '<div class="navcta">' +
          '<a class="btn btn-ghost-dark" href="contacto.html">Contacto</a>' +
          '<a class="btn btn-primary" href="ser-asociado.html">Ser Asociado</a>' +
        '</div>' +
        '<button class="burger" id="burger" aria-label="Abrir menú"><span></span></button>' +
      '</div>';
  }

  /* drawer movil */
  let drawer;
  function buildDrawer(){
    drawer = document.createElement('div');
    drawer.className = 'drawer';
    drawer.innerHTML =
      '<div class="drawer-top"><img src="images/logo-blanco.svg" alt="Asoclicper"><button class="drawer-close" aria-label="Cerrar">✕</button></div>' +
      '<a class="d-link" href="index.html">Inicio</a>' +
      NAV.map(it => it.sub
        ? '<details><summary>' + it.t + '<svg class="caret" viewBox="0 0 24 24">' + ICONS.chevron + '</svg></summary><div class="d-sub"><a href="' + it.href + '">Ver sección</a>' + it.sub.map(s => '<a href="' + s.href + '">' + s.t + '</a>').join('') + '</div></details>'
        : '<a class="d-link" href="' + it.href + '">' + it.t + '</a>').join('') +
      '<a class="d-link" href="contacto.html">Contacto</a>' +
      '<div class="d-cta"><a class="btn btn-primary" href="ser-asociado.html">Ser Asociado</a></div>';
    document.body.appendChild(drawer);
    drawer.querySelector('.drawer-close').addEventListener('click', () => drawer.classList.remove('is-open'));
    drawer.addEventListener('click', (e) => { if(e.target.closest('a')) drawer.classList.remove('is-open'); });
  }
  document.addEventListener('click', (e) => {
    if(e.target.closest('#burger')){ if(!drawer) buildDrawer(); drawer.classList.add('is-open'); }
  });
  document.addEventListener('keydown', (e) => { if(e.key === 'Escape' && drawer) drawer.classList.remove('is-open'); });

  /* estado de scroll + barra de progreso */
  let bar = document.getElementById('progress');
  if(!bar){ bar = document.createElement('div'); bar.id = 'progress'; document.body.prepend(bar); }
  function onScroll(){
    const y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    if(header) header.classList.toggle('scrolled', y > 40);
  }
  document.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* footer */
  const footer = document.getElementById('siteFooter');
  if(footer){
    const C = (window.ASOC && window.ASOC.contact) || {address:'Carrera 50 # 9B - 20, Edif. Torres de la 50, Ofic. 216, Santiago de Cali, Colombia', phone:'(+57) 315 307 54 63', tel:'+573153075463', mail:'info@asoclicper.com.co', fb:'http://facebook.com/asoclicper/', ig:'https://www.instagram.com/asoclicper/', li:'https://www.linkedin.com/company/asoclicper/'};
    const allies = [['aliado-2.jpeg','Alcaldía de Santiago de Cali'],['aliado-sec-salud.png','Alcaldía de Cali · Salud'],['aliado-sec-turismo.jpg','Alcaldía de Cali · Turismo'],['aliado-gobernacion.png','Gobernación del Valle del Cauca'],['aliado-sociedad-turismo.jpg','Sociedad Colombiana de Turismo en Salud y Bienestar'],['aliado-ccc.svg','Cámara de Comercio de Cali']];
    footer.innerHTML =
      '<div class="wrap">' +
        '<div class="foot-allies"><span>Aliados estratégicos</span>' + allies.map(a => '<img src="images/site/' + a[0] + '" alt="' + a[1] + '" title="' + a[1] + '" loading="lazy">').join('') + '</div>' +
        '<div class="foot-grid" style="padding-top:44px;">' +
          '<div><img src="images/logo-blanco.svg" alt="Asoclicper"><p>Unidos por la excelencia en cirugía plástica y la seguridad del paciente. Asociación Colombiana de Clínicas de Cirugía Plástica, Estética y Reconstructiva.</p>' +
            '<div class="social"><a href="' + C.fb + '" target="_blank" rel="noopener" aria-label="Facebook">' + svg('facebook') + '</a><a href="' + C.ig + '" target="_blank" rel="noopener" aria-label="Instagram">' + svg('instagram') + '</a><a href="' + C.li + '" target="_blank" rel="noopener" aria-label="LinkedIn">' + svg('linkedin') + '</a></div></div>' +
          '<div class="foot-col"><h4>Portal</h4><a href="index.html">Inicio</a><a href="nosotros.html">Nosotros</a><a href="noticias.html">Noticias</a><a href="contacto.html">Contacto</a></div>' +
          '<div class="foot-col"><h4>Clínicas y aliados</h4><a href="clinicas-asociadas.html">Directorio de clínicas</a><a href="beneficios.html">Beneficios y calculadora</a><a href="ser-asociado.html">Ser Asociado</a><a href="aliados.html">Aliados comerciales</a></div>' +
          '<div class="foot-col"><h4>Pacientes</h4><a href="turismo-medico.html">Turismo médico</a><a href="seguridad-del-paciente.html">Seguridad del paciente</a><a href="seguridad-del-paciente.html#verifica">Verifica tu clínica</a><a href="seguridad-del-paciente.html#podcast">Podcast «Bajo el Bisturí»</a></div>' +
          '<div class="foot-col"><h4>Contacto</h4><a href="https://www.google.com/maps/search/?api=1&query=Carrera+50+%23+9B-20+Cali" target="_blank" rel="noopener">' + C.address + '</a><a href="tel:' + C.tel + '">' + C.phone + '</a><a href="mailto:' + C.mail + '">' + C.mail + '</a></div>' +
        '</div>' +
        '<div class="foot-bottom"><span>© 2026 ASOCLICPER — Asociación Colombiana de Clínicas de Cirugía Plástica, Estética y Reconstructiva.</span>' +
          '<span><a href="transparencia.html#aviso" style="color:inherit">Aviso de privacidad</a> · <a href="transparencia.html#politica" style="color:inherit">Protección de datos</a> · <a href="transparencia.html#financieros" style="color:inherit">Estados financieros</a> · <a href="transparencia.html#rte" style="color:inherit">Régimen Tributario Especial</a> · <a href="transparencia.html#documental" style="color:inherit">Asoclicper Documental</a></span></div>' +
        '<div class="foot-bottom" style="padding-top:10px;"><span>Propuesta de rediseño del portal — prototipo navegable con contenido de asoclicper.com.</span></div>' +
      '</div>';
  }
  asocFillIcons();
})();
