# Escena cinematográfica de EVIA — publicación autorizada

## Versión final con gestos y giros

El propietario pidió girar cada opción con la mano, dar movimiento al astronauta
y publicar las peticiones. Esta solicitud sustituye el estado de vista previa de
la primera propuesta que se conserva documentada más abajo.

- Modelo: Kling 3.0 Pro; 12 segundos, 16:9, sin sonido; coste estimado 18 créditos.
- Job completado: `fad32d27-f022-4fca-be80-07bd55efd512`.
- Referencia confirmada: `7e6b583a-95fa-4f77-ad13-a34774941249`.
- Fuente: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261029_181922_fad32d27-f022-4fca-be80-07bd55efd512.mp4
- Acciones: EVIA mueve brazo, muñeca, casco y torso, operando sucesivamente los
  hologramas de auto, hogar y salud, con giros verticales y luz de respuesta.
- Preparación: `scripts/prepare_premium_evia_loop.py`; H.264, 24 fps, sin audio,
  faststart, 1280×720 y 720×800. Ciclo de 11,5 s con disolución de medio segundo
  al regresar al inicio, sin invertir las acciones. Posters del primer fotograma.
- Destino: portada raíz y `/nueva/`, con archivos fechados `evia-premium-gestures`.
- El original se conserva fuera de `public/`, en
  `/workspace/output/efy-evia-gestos-20261029/evia-gestos-original.mp4`.

## Primera propuesta, conservada como antecedente

El propietario pidió una toma realmente nueva, con estética premium, y había
pedido ver las propuestas antes de aplicarlas. Se publica el nuevo logo ahora;
la nueva película no se enlaza como fondo de la portada hasta su revisión.

- Modelo: Kling 3.0 Pro; 8 segundos, 16:9, sin audio; preflight de 12 créditos.
- Job: `643447be-5af7-4104-8e7f-c65d3b79cda9` (completado).
- Referencia de imagen: `7e6b583a-95fa-4f77-ad13-a34774941249`.
- Fuente del resultado: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261029_173622_643447be-5af7-4104-8e7f-c65d3b79cda9.mp4
- Identidad: referencia original de EVIA de `tooling/efy/EVIA-reference.jpg`.
- Nuevo entorno: observatorio nocturno, mesa de cristal, hologramas de auto,
  hogar y salud, luz azul/magenta y espacio oscuro para el texto HTML.

Archivos de revisión en `/workspace/output/efy-brand-and-film-20261029/`:

- `evia-premium-original.mp4`: render original.
- `EVIA-premium-nuevo-bucle.mp4`: bucle de 14 s, 1280×720, ida y vuelta.
- `EVIA-premium-nuevo-movil.mp4`: bucle de 14 s, 720×800, con encuadre móvil.
- `nuevo-poster-desktop.jpg`, `nuevo-poster-mobile.jpg`: primeros fotogramas.
- `propuesta-nueva-1440.png`, `propuesta-nueva-390.png`: encaje en la portada.
- `index.html`: maqueta privada; requiere servir los assets existentes del sitio.

El bucle usa los primeros siete segundos y su secuencia inversa, para mantener
coincidencia en los extremos. Al aplicar la nueva toma, sustituir también el
poster y el encuadre móvil, y retirar las tarjetas holográficas HTML superpuestas
que estaban diseñadas para la composición anterior. Conservar encabezado,
tipografía, colores, movimiento reducido, ahorro de datos y pausa fuera de vista.

Se corrigió además una ruta relativa duplicada (`..../assets/`) de la plantilla
anterior que impedía reproducir el fondo en `/nueva/`; la prueba de navegador
ahora reproduce el video tanto en raíz como en esa copia compatible.
