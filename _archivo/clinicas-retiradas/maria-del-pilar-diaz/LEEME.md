# Clínica Integrativa María del Pilar Díaz (CEMEIN): retirada de la asociación

- **Clínica:** Clínica Integrativa María del Pilar Díaz, IPS Centro Especializado en Medicina Estética Integral S.A.S. (CEMEIN)
- **Ciudad:** Santander de Quilichao, Cauca (era la única clínica de la red en Cauca)
- **Sitio web:** https://www.clinicacemein.com/ · **Tel.:** +57 300 476 4142 · **Dirección:** Carrera 7 # 5-42
- **Retirada del sitio:** 3 de noviembre de 2026, porque la clínica salió de la asociación.
- **Estado del sitio justo antes del retiro:** commit `25797e0` (`git show 25797e0:<archivo>` recupera cualquier archivo tal como estaba).

## Qué se guardó aquí

| Archivo | Contenido |
|---|---|
| `ficha.json` | Todos los datos de la ficha (nombre, ciudad, descripción, dirección, teléfono, web) en JSON |
| `1-ficha-assets-data.js.txt` | El objeto exacto que estaba en `assets/data.js` |
| `2-pin-mapa-clinicas-asociadas.html.txt` | El pin del mapa de `clinicas-asociadas.html` |
| `3-logo-home-index.html.txt` | El logo del orbit de clínicas del home (`index.html`) |
| `logo/mariadelpilar.png` | El logo |
| `noticia/` | La nota «Uniendo estética y eficiencia…» (25 ene 2024), firmada por esta clínica: JSON limpio + imágenes |

## Qué se cambió en el sitio al retirarla

1. Se quitó la ficha de `assets/data.js` (de ahí salen el directorio, los filtros por departamento, el buscador «Verifica tu clínica», el carrusel de logos de Ser Asociado, etc.).
2. Se quitó el pin de Santander de Quilichao del mapa y el logo del home.
3. **Clínicas 17 → 16** en: home, nosotros, opcion-megamenu, aliados, beneficios, ser-asociado, seguridad-del-paciente, clinicas-asociadas (título, texto, estadística, meta descripción y «Celebramos tener…»), menú y mega menú, buscador de clínicas.
4. **Departamentos 8 → 7**, porque era la única clínica de Cauca (home, nosotros, opcion-megamenu, aliados, ser-asociado, clinicas-asociadas, mega menú).
5. Se retiró la nota firmada por la clínica (id 6743 en `_build/build_news_data.py`, constante `EXCLUDE`).

## Cómo reincorporarla

```bash
python -X utf8 _archivo/clinicas-retiradas/maria-del-pilar-diaz/_restaurar.py
```

Revierte los 5 puntos (probado: deja los archivos idénticos a como estaban antes del retiro). Después, a mano:

- Volver a revisar los **totales que calcula el cliente** (pacientes atendidos, quirófanos, cirujanos plásticos), que no dependen de este archivo.
- Revisar el video «Celebramos las clínicas» de `clinicas-asociadas.html`, que es un archivo de video.
- Si la clínica cambió datos (dirección, teléfono, web), editar `assets/data.js` después de restaurar.

`_aplicar-retiro.py` (en `_archivo/`) es el registro exacto de lo que se editó al retirarla.
