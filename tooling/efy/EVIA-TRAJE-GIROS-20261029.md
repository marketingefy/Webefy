> Actualización: el propietario autorizó publicar todos los cambios pendientes, con una respuesta más animada de los iconos.

# EVIA: traje de referencia y tres giros equivalentes — revisión pendiente

El usuario señaló el video `5bc71bc6-e988-4351-a0ca-e847b9782f70` y pidió
corregir el traje según su nueva foto, además de dar a Hogar la misma respuesta
que a Vehículo y Salud. No se publica antes de revisar, conforme a su preferencia.

## Identidad y fuente

- Referencia principal: imagen del traje adjuntada por el usuario en esta petición.
- Nuevo fotograma: `/workspace/generated_images/exec-e417bc79-2772-48d8-b9b6-3dbb7bea79cc.png`.
- Conserva la placa rectangular con dos botones a la izquierda y emblema circular
  a la derecha, EVIA azul debajo, válvulas, arnés y bandas rosas, rodilleras y botas.
- Referencia confirmada en Higgsfield: `9a9b93a0-6a3e-4427-828b-9f37751553da`.
- Toma base: Kling 3.0 Pro, 12 segundos, sin sonido, estimación de 18 créditos;
  job `c2b3e971-5118-4595-95b3-01ae5ee81998`.
- Fuente: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261029_203520_c2b3e971-5118-4595-95b3-01ae5ee81998.mp4

## Corrección de la interacción

La toma base conserva el traje y anima la mano con la mesa vacía. Los tres
hologramas se componen después para controlar su respuesta de forma idéntica.
El atlas transparente original está en
`/workspace/generated_images/exec-c10bfd0e-1fcb-481c-98e0-b0719fb996ca.png`.
No se altera: sus tres figuras se encuadran mediante CSS.

`hero-holograms.html` usa la misma rotación de 360° sobre Y y la misma curva
suave de 2,5 s para los tres iconos. El marco y el nombre permanecen legibles.
Inicios sobre la toma original: 1,0 s, 4,2 s y 7,4 s. Se calibraron las posiciones
con los gestos del video, sin cubrir la placa y el nombre del traje.
`render_hero_holograms.cjs` produce 288 fotogramas a 1280×720 y compara las matrices
3D realmente renderizadas de los tres giros al 25%, 50% y 75% de su recorrido.
La comprobación pasó para Vehículo, Hogar y Salud.

`prepare_exact_suit_hero.py` forma el video y el bucle de 11,5 s con disolución
final de medio segundo. H.264, 24 fps, sin sonido, faststart; escritorio 1280×720,
móvil 720×800 con encuadre que conserva traje y tres iconos. Posters del primer
fotograma del bucle. Se mantienen movimiento reducido y pausa fuera de vista.

## Entrega y validación

Carpeta: `/workspace/output/efy-evia-traje-giro-20261029/`.
- `Evia-traje-y-giros-corregidos.mp4`: video final compuesto, no la toma vacía.
- `Evia-traje-y-giros-celular.mp4`: encuadre móvil.
- `Efy-vista-previa-interactiva.html`: incluye los cambios anteriores y este video.
- Imágenes de inicio en escritorio y celular.

78 vistas verificadas, video en raíz y `/nueva/`, fuentes, filtros y alternativas
estáticas. Artefacto autocontenido verificado sin peticiones externas. Tres giros
con matrices coincidentes. Dos formatos con 11,5 s y diferencia media entre
último y primer fotograma inferior a 0,6/255. Rama de revisión; sin push a main.
