# Calidad de medios, selector y Contacto

El propietario pidió mejorar el video de la portada, una animación transparente de EVIA para Contacto con teléfono y redes, estrellas fugaces y destellos en todas las páginas, mover el selector bajo «¿Qué necesitas hoy?» y usar iconos PNG de buena calidad. Autorizó aplicar el conjunto.

- La portada se volvió a componer desde el original Full HD, sin ampliar el video anterior de 720p. El MP4 contiene RGB 1920×1080 y una máscara alfa contigua (3840×1080 total), 600 fotogramas, 24 fps y 25 segundos en ida y vuelta. Se exportó un PNG transparente de respaldo de 1320×1080. El lienzo conserva hasta 2× densidad del dispositivo; ya no reduce la resolución de EVIA para compensar el costo del fondo.
- Se crearon seis iconos 3D originales de 1254×1254 en PNG RGBA: Auto, Salud, Vida, Hogar, Empresa y Cooperativas. Se conservan las ilustraciones originales del catálogo completo y los logos de aseguradoras. Los PNG nuevos no usan fondos blancos, recortes de atlas ni mezcla multiplicada.
- El selector de cinco necesidades aparece bajo el título y la frase de servicios. Cambia la descripción, desplaza el carrusel al seguro seleccionado y prepara un enlace de cotización con su ramo. La portada no cambia de frase al seleccionar un seguro.
- El nuevo titular es «Un seguro para lo que más importa.». El inicio continúa breve: portada, servicios/consulta de cobertura y accesos esenciales.
- Contacto reutiliza los gestos del video original de EVIA, con segmentación local para retirar el fondo y las burbujas originales. La máscara conserva el traje y el visor. El MP4 RGB+alfa de 720×960 por mitad dura 15 segundos y vuelve sobre su recorrido. El PNG de respaldo tiene alfa. Un reproductor WebGL pequeño, independiente de Three.js, muestra el recorte. El teléfono, Instagram y Facebook se animan como capas vectoriales con enlaces reales; no se envían mensajes automáticamente.
- Todas las páginas tienen destellos y estrellas fugaces, en azul y rosa. Fuera de la portada, una capa fija evita los textos, controles y paneles. Los efectos se detienen con movimiento reducido, pestaña oculta, chat abierto o ahorro de datos. Conócenos y Reseñas conservan sus videos propios.

Comprobaciones: sintaxis, caché, 78 vistas del recorrido guiado, fuentes IBM Plex Sans reales, PNG nativos con canal alfa, selector/ramo y reproducción de medios en 390/1440 px, estrellas en páginas internas y movimiento reducido. Las capturas y los intermedios de segmentación se guardan fuera de `public/`. No se envían datos de clientes ni correos reales durante las pruebas.

## Autorización y fondo compartido

Después de revisar las vistas previas, el propietario indicó: «Autorizo en todas las páginas pon el mismo fondo y destellos, estrella fugaz como en la primera». La publicación de la versión preparada queda autorizada con ese fondo en todo el sitio.

`cinema-background.js` reutiliza el material, iluminación y las ecuaciones del paisaje reflectante de la portada. El fondo se mantiene detrás de los contenidos de las páginas. En Inicio se activa al salir de la escena principal, para evitar dos motores simultáneos. Las estrellas globales siguen la misma regla; el cielo propio de la portada permanece activo dentro de esa escena. Los formularios conservan sus superficies y contraste, y los logos de aseguradoras no se recolorean. Con movimiento reducido o ahorro de datos se conserva el fondo azul estático y se detienen los efectos.
