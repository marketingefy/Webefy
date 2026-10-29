# Nueva propuesta cinematográfica de EVIA — en revisión

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
