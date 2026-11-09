# Efy Cinema · publicación aprobada

El propietario aprobó la vista previa con EVIA recortada, mesa y hologramas sobre el fondo azul reflectante, el título «Tu futuro, protegido.» y los acentos magenta. Autorizó publicar y añadió destellos y estrellas fugaces. Después pidió extender la misma presentación a cada página y módulo.

La portada y las introducciones de los módulos usan la película original de EVIA, segmentada localmente, con transparencia por RGB + máscara alfa en un MP4 H.264 de 25 segundos. El recorrido de ida y vuelta conserva las mismas poses en los extremos. La mesa, el traje y los tres hologramas se mantienen. No se generaron nuevos personajes ni se enviaron medios a otro servicio.

`cinema-scene.js` dibuja el fondo reflectante y el recorte con Three.js r180, distribuido localmente con su licencia MIT. `cinema-stars.js` añade destellos lentos y estrellas fugaces azules y rosas. La escena se detiene fuera de pantalla, en pestañas ocultas, al abrir el chat, con ahorro de datos o movimiento reducido. Cada componente se carga sólo cuando se aproxima al área visible. El WebP con alfa conserva a EVIA si el navegador no reproduce el video o no admite WebGL.

`cinema-hero.html` contiene la portada aprobada; `cinema_module()` en el generador enmarca las introducciones existentes. `evia_film()` comparte el recorte en los módulos y los resúmenes del inicio. Los formularios, endpoints, navegación, socios y datos de contacto existentes se conservan. Ninguna consulta real ni correo fue enviado para verificar el diseño.

La publicación se genera con `python3 scripts/build_site.py`. Los módulos publicados y `/nueva/` mantienen la misma versión de recursos para revalidar las páginas al navegar.

Validación: sintaxis JS/Python, pruebas de caché, recorrido guiado del navegador, revisión de portadas en 390/1440 px, reproducción del recorte, aparición de estrellas fugaces, navegación, parámetros de cotización y movimiento reducido. Las capturas se guardan fuera de `public/`.
