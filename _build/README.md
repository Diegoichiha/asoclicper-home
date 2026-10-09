# Noticias: single post + importador

Los artículos de https://asoclicper.com se importan de la API REST de WordPress, se limpian y se publican como páginas
estáticas con una sola plantilla (single post).

| Pieza | Archivo |
|---|---|
| Plantilla del single post (HTML, textos ES/EN, JSON-LD, anterior/siguiente, relacionados, CTA) | `build_news_pages.py` |
| Estilos del single post | `assets/post.css` (tarjetas compartidas con el listado: `assets/news.css`) |
| Comportamiento (progreso de lectura, índice, compartir, visor de imágenes, video diferido, paralaje) | `assets/post.js` |
| Listado `noticias.html` | lee `assets/news-data.js` (índice generado) |
| Contenido limpio de los 74 artículos | `news.json` |
| Páginas generadas | `noticias/<slug>.html` (74) |
| Imágenes optimizadas (WebP) | `images/news/` |
| Audio de la entrevista (re-codificado) | `media/news/` |

## Flujo

```bash
# 1) traer y limpiar artículos (descarga imágenes a WebP; usa _build/raw como caché)
python -X utf8 _build/build_news_data.py
# 2) generar las páginas del single post y assets/news-data.js
python -X utf8 _build/build_news_pages.py
```

Requisitos: Python 3, `pillow`, `lxml` y `ffmpeg` (solo para el audio).

- Para cambiar el diseño del artículo se edita `build_news_pages.py` (marcado) + `assets/post.css`, y se vuelve a ejecutar el paso 2.
- Los títulos limpios (sentence case) y las parejas de traducción ES/EN están en `build_news_data.py` (`TITLES`, `PAIRS`).
- Las páginas usan `<base href="../">` porque viven en `noticias/`; por eso los enlaces del encabezado y el pie funcionan igual que en la raíz.
