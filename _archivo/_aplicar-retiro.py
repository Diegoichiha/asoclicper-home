# -*- coding: utf-8 -*-
# Aplica el retiro de la Clinica Integrativa Maria del Pilar Diaz (17 -> 16 clinicas, 8 -> 7 departamentos).
# Script de uso unico: queda en _archivo/ como registro de exactamente que se cambio.
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def edit(rel, pairs):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    for old, new, n in pairs:
        c = s.count(old)
        if c != n:
            sys.exit('%s: se esperaban %d coincidencias y hay %d -> %r' % (rel, n, c, old[:70]))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', rel)


# ---- ficha de la clinica (assets/data.js): se quitan las 4 lineas del objeto
p = os.path.join(ROOT, 'assets/data.js')
lines = open(p, encoding='utf-8').read().split('\n')
i = next(k for k, l in enumerate(lines) if l.lstrip().startswith("{ id:'mariadelpilar'"))
assert lines[i + 3].rstrip().endswith('},') and lines[i + 4].lstrip().startswith("{ id:'alejandria'"), 'estructura inesperada en data.js'
del lines[i:i + 4]
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('ok assets/data.js (ficha retirada)')

edit('clinicas-asociadas.html', [
    ("    {city:'Santander de Quilichao', x:24.2, y:57.2, id:'mariadelpilar', n:1},\n", '', 1),
    ('Directorio de las 17 clínicas de cirugía plástica asociadas a ASOCLICPER en 8 departamentos', 'Directorio de las 16 clínicas de cirugía plástica asociadas a ASOCLICPER en 7 departamentos', 1),
    ('<span class="grad-text">17 clínicas</span>', '<span class="grad-text">16 clínicas</span>', 1),
    ('Contamos con 17 clínicas asociadas', 'Contamos con 16 clínicas asociadas', 1),
    ('<b data-count="17">0</b><span>Clínicas</span>', '<b data-count="16">0</b><span>Clínicas</span>', 1),
    ('<b data-count="8">0</b><span>Departamentos</span>', '<b data-count="7">0</b><span>Departamentos</span>', 1),
    ('<!-- CELEBRAMOS 17 CLINICAS', '<!-- CELEBRAMOS LAS CLINICAS', 1),
    ('¡Celebramos tener 17 clínicas asociadas!', '¡Celebramos tener 16 clínicas asociadas!', 1),
    ('aria-label="Video: 17 clínicas asociadas a ASOCLICPER"', 'aria-label="Video: clínicas asociadas a ASOCLICPER"', 1),
])

# ---- home: logo en el orbit + cifras
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()
chip = re.search(r'[ \t]*<div class="orbit-chip"><a href="https://www\.clinicacemein\.com/"[^\n]*mariadelpilar\.png[^\n]*</div>\n', s)
assert chip, 'no se encontro el logo en el orbit del home'
s = s.replace(chip.group(0), '', 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok index.html (logo retirado)')
edit('index.html', [
    ('<div class="num" data-count="17">0</div><div class="lbl">Clínicas Asociadas</div>', '<div class="num" data-count="16">0</div><div class="lbl">Clínicas Asociadas</div>', 1),
    ('<div class="num" data-count="8">0</div><div class="lbl">Departamentos del país</div>', '<div class="num" data-count="7">0</div><div class="lbl">Departamentos del país</div>', 1),
])

for rel in ('nosotros.html', 'opcion-megamenu.html'):
    edit(rel, [
        ('<b data-count="17">0</b><span>clínicas asociadas</span>', '<b data-count="16">0</b><span>clínicas asociadas</span>', 1),
        ('<div class="num" data-count="17">0</div><div class="lbl">Clínicas asociadas</div>', '<div class="num" data-count="16">0</div><div class="lbl">Clínicas asociadas</div>', 1),
        ('<div class="num" data-count="8">0</div><div class="lbl">Departamentos del país</div>', '<div class="num" data-count="7">0</div><div class="lbl">Departamentos del país</div>', 1),
    ])

edit('aliados.html', [
    ('reúne a 17 clínicas habilitadas en 8 departamentos', 'reúne a 16 clínicas habilitadas en 7 departamentos', 1),
    ('<div class="num" data-count="17">0</div><div class="lbl">Clínicas asociadas</div>', '<div class="num" data-count="16">0</div><div class="lbl">Clínicas asociadas</div>', 1),
])
edit('beneficios.html', [
    ('<b data-count="17">0</b><span>clínicas ya en la red</span>', '<b data-count="16">0</b><span>clínicas ya en la red</span>', 1),
])
edit('ser-asociado.html', [
    ('<b data-count="17">0</b><span>clínicas ya son parte</span>', '<b data-count="16">0</b><span>clínicas ya son parte</span>', 1),
    ('<b data-count="8">0</b><span>departamentos con presencia</span>', '<b data-count="7">0</b><span>departamentos con presencia</span>', 1),
    ('Ya son 17', 'Ya son 16', 1),
])
edit('seguridad-del-paciente.html', [
    ('<b data-count="17">0</b><span>clínicas habilitadas</span>', '<b data-count="16">0</b><span>clínicas habilitadas</span>', 1),
    ('Ver las 17 clínicas', 'Ver las 16 clínicas', 1),
])
edit('assets/megamenu.js', [
    ('Una red de 17 clínicas habilitadas y con cirujanos plásticos acreditados, en 8 departamentos del país.', 'Una red de 16 clínicas habilitadas y con cirujanos plásticos acreditados, en 7 departamentos del país.', 1),
])
edit('assets/nav.js', [('Directorio de las 17 clínicas', 'Directorio de las 16 clínicas', 1)])
edit('assets/site.js', [
    ('hacen parte de nuestra red de 17 asociadas', 'hacen parte de nuestra red de 16 asociadas', 1),
    ('entre las 17 clínicas asociadas', 'entre las 16 clínicas asociadas', 1),
])
edit('assets/site.css', [('/* bloque "Celebramos 17 clinicas": texto + video de la asociacion */', '/* bloque "Celebramos las clinicas asociadas": texto + video de la asociacion */', 1)])

# ---- el logo ya no se usa en el sitio (queda copia en _archivo/)
logo = os.path.join(ROOT, 'images/clinics/mariadelpilar.png')
if os.path.exists(logo):
    os.remove(logo)
    print('ok images/clinics/mariadelpilar.png eliminado')
