# Recortes, legibilidad y accesos

El propietario reportó pérdida de partes de EVIA al moverse y solicitó ajustes de contenido, contraste, navegación, coberturas y un cohete de fondo. Añadió el slogan «Un universo de confianza», ubicado encima del título de la portada.

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
- Se retiran puntos al final de las líneas de títulos grandes, conservando la puntuación de párrafos y preguntas.
- Los 16 motivos del catálogo se restauraron conservando su significado, paleta y orden, y se sirven en PNG sin una nueva compresión con pérdida.
- Un pequeño cohete azul, marfil y rosa recorre ocasionalmente el fondo. Se dibuja en la capa de estrellas, detrás del contenido; no intercepta controles. Respeta movimiento reducido, ahorro de datos, pestaña oculta y chat abierto.

## Validación

`python tests/media/check_video_edges.py`, pruebas de caché y sintaxis; recorrido guiado de 78 vistas; revisión en 390 y 1440 px de Inicio, Contacto, Asistencia, Coberturas, líneas de emergencia, Aliados, Ayuda, Cotización y Servicios. No se envían formularios ni mensajes reales. Los endpoints y los datos de contacto se conservan.


## Segunda revisión del inicio

El propietario señaló que la primera corrección todavía perdía casco, traje y mesa. La prueba anterior de un punto de mochila era insuficiente. La nueva comprobación `python tests/media/check_video_edges.py --previous` inspecciona siete superficies en los 600 fotogramas. Reproduce los huecos de mesa y también detecta fotogramas con pérdida del 100 % en áreas de casco y traje en la exportación `contorno`.

Se detectaron dos causas: la máscara estática de mesa retenía huecos abiertos en los reflejos y capturar el video con una máscara CSS recién sustituida podía exportar una rasterización parcial. Se separó la exportación de hologramas de la composición del film original. FFmpeg aplica la máscara completa al fotograma nativo antes de superponer los hologramas; ya no depende de capturar una máscara CSS en curso. Se conserva el traje original, se cierran visor y superficies interiores, se suaviza solo el borde y se elimina el anillo irregular que correspondía al reflejo del suelo de la habitación original. La mesa conserva su cristal, aro y pedestal completos. El nuevo film `integro` conserva Full HD y la secuencia de 600 fotogramas de ida y vuelta.

Se elimina también el punto del slogan, por solicitud expresa. Los intermedios y el MP4 normal para vista previa están en `/workspace/output/efy-contorno-seguro-20261110/`. Esta corrección queda preparada localmente; la publicación de la versión previa fue rechazada por revisión automática y no se elude ese bloqueo.


Validación de la segunda revisión: `python tests/media/check_video_edges.py` recorre los 600 fotogramas del MP4 final y registra 0 % de pérdida interior en cada una de las siete superficies. El recorrido guiado volvió a pasar sus 78 vistas, incluidas las fuentes reales IBM Plex y el slogan sin punto. Se inspeccionaron 12 poses del film original compuesto y cuatro poses del inicio renderizado en 390 y 1440 px. Las comprobaciones de Contacto siguen pasando. La comprobación de áreas de superficie y la composición fuera de la captura CSS previenen la repetición del fallo; la prueba anterior de un único píxel se conserva solo como complemento.
