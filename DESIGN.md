# EFY Seguros: el próximo capítulo

Brief vigente: una página informativa de espera con EVIA construyendo la futura
web en un taller digital espacial. El propietario autorizó este rediseño y la
integración de un video de Higgsfield con reproducción de ida y vuelta.

Composición: escena cinematográfica de fondo, mensaje a la izquierda en escritorio,
EVIA y los paneles de la web a la derecha. En móvil, escena superior con encuadre
propio y texto debajo. El encabezado conserva el logo oficial a color sobre blanco.
El contenido explica que el sitio está en preparación, sin fecha de lanzamiento,
porcentajes, testimonios ni funcionalidades no confirmadas.

Identidad: grafito `#080E1D`, blanco `#F8F9FC`, texto secundario `#B2BBCE` y rosa
claro `#FF91B2` para lectura sobre oscuro. La escena utiliza magenta y azul EFY.
Nunito Sans 700 e IBM Plex Sans 400 se alojan localmente, con sus licencias.
La página sigue siendo estática, sin dependencias de aplicaciones ni fuentes externas.

## Escena de EVIA

- Referencia de identidad: creación Higgsfield `d4fbf617-7ded-4148-9898-814969f9d830`.
- Imagen del taller: `53e25b36-b0be-4f2f-bc35-ee89614862de`, GPT Image 2.5.
- Animación: `096b68bc-0947-4801-bb36-4437c93cc576`, Kling 3.0 Pro, sin sonido.
- Fuente de video: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261009_180942_096b68bc-0947-4801-bb36-4437c93cc576.mp4

`scripts/prepare_evia_loop.py` une los fotogramas originales y su secuencia inversa
con FFmpeg, a 24 fps. Cada ciclo dura aproximadamente 12,08 segundos. El comienzo
y el final representan el mismo fotograma; los puntos de retorno también coinciden.
Se publica MP4/H.264 sin audio y con faststart: 1280×720 para escritorio y 720×800
con encuadre de EVIA para móvil. El original no se sube al sitio.

Las imágenes WebP se ven antes del video, sin JavaScript y si falla la reproducción.
El botón permite pausar y reanudar. La preferencia de movimiento reducido y el
ahorro de datos evitan la descarga automática del video. La reproducción se pausa
cuando la escena sale de pantalla o la pestaña queda oculta, respetando una pausa
manual. Se puede activar explícitamente aun con movimiento reducido.

## Comprobación

Revisar 320, 390, 768 y 1440 px, carga de recursos, teclado, controles, anclas,
movimiento reducido, ausencia de JavaScript y fallo del video. Comprobar los
fotogramas en los dos puntos de retorno y el peso de ambas versiones del bucle.
Los cambios de `public/` en `main` se publican mediante el workflow existente de
HostGator; no cambiar el hosting. La verificación HTTPS compara todos los recursos.
