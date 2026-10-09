# -*- coding: utf-8 -*-
"""
Trae los articulos de asoclicper.com (API REST de WordPress), los limpia (quita el maquetado de Elementor y
el HTML basura del editor), descarga y optimiza las imagenes a WebP y deja un JSON limpio por articulo.

Uso:  python -X utf8 build_news_data.py
Salida:  news.json  +  <site>/images/news/*.webp  +  <site>/media/news/*.mp3
"""
import json, re, os, sys, html as H, hashlib, io, urllib.request, urllib.parse, subprocess
from concurrent.futures import ThreadPoolExecutor
import lxml.html as LH
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
# el script vive en <sitio>/_build/ (o, en el entorno de trabajo, junto a la carpeta 'site')
SITE = os.path.abspath(os.path.join(HERE, '..')) if os.path.basename(HERE) == '_build' else os.path.abspath(os.path.join(HERE, '..', 'site'))
RAW = os.path.join(HERE, 'raw')   # cache de descargas (no se versiona)
OUT_IMG = os.path.join(SITE, 'images', 'news')
OUT_MEDIA = os.path.join(SITE, 'media', 'news')
os.makedirs(RAW, exist_ok=True); os.makedirs(OUT_IMG, exist_ok=True); os.makedirs(OUT_MEDIA, exist_ok=True)

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
API = 'https://asoclicper.com/wp-json/wp/v2/'

# ------------------------------------------------------------------ titulos limpios (los del WP vienen en Title Case / MAYUSCULAS)
TITLES = {
 8294: 'Medicina de Precisión en la Cirugía Plástica: el rol transformador del monitoreo digital postoperatorio',
 8114: 'Medidas de prevención y control del hematoma en procedimientos de abdominoplastia',
 8052: 'Clínica San Fernando S.A.: más de 70 años dedicados al bienestar',
 8001: 'Juntos avanzamos: formación para la excelencia',
 7994: 'Clínicas se destacan en excelencia y seguridad',
 7971: 'Workshop 2024: un encuentro exitoso sobre seguridad del paciente en cirugía plástica',
 7893: 'Colombia, «Número Uno» en turismo médico según las estadísticas mundiales de cirugía plástica estética',
 7119: 'La interdependencia en cirugía plástica como herramienta en la seguridad del paciente',
 6966: 'Reuniones administrativas: compromiso con la excelencia y seguridad',
 6961: 'Junta Directiva y jornada de referenciación en Clínica Bellatriz',
 6958: 'VII Asamblea General Ordinaria de Asociados 2024',
 6955: 'Impulsando el turismo de salud en el Valle del Cauca y Cali',
 6809: '¡Asoclicper en los medios!',
 6806: 'Excelencia e innovación en cirugía plástica: Clínica El Pinar a la vanguardia',
 6746: 'Clínica Gómez Arbeláez: excelencia quirúrgica y compromiso social en cirugía plástica y reconstructiva',
 6743: 'Uniendo estética y eficiencia: el impacto administrativo de Asoclicper en las clínicas de cirugía plástica asociadas',
 6612: '¡Celebramos el reconocimiento de IQ InterQuirófanos «Medellín Me Cuida con Amor»!',
 6609: 'Comprometidos con la humanización en la cirugía plástica: Asoclicper',
 6393: 'Excelencia en cirugía plástica: priorizando la seguridad del paciente',
 6381: 'Clínica El Pinar: ¡nuevo miembro de nuestra comunidad!',
 5431: 'Fortaleciendo las capacidades de nuestras clínicas para garantizar la seguridad del paciente',
 5426: 'Fortaleciendo nuestra red de clínicas asociadas a Asoclicper',
 5409: 'Gobierno corporativo',
 4821: 'Presentes en «Tardes del Sol»: concientizando sobre los riesgos de los biopolímeros',
 4742: 'Exitosa participación en el Curso Internacional de Cirugía Plástica Estética junto a nuestras clínicas asociadas',
 4656: 'El Dr. Álvaro Humberto Arana en el programa «La Tertulia» de RCN Radio 98.0',
 4554: 'Asoclicper celebra la aprobación de la Ley 2316 como avance en la seguridad y salud pública en la cirugía plástica estética',
 4551: 'Uniendo esfuerzos por la excelencia: resumen de la asistencia técnica con enfoque en la Resolución 3100',
 4547: 'Enriqueciendo la experiencia del paciente: exitoso taller de servicio',
 4543: 'Presentes en el Gran Foro «Colombianos en el Exterior» de La FM RCN Radio',
 4532: 'Editorial del Dr. Gustavo Adolfo Arboleda Palacio',
 4528: 'Lanzamiento de Asoclicper: 23 de febrero de 2022',
 4525: 'Momentos destacados: nuestra Asamblea General Ordinaria de Asociados 2022',
 4523: 'Celebramos obtención de certificación del Régimen Tributario Especial DIAN 2022',
 4518: 'Destacada participación de Asoclicper en el XXXVIII Congreso Nacional de la SCCP 2022',
 4514: 'Importante reunión entre Asoclicper y la ANDI',
 4492: 'La responsabilidad médica en las cirugías estéticas: ¿obligación de medio o de resultado?',
 4480: '¿Qué es la blefaroplastia?',
 4165: 'Lifting facial: el secreto para una apariencia juvenil y radiante',
 4161: 'Retiro de biopolímeros en glúteos: recuperando la salud y la estética',
 4052: 'Beneficios de la lipólisis láser no invasiva',
 4049: 'Bichectomía: ¿qué es?',
 4046: '¿Para qué sirve la cirugía capilar?',
 4040: 'Asoclicper, al ser la voz oficial, lidera el camino en el campo de la cirugía plástica en Colombia',
 3799: '¿A qué edad se puede hacer una rinoplastia?',
 3796: 'Lipotransferencia: riesgos, ¡conoce cuáles son!',
 3793: '¿Qué es una mamoplastia?',
 3769: 'Calidad y calidez, dos valores que proveen servicio en la atención de las cirugías plásticas',
 3439: '¿Es realmente segura la cirugía plástica en Colombia?',
 2958: 'Gobierno corporativo y planeación estratégica, un círculo virtuoso para las empresas',
 1109: 'El crecimiento no es por casualidad',
 # ---- ingles
 6029: 'Corporate governance',
 6027: 'Medical responsibility in aesthetic surgeries: means or results obligation?',
 6024: 'Enriching the patient experience: successful service workshop',
 6022: 'Joining forces for excellence: summary of technical assistance with a focus on Resolution 3100',
 6020: 'Present in the great forum “Colombians Abroad” of FM RCN Radio',
 6017: 'Strengthening our network of clinics associated with ASOCLICPER',
 6015: 'Strengthening the capabilities of our clinics to ensure patient safety',
 5837: 'At what age can a rhinoplasty be done?',
 5835: 'Strategic planning based on the “MEGA” strategy',
 5833: 'What is hair surgery for?',
 5831: 'Removing biopolymers in the buttocks: recovering your health and aesthetic appearance',
 5829: 'What is bichectomy?',
 5827: 'Benefits of non-invasive laser lipolysis',
 5824: 'Facelift: the secret for a radiant and youthful appearance',
 5822: 'We celebrate obtaining certification of the DIAN 2022 Special Tax Regime',
 5809: 'Present in the great forum “Colombians Abroad” of FM RCN Radio',
 5806: 'Present in “Afternoons of the Sun”: raising awareness about the risks of biopolymers',
 5800: 'Editorial by Dr. Gustavo Adolfo Arboleda Palacio',
 5797: 'ASOCLICPER launch – February 23, 2022',
 5793: 'Highlighted moments: our Ordinary General Assembly of Associates 2022',
 5791: 'ASOCLICPER celebrates the approval of Law 2316 as an advance in public safety and health in aesthetic plastic surgery',
 5788: 'Successful participation in the International Aesthetic Plastic Surgery Course with our member clinics',
 5777: 'Important meeting between ASOCLICPER and ANDI',
}

# traduccion EN -> ES (mismo contenido en el otro idioma)
PAIRS = {6029:5409, 6027:4492, 6024:4547, 6022:4551, 6020:4656, 6017:5426, 6015:5431, 5837:3799, 5833:4046, 5831:4161,
         5829:4049, 5827:4052, 5824:4165, 5822:4523, 5809:4543, 5806:4821, 5800:4532, 5797:4528, 5793:4525,
         5791:4554, 5788:4742, 5777:4514}

POSTERS = {4532, 5800, 5822, 4523}   # portadas que son graficos con texto: se muestran completas (contain)

CATS = {  # slug WP -> (clave, lang, nombre)
 'cirujanos-en-accion': ('accion', 'es', 'Cirujanos en Acción'),
 'enfocados-en-la-excelencia': ('excelencia', 'es', 'Enfocados en la Excelencia'),
 'eventos-y-oportunidades': ('eventos', 'es', 'Eventos y Oportunidades'),
 'interes-general': ('general', 'es', 'Interés General'),
 'surgeons-in-action': ('accion', 'en', 'Surgeons in Action'),
 'focused-on-excellence': ('excelencia', 'en', 'Focused on Excellence'),
 'events-and-opportunities': ('eventos', 'en', 'Events and Opportunities'),
 'general-interest': ('general', 'en', 'General Interest'),
}

MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

# enlaces internos del sitio viejo -> paginas del sitio nuevo
SITE_MAP = {
 'turismo-medico-cirugia-plastica': 'turismo-medico.html',
 'quienes-somos-cirujanos-plasticos-medellin': 'nosotros.html',
 'ser-asociado-clinica-de-cirugia-plastica': 'ser-asociado.html',
 'blog-cirujanos-plasticos-bogota': 'noticias.html',
 'noticias-clinica-estetica': 'noticias.html',
 'blog': 'noticias.html',
 'news': 'noticias.html',
}


def fetch(url, binary=True, tries=3):
    key = hashlib.md5(url.encode()).hexdigest()
    p = os.path.join(RAW, key + '.bin')
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return open(p, 'rb').read()
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            open(p, 'wb').write(data)
            return data
        except Exception as e:  # noqa
            last = e
    raise last


def strip_size(url):
    return re.sub(r'-\d{2,4}x\d{2,4}(?=\.[A-Za-z]+$)', '', url)


def img_key(url):
    b = os.path.basename(urllib.parse.urlparse(url).path)
    b = re.sub(r'-\d{2,4}x\d{2,4}(?=\.[A-Za-z]+$)', '', b)
    b = re.sub(r'-scaled(?=\.[A-Za-z]+$)', '', b)
    return os.path.splitext(b)[0].lower()


def get_image(url):
    """descarga (probando la version original sin sufijo de tamano) y devuelve PIL.Image"""
    cands = []
    s = strip_size(url)
    if s != url: cands.append(s)
    cands.append(url)
    for u in cands:
        try:
            data = fetch(u)
            im = Image.open(io.BytesIO(data)); im.load()
            try:
                im = ImageOps.exif_transpose(im)   # fotos de celular: respeta la orientacion EXIF
            except Exception:
                pass
            return im
        except Exception:
            continue
    return None


def save_webp(im, path, max_w, max_h=None, q=76):
    if im.mode in ('P', 'LA'):
        im = im.convert('RGBA')
    has_alpha = im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] < 250
    if im.mode == 'RGBA' and not has_alpha:
        im = im.convert('RGB')
    elif im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGB')
    w, h = im.size
    r = min(1.0, max_w / w, (max_h / h) if max_h else 1.0)
    if r < 1.0:
        im = im.resize((max(1, round(w * r)), max(1, round(h * r))), Image.LANCZOS)
    for qq in (q, q - 6, q - 12, q - 18):
        im.save(path, 'WEBP', quality=qq, method=6)
        if os.path.getsize(path) < 190 * 1024:
            break
    return im.size


# ------------------------------------------------------------------ limpieza de texto / HTML
INLINE_KEEP = {'strong': 'strong', 'b': 'strong', 'em': 'em', 'i': 'em', 'u': 'u', 's': 's', 'del': 's', 'sup': 'sup', 'sub': 'sub'}


def norm_ws(s):
    s = s.replace('\xa0', ' ').replace('​', '').replace('﻿', '')
    return re.sub(r'[ \t\r\n\f]+', ' ', s)


def fix_link(href, ctx):
    href = (href or '').strip()
    if not href or href.startswith('#') or href.lower().startswith('javascript'):
        return None
    m = re.match(r'^https?://(?:www\.)?asoclicper\.com/(.*)$', href, re.I)
    if m:
        path = m.group(1).split('#')[0].split('?')[0]
        if path.startswith('wp-content/'):
            return None
        slug = path.strip('/').split('/')[-1] if path.strip('/') else ''
        if not slug:
            return 'index.html'
        if slug in ctx['slugs']:
            return 'noticias/' + ctx['slugs'][slug] + '.html'
        if slug in SITE_MAP:
            return SITE_MAP[slug]
        return 'noticias.html' if False else None
    return href


def a_open(href):
    if re.match(r'^https?://', href, re.I) or href.startswith('mailto:') or href.startswith('tel:'):
        ext = href.startswith('http')
        return '<a href="%s"%s>' % (H.escape(href, quote=True), ' target="_blank" rel="noopener"' if ext else '')
    return '<a href="%s">' % H.escape(href, quote=True)


def inline_html(el, ctx):
    out = []

    def rec(n):
        if n.text: out.append(H.escape(n.text, quote=False))
        for c in n:
            if isinstance(c.tag, str):
                t = c.tag.lower()
                if t == 'br':
                    out.append('<br>')
                elif t == 'a':
                    href = fix_link(c.get('href'), ctx)
                    inner = inline_html(c, ctx)
                    if href and re.search(r'\w', re.sub(r'<[^>]+>', '', inner)):
                        out.append(a_open(href) + inner + '</a>')
                    else:
                        out.append(inner)
                elif t in INLINE_KEEP:
                    k = INLINE_KEEP[t]
                    out.append('<%s>' % k); rec(c); out.append('</%s>' % k)
                elif t in ('img', 'script', 'style', 'iframe', 'audio', 'figure'):
                    pass
                else:
                    rec(c)
            if c.tail: out.append(H.escape(c.tail, quote=False))

    rec(el)
    s = norm_ws(''.join(out))
    s = re.sub(r'<(strong|em|u|s|sup|sub)>\s*</\1>', ' ', s)
    s = re.sub(r'</(strong|em)>(\s*)<\1>', r'\2', s)       # une negritas contiguas
    s = re.sub(r'(?:\s*<br>\s*){3,}', '<br><br>', s)
    s = re.sub(r'^(?:\s|<br>)+|(?:\s|<br>)+$', '', s)
    s = re.sub(r' {2,}', ' ', s)
    s = re.sub(r',(?:\s|</strong>|</em>)*,', ',', s)
    return s.strip()


import unicodedata


def fold(s):
    s = unicodedata.normalize('NFKD', H.unescape(re.sub(r'<[^>]+>', ' ', s)))
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def same_title(a, b):
    a, b = fold(a), fold(b)
    return bool(a) and bool(b) and (a == b or a.startswith(b) or b.startswith(a))


def slugify(s, n=40):
    return fold(s).replace(' ', '-')[:n].strip('-') or 'seccion'


def text_of(html_s):
    return norm_ws(re.sub(r'<[^>]+>', '', H.unescape(html_s))).strip()


class Ctx(dict):
    pass


def yt_id(u):
    m = re.search(r'(?:embed/|v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})', u or '')
    return m.group(1) if m else None


INLINE_TAGS = {'a', 'strong', 'b', 'em', 'i', 'u', 's', 'span', 'br', 'sup', 'sub', 'small', 'mark', 'font', 'del'}
BLOCKISH = {'p', 'div', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figure', 'iframe', 'img', 'table', 'blockquote', 'audio', 'hr', 'section'}


def is_inline(ch):
    t = ch.tag.lower()
    if t not in INLINE_TAGS:
        return False
    for d in ch.iter():
        if d is ch or not isinstance(d.tag, str):
            continue
        if d.tag.lower() in BLOCKISH:
            return False
    return True


def inline_fragment(ch, ctx):
    """HTML en linea de un elemento (incluido el propio elemento, sin su cola)"""
    import copy
    holder = LH.Element('div')
    c2 = copy.deepcopy(ch)
    c2.tail = None
    holder.append(c2)
    tc = ch.text_content()
    lead = ' ' if tc[:1].isspace() else ''
    trail = ' ' if tc[-1:].isspace() else ''
    return lead + inline_html(holder, ctx) + trail


def parse_blocks(el, ctx, out):
    """recorre el arbol y agrega bloques limpios a out (lista de dicts).
    El texto suelto y los elementos en linea contiguos (a, strong, em...) se agrupan en un solo parrafo."""
    buf = []

    def flush():
        if buf:
            add_par(''.join(buf), ctx, out)
            del buf[:]

    if el.text:
        buf.append(H.escape(el.text, quote=False))
    for ch in el:
        if isinstance(ch.tag, str):
            if is_inline(ch):
                buf.append(inline_fragment(ch, ctx))
            else:
                flush()
                block(ch, ctx, out)
        if ch.tail:
            buf.append(H.escape(ch.tail, quote=False))
    flush()


def add_par(raw, ctx, out):
    s = norm_ws(raw).strip()
    if s and re.sub(r'<[^>]+>|\s', '', s):
        out.append({'t': 'p', 'h': s})


def imgs_in(el):
    return [i for i in el.iter('img')]


def img_url(i):
    for k in ('data-src', 'data-lazy-src', 'src'):
        v = i.get(k)
        if v and not v.startswith('data:'):
            return v
    return None


def bg_urls(el):
    res = []
    for e in el.iter():
        if not isinstance(e.tag, str): continue
        st = e.get('style') or ''
        m = re.search(r'url\(\s*[\'"]?([^\'")]+)', st)
        if m and 'background' in st:
            res.append(m.group(1))
    return res


def block(el, ctx, out):
    t = el.tag.lower()
    cls = (el.get('class') or '').split()
    if t in ('script', 'style', 'noscript', 'form', 'button', 'svg'):
        return
    if t == 'p':
        imgs = imgs_in(el)
        if imgs:
            for i in imgs:
                u = img_url(i)
                if u: out.append({'t': 'img', 'u': u, 'alt': i.get('alt') or ''})
        h = inline_html(el, ctx)
        if text_of(h):
            out.append({'t': 'p', 'h': h})
        return
    if t in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        h = inline_html(el, ctx)
        if text_of(h):
            lvl = 2 if t in ('h1', 'h2') else 3
            out.append({'t': 'h', 'l': lvl, 'h': re.sub(r'</?(strong|em|b|i)>', '', h)})
        return
    if t in ('ul', 'ol'):
        items = []
        for li in el.iter('li'):
            # solo li "hoja": los contenedores de listas anidadas se aplanan
            if any(isinstance(c.tag, str) and c.tag.lower() in ('ul', 'ol') for c in li):
                # texto propio del li contenedor (si lo hay)
                own = (li.text or '').strip()
                if own: items.append(H.escape(norm_ws(own), quote=False))
                continue
            h = inline_html(li, ctx)
            if text_of(h): items.append(h)
        if items:
            out.append({'t': 'list', 'o': t == 'ol', 'i': items})
        return
    if t == 'blockquote':
        sub = []
        parse_blocks(el, ctx, sub)
        h = ' '.join(b['h'] for b in sub if b['t'] == 'p')
        if text_of(h): out.append({'t': 'quote', 'h': h})
        return
    if t == 'hr':
        out.append({'t': 'hr'}); return
    if t == 'img':
        u = img_url(el)
        if u: out.append({'t': 'img', 'u': u, 'alt': el.get('alt') or ''})
        return
    if t == 'a':
        imgs = imgs_in(el)
        if imgs:
            for i in imgs:
                u = img_url(i)
                if u: out.append({'t': 'img', 'u': u, 'alt': i.get('alt') or ''})
            return
        h = inline_html(el, ctx)
        if text_of(h):
            out.append({'t': 'p', 'h': h})
        return
    if t == 'iframe':
        y = yt_id(el.get('src'))
        if y: out.append({'t': 'yt', 'id': y})
        return
    if t == 'audio':
        s = el.get('src')
        if not s:
            for so in el.iter('source'):
                s = so.get('src'); break
        if s: out.append({'t': 'audio', 'u': s})
        return
    if t == 'figure':
        if 'wp-block-gallery' in cls:
            urls = []
            for i in imgs_in(el):
                u = img_url(i)
                if u: urls.append((u, i.get('alt') or ''))
            if len(urls) == 1: out.append({'t': 'img', 'u': urls[0][0], 'alt': urls[0][1]})
            elif urls: out.append({'t': 'gallery', 'u': [x[0] for x in urls]})
            return
        if 'wp-block-embed' in cls or any(isinstance(c.tag, str) for c in el.iter('iframe')):
            for fr in el.iter('iframe'):
                y = yt_id(fr.get('src'))
                if y: out.append({'t': 'yt', 'id': y}); return
        imgs = imgs_in(el)
        if imgs:
            cap = ''
            for fc in el.iter('figcaption'):
                cap = inline_html(fc, ctx)
            for k, i in enumerate(imgs):
                u = img_url(i)
                if u: out.append({'t': 'img', 'u': u, 'alt': i.get('alt') or '', 'cap': cap if k == len(imgs) - 1 else ''})
            return
        parse_blocks(el, ctx, out)
        return
    # ---------- contenedores / widgets de Elementor
    widget = ''
    for c in cls:
        if c.startswith('elementor-widget-') and c != 'elementor-widget-container':
            widget = c[len('elementor-widget-'):]
    if widget in ('media-carousel', 'image-carousel', 'gallery', 'image-gallery'):
        urls = []
        for e in el.iter():
            if not isinstance(e.tag, str): continue
            ec = (e.get('class') or '')
            if 'swiper-slide-duplicate' in ec: continue
        for e in el.iter('div', 'img', 'a'):
            ec = e.get('class') or ''
            if e.tag == 'img':
                # se descartan las miniaturas de los duplicados del carrusel
                anc = e.getparent()
                dup = False
                while anc is not None:
                    if 'swiper-slide-duplicate' in (anc.get('class') or ''): dup = True; break
                    anc = anc.getparent()
                if dup: continue
                u = img_url(e)
                if u: urls.append(u)
            elif 'elementor-carousel-image' in ec or 'e-gallery-image' in ec:
                anc = e.getparent(); dup = False
                while anc is not None:
                    if 'swiper-slide-duplicate' in (anc.get('class') or ''): dup = True; break
                    anc = anc.getparent()
                if dup: continue
                m = re.search(r'url\(\s*[\'"]?([^\'")]+)', e.get('style') or '')
                if m: urls.append(m.group(1))
                elif e.get('data-thumbnail'): urls.append(e.get('data-thumbnail'))
            elif e.tag == 'a' and e.get('data-elementor-lightbox-slideshow') is not None:
                pass
        seen = []
        for u in urls:
            if img_key(u) not in [img_key(x) for x in seen]: seen.append(u)
        if len(seen) == 1: out.append({'t': 'img', 'u': seen[0], 'alt': ''})
        elif seen: out.append({'t': 'gallery', 'u': seen})
        return
    if widget == 'video':
        st = el.get('data-settings') or ''
        try:
            js = json.loads(H.unescape(st))
        except Exception:
            js = {}
        y = yt_id(js.get('youtube_url') or js.get('vimeo_url') or '')
        if y: out.append({'t': 'yt', 'id': y})
        return
    if widget == 'button':
        for a in el.iter('a'):
            href = fix_link(a.get('href'), ctx)
            txt = text_of(inline_html(a, ctx))
            if href and txt: out.append({'t': 'btn', 'u': href, 'h': txt})
        return
    if widget == 'heading':
        for hh in el.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'):
            h = inline_html(hh, ctx)
            if text_of(h): out.append({'t': 'h', 'l': 2, 'h': h})
            return
        return
    if widget in ('text-editor',):
        # contenido de editor: puede traer texto suelto
        for ch in el:
            pass
    parse_blocks(el, ctx, out)


PSEUDO_MAX = 96


def finalize_blocks(blocks, ctx, cover_key):
    """pasa el listado de bloques a HTML final; descarga y optimiza imagenes"""
    res = []
    toc = []
    used = set([cover_key]) if cover_key else set()
    n_img = [0]
    hcount = [0]

    def slugify(s):
        s = re.sub(r'[^a-z0-9]+', '-', H.unescape(re.sub(r'<[^>]+>', '', s)).lower().encode('ascii', 'ignore').decode()).strip('-')
        return s[:48] or 'seccion'

    def prep_img(u):
        k = img_key(u)
        if k in used: return None
        im = get_image(u)
        if im is None:
            print('   ! imagen no disponible:', u); return None
        used.add(k)
        n_img[0] += 1
        name = '%d-%02d.webp' % (ctx['id'], n_img[0])
        w, h = save_webp(im, os.path.join(OUT_IMG, name), 1200, 1500, q=76)
        return {'src': 'images/news/' + name, 'w': w, 'h': h}

    for b in blocks:
        t = b['t']
        if t == 'img':
            r = prep_img(b['u'])
            if r:
                r.update({'alt': b.get('alt') or '', 'cap': b.get('cap') or ''}); r['t'] = 'img'; res.append(r)
        elif t == 'gallery':
            items = []
            for u in b['u']:
                r = prep_img(u)
                if r: items.append(r)
            if len(items) == 1:
                items[0]['t'] = 'img'; items[0]['alt'] = ''; items[0]['cap'] = ''; res.append(items[0])
            elif items:
                res.append({'t': 'gallery', 'items': items})
        else:
            res.append(b)

    # ---------- afinado de estructura ----------
    MEDIA = ('img', 'gallery', 'yt', 'audio')
    # 1) lista de un solo item todo en negrita = parrafo; "<strong>Subtitulo<br></strong>texto" = subtitulo + parrafo
    fx = []
    for b in res:
        if b['t'] == 'list' and len(b['i']) == 1 and re.fullmatch(r'(?:<(?:strong|em)>)+.*(?:</(?:strong|em)>)+', b['i'][0].strip()):
            b = {'t': 'p', 'h': b['i'][0]}
        if b['t'] == 'p':
            h = b['h'].strip()
            m = re.match(r'^<strong>(.{3,140}?)(?:<br>)?</strong>(?:<br>)?\s*(.+)$', h, re.S)
            if m and '<strong>' not in m.group(1) and (h.startswith('<strong>' + m.group(1) + '<br>') or h.startswith('<strong>' + m.group(1) + '</strong><br>')):
                head, rest = m.group(1).strip(), m.group(2).strip()
                fx.append({'t': 'p', 'h': '<strong>' + head + '</strong>', 'bold': True})
                if rest: fx.append({'t': 'p', 'h': rest})
                continue
        fx.append(b)
    res = fx
    # 2) titulo repetido al inicio
    while res and res[0]['t'] in ('p', 'h') and same_title(text_of(res[0]['h']), ctx['title']):
        res.pop(0)
    # 3) firma al final: corridas de lineas cortas ("Por / Dr. ... / Clinica ...")
    k = len(res)
    def sign_line(x):
        if x['t'] not in ('p', 'h'):
            return False
        tx = text_of(x['h'])
        return len(tx) <= 110 and not (len(tx) > 60 and tx.endswith('.'))
    while k > 0 and sign_line(res[k - 1]):
        k -= 1
    tail = res[k:]
    if len(tail) >= 2 and k > 0 and any(x['t'] == 'p' and len(text_of(x['h'])) > 110 for x in res[max(0, k - 3):k]):
        res = res[:k] + [{'t': 'sign', 'i': [x['h'] for x in tail]}]
    # 4) linea corta toda en negrita seguida de contenido = subtitulo
    fx = []
    for i, b in enumerate(res):
        if b['t'] == 'p':
            txt = text_of(b['h'])
            m = re.fullmatch(r'<strong>(.*)</strong>', b['h'].strip())
            nxt = res[i + 1] if i + 1 < len(res) else None
            has_body = nxt is not None and ((nxt['t'] in MEDIA and nxt['t'] != 'yt') or nxt['t'] == 'list' or (nxt['t'] == 'p' and len(text_of(nxt['h'])) >= 70))
            if m and fx and len(txt) <= PSEUDO_MAX and not re.search(r'[.:,]$', txt) and '<br>' not in b['h'] and len(txt.split()) >= 2 and has_body:
                fx.append({'t': 'h', 'l': 3, 'h': m.group(1)})
                continue
        fx.append(b)
    res = fx
    # 5) encabezados al final sin contenido debajo -> parrafo en negrita
    for i in range(len(res) - 1, -1, -1):
        if res[i]['t'] == 'h' and not any(x['t'] != 'h' and x['t'] != 'hr' for x in res[i + 1:]):
            res[i] = {'t': 'p', 'h': '<strong>' + res[i]['h'] + '</strong>'}
        elif res[i]['t'] not in ('h', 'hr'):
            break
    # 6) etiqueta corta antes de un video = pie del video
    fx = []
    for b in res:
        if b['t'] == 'yt' and fx and fx[-1]['t'] == 'p' and len(text_of(fx[-1]['h'])) <= 80:
            b['label'] = text_of(fx.pop()['h'])
        fx.append(b)
    res = fx
    # 7) separadores: se quitan los pegados a medios, los repetidos y los del borde
    out = []
    for i, b in enumerate(res):
        if b['t'] == 'hr':
            prv = out[-1]['t'] if out else None
            nxt = res[i + 1]['t'] if i + 1 < len(res) else None
            if prv in (None, 'hr', 'audio', 'gallery', 'yt', 'img', 'sign') or nxt in (None, 'audio', 'gallery', 'yt', 'img', 'sign'):
                continue
        out.append(b)
    return out, n_img[0]


def to_html(blocks, ctx):
    L = ctx['L']
    html = []
    toc = []
    k = 0
    gk = 0
    for b in blocks:
        t = b['t']
        if t == 'p':
            html.append('<p>%s</p>' % b['h'])
        elif t == 'h':
            k += 1
            hid = 's%d-%s' % (k, slugify(b['h']))
            html.append('<h%d id="%s">%s</h%d>' % (b['l'], hid, b['h'], b['l']))
            toc.append({'id': hid, 'l': b['l'], 't': text_of(b['h'])})
        elif t == 'list':
            tag = 'ol' if b['o'] else 'ul'
            html.append('<%s>%s</%s>' % (tag, ''.join('<li>%s</li>' % i for i in b['i']), tag))
        elif t == 'quote':
            html.append('<blockquote><p>%s</p></blockquote>' % b['h'])
        elif t == 'hr':
            html.append('<hr>')
        elif t == 'img':
            alt = b.get('alt') or ''
            alt_attr = H.escape(alt or ctx['title'], quote=True)
            cap = ('<figcaption>%s</figcaption>' % b['cap']) if b.get('cap') else ''
            html.append('<figure class="pimg"><a href="%s" class="lb-i" data-lb="%s" aria-label="%s"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>%s</figure>' %
                        (b['src'], 'g0', L['zoom'], b['src'], b['w'], b['h'], alt_attr, cap))
        elif t == 'gallery':
            n = len(b['items'])
            gk += 1
            its = ''.join('<a href="%s" class="lb-i" data-lb="g%d" aria-label="%s"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></a>' %
                          (it['src'], gk, L['zoom'], it['src'], it['w'], it['h'], H.escape('%s (%d/%d)' % (ctx['title'], j + 1, n), quote=True)) for j, it in enumerate(b['items']))
            html.append('<div class="pgal n%d" data-n="%d">%s</div>' % (min(n, 9), n, its))
        elif t == 'yt':
            html.append('<figure class="pvid" data-yt="%s"><button type="button" class="pvid-btn" aria-label="%s"><img src="images/news/yt-%s.webp" alt="" width="1280" height="720" loading="lazy" decoding="async"><span class="pvid-play"></span><span class="pvid-cap">%s</span></button></figure>' %
                        (b['id'], H.escape(b.get('label') or L['play_video'], quote=True), b['id'], H.escape(b.get('label') or L['video_cap'], quote=False)))
        elif t == 'audio':
            html.append('<figure class="paud"><span class="paud-ico"></span><div class="paud-b"><b>%s</b><small>%s</small><audio controls preload="none" src="%s"></audio></div></figure>' %
                        (L['audio_t'], L['audio_s'], b['src']))
        elif t == 'sign':
            html.append('<div class="psign">%s</div>' % ''.join('<p>%s</p>' % x for x in b['i']))
        elif t == 'btn':
            html.append('<p class="pbtn"><a class="btn btn-primary" href="%s"%s>%s</a></p>' %
                        (H.escape(b['u'], quote=True), ' target="_blank" rel="noopener"' if b['u'].startswith('http') else '', b['h']))
    return '\n'.join(html), toc


def make_slugs(posts):
    """slug nuevo (corto, desde el titulo limpio) por id; conserva el slug original de WordPress para redirecciones"""
    out, used = {}, set()
    for p in sorted(posts, key=lambda x: (x['date'], x['id']), reverse=True):
        t = TITLES.get(p['id']) or H.unescape(p['title']['rendered'])
        sl = fold(t).replace(' ', '-')
        if len(sl) > 60:
            cut = sl[:61]
            sl = cut.rsplit('-', 1)[0] if '-' in cut else cut[:60]
            sl = sl[:60].strip('-')
        base = sl or 'noticia'
        k, n = base, 2
        while k in used:
            k = '%s-%d' % (base, n); n += 1
        used.add(k); out[p['id']] = k
    return out


def main():
    pj = os.path.join(HERE, 'posts.json')
    if not os.path.exists(pj):
        print('descargando articulos de asoclicper.com (API de WordPress)...')
        open(pj, 'wb').write(fetch(API + 'posts?per_page=100&_embed=1'))
    posts = json.load(open(pj, encoding='utf-8'))
    new_slug = make_slugs(posts)
    slugs = {p['slug']: new_slug[p['id']] for p in posts}   # slug WordPress -> slug nuevo
    # posts de WP traen a veces el slug con sufijo; el enlace interno usa el slug real
    LS = {
        'es': {'zoom': 'Ampliar imagen', 'play_video': 'Reproducir video', 'video_cap': 'Ver video', 'audio_t': 'Escucha la entrevista', 'audio_s': 'Audio del programa de radio'},
        'en': {'zoom': 'Enlarge image', 'play_video': 'Play video', 'video_cap': 'Watch video', 'audio_t': 'Listen to the interview', 'audio_s': 'Radio program audio'},
    }
    result = []
    yt_ids = set()
    mp3 = {}
    for p in sorted(posts, key=lambda x: (x['date'], x['id']), reverse=True):
        pid = p['id']
        terms = [c for c in p['_embedded']['wp:term'][0] if c['slug'] in CATS]
        if not terms:
            print('SIN CATEGORIA', pid); continue
        ck, lang, cname = CATS[terms[0]['slug']]
        title = TITLES.get(pid) or H.unescape(p['title']['rendered'])
        print(pid, lang, ck, title[:70])
        ctx = Ctx(id=pid, title=title, slugs=slugs, L=LS[lang])
        # --- portada
        fm = p['_embedded'].get('wp:featuredmedia', [{}])[0]
        cover_url = fm.get('source_url')
        if not cover_url and p.get('featured_media'):
            try:
                cover_url = json.loads(fetch(API + 'media/%d' % p['featured_media']).decode('utf-8')).get('source_url')
            except Exception:
                cover_url = None
        if not cover_url:
            try:
                pg = fetch(p['link']).decode('utf-8', 'ignore')
                m = re.search(r'<meta property="og:image" content="([^"]+)"', pg)
                cover_url = m.group(1) if m else None
            except Exception:
                cover_url = None
        cover = thumb = None; cw = chh = 0
        if cover_url:
            im = get_image(cover_url)
            if im is not None:
                cw, chh = save_webp(im, os.path.join(OUT_IMG, '%d-cover.webp' % pid), 1400, 1400, q=78)
                tw, th = save_webp(im.copy(), os.path.join(OUT_IMG, '%d-thumb.webp' % pid), 640, 800, q=72)
                cover = 'images/news/%d-cover.webp' % pid; thumb = 'images/news/%d-thumb.webp' % pid
        # --- cuerpo
        root = LH.fromstring('<div>' + p['content']['rendered'] + '</div>')
        for c in root.iter(LH.etree.Comment):
            pass
        etree = LH.etree
        for c in list(root.iter(etree.Comment)):
            par = c.getparent()
            if par is not None:
                tail = c.tail
                prev = c.getprevious()
                if tail:
                    if prev is not None: prev.tail = (prev.tail or '') + tail
                    else: par.text = (par.text or '') + tail
                par.remove(c)
        blocks = []
        parse_blocks(root, ctx, blocks)
        # si el primer bloque es la imagen de portada se descarta (se muestra arriba)
        blocks, n_img = finalize_blocks(blocks, ctx, img_key(cover_url) if cover_url else None)
        # video y audio
        for b in blocks:
            if b['t'] == 'yt': yt_ids.add(b['id'])
            if b['t'] == 'audio':
                src = b['u']
                key = hashlib.md5(src.encode()).hexdigest()[:8]
                b['src'] = 'media/news/entrevista-%s.mp3' % key
                mp3[src] = b['src']
        body, toc = to_html(blocks, ctx)
        # --- extracto
        ex = ''
        for b in blocks:
            if b['t'] == 'p':
                s = text_of(b['h'])
                if len(s) >= 70:
                    ex = s; break
        if not ex:
            for b in blocks:
                if b['t'] in ('p', 'list'):
                    ex = text_of(b['h'] if b['t'] == 'p' else ' '.join(b['i']))
                    if ex: break
        if not ex or len(ex) < 40:
            for b in blocks:
                if b['t'] == 'h' and len(text_of(b['h'])) > 25:
                    ex = text_of(b['h']); break
        if len(ex) > 170:
            ex = ex[:170].rsplit(' ', 1)[0].rstrip(',;:.') + '…'
        words = len(re.sub(r'<[^>]+>', ' ', body).split())
        d = p['date'][:10]
        y, mo, da = map(int, d.split('-'))
        date_label = ('%d de %s de %d' % (da, MESES[mo - 1], y)) if lang == 'es' else ('%s %d, %d' % (MONTHS[mo - 1], da, y))
        result.append({
            'id': pid, 'slug': new_slug[pid], 'wp_slug': p['slug'], 'lang': lang, 'cat': ck, 'catName': cname, 'title': title, 'date': d, 'dateLabel': date_label,
            'excerpt': ex, 'cover': cover, 'thumb': thumb, 'cw': cw, 'ch': chh, 'words': words, 'poster': pid in POSTERS,
            'min': max(1, round(words / 200)), 'body': body, 'toc': toc, 'imgs': n_img,
            'tr': PAIRS.get(pid) or next((k for k, v in PAIRS.items() if v == pid), None),
        })

    # --- miniaturas de YouTube
    def yt_thumb(i):
        path = os.path.join(OUT_IMG, 'yt-%s.webp' % i)
        if os.path.exists(path): return
        for q in ('maxresdefault', 'sddefault', 'hqdefault'):
            try:
                data = fetch('https://i.ytimg.com/vi/%s/%s.jpg' % (i, q))
                im = Image.open(io.BytesIO(data)); im.load()
                if im.size[0] < 400: continue
                # 16:9 limpio (hqdefault trae barras negras 4:3)
                w, h = im.size
                if abs(w / h - 16 / 9) > 0.05:
                    nh = round(w * 9 / 16); top = (h - nh) // 2; im = im.crop((0, top, w, top + nh))
                save_webp(im, path, 1280, None, q=78)
                return
            except Exception:
                continue
        print('   ! sin miniatura YouTube', i)
    for i in sorted(yt_ids): yt_thumb(i)

    # --- audio (se re-codifica a voz mono liviana)
    for src, dst in mp3.items():
        out = os.path.join(SITE, dst)
        if os.path.exists(out): continue
        raw = os.path.join(RAW, hashlib.md5(src.encode()).hexdigest() + '.mp3')
        if not os.path.exists(raw):
            print('descargando audio…', src)
            open(raw, 'wb').write(fetch(src))
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-vn', '-ac', '1', '-ar', '32000', '-b:a', '48k', out], check=True)
        print('   audio', dst, os.path.getsize(out) // 1024, 'KB')

    json.dump(result, open(os.path.join(HERE, 'news.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, 'redirects.csv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# URL anterior (asoclicper.com) -> pagina nueva\n')
        for r in sorted(result, key=lambda x: x['id']):
            fh.write('/%s/,/noticias/%s.html\n' % (r['wp_slug'], r['slug']))
    print('\nTOTAL', len(result), 'articulos', sum(1 for r in result if r['lang'] == 'es'), 'ES /', sum(1 for r in result if r['lang'] == 'en'), 'EN')


if __name__ == '__main__':
    main()
