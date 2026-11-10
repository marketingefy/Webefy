# Recortes, legibilidad y accesos

El propietario reportó pérdida de partes de EVIA al moverse y solicitó ajustes de contenido, contraste, navegación, coberturas y un cohete de fondo. Añadió el slogan «Un universo de confianza.», ubicado encima del título de la portada.

## Diagnóstico y corrección de video

La comprobación `python tests/media/check_video_edges.py --old` reproduce un fallo concreto: la opacidad de un punto visible de la mochila en el video anterior es 0. La misma prueba con la nueva exportación devuelve 1. La revisión de 288 máscaras del inicio detectó 14 pérdidas de la zona de contacto del dedo en la versión anterior. El seguimiento corregido dejó un único fotograma, que se reparó usando los píxeles del fotograma nativo, no una pose interpolada.

Se volvió a seguir la silueta de EVIA con la mochila incluida, se cerraron agujeros internos del traje y se conservaron por separado las superficies de la mesa. Se revisó la vuelta completa con los mismos gestos y objetos. La portada conserva Full HD y 25 segundos de ida y vuelta. En Contacto se recortó el traje a partir de cada fotograma nativo, usando el seguimiento existente para excluir las burbujas originales: esto evita que un halo se incorpore a la silueta. La comparación de 45 poses del video final arroja una pérdida máxima de 0,058 % en los píxeles cálidos del traje, frente a más de 1 % en los ejemplos anteriores. Contacto mantiene 15 segundos de ida y vuelta y un respaldo PNG transparente.

La guía de diagnóstico se aplicó a este problema: reproducción determinista, causa, corrección y prueba antes/después. Los experimentos e intermedios están en `/workspace/output/efy-correcciones-20261110/`; no se publican.

## Cambios visibles

- Acceso destacado «Tu cooperativa / Tu cobertura» debajo de la escena inicial y antes del carrusel, conservando el acceso existente de Cooperativas.
- Resumen breve al final del inicio: dirección de Quito, WhatsApp comercial y operativo, correos y redes, con datos de la misma configuración de Contacto.
- Se retiran el marcador «01 Protección personal», los rótulos rosas «Asistencias»/«Ayuda» solicitados y «Ya soy cliente».
- Aliados conserva su buscador interno con el rótulo «Buscar aseguradora»; se retira ese acceso del desplegable. Conócenos mantiene trayectoria y reseñas en el menú, sin el acceso «Conoce a EVIA».
- Aviso de datos personales en azul claro cristalino; emergencias en magenta cristalino; búsqueda y contador de Ayuda con contraste oscuro; etiquetas y pasos de Cotización legibles. La guía «Un buen seguro empieza escuchándote» se muestra sin panel propio.
- Se retiran puntos al final de las líneas de títulos grandes, conservando la puntuación de párrafos, preguntas y el slogan.
- Los 16 motivos del catálogo se restauraron conservando su significado, paleta y orden, y se sirven en PNG sin una nueva compresión con pérdida.
- Un pequeño cohete azul, marfil y rosa recorre ocasionalmente el fondo. Se dibuja en la capa de estrellas, detrás del contenido; no intercepta controles. Respeta movimiento reducido, ahorro de datos, pestaña oculta y chat abierto.

## Validación

`python tests/media/check_video_edges.py`, pruebas de caché y sintaxis; recorrido guiado de 78 vistas; revisión en 390 y 1440 px de Inicio, Contacto, Asistencia, Coberturas, líneas de emergencia, Aliados, Ayuda, Cotización y Servicios. No se envían formularios ni mensajes reales. Los endpoints y los datos de contacto se conservan.
