# Primera web Efy: Inicio, Servicios, Contáctanos, Conócenos, Socios estratégicos, Reseñas, Ayuda y Asistencia

Petición del propietario: comenzar la web pública con cuatro módulos. La vista de
trabajo está en `public/nueva/`; la portada de espera se mantiene en `public/index.html`
mientras se completan los datos oficiales. Esta versión no cambia el hosting.

## Dirección de diseño

Público: personas que quieren conocer Efy y entender cómo consultar por sus seguros.
Trabajo de la portada: presentar la marca y dirigir a la información o el contacto.

Tokens: grafito #080E1D, tinta secundaria #17233D, blanco #F8F9FC, lienzo #F7F8FB,
magenta de lectura #F25C9D, azul de acción #445EA5. Magenta #CE005E para acentos y botones con texto blanco (contraste 5,55:1).
Nunito Sans 700 para titulares; IBM Plex Sans 400 para texto y navegación.

Firma: EVIA trabajando en el universo digital de Efy, integrada en una portada
cinematográfica; el resto de la web ofrece superficies claras y lectura sencilla.
La composición de la escena aprobada se conserva y no hay botón de pausa.

```
Inicio:    navegación / mensaje + taller EVIA / accesos a información / cierre
Contáctanos: navegación / introducción / canales oficiales / preparar consulta
Conócenos:  navegación / identidad / EVIA / principios / acceso a contacto
Ayuda:     navegación / búsqueda / categorías / respuestas / reporte de errores
Servicios: navegación / introducción / catálogo / guía para comparar / consulta
Socios:    navegación / búsqueda / 26 logos y nombres / guía de póliza / asistencia
Reseñas:   navegación / presentación / opiniones de clientes / conocer Efy
Asistencia: hub / reportar-siniestro.html / consultas.html / lineas-asistencia.html
```

Revisión del 10 de octubre: se mantiene el azul, el grafito, el blanco y la escena
aprobada de EVIA. El rosa se desplaza hacia magenta con contraste suficiente.
La jerarquía distingue los ramos, las tres gestiones de Asistencia y los equipos
comercial/operativo. Los logos aprobados se conservan en sus colores originales.

## Contactos y datos pendientes

El propietario confirmó los cuatro teléfonos, los dos correos y la dirección de
Green Tower en Quito. `tooling/efy/contactos.json` contiene estos datos y el correo
para formularios. Contáctanos enlaza a llamadas, correo y búsqueda de la dirección
(es una búsqueda, no una ubicación geocodificada confirmada).
WhatsApp y horarios no están confirmados; no se inventan.

Ayuda incorpora `reportar-error.html`. Prepara un texto en el navegador, permite
copiarlo y abre un correo dirigido a `formularios@efyseguros.com` para que el cliente
lo envíe desde su aplicación. No almacena el reporte ni declara que se haya enviado.
Sin JavaScript queda disponible el enlace al correo. No hay un nuevo backend de errores.

EVIA responde con una base local de preguntas frecuentes, que incluye los contactos
confirmados; no consulta pólizas ni recibe reportes. El envío de siniestros continúa
por el backend existente a `siniestros@efyseguros.com`. Véase [SINIESTROS.md](SINIESTROS.md).

La consulta en línea de estados necesita el sistema externo, su API y verificación
de identidad. La reseñas necesitan una fuente real. El sitio completo se publica
como vista previa en `/nueva/`; la portada de espera permanece en `/`.

## Servicios

El propietario confirmó 14 apartados: Finanzas (expresamente distinto de Fianzas),
Accidentes personales, Vehículos, Transporte pesado, Motos, Asistencia médica,
Gastos médicos mayores, Asistencia de viaje, Vida, Vida indexada, Seguro dental,
Responsabilidad civil, Caución y Fidelidad privada.

`tooling/efy/servicios.json` contiene `id`, `name`, `group`, `description` y `details`.
Cuatro grupos facilitan la navegación: Movilidad, Salud, Vida y bienestar, Patrimonio
y actividad. Los detalles son orientación general y preguntas para la propuesta;
no prometen coberturas concretas, precios, resultados financieros ni productos de
una aseguradora. Finanzas necesita aún el detalle concreto del servicio del equipo.
Cada ramo abre una consulta por correo a Formularios con el asunto correspondiente.
La respuesta de EVIA se genera desde la misma lista. El generador valida los IDs,
textos y grupos, y escapa el contenido HTML.

## Socios estratégicos y Conócenos

El propietario pidió renombrar «Nosotros» a «Conócenos» y mostrar las aseguradoras
con las que trabaja Efy. El nombre se actualiza en todos los accesos, conservando
la URL `nosotros.html` para que los enlaces existentes sigan funcionando.

`socios.html` queda integrado en la navegación y la portada. Sus nombres proceden
de `tooling/efy/socios.json`: cada entrada contiene `id` único, `name` confirmado,
sitio oficial, logo local original, fuente del logo y fecha de revisión.
El propietario confirmó 26 socios de seguros, medicina prepagada y asistencia de
viaje. Todos aparecen con sus logos, buscador por nombre y enlace oficial.
EVIA usa la misma lista. Las líneas de Asistencia proceden de las fuentes oficiales
de cada proveedor; su etiqueta distingue el servicio y el enlace permite comprobarlo.
Fuentes y mantenimiento: [SOCIOS-Y-ASISTENCIA.md](SOCIOS-Y-ASISTENCIA.md).

La consulta de siniestros y reembolsos queda en preparación: falta el nombre y URL
del sistema donde se registran los estados, solicitado al propietario. Los campos
de cédula y placa están deshabilitados. No se hace una búsqueda ficticia ni se
publica información por un identificador sin verificar la identidad del cliente.

`asistencia.html` ofrece tres accesos separados. Los enlaces antiguos con fragmentos
llevan al acceso correspondiente del hub. `siniestros.html` conserva el formulario
operativo y el endpoint relativo. Sólo las páginas del reporte cargan su script;
`consultas.html` carga el selector de caso/cédula/placa sin enviar identificadores.
Cada socio permite desplegar sus teléfonos y fuentes oficiales; el directorio
completo tiene un buscador propio y ECU 911 separado.

## Reseñas de clientes

El propietario solicitó un apartado de reseñas. Se añade `resenas.html` con
accesos desde el menú, Inicio, el pie y EVIA. Se ha solicitado una fuente o las
reseñas reales. Mientras faltan, se muestra «Próximamente», sin nombres, citas,
estrellas, puntuaciones agregadas ni cantidades inventadas.

El contenido se carga de `tooling/efy/resenas.json`: `profile_url` es el enlace
opcional al perfil oficial de reseñas; `items` contiene las opiniones reales.
Cada opinión necesita `id` único, `author` (nombre público) y `text` (texto original).
Puede incluir `rating` (entero de 1 a 5), `date` (`YYYY-MM-DD`) y `source_url`
(enlace HTTPS a la reseña original). Los campos ausentes no se rellenan ni se
deducen. El texto se conserva, incluyendo saltos de línea, y se escapa para HTML.
Las URLs se validan, sin esquemas ejecutables ni credenciales. No hay descarga
automática de Google, widgets externos, formulario de recepción ni publicación
automática de comentarios. La fuente enlazada se abre con navegación normal.

Dirección: titular oscuro con el rosa de Efy, seguido de opiniones en superficies
claras. Las citas y sus autores llevan la jerarquía visual; se descartó una nota
global o una reseña destacada hasta tener datos reales. Se conservan las fuentes,
el logo blanco, EVIA y la escena aprobada de Inicio.

## Validación

Navegación entre las páginas y menú móvil, búsqueda y filtros de preguntas,
acordeones, borrador de consulta y copia, teclado, preferencias de movimiento,
recursos locales y vistas de 320/390/768/1440 px. No enviar mensajes reales en pruebas.

## Revisión de esta entrega

- Cuatro módulos comprobados a 320, 390, 768 y 1440 px sin desbordamiento.
- Menú móvil y navegación entre páginas; todas las imágenes cargan correctamente.
- Búsqueda con acentos, filtros, estado vacío y acordeones.
- Chat: preguntas conocidas, ubicación Quito, preguntas sobre pólizas particulares,
  respuesta desconocida, texto como texto, cierre con Escape y devolución del foco.
- Resumen de consulta, copia, aviso de que no se envía y limpieza tras editarlo.
- Movimiento reducido evita cargar el video; al desactivarlo se reproduce.
- Sin JavaScript, la navegación y los acordeones siguen funcionando.
- Publicación: se corrigió la exclusión de los `index.html` anidados; comprobado con
  una ejecución simulada de SFTP, sin conexión ni uso de credenciales reales.
- Servicios, Conócenos y Socios: siete páginas comprobadas a 320, 390, 768, 1101,
  1280 y 1440 px sin desbordamiento; menú con siete accesos, cierre con Escape,
  navegación sin JavaScript, preguntas nuevas en Ayuda y enlaces de EVIA a los
  módulos. Sin errores de JavaScript. Revisión visual de capturas móvil y escritorio.
- Reseñas: ocho páginas y el menú comprobados a 320, 390, 768, 1101, 1440 y
  1600 px sin desbordamiento ni errores de JavaScript. Acceso desde EVIA, búsqueda
  de la nueva pregunta en Ayuda, cierre con Escape y navegación sin JavaScript.
  Capturas revisadas en móvil y escritorio. Renderizado de una reseña de prueba
  comprobado en un directorio temporal: conserva el texto y sus saltos, escapa
  HTML y muestra sólo fecha y calificación suministradas. Las fuentes no HTTPS
  y las URLs con credenciales son rechazadas. No se publican datos de prueba.

- Asistencia y 26 socios: las ocho páginas pasan a 320, 390, 768, 1101, 1440 y
  1600 px sin desbordamientos o errores de JavaScript. Todos los logos decodifican;
  versiones blancas sobre superficie oscura. Búsquedas por nombre con acentos,
  estados vacíos, 38 líneas con fuentes, y directorios visibles sin JavaScript.
  Cédula y placa permanecen deshabilitadas; reembolsos y otros siniestros no ofrecen
  placa. Comprobado el recorrido del reporte hasta revisión y vuelta para corregir,
  sin enviar correos. La URL antigua sigue mostrando el módulo Asistencia. EVIA
  dirige a líneas y consulta pendiente sin inventar resultados.

## Verificación del 10 de octubre de 2026

13 páginas a 320, 390, 768, 1101, 1440 y 1600 px: sin desbordamientos ni errores
de JavaScript. Revisados menú/Escape, navegación del módulo padre, catálogo de
14 servicios, detalles nativos, 26 logos, 40 teléfonos/canales, filtros y vacíos,
selector de estado pendiente, revisión y retorno del reporte de siniestro sin
enviar un correo real, borrador de errores y destinos, contactos y enlaces EVIA.
Revisados los enlaces y anclas locales, las alternativas sin JavaScript y las
capturas de escritorio/móvil de Inicio, Servicios, Asistencia, Contactos, Ayuda
y Socios. Contrastes: blanco/magenta 5,55:1; magenta claro/grafito 6,23:1;
azul/lienzo 5,83:1. No cambió el backend de siniestros.
