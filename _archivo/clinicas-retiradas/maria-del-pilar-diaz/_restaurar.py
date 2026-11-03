# -*- coding: utf-8 -*-
"""
Reincorpora la Clinica Integrativa Maria del Pilar Diaz al sitio (inverso de _archivo/_aplicar-retiro.py):
  - ficha en assets/data.js, pin del mapa, logo del orbit del home y archivo del logo
  - cifras 16 -> 17 clinicas y 7 -> 8 departamentos (donde el retiro las cambio)
  - la noticia firmada por la clinica (id 6743): vuelve a news.json, imagenes y paginas

Uso (desde la raiz del sitio):   python -X utf8 _archivo/clinicas-retiradas/maria-del-pilar-diaz/_restaurar.py
Despues revisa los totales que el cliente calcula aparte (pacientes, quirofanos, cirujanos) y el video "Celebramos...".
"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def rd(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


def wr(rel, s):
    open(os.path.join(ROOT, rel), 'w', encoding='utf-8', newline='').write(s)


def edit(rel, pairs):
    s = rd(rel)
    for old, new, n in pairs:
        c = s.count(old)
        if c != n:
            sys.exit('%s: se esperaban %d coincidencias y hay %d -> %r (el archivo ya cambio; revisa a mano con el README)' % (rel, n, c, old[:70]))
        s = s.replace(old, new)
    wr(rel, s)
    print('ok', rel)


def snippet(name):
    return open(os.path.join(HERE, name), encoding='utf-8').read()


if "id:'mariadelpilar'" in rd('assets/data.js'):
    sys.exit('La clinica ya esta en assets/data.js: nada que restaurar.')

# 1) ficha en data.js (antes de Clinica Alejandria, su lugar original)
s = rd('assets/data.js')
ficha = snippet('1-ficha-assets-data.js.txt').rstrip('\n') + '\n'
anchor = "    { id:'alejandria'"
assert s.count(anchor) == 1
wr('assets/data.js', s.replace(anchor, ficha + anchor, 1))
print('ok assets/data.js')

# 2) pin del mapa (despues de Cali)
s = rd('clinicas-asociadas.html')
m = re.search(r"    \{city:'Cali'[^\n]*\n", s)
assert m, 'no se encontro el nodo de Cali'
wr('clinicas-asociadas.html', s.replace(m.group(0), m.group(0) + snippet('2-pin-mapa-clinicas-asociadas.html.txt').rstrip('\n') + '\n', 1))
print('ok clinicas-asociadas.html (pin)')

# 3) logo en el orbit del home (antes de Alejandria) + archivo del logo
s = rd('index.html')
m = re.search(r'[ \t]*<div class="orbit-chip"><a href="[^"]*"[^\n]*images/clinics/alejandria\.png[^\n]*\n', s)
assert m, 'no se encontro el logo de Alejandria en el home'
wr('index.html', s.replace(m.group(0), snippet('3-logo-home-index.html.txt').rstrip('\n') + '\n' + m.group(0), 1))
shutil.copy(os.path.join(HERE, 'logo', 'mariadelpilar.png'), os.path.join(ROOT, 'images', 'clinics', 'mariadelpilar.png'))
print('ok index.html + images/clinics/mariadelpilar.png')

# 4) cifras
edit('clinicas-asociadas.html', [
    ('Directorio de las 16 clínicas de cirugía plástica asociadas a ASOCLICPER en 7 departamentos', 'Directorio de las 17 clínicas de cirugía plástica asociadas a ASOCLICPER en 8 departamentos', 1),
    ('<span class="grad-text">16 clínicas</span>', '<span class="grad-text">17 clínicas</span>', 1),
    ('Contamos con 16 clínicas asociadas', 'Contamos con 17 clínicas asociadas', 1),
    ('<b data-count="16">0</b><span>Clínicas</span>', '<b data-count="17">0</b><span>Clínicas</span>', 1),
    ('<b data-count="7">0</b><span>Departamentos</span>', '<b data-count="8">0</b><span>Departamentos</span>', 1),
    ('<!-- CELEBRAMOS LAS CLINICAS', '<!-- CELEBRAMOS 17 CLINICAS', 1),
    ('¡Celebramos tener 16 clínicas asociadas!', '¡Celebramos tener 17 clínicas asociadas!', 1),
    ('aria-label="Video: clínicas asociadas a ASOCLICPER"', 'aria-label="Video: 17 clínicas asociadas a ASOCLICPER"', 1),
])
edit('index.html', [
    ('<div class="num" data-count="16">0</div><div class="lbl">Clínicas Asociadas</div>', '<div class="num" data-count="17">0</div><div class="lbl">Clínicas Asociadas</div>', 1),
    ('<div class="num" data-count="7">0</div><div class="lbl">Departamentos del país</div>', '<div class="num" data-count="8">0</div><div class="lbl">Departamentos del país</div>', 1),
])
for rel in ('nosotros.html', 'opcion-megamenu.html'):
    edit(rel, [
        ('<b data-count="16">0</b><span>clínicas asociadas</span>', '<b data-count="17">0</b><span>clínicas asociadas</span>', 1),
        ('<div class="num" data-count="16">0</div><div class="lbl">Clínicas asociadas</div>', '<div class="num" data-count="17">0</div><div class="lbl">Clínicas asociadas</div>', 1),
        ('<div class="num" data-count="7">0</div><div class="lbl">Departamentos del país</div>', '<div class="num" data-count="8">0</div><div class="lbl">Departamentos del país</div>', 1),
    ])
edit('aliados.html', [
    ('reúne a 16 clínicas habilitadas en 7 departamentos', 'reúne a 17 clínicas habilitadas en 8 departamentos', 1),
    ('<div class="num" data-count="16">0</div><div class="lbl">Clínicas asociadas</div>', '<div class="num" data-count="17">0</div><div class="lbl">Clínicas asociadas</div>', 1),
])
edit('beneficios.html', [('<b data-count="16">0</b><span>clínicas ya en la red</span>', '<b data-count="17">0</b><span>clínicas ya en la red</span>', 1)])
edit('ser-asociado.html', [
    ('<b data-count="16">0</b><span>clínicas ya son parte</span>', '<b data-count="17">0</b><span>clínicas ya son parte</span>', 1),
    ('<b data-count="7">0</b><span>departamentos con presencia</span>', '<b data-count="8">0</b><span>departamentos con presencia</span>', 1),
    ('Ya son 16', 'Ya son 17', 1),
])
edit('seguridad-del-paciente.html', [
    ('<b data-count="16">0</b><span>clínicas habilitadas</span>', '<b data-count="17">0</b><span>clínicas habilitadas</span>', 1),
    ('Ver las 16 clínicas', 'Ver las 17 clínicas', 1),
])
edit('assets/megamenu.js', [('Una red de 16 clínicas habilitadas y con cirujanos plásticos acreditados, en 7 departamentos del país.', 'Una red de 17 clínicas habilitadas y con cirujanos plásticos acreditados, en 8 departamentos del país.', 1)])
edit('assets/nav.js', [('Directorio de las 16 clínicas', 'Directorio de las 17 clínicas', 1)])
edit('assets/site.js', [
    ('hacen parte de nuestra red de 16 asociadas', 'hacen parte de nuestra red de 17 asociadas', 1),
    ('entre las 16 clínicas asociadas', 'entre las 17 clínicas asociadas', 1),
])
edit('assets/site.css', [('/* bloque "Celebramos las clinicas asociadas": texto + video de la asociacion */', '/* bloque "Celebramos 17 clinicas": texto + video de la asociacion */', 1)])

# 5) noticia firmada por la clinica (id 6743)
art = json.load(open(os.path.join(HERE, 'noticia', '6743-noticia.json'), encoding='utf-8'))
nj = os.path.join(ROOT, '_build', 'news.json')
data = json.load(open(nj, encoding='utf-8'))
if not any(x['id'] == art['id'] for x in data):
    data.append(art)
    data.sort(key=lambda x: (x['date'], x['id']), reverse=True)
    with open(nj, 'w', encoding='utf-8', newline='
') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
for f in os.listdir(os.path.join(HERE, 'noticia', 'imagenes')):
    shutil.copy(os.path.join(HERE, 'noticia', 'imagenes', f), os.path.join(ROOT, 'images', 'news', f))
edit('_build/build_news_data.py', [('EXCLUDE = {6743}', 'EXCLUDE = set()', 1)])
with open(os.path.join(ROOT, '_build', 'redirects.csv'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('# URL anterior (asoclicper.com) -> pagina nueva\n')
    for r in sorted(data, key=lambda x: x['id']):
        fh.write('/%s/,/noticias/%s.html\n' % (r['wp_slug'], r['slug']))
subprocess.run([sys.executable, '-X', 'utf8', '-I', os.path.join(ROOT, '_build', 'build_news_pages.py')], check=True)
print('\nListo: clinica y noticia reincorporadas. Revisa en el navegador y publica.')
