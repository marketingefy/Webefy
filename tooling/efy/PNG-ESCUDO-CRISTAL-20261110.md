# PNG completo, escudo y Ayuda cristalina

La revisión anterior comprobaba regiones interiores del video, pero no garantizaba un contorno limpio en todas las partes visibles. Se reemplaza la base del inicio por una nueva ilustración PNG RGBA generada a partir de la EVIA y la mesa aprobadas. Se mantienen opacos casco, visor, mochila, traje, guantes, botas, cristal, aro y pedestal. Los hologramas se componen aparte; el gesto de mano es sutil y la escena conserva sus 25 segundos de ida y vuelta. No se vuelve a estimar una máscara sobre cada fotograma del antiguo fondo urbano.

`tests/media/check_png_source.py` compara todos los fotogramas codificados con el interior de la silueta del PNG original. No se limita a puntos aislados ni a siete rectángulos. Comprueba más de 217 000 píxeles interiores por fotograma y la continuidad del bucle.

Servicios incorpora una animación propia de EVIA con un escudo azul y un candado blanco. La generación usa Higgsfield y una referencia del traje aprobado. Se descarta el primer resultado porque cortaba las botas; el segundo exige un encuadre completo con margen. La transparencia del resultado se extrae de un fondo de croma uniforme, se cierran solo huecos interiores y se conserva una versión PNG de respaldo del mismo fotograma. El film se reproduce con el visor de transparencia local, sin servicios externos en tiempo de ejecución.

Se elimina la tarjeta de Cooperativas del carrusel del inicio: permanece el acceso destacado superior. El carrusel queda con Auto, Salud, Vida, Hogar y Empresa. Se retira únicamente el rótulo «Socios de Coopartamos» de la guía; se mantienen la selección, la confirmación y el funcionamiento de la consulta.

En Ayuda, el buscador, el contador y el conjunto de preguntas pasan a cristal azul translúcido, con preguntas blancas y categorías/enlaces rosa magenta. Se conserva la tipografía IBM Plex y las estrellas del fondo.

Los intermedios y las vistas previas se conservan en `/workspace/output/efy-png-escudo-20261110/`.


## Validación final

- Inicio: 600 fotogramas contrastados contra 217 765 píxeles interiores del PNG por fotograma; pérdida máxima 0 %. El bucle vuelve a la misma silueta.
- Servicios: 240 fotogramas; margen mínimo de 51 píxeles hasta el borde del video y ningún agujero transparente interior. La exportación tiene 1620×1080 píxeles (RGB y alfa empaquetados), dura 10 segundos y conserva PNG de respaldo exacto.
- Ocho vistas de Inicio, Servicios, Ayuda y Coberturas en 390 y 1440 píxeles: sin errores de JavaScript ni desbordamiento. El rótulo solicitado y la tarjeta duplicada no aparecen. Las categorías de Ayuda se renderizan en rosa magenta y el panel aplica desenfoque de 20 píxeles.
- Se conservan logotipo, IBM Plex Sans, contactos, 26 aliados, formularios y sus destinatarios. No se realizan envíos de formularios reales.

Generación Higgsfield aceptada: `c68dcb34-035f-4e02-bc2f-719e4a7f3bc5`. Primera generación descartada por encuadre: `7bdcbe06-37d7-4e6b-9009-54252987bf6a`. El sitio usa solo archivos locales exportados; no carga los enlaces temporales del generador.

El recorrido guiado completo volvió a pasar sus 78 vistas, con IBM Plex Sans 400/500/600 real. Incluye reproducción y pausa de la nueva animación de Servicios en las rutas principal y /nueva/. Esta versión se entrega primero como vista previa, de acuerdo con la preferencia del propietario; no se ha publicado todavía.
