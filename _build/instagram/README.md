# Feed de Instagram (Noticias)

La sección **«Síguenos en @asoclicper»** de `noticias.html` es un carrusel que lee `assets/instagram.json`.
El diseño ya está terminado; lo que falta es **cambiar la fuente del JSON** (hoy son 10 publicaciones de muestra tomadas de un pantallazo).

| Pieza | Archivo |
|---|---|
| Estilos | `assets/instagram.css` |
| Comportamiento (carga el JSON, flechas, arrastre, teclado, barra de progreso) | `assets/instagram.js` |
| Datos | `assets/instagram.json` (+ imágenes en `images/instagram/`) |
| Marcado | sección `#instagram` en `noticias.html` (`data-src` indica el JSON; `data-limit` cuántas publicaciones) |

Para usarlo en otra página (por ejemplo el home) basta copiar la sección, enlazar el CSS y el JS.

## Formato del JSON

```json
{
  "sample": false,
  "profile": { "username": "asoclicper", "url": "https://www.instagram.com/asoclicper/" },
  "updated": "2026-11-03T00:00:00Z",
  "posts": [
    { "id": "1789…", "type": "IMAGE | VIDEO | CAROUSEL_ALBUM",
      "image": "images/instagram/1789.webp", "permalink": "https://www.instagram.com/p/…/",
      "caption": "texto de la publicación", "timestamp": "2026-10-28T15:00:00+0000" }
  ]
}
```

Los campos equivalen a los de la API (`media_type`, `media_url` / `thumbnail_url`, `permalink`, `caption`, `timestamp`).
`data-src` también acepta una URL externa (por ejemplo la de un servicio de feed) mientras devuelva este formato.

## Opciones para conectar la cuenta real

**A. Servicio de feed (rápido).** Se conecta @asoclicper en el panel del servicio (Behold, por ejemplo) y se apunta `data-src` a su URL JSON (hay un paso de adaptación al formato de arriba). Cuesta una mensualidad si se quiere más de lo que da el plan gratis (en Behold: hasta 6 publicaciones, actualización cada 24 horas).

**B. API oficial de Meta + tarea programada (definitiva).** Sin costo recurrente y sin scripts de terceros.
1. La cuenta debe ser **Business o Creator** (ya lo es).
2. Crear una app en Meta for Developers con el producto *Instagram API with Instagram Login* y agregar la cuenta del cliente como probador/administrador; el cliente autoriza y se genera el **token de acceso de larga duración** (60 días).
3. Una tarea programada (GitHub Actions cada pocas horas, o un cron en el cPanel de Dongee) hace: `GET https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&limit=12`, descarga las imágenes (las URL de Instagram caducan) a `images/instagram/` y escribe `assets/instagram.json`.
4. La misma tarea **renueva el token** antes de que venza (`GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=…`; se puede renovar cuando tiene más de 24 horas y aún no ha vencido).
5. El token se guarda como secreto (nunca en el código de la página).

## Qué se necesita del cliente (opción B)

- Acceso a la cuenta de Facebook/Meta que administra @asoclicper, o que autorice la app desde su propio acceso.
- Decidir si se muestran también los reels y cuántas publicaciones (hoy 10).
- Saber dónde se publicará el sitio al final (GitHub Pages o Dongee) para elegir dónde corre la tarea.
