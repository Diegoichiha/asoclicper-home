# -*- coding: utf-8 -*-
"""
Genera el single post de cada articulo (noticias/<slug>.html) y assets/news-data.js (indice para el listado)
a partir de news.json (salida de build_news_data.py).

Uso:  python -X utf8 build_news_pages.py
"""
import json, os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..')) if os.path.basename(HERE) == '_build' else os.path.abspath(os.path.join(HERE, '..', 'site'))
OUT = os.path.join(SITE, 'noticias')
os.makedirs(OUT, exist_ok=True)
SITE_URL = 'https://diegoichiha.github.io/asoclicper-home/'

CATCLS = {'excelencia': '', 'accion': 'c2', 'eventos': 'c3', 'general': 'c4'}
CATNAMES = {
    'es': {'accion': 'Cirujanos en Acción', 'excelencia': 'Enfocados en la Excelencia', 'eventos': 'Eventos y Oportunidades', 'general': 'Interés General'},
    'en': {'accion': 'Surgeons in Action', 'excelencia': 'Focused on Excellence', 'eventos': 'Events and Opportunities', 'general': 'General Interest'},
}

S = {
    'es': {
        'home': 'Inicio', 'news': 'Noticias', 'read': 'min de lectura', 'read_s': 'de lectura', 'by': 'Equipo ASOCLICPER',
        'by_sub': 'Asociación Colombiana de Clínicas de Cirugía Plástica, Estética y Reconstructiva',
        'toc': 'En este artículo', 'published': 'Publicado', 'cat': 'Categoría', 'reading': 'Lectura', 'share': 'Compartir',
        'share_this': 'Compartir este artículo', 'copy': 'Copiar enlace', 'wa': 'Compartir en WhatsApp', 'fb': 'Compartir en Facebook',
        'li': 'Compartir en LinkedIn', 'x': 'Compartir en X', 'mail': 'Enviar por correo', 'native': 'Compartir',
        'back': 'Volver a noticias', 'more_t': 'Sigue leyendo', 'more_p': 'Más noticias de la red de clínicas asociadas a ASOCLICPER.',
        'prev': 'Noticia anterior', 'next': 'Noticia siguiente', 'more': 'Leer más',
        'about_t': 'Publicado por ASOCLICPER',
        'about_p': 'Somos la asociación que reúne a las clínicas de cirugía plástica, estética y reconstructiva de Colombia, unidas por la excelencia y la seguridad del paciente.',
        'tr': 'Read this article in English', 'tr_lang': 'en',
        'cta_e': 'Únete a la comunidad', 'cta_h': '¿Tu clínica quiere hacer parte de esta comunidad con un claro propósito?',
        'cta_p': 'Tener voz en el sector es clave. En Asoclicper representamos tus intereses y encuentras apoyo integral.',
        'cta_b1': '¡Conviértete en asociado!', 'cta_b2': 'Conoce los beneficios', 'nav': 'Navegación entre noticias', 'crumbs': 'Ruta de navegación',
        'min': 'min', 'cat_hash': 'noticias.html#cat-%s', 'locale': 'es_CO', 'img_alt': 'Portada de la noticia',
    },
    'en': {
        'home': 'Home', 'news': 'News', 'read': 'min read', 'read_s': 'read', 'by': 'ASOCLICPER Team',
        'by_sub': 'Colombian Association of Plastic, Aesthetic and Reconstructive Surgery Clinics',
        'toc': 'In this article', 'published': 'Published', 'cat': 'Category', 'reading': 'Reading time', 'share': 'Share',
        'share_this': 'Share this article', 'copy': 'Copy link', 'wa': 'Share on WhatsApp', 'fb': 'Share on Facebook',
        'li': 'Share on LinkedIn', 'x': 'Share on X', 'mail': 'Send by email', 'native': 'Share',
        'back': 'Back to news', 'more_t': 'Keep reading', 'more_p': 'More news from the network of clinics associated with ASOCLICPER.',
        'prev': 'Previous story', 'next': 'Next story', 'more': 'Read more',
        'about_t': 'Published by ASOCLICPER',
        'about_p': 'We are the association that brings together the plastic, aesthetic and reconstructive surgery clinics of Colombia, united by excellence and patient safety.',
        'tr': 'Leer este artículo en español', 'tr_lang': 'es',
        'cta_e': 'Join the community', 'cta_h': 'Does your clinic want to be part of this community with a clear purpose?',
        'cta_p': 'Having a voice in the sector is key. At ASOCLICPER we represent your interests and you find comprehensive support.',
        'cta_b1': 'Become a member!', 'cta_b2': 'Discover the benefits', 'nav': 'Navigate between stories', 'crumbs': 'Breadcrumb',
        'min': 'min', 'cat_hash': 'noticias.html#en', 'locale': 'en_US', 'img_alt': 'Story cover',
    },
}

X_SVG = '<svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'


def e(s):
    return H.escape(s or '', quote=True)


def share_html(t, big=False):
    return ('<div class="share" role="group" aria-label="%s">'
            '<button type="button" data-act="copy" aria-label="%s" title="%s"><span data-i="link"></span></button>'
            '<a data-net="whatsapp" target="_blank" rel="noopener" aria-label="%s" title="%s"><span data-i="whatsapp"></span></a>'
            '<a data-net="facebook" target="_blank" rel="noopener" aria-label="%s" title="%s"><span data-i="facebook"></span></a>'
            '<a data-net="linkedin" target="_blank" rel="noopener" aria-label="%s" title="%s"><span data-i="linkedin"></span></a>'
            '<a data-net="x" target="_blank" rel="noopener" aria-label="%s" title="%s">%s</a>'
            '<a data-net="mail" aria-label="%s" title="%s"><span data-i="mail"></span></a>'
            '<button type="button" data-act="native" hidden aria-label="%s" title="%s"><span data-i="external"></span></button>'
            '</div>') % (e(t['share_this']), e(t['copy']), e(t['copy']), e(t['wa']), e(t['wa']), e(t['fb']), e(t['fb']), e(t['li']), e(t['li']),
                         e(t['x']), e(t['x']), X_SVG, e(t['mail']), e(t['mail']), e(t['native']), e(t['native']))


def card(p, t, lang, delay=0):
    cn = CATNAMES[lang][p['cat']]
    return ('<a class="post rv" style="--d:%ss" href="noticias/%s.html"><div class="im%s"><img src="%s" alt="" width="640" height="400" loading="lazy" decoding="async"></div>'
            '<div class="bd"><span class="cat %s">%s</span><h3>%s</h3><span class="when">%s<i class="meta-dot"></i>%d %s</span>'
            '<span class="more">%s <span class="ico" data-i="arrow-right"></span></span></div></a>') % (
        delay, p['slug'], ' is-poster' if p.get('poster') else '', p['thumb'] or p['cover'] or 'images/icon-color.svg',
        CATCLS[p['cat']], e(cn), e(p['title']), e(p['dateLabel']), p['min'], t['min'], t['more'])


def build(p, order, by_id, by_slug_en):
    lang = p['lang']
    t = S[lang]
    cn = CATNAMES[lang][p['cat']]
    same = [x for x in order if x['lang'] == lang]
    i = next(k for k, x in enumerate(same) if x['id'] == p['id'])
    newer = same[i - 1] if i > 0 else None
    older = same[i + 1] if i + 1 < len(same) else None

    # relacionados: misma categoria primero
    rel = [x for x in same if x['id'] != p['id'] and x['cat'] == p['cat']][:3]
    if len(rel) < 3:
        rel += [x for x in same if x['id'] != p['id'] and x not in rel][:3 - len(rel)]

    toc = p['toc'] if len(p['toc']) >= 2 else []
    has_cover = bool(p['cover'])
    ratio = (p['cw'] / p['ch']) if (p['cw'] and p['ch']) else 1.2
    ar = max(0.8, min(1.6, ratio))
    contain = bool(p.get('poster')) or ratio < 0.8 or ratio > 1.75
    tr = by_id.get(p['tr']) if p.get('tr') else None

    # ---------- hero
    if has_cover:
        amb = '<span class="pc-amb" style="background-image:url(%s)" aria-hidden="true"></span>' % p['cover'] if contain else ''
        cover = ('<figure class="post-cover rv rv-s" data-d=".12"><div class="pc-frame%s" style="--ar:%.3f">%s'
                 '<img src="%s" width="%d" height="%d" alt="%s" fetchpriority="high" decoding="async"></div>'
                 '<div class="ph-float"><span data-i="clock"></span><div><b>%d %s</b><span class="lbl">%s</span></div></div></figure>') % (
            ' is-contain' if contain else '', ar, amb, p['cover'], p['cw'], p['ch'], e(p['title']), p['min'], t['min'], t['read_s'])
    else:
        cover = ''
    kicker = ('<div class="post-kicker rv" data-d=".05"><a class="cat %s" href="%s">%s</a><span class="kmeta">'
              '<time datetime="%s">%s</time><span class="dot"></span><span>%d %s</span></span></div>') % (
        CATCLS[p['cat']], (t['cat_hash'] % p['cat']) if lang == 'es' else t['cat_hash'], e(cn), p['date'], e(p['dateLabel']), p['min'], t['read'])
    trpill = ''
    if tr:
        trpill = '<a class="tr-pill" href="noticias/%s.html" hreflang="%s" lang="%s"><span data-i="globe"></span>%s</a>' % (tr['slug'], t['tr_lang'], t['tr_lang'], e(t['tr']))

    hero = ('<header class="page-hero post-hero">'
            '<div class="ph-field"><span class="ph-blob pb1"></span><span class="ph-blob pb2"></span><span class="ph-blob pb3"></span><span class="ph-blob pb4"></span></div>'
            '<div class="ph-grid"></div><div class="ph-scrim"></div>'
            '<div class="wrap ph-inner%s"><div class="post-head">'
            '<nav class="crumbs rv" aria-label="%s"><a href="index.html">%s</a><span class="sep">/</span><a href="noticias.html">%s</a><span class="sep">/</span><span>%s</span></nav>'
            '%s<h1 class="rv" data-d=".1" itemprop="headline">%s</h1>'
            '<div class="post-by rv" data-d=".18"><span class="by-av"><img src="images/icon-color.svg" alt=""></span>'
            '<div><b itemprop="author">%s</b><small>%s</small></div>%s</div>'
            '</div>%s</div></header>') % (
        '' if has_cover else ' no-cover', e(t['crumbs']), t['home'], t['news'], e(cn), kicker, e(p['title']), t['by'], e(t['by_sub']), trpill, cover)

    # ---------- aside
    aside = []
    if toc:
        aside.append('<details class="toc rv" open><summary><h4>%s</h4><span class="ico" data-i="chevron"></span></summary><ol>%s</ol></details>' % (
            t['toc'],
            ''.join('<li class="l%d"><a href="noticias/%s.html#%s" data-h="%s">%s</a></li>' % (x['l'], p['slug'], x['id'], x['id'], e(x['t'])) for x in toc)))
    aside.append('<div class="pinfo rv" data-d=".08"><dl><div><dt>%s</dt><dd><time datetime="%s">%s</time></dd></div>'
                 '<div><dt>%s</dt><dd><a class="cat %s" href="%s">%s</a></dd></div>'
                 '<div><dt>%s</dt><dd>%d %s</dd></div></dl><span class="share-t">%s</span>%s</div>' % (
        t['published'], p['date'], e(p['dateLabel']), t['cat'], CATCLS[p['cat']], (t['cat_hash'] % p['cat']) if lang == 'es' else t['cat_hash'], e(cn),
        t['reading'], p['min'], t['min'], t['share'], share_html(t)))

    # ---------- cierre
    end = ('<footer class="post-end"><div class="post-end-row"><div class="share-line"><span class="lbl">%s</span>%s</div>'
           '<a class="link-arrow" href="noticias.html"><span class="ico flip" data-i="arrow-right"></span> %s</a></div>'
           '<div class="about-box"><span class="by-av"><img src="images/icon-color.svg" alt=""></span><div><b>%s</b><p>%s</p></div></div></footer>') % (
        e(t['share_this']), share_html(t), t['back'], t['about_t'], e(t['about_p']))

    # ---------- anterior / siguiente
    def pn(x, cls, label, flip):
        return ('<a class="%s" href="noticias/%s.html"><span class="th"><img src="%s" alt="" width="96" height="96" loading="lazy"></span>'
                '<span><small>%s%s%s</small><b>%s</b></span></a>') % (
            cls, x['slug'], x['thumb'] or x['cover'] or 'images/icon-color.svg',
            '<span class="ico flip" data-i="arrow-right"></span>' if flip else '', label, '' if flip else '<span class="ico" data-i="arrow-right"></span>', e(x['title']))
    pns = []
    if newer: pns.append(pn(newer, 'prev', t['prev'], True))
    if older: pns.append(pn(older, 'next', t['next'], False))
    pnav = '<section class="post-nav"><div class="wrap"><nav class="pn%s" aria-label="%s">%s</nav></div></section>' % (
        ' one' if len(pns) == 1 else '', e(t['nav']), ''.join(pns)) if pns else ''

    related = ('<section class="related"><div class="wrap"><div class="tag-row rv"><div><span class="eyebrow">%s</span><h2 class="sec-title">%s</h2></div><p>%s</p></div>'
               '<div class="posts">%s</div></div></section>') % (
        t['news'], t['more_t'], e(t['more_p']), ''.join(card(x, t, lang, k * .08) for k, x in enumerate(rel)))

    cta = ('<section class="post-cta"><div class="wrap"><div class="cta-band rv rv-s"><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p>'
           '<div class="row"><a class="btn btn-primary" href="ser-asociado.html">%s</a><a class="btn btn-ghost" href="beneficios.html">%s</a></div></div></div></section>') % (
        e(t['cta_e']), e(t['cta_h']), e(t['cta_p']), e(t['cta_b1']), e(t['cta_b2']))

    # ---------- meta
    img_abs = SITE_URL + (p['cover'] or 'images/logo-asoclicper.png')
    page_url = SITE_URL + 'noticias/' + p['slug'] + '.html'
    ld = {
        '@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': p['title'], 'datePublished': p['date'], 'dateModified': p['date'],
        'inLanguage': lang, 'articleSection': cn, 'image': [img_abs], 'mainEntityOfPage': page_url, 'description': p['excerpt'],
        'author': {'@type': 'Organization', 'name': 'ASOCLICPER'},
        'publisher': {'@type': 'Organization', 'name': 'ASOCLICPER', 'logo': {'@type': 'ImageObject', 'url': SITE_URL + 'images/logo-asoclicper.png'}},
    }
    alt = ''
    if tr:
        alt = '<link rel="alternate" hreflang="%s" href="%s">\n' % (t['tr_lang'], SITE_URL + 'noticias/' + tr['slug'] + '.html')

    html = '''<!doctype html>
<html lang="%(lang)s" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<base href="../">
<title>%(title)s | ASOCLICPER</title>
<meta name="description" content="%(desc)s">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ASOCLICPER">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(img)s">
<meta property="og:url" content="%(url)s">
<meta property="og:locale" content="%(locale)s">
<meta property="article:published_time" content="%(date)s">
<meta property="article:section" content="%(cat)s">
<meta name="twitter:card" content="summary_large_image">
%(alt)s<link rel="icon" href="images/icon-color.svg">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/nav.css">
<link rel="stylesheet" href="assets/news.css">
<link rel="stylesheet" href="assets/post.css">
<script>document.documentElement.classList.remove('no-js')</script>
<script type="application/ld+json">%(ld)s</script>
</head>
<body data-page="noticias" class="post-page">
<div id="progress" aria-hidden="true"></div>
<header id="siteHeader"></header>

<main id="top">
<article itemscope itemtype="https://schema.org/NewsArticle">
%(hero)s
<div class="post-body">
  <div class="wrap post-grid">
    <div class="post-main">
      <div class="prose" id="postBody" itemprop="articleBody">
%(body)s
      </div>
      %(end)s
    </div>
    <aside class="post-aside">%(aside)s</aside>
  </div>
</div>
</article>
%(pnav)s
%(related)s
%(cta)s
</main>

<footer id="siteFooter"></footer>
<script src="assets/data.js"></script>
<script src="assets/nav.js"></script>
<script src="assets/site.js"></script>
<script src="assets/post.js"></script>
</body>
</html>
''' % {
        'lang': lang, 'title': e(p['title']), 'desc': e(p['excerpt']), 'img': e(img_abs), 'url': e(page_url), 'locale': t['locale'],
        'date': p['date'], 'cat': e(cn), 'alt': alt, 'ld': json.dumps(ld, ensure_ascii=False).replace('</', '<\\/'),
        'hero': hero, 'body': p['body'], 'end': end, 'aside': ''.join(aside), 'pnav': pnav, 'related': related, 'cta': cta,
    }
    # el video sin miniatura propia usa la portada del articulo
    def fix_thumb(m):
        f = os.path.join(SITE, 'images', 'news', 'yt-%s.webp' % m.group(1))
        return m.group(0) if os.path.exists(f) else m.group(0).replace('images/news/yt-%s.webp' % m.group(1), p['cover'] or 'images/icon-color.svg')
    html = re.sub(r'images/news/yt-([A-Za-z0-9_-]{11})\.webp', lambda m: m.group(0) if os.path.exists(os.path.join(SITE, 'images', 'news', 'yt-%s.webp' % m.group(1))) else (p['cover'] or 'images/icon-color.svg'), html)
    open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8', newline='\n').write(html)


def main():
    data = json.load(open(os.path.join(HERE, 'news.json'), encoding='utf-8'))
    order = sorted(data, key=lambda x: (x['date'], x['id']), reverse=True)
    by_id = {p['id']: p for p in data}
    by_slug = {p['slug']: p for p in data}
    # traducciones en ambos sentidos
    for p in data:
        if p.get('tr') and by_id.get(p['tr']):
            by_id[p['tr']]['tr'] = p['id']
    for f in os.listdir(OUT):          # evita paginas huerfanas si cambia algun slug
        if f.endswith('.html'):
            os.remove(os.path.join(OUT, f))
    for p in order:
        build(p, order, by_id, by_slug)
    # indice para el listado
    idx = []
    for p in order:
        idx.append({'i': p['id'], 's': p['slug'], 'l': p['lang'], 'c': p['cat'], 't': p['title'], 'd': p['date'], 'dl': p['dateLabel'],
                    'th': p['thumb'] or p['cover'] or '', 'x': p['excerpt'], 'm': p['min'], 'po': 1 if p.get('poster') else 0})
    js = ('/* generado por _build/build_news_pages.py: indice de noticias para el listado y los buscadores */\n'
          'window.ASOC_NEWS = ' + json.dumps(idx, ensure_ascii=False, separators=(',', ':')) + ';\n'
          'window.ASOC_NEWS_CATS = ' + json.dumps(CATNAMES, ensure_ascii=False) + ';\n')
    open(os.path.join(SITE, 'assets', 'news-data.js'), 'w', encoding='utf-8', newline='\n').write(js)
    print('paginas:', len(order), '| news-data.js:', len(js) // 1024, 'KB')


if __name__ == '__main__':
    main()
