# Efy Cinema · alcance corregido

La escena cinematográfica aprobada de EVIA con la mesa, los hologramas y las estrellas fugaces se mantiene exclusivamente en la portada. El propietario corrigió la extensión a todos los módulos y pidió una página de inicio breve.

El inicio contiene la portada, el carrusel de seguros y consulta de cobertura de cooperativas, y dos accesos a asistencia y contacto. Las secciones completas de Conócenos, Aliados, Reseñas, Contacto y Ayuda permanecen en sus páginas, accesibles desde el menú; no se reproducen dentro del inicio.

Conócenos y Reseñas vuelven a sus películas originales, con su composición propia y los bordes disueltos en el azul del módulo mediante `evia_media.py` y `evia-clips.js`. Se eliminaron las inserciones de la película de la mesa en las demás páginas. Three.js y el motor de estrellas sólo se cargan en `index.html`.

Los iconos de seguros del catálogo y el carrusel flotan sobre aros de luz azul y magenta. Se preservan las imágenes originales, los nombres y los destinos. Los logos de aseguradoras no se alteran. La hoja de ilustraciones del catálogo se carga sin demora: los 16 recortes comparten un único archivo de 86 KB. La animación LED dura siete segundos, se reduce en móvil y se desactiva con movimiento reducido.

La portada conserva el video original recortado mediante RGB + alfa, en un MP4 H.264 de 25 segundos con recorrido de ida y vuelta. El WebP transparente queda disponible como alternativa. Los efectos se detienen al salir de pantalla, ocultar la pestaña, abrir el chat o activar movimiento reducido/ahorro de datos. Los formularios, endpoints, socios y datos de contacto se conservan.

Generación: `python3 scripts/build_site.py`. Validación: pruebas de caché, navegación y cotización guiada, fuentes reales IBM Plex Sans, diseños móviles/de escritorio, restauración de las películas, carga de ilustraciones y pausa de la portada al bajar al carrusel. No se envían mensajes ni formularios reales durante las pruebas.
