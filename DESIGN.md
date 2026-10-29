# Efy Seguros: el próximo capítulo

## Recorrido de protección, 28 de octubre de 2026

La portada conserva el taller cinematográfico y al astronauta aprobado. Sus dos
acciones principales son Solicitar cotización y Necesito asistencia. El selector
de Auto, Salud, Vida, Hogar y Empresa usa iconos lineales azules sobre tarjetas
blancas, con un reflejo rosa al interactuar. Las superficies claras equilibran
la escena espacial sin añadir imágenes de clientes o personal no confirmadas.

Se mantienen grafito `#080e1d`, azul `#445ea5`, rosa `#f25c9d`, magenta `#ce005e`
y blanco `#f8f9fc`. La tipografía de la web completa es IBM Plex Sans local:
Regular 400 en información, Medium 500 en acciones y SemiBold 600 en títulos y
énfasis. Los archivos del logo y videos conservan su identidad gráfica original.

La animación acompaña acciones concretas: entrada breve al desplazar, elevación
de las tarjetas con puntero y avance entre los tres pasos de una consulta. El
movimiento reducido suprime estas transiciones. Los contenidos permanecen
visibles si una animación o JavaScript no se ejecutan. El área Clientes reúne
atención real; no presenta datos privados ni un portal autenticado ficticio.

El resto del documento registra las decisiones anteriores y la procedencia de
los medios que se siguen utilizando.

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

Por la referencia posterior del propietario, la navegación usa listas verticales
compactas bajo cada módulo. Las superficies blancas interiores tienen un acabado
de cristal suave, con transparencia reducida como alternativa del sistema.
La portada omite el rótulo rosa repetido de la marca y la frase sobre una nueva
experiencia desde Quito; el logo, la escena de EVIA y el mensaje principal siguen
siendo los elementos de identidad de ese encabezado.

Los desplegables usan azul Efy cristalizado, con texto blanco. La opción señalada,
enfocada o actual recibe el rosa Efy; la selección refleja también la categoría
activa del carrusel. Las superficies interiores conservan su cristal blanco.

## Tipografía corporativa de la web · 26 de octubre de 2026

La web completa usa IBM Plex Sans alojada localmente: SemiBold 600 para títulos,
leyendas de pasos y palabras importantes; Regular 400 para información y
beneficios; Medium 500 para botones y llamados a la acción. Los tres pesos se
precargan en las páginas compartidas. Se elimina Nunito de los estilos activos
del sitio y se aplica IBM Plex Sans también a la conversación de EVIA.
Los tamaños y el interlineado siguen siendo adaptables para móvil y escritorio.

## Ambiente holográfico, 28 de octubre de 2026

La portada mantiene la imagen original del taller como fondo fijo. EVIA no se
anima: se retira la reproducción de video en Inicio. Capas SVG separadas añaden
luz a las pantallas y recorridos luminosos sobre líneas existentes de la mesa.
Los ciclos continuos duran entre 10 y 15 segundos, sin parpadeos. Las capas se
alinean al recorte real de la imagen y se enmascaran fuera de la zona del texto.
En móvil se usan solo dos partículas; no se utiliza movimiento por cursor.
El movimiento o transparencia reducidos ocultan las capas, y la pestaña oculta,
el ahorro de datos o la escena fuera de pantalla pausan las animaciones.
El video de Conócenos y los medios originales se conservan.

## Entrada coordinada, 29 de octubre de 2026

La referencia de video aportada por el propietario muestra una composición que
se presenta por partes y revela nuevas secciones al desplazarse. La adaptación
usa títulos por líneas con 140 ms de desfase, texto y acciones escalonados, y
una revelación del taller de 1,4 segundos. EVIA conserva su imagen fija.
El módulo motion.js coordina también tarjetas y encabezados al entrar en la
ventana, con grupos breves y sin interceptar el desplazamiento nativo.
Las animaciones no bloquean controles ni mantienen el contenido oculto: sus
estilos finales son los originales. El teclado finaliza la animación de un
control enfocado y el movimiento reducido cancela las transiciones activas.
Se sustituye el efecto de aparición anterior para evitar animaciones duplicadas.

## Publicación de la propuesta premium, 29 de octubre de 2026

El propietario aprobó aplicar la maqueta premium y pidió ayuda con el logo. Se
conserva el logo blanco aprobado, con mayor tamaño y alineación en el encabezado,
a la espera de una elección explícita de otra variante. La portada adopta la
composición revisada: IBM Plex Sans 400/500/600, azul profundo, rosa, cristal,
espacios claros y las ilustraciones 3D originales para Auto, Salud, Vida, Hogar
y Empresa. El bucle aprobado de EVIA vuelve a reproducirse, con apertura suave
de la escena y efectos luminosos. Movimiento reducido, ahorro de datos, error
de video y salida de pantalla conservan una alternativa estática legible.

La navegación contiene siete módulos y desplegables por clic, accesibles con
teclado y en móvil. Los productos abren su ramo en Servicios; los enlaces a
consultas preseleccionan siniestro o reembolso. El chat y los endpoints existentes
se conservan. La plantilla pública no contiene controles ni mensajes de maqueta.

## Logo blanco y nueva propuesta de EVIA, 29 de octubre de 2026

El propietario aporta un JPG de marca blanca casi imperceptible sobre blanco y
confirma mantenerla blanca. La versión con transparencia está en
`public/assets/efy-logo-white-20261029.png`; conserva el conjunto de llama y
wordmark sin añadir el lema que no aparece en la nueva referencia. Se utiliza
en todos los encabezados, referencias de marca y favicon de las páginas actuales
y de las vistas anteriores. El nombre nuevo evita la caché de los archivos viejos.
El encuadre por CSS elimina el margen transparente de exportación en el encabezado.

Se generó una toma nueva de EVIA con Kling 3.0 Pro, distinta del taller anterior:
observatorio nocturno, mesa de cristal y hologramas de Auto, Hogar y Salud. Está
en revisión; no sustituye todavía el video principal, respetando la petición de
ver la propuesta antes de aplicarla. Ver `tooling/efy/EVIA-PREMIUM-20261029.md`.
