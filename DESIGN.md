# Efy Seguros: el próximo capítulo

Brief vigente: una página informativa de espera con EVIA construyendo la futura
web en un taller digital espacial. El propietario autorizó este rediseño y la
integración de un video de Higgsfield con reproducción de ida y vuelta.

Composición: escena cinematográfica de fondo, mensaje a la izquierda en escritorio,
EVIA y los paneles de la web a la derecha. En móvil, escena superior con encuadre
propio y texto debajo. El encabezado usa el nuevo logo aportado por el propietario el 9 de octubre,
con el fondo retirado y guardado como PNG con transparencia. El logo conserva
su composición, y se muestra completamente blanco mediante un filtro CSS de
color que conserva la transparencia. Su contenedor no añade fondo, sombra ni recuadro.
El contenido explica que el sitio está en preparación, sin fecha de lanzamiento,
porcentajes, testimonios ni funcionalidades no confirmadas.

Identidad: grafito `#080E1D`, blanco `#F8F9FC`, texto secundario `#B2BBCE` y magenta
de lectura `#F25C9D` sobre oscuro, actualizado por petición del propietario el 10 de octubre. La escena utiliza magenta y azul Efy.
Nunito Sans 700 e IBM Plex Sans 400 se alojan localmente, con sus licencias.
La página sigue siendo estática, sin dependencias de aplicaciones ni fuentes externas.

## Escena de EVIA

- Referencia de identidad vigente: foto aportada por el propietario, conservada en
  [EVIA-reference.jpg](tooling/efy/EVIA-reference.jpg). Visor negro liso, traje crema
  con detalles rosados, emblema de la llama y nombre EVIA en el pecho.
  Medio Higgsfield: `da0e9bd7-d662-47a4-90b0-62910e21f20e`.
- Imagen del taller: `53e25b36-b0be-4f2f-bc35-ee89614862de`, GPT Image 2.5.
- Animación original: `096b68bc-0947-4801-bb36-4437c93cc576`, Kling 3.0 Pro, sin sonido.
- Plano amplio restaurado por petición del propietario: mantiene la mesa, los
  paneles holográficos y a EVIA de cuerpo completo junto a ellos. El primer
  fotograma original se editó con la foto del personaje como referencia; medio
  Higgsfield de esa composición: `72d8b14f-8265-4267-bf90-be88a9814e55`.
- Sustitución vigente: `fddeb75d-d981-40db-89b8-53c04af1e038`, Higgsfield Genjutsu,
  usando el video original y la composición completa para conservar el plano amplio.
- Fuente de video: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261009_202817_fddeb75d-d981-40db-89b8-53c04af1e038.mp4

`scripts/prepare_evia_loop.py` une los fotogramas originales y su secuencia inversa
con FFmpeg, a 24 fps. Cada ciclo dura aproximadamente 12,08 segundos. El comienzo
y el final representan el mismo fotograma; los puntos de retorno también coinciden.
Se publica MP4/H.264 sin audio y con faststart: 1280×720 para escritorio y 720×800
con encuadre de EVIA para móvil. El original no se sube al sitio.

Las imágenes WebP proceden del primer fotograma del video final, con el mismo
encuadre en cada formato. Se ven antes del video, sin JavaScript y si falla la reproducción.
Por petición del propietario, la página no muestra botón de pausa ni reproducción.
La preferencia de movimiento reducido y el ahorro de datos evitan la descarga
automática del video. La reproducción se pausa cuando la escena sale de pantalla
o la pestaña queda oculta.

## Comprobación

Revisar 320, 390, 768 y 1440 px, carga de recursos, teclado, anclas,
movimiento reducido, ausencia de JavaScript y fallo del video. Comprobar los
fotogramas en los dos puntos de retorno y el peso de ambas versiones del bucle.
Los cambios de `public/` en `main` se publican mediante el workflow existente de
HostGator; no cambiar el hosting. La verificación HTTPS compara todos los recursos.

## Afinado de la web completa, 10 de octubre de 2026

La web completa del commit `94b683b` amplía esta dirección visual a sus 13 páginas
y al diálogo de cristal de EVIA. La mejora autorizada conserva las fuentes,
colores, videos, contactos, textos y flujos existentes. El encabezado se compacta
a 96 px y la tipografía usa `rem` equivalentes para respetar texto ampliado.
El chat mejora su lectura y sus objetivos táctiles; la página y el diálogo
respetan las zonas seguras del teléfono.

Las respuestas visuales usan `cubic-bezier(.23,1,.32,1)`: pulsación de 160 ms,
entrada del chat de 200 ms y mensajes de 180 ms. El movimiento reducido anula
las nuevas transiciones. La preferencia de transparencia reducida emplea el
color de superficie existente, sin sustituir el acabado de cristal habitual.
Los derivados WebP del logo y de los retratos preservan los originales como
alternativa. Ver [MEJORAS-UI.md](MEJORAS-UI.md) para las skills y comprobaciones.

## Interacción del catálogo y módulos, 13 de octubre de 2026

Las vistas previas del menú anticipan cada módulo en escritorio sin reemplazar
sus enlaces. El catálogo de 16 seguros se explora en un carrusel manual, con
ilustraciones en los colores de Efy y detalles nativos. Los servicios mantienen
su contenido confirmado. La consulta por cédula o placa prepara un correo al
equipo mientras el registro de estados no está conectado. Ver
[MEJORAS-INTERACCION.md](MEJORAS-INTERACCION.md) para comportamiento y pruebas.
