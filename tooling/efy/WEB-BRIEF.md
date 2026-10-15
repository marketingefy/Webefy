# Primera web Efy: Inicio, Servicios, Socios estratégicos, Conócenos, Asistencias, Reseñas, Contáctanos y Ayuda

Petición del propietario: comenzar la web pública con cuatro módulos. La vista de
trabajo está en `public/nueva/`; la portada de espera se mantiene en `public/index.html`
mientras se completan los datos oficiales. Esta versión no cambia el hosting.

## Dirección de diseño

Público: personas que quieren conocer Efy y entender cómo consultar por sus seguros.
Trabajo de la portada: presentar la marca y dirigir a la información o el contacto.

Tokens: grafito #080E1D, tinta secundaria #17233D, blanco #F8F9FC, lienzo #F7F8FB,
magenta de lectura #F25C9D, azul de acción #445EA5. Magenta #CE005E para acentos y botones con texto blanco (contraste 5,55:1).
IBM Plex Sans 600 para títulos, 500 para menú y 400 para texto. Los pesos nuevos
se alojan localmente, con la licencia IBM Plex ya incluida. Nunito Sans se conserva
para algunos datos y para la portada de espera.

Firma: EVIA trabajando en el universo digital de Efy, integrada en una portada
cinematográfica; el resto de la web ofrece superficies claras y lectura sencilla.
La composición de la escena aprobada se conserva y no hay botón de pausa.

```
Inicio:    navegación / mensaje + taller EVIA / accesos a información / cierre
Contáctanos: navegación / introducción / canales oficiales / preparar consulta
Conócenos:  navegación / identidad y EVIA / trayectoria / historia / WhatsApp
Ayuda:     navegación / búsqueda / categorías / respuestas / reporte de errores
Servicios: navegación / introducción / catálogo / guía para comparar / consulta
Socios:    navegación / búsqueda / 26 logos y nombres / guía de póliza / asistencia
Reseñas:   navegación / presentación / opiniones de clientes / conocer Efy
Asistencias: hub / reportar-siniestro.html / consultas.html / lineas-asistencia.html
```

Revisión del 10 de octubre: se mantiene el azul, el grafito, el blanco y la escena
aprobada de EVIA. El rosa se desplaza hacia magenta con contraste suficiente.
La jerarquía distingue los ramos, las tres gestiones de Asistencia y los equipos
comercial/operativo. Los logos aprobados se conservan en sus colores originales.

## Contactos y datos pendientes

El propietario confirmó los cuatro teléfonos y la dirección de Green Tower en Quito.
Solicitó sustituir el correo de información por `info@efyseguros.com` y dirigir
el contacto comercial a WhatsApp de 0967146828 y 0983538633. Estos datos están
en `tooling/efy/contactos.json`. Contáctanos conserva llamadas para el equipo
operativo, correo y búsqueda de la dirección (no una ubicación geocodificada
confirmada). Los horarios no están confirmados; no se inventan.

Ayuda incorpora `reportar-error.html`. Prepara un texto en el navegador, permite
copiarlo y abre un correo dirigido a `info@efyseguros.com` para que el cliente
lo envíe desde su aplicación. No almacena el reporte ni declara que se haya enviado.
Sin JavaScript queda disponible el enlace al correo. No hay un nuevo backend de errores.

EVIA responde con una base local de preguntas frecuentes, que incluye los contactos
confirmados; no consulta pólizas ni recibe reportes. El envío de siniestros continúa
por el backend existente a `siniestros@efyseguros.com`. Véase [SINIESTROS.md](SINIESTROS.md).

La consulta en línea de estados necesita el sistema externo, su API y verificación
de identidad. La reseñas necesitan una fuente real. El sitio completo se publica
como vista previa en `/nueva/`; la portada de espera permanece en `/`.

## Servicios

El propietario confirmó 16 apartados: Finanzas (expresamente distinto de Fianzas),
Accidentes personales, Vehículos, Transporte pesado, Motos, Asistencia médica,
Gastos médicos mayores, Asistencia de viaje, Vida, Vida indexada, Seguro dental,
Responsabilidad civil, Caución, Fidelidad privada, Seguro de hogar y Seguro para pymes.

`tooling/efy/servicios.json` contiene `id`, `name`, `group`, `description` y `details`.
Cuatro grupos facilitan la navegación: Movilidad, Salud, Vida y bienestar, Patrimonio
y actividad. Los detalles son orientación general y preguntas para la propuesta;
no prometen coberturas concretas, precios, resultados financieros ni productos de
una aseguradora. Finanzas necesita aún el detalle concreto del servicio del equipo.
Cada ramo abre WhatsApp comercial con un borrador específico. El visitante decide
enviarlo. La consulta de Contáctanos también ofrece WhatsApp con su resumen.
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
accesos desde el menú, Inicio y EVIA. Se ha solicitado una fuente o las
reseñas reales. La base `resenas.json` continúa vacía hasta recibirlas. A petición
posterior del propietario, la vista previa muestra diez ejemplos de diseño,
separados en `resenas-demo.json` y etiquetados como ficticios. No hay puntuaciones
agregadas ni afirmaciones de reseñas reales o verificadas.

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

## Ajuste corporativo del 10 de octubre

Menú e información de Inicio ordenados como pidió el propietario: Inicio, Servicios,
Socios estratégicos, Conócenos, Asistencias, Reseñas, Contáctanos y Ayuda. Las rutas
se conservan; las subpáginas mantienen activo el módulo correspondiente. El menú
se presenta en mayúsculas, con IBM Plex Sans 500 y un espaciado moderado. Los títulos
usan IBM Plex Sans 600. La escena, logo superior y paleta aprobada se conservan.

La oficina muestra una sola dirección, dividida en tres líneas para calle, edificio
y piso/oficina. El pie se reduce a copyright y lema: sin logo ni menú repetidos.

Verificación del ajuste: 13 páginas en siete anchos (320, 390, 768, 1101, 1280,
1440 y 1600 px), sin desbordamiento ni errores de JavaScript. Menú ordenado,
módulo activo, teclado/Escape y alternativa sin JavaScript correctos; sin logo
o navegación en el pie. Pesos 500/600 cargados, dirección única y capturas
revisadas de Inicio, Servicios y Contáctanos en móvil y escritorio.

## Conócenos y conversación de EVIA

La referencia del propietario se adapta a HTML responsive, con los 5 años de Efy
y los más de 15 años de experiencia que confirmó. `conocenos.json` conserva las
cifras, el lema «Experiencia que respalda. Cercanía que protege.», el subtítulo y
sus tres párrafos completos. Magenta y azul distinguen las dos cifras. La entrada
en pantalla anima los contadores una sola vez; sus etiquetas accesibles son
estáticas. Sin JavaScript o con movimiento reducido se mantienen los datos finales.

EVIA aparece sobre grafito, con luz magenta y azul y un panel holográfico. Se generó
en Higgsfield a partir del astronauta aprobado, sin voz ni sonido. Primer fotograma:
GPT Image 2.5, trabajo `e36fc8b0-7298-486c-9154-2bc1b3269530`. Video de 6 segundos:
Seedance 2.5, trabajo `1b112559-1f8d-4561-8d4b-3593f28e0d86`. El proceso local
`scripts/prepare_about_loop.py <video-original>` une avance y reversa y genera un
póster del primer fotograma. Resultado: H.264, 720×960, 12,08 segundos, 635472 bytes,
sin audio. El taller aprobado de Inicio se conserva.

`evia-about.js` carga el video cuando la figura está visible, lo pausa fuera de
pantalla y mantiene el póster si falla. Respeta movimiento reducido y ahorro de
datos. La fotografía y todo el texto permanecen disponibles sin JavaScript.

El chat tiene fondo blanco, cabecera fucsia y respuestas de EVIA en burbujas
fucsias con texto blanco. Los mensajes del visitante son claros, con texto oscuro.
Ofrece ambos WhatsApp comerciales en las respuestas de contacto, además
de un acceso persistente. Las preguntas sobre contacto con una aseguradora llevan
al directorio de asistencia. No envía mensajes automáticamente, no guarda la
conversación ni sustituye los canales de gestión de siniestros.

## Preguntas investigadas y reseñas de demostración

El 10 de octubre se consultaron fuentes oficiales de MAPFRE Ecuador, Chubb Ecuador
y Saludsa. `preguntas-frecuentes.json` documenta las fuentes, fecha de revisión,
21 preguntas nuevas, respuestas breves en redacción propia y variantes de consulta.
Las 37 preguntas quedan disponibles en Ayuda y en EVIA. Temas: función del bróker,
comparación, acompañamiento, costos, prima, vigencia, límites, beneficiarios,
modificaciones, pagos, carencias, preexistencias, copagos, red médica, reembolsos,
documentación, revisión de reclamos, conductores, territorio y cancelación.

Las respuestas describen conceptos y remiten a la póliza particular. No trasladan
los plazos, beneficios ni porcentajes de un producto a todas las aseguradoras.
El PDF histórico de educación financiera de MAPFRE se usa sólo para conceptos;
no se reproducen sus referencias legales, organismos ni plazos antiguos. Los
enlaces a fuentes aparecen en cada respuesta investigada y en Ayuda. El chat
ofrece tres grupos de sugerencias: Contratar, Mi póliza y Siniestros.

La demostración de Reseñas usa diez nombres abreviados, comentarios positivos y
estrellas ficticios. El rótulo «Opiniones de demostración» identifica su naturaleza.
No utiliza logo de Google, enlaces a reseñas inexistentes, fechas aparentes,
calificaciones agregadas ni metadatos de valoraciones. El carrusel responde a
botones, teclado y desplazamiento nativo; no avanza automáticamente. Sin
JavaScript quedan los diez ejemplos y el desplazamiento. Al añadir opiniones
reales a `resenas.json`, el generador retira automáticamente la demostración.

Verificación: 13 páginas en siete anchos, más revisión específica del carrusel
a 320, 390, 768, 1101, 1280, 1440 y 1600 px. Preguntas exactas, variantes, fuentes,
temas del chat, WhatsApp, correos, dirección única y pie reducido comprobados.
Video real sin audio, pausa fuera de pantalla, póster ante fallo y ausencia de
descarga con movimiento reducido. Menú, chat y carrusel por teclado; alternativas
sin JavaScript y enlaces/anclas locales válidos. No se envían mensajes de prueba
ni reportes al backend de producción.

## Ajuste del chat y nuevos servicios

A petición del propietario, el fucsia del chat se concentra en la cabecera y las
burbujas de EVIA; el fondo queda blanco. Las sugerencias, el campo de entrada y
los enlaces mantienen contraste y foco visible. Se retira el rótulo fucsia «EVIA»
bajo el astronauta de Conócenos y se conserva su video y el pie descriptivo.

Hogar y Pymes se añaden a Patrimonio y actividad, con detalles orientativos y
consultas por WhatsApp. La lista compartida actualiza también la respuesta del
chat y de Ayuda. El catálogo pasa de 14 a 16 apartados. Las condiciones concretas
se remiten a la propuesta y la póliza, sin coberturas ni precios inventados.

## Refinamiento de reseñas y actualización de la vista

Se retiran las etiquetas «Ejemplo ficticio» de las tarjetas y el cuadro de
demostración. Una única nota breve mantiene identificados los comentarios y las
estrellas como simulaciones para la vista previa. Bajo «Tu experiencia también
cuenta» aparece: «La confianza se construye en cada conversación. Tu opinión nos
ayuda a seguir acompañándote mejor.»

El acceso flotante a EVIA queda a 12 px del borde inferior en escritorio y 10 px
en móvil, además del margen seguro del dispositivo. Conserva el chat blanco,
cabecera y burbujas fucsia. Las 13 páginas mantienen el pie reducido sin logo ni
navegación repetida. Los HTML de `/nueva/` revalidan su caché mediante `.htaccess`;
la publicación verifica las cabeceras y el contenido recibido por HTTPS.

La conexión de las cotizaciones al CRM requiere acceso a su API o repo y
su formulario de recepción. Hasta contar con esa información, los enlaces
comerciales siguen preparando consultas por WhatsApp y no afirman registrarlas
en un CRM. La consulta de estados de siniestros sigue siendo una integración
independiente pendiente del sistema que gestiona los casos.

Verificación de este ajuste: 13 pies sin duplicaciones; carrusel, menú y chat sin
errores de navegador; anchos de 320, 390, 768, 1101 y 1440 px sin desbordamiento;
posición inferior del botón, nueva introducción y nota de simulación comprobadas.

## Redes sociales y chat con acento sutil

El propietario confirma Instagram `@efyseguros` y el enlace de Facebook de la
marca. Se añaden dos enlaces en Contáctanos con iconos vectoriales reconocibles,
nombre de la plataforma y perfil; abren una nueva pestaña con `noopener noreferrer`.
Instagram utiliza la URL del perfil sin parámetros de seguimiento; Facebook
conserva el enlace compartido por el propietario. No se cargan widgets ni scripts
de las redes sociales.

El acento del chat pasa a `#914665` en cabecera y botón flotante. Las burbujas de
EVIA usan `#f8eef3` con texto oscuro, enlaces `#823b5c` y borde suave; el fondo sigue
blanco. Los botones comerciales y colores de la página conservan su identidad.

CRM confirmado: `https://app.latamyanez.com/login`, cuya página pública se titula
«EFY Analyzer IA · Efy Seguros» y muestra un inicio de sesión. La inspección se
limita a HTML y scripts públicos, sin iniciar sesión ni enviar solicitudes. Falta
la documentación de recepción de cotizaciones o acceso a la repo del CRM; el
enlace de login por sí solo no determina los campos ni la autenticación de la API.

Verificación: perfiles y sus iconos visibles, enlaces y protección de nueva
pestaña comprobados; Contáctanos sin desbordamiento a 320, 390, 768, 1101 y
1440 px. Chat dentro del área móvil, cierre con Escape y acceso a los dos
WhatsApp comerciales correctos. Contraste medido: 6,43:1 en la cabecera,
16,97:1 en el texto de los mensajes y 6,78:1 en el rótulo de EVIA.

## Ubicación inferior de EVIA y rótulo breve de reseñas

El propietario confirma que el botón de EVIA debe permanecer fijo en la esquina
inferior derecha de la pantalla mientras navega, tanto en móvil como en escritorio.
El margen inferior pasa a 8 px, o al área segura del dispositivo si es mayor;
el margen derecho es 16 px en escritorio y 12 px en móvil, también respetando el
área segura. Se conserva el tono sobrio del chat y su apertura accesible.

Se elimina el párrafo «Comentarios y estrellas simulados para esta vista previa».
El encabezado del carrusel utiliza «Opiniones de demostración», una identificación
breve para conservar la transparencia de los diez comentarios creados para el
diseño. Las opiniones reales siguen pendientes de recibir y reemplazarán la
demostración cuando se incorporen al catálogo.

La revisión visual utiliza capturas del área visible del navegador. Una captura
de toda la página puede colocar un elemento fijo a mitad de la imagen larga,
aunque el botón esté en el borde inferior de la pantalla al navegar.

Verificación de este ajuste: cinco anchos (320, 390, 768, 1101 y 1440 px), al
inicio, a mitad y al final de la página. El botón permanece a 8 px del borde
inferior en los 15 escenarios, sin desbordamiento horizontal. Apertura, cierre
con Escape y retorno de foco comprobados; el carrusel conserva sus diez ejemplos
y su navegación. Capturas de escritorio y móvil realizadas sin extender la imagen
a toda la página.

## Corrección comercial y rosa corporativo dentro del chat

El propietario corrige el segundo número comercial a `0983538633`, con WhatsApp
`https://wa.me/593983538633`. Se actualizan contactos, datos compartidos y la
respuesta de EVIA; esta última se genera desde los números de `contactos.json`
para evitar discrepancias entre el texto y los enlaces.

Al abrir el chat, la cabecera utiliza el rosa corporativo `#f25c9d` y las burbujas
un tinte rosa `#fce8f1`. Los textos, el cierre y el foco de la cabecera son oscuros
para mantener legibilidad. El botón flotante exterior conserva su acento sobrio,
aspecto y posición fija en la esquina inferior derecha. Servicios mantiene las
tarjetas «Seguro de hogar» y «Seguro para pymes» con sus consultas comerciales.

Verificación: número mostrado, respuesta de EVIA y enlace de WhatsApp corregidos,
sin restos del número anterior en el sitio generado. Contraste de cabecera y
cierre 6,23:1, subtítulo 4,59:1 y mensajes 16,46:1. Color exterior conservado.
Hogar y Pymes visibles en el catálogo en anchos de 320, 390, 768 y 1440 px sin
desbordamiento; consultas por WhatsApp conservadas. Sin errores de navegador.

## Chat con opciones de atención y revisión de todos los módulos

El propietario pide una conversación similar a WhatsApp Business y confirma en
su captura el color del botón «Conócenos»: fucsia `#ce005e`. La cabecera del chat
usa ese fucsia con texto blanco. Las burbujas de EVIA mantienen un tinte rosa
suave; las del visitante quedan alineadas a la derecha. El fondo blanco conserva
un patrón tenue, y cada mensaje muestra la hora local real del navegador. No se
añaden estados de lectura, confirmaciones de entrega ni presencia de un agente.

El menú inicial tiene cuatro opciones: cotización, dudas de póliza, siniestros y
asistencia, y hablar con un asesor. Los submenús enlazan con los seguros, reportes,
consulta de casos y líneas oficiales existentes; las respuestas de póliza y
reembolso conservan sus fuentes. «Ver opciones» permite volver al menú dentro de
la conversación. Se conserva el texto libre y el acceso a los dos WhatsApp
comerciales. Abrir el chat enfoca su cierre, evitando desplegar el teclado móvil
antes de que el visitante elija una opción.

El botón exterior usa el mismo fucsia con 84 % de opacidad de fondo y desenfoque
del fondo; avatar y texto no pierden opacidad. Permanece fijo abajo a la derecha,
incluidas las páginas de Asistencia donde antes estaba oculto. Texto blanco con
contraste mínimo calculado de 4,72:1 sobre blanco y superior sobre fondos oscuros.

Los 13 HTML comparten versión, tipografía, contactos y chat. El menú y los enlaces
internos conservan `SITE_VERSION` en su URL; el chat lo aplica también a sus rutas
dinámicas. Los enlaces externos, WhatsApp, correo y fuentes oficiales conservan
sus destinos. La revalidación de HTML sigue activa.

La conexión de cotizaciones al CRM y la consulta automática de estados siguen
requiriendo acceso a sus sistemas. El menú no afirma registrar solicitudes ni
consultar casos; los formularios y las páginas mantienen su comportamiento real.

Revisión de esta versión: 13 páginas en móvil y escritorio (26 vistas), sin
errores de navegador ni desbordamiento. Orden de módulos, versión de los enlaces,
chat disponible, posición inferior, fucsia y foco comprobados en todas ellas.
181 enlaces y anclas locales válidos. Se verifican 16 servicios con Hogar/Pymes,
26 logos que cargan correctamente, 40 canales oficiales de asistencia, historia y
cifras confirmadas, diez opiniones de demostración, dirección única, dos redes,
correos y número comercial corregido. Menús de cotización, póliza, asistencia y
asesores comprobados; preguntas libres y fuentes conservadas. El chat cabe también
en pantallas de 320 × 568 y 768 × 600 px. No se envían mensajes, cotizaciones ni
reportes de prueba a sistemas reales.

## Tipografía del chat y distintivo de marca

La conversación usa las fuentes nativas de cada plataforma (sistema Apple,
Segoe UI o Roboto), con alternativas locales, para una lectura similar a la de
WhatsApp. Se aplica solo al diálogo, incluidos el nombre, los mensajes, el menú
y el campo de escritura; la página conserva IBM Plex Sans.

El nombre EVIA lleva un círculo azul con un check blanco. Su título y nombre
accesible lo identifican como distintivo propio de Efy: no afirma una
verificación de una plataforma externa. Cabecera, burbujas, acceso flotante y
menú conservan el diseño aprobado.

Revisión: los 13 HTML incluyen el distintivo y la misma versión. Tipografía
calculada del diálogo, nombre, mensajes, botones y campo de escritura comprobada
en 320, 390, 768 y 1440 px; IBM Plex Sans permanece en el resto de la página.
Sin desbordamiento ni errores de JavaScript. Menú de cotización, pregunta libre,
horas y cierre por teclado conservan su funcionamiento.

## Simulación de chat en cristal

La URL de la vista previa admite `?evia=cristal` para abrir una propuesta visual
inspirada en los paneles del inicio. Solo esa opción activa el fondo grafito
translúcido, desenfoque de 24 px, borde iluminado y reflejo sutil. Cabecera fucsia,
tipografía de sistema, distintivo de Efy y acciones se conservan; mensajes claros
y burbujas oscuras aseguran lectura sobre la escena. Los enlaces a módulos y
respuestas mantienen el modo durante esa visita. Sin el parámetro, se conserva
el chat blanco aprobado. Navegadores sin desenfoque reciben un panel más opaco.

Revisión de la simulación: panel y menús operativos en 320, 390 y 1440 px, sin
desbordamiento ni errores. Enlaces de cotización y navegación conservan el modo;
pregunta libre, apertura/cierre y foco comprobados. El chat blanco conserva
su comportamiento al acceder sin el parámetro de simulación.

## Publicación de la web completa y cristal aprobado

El propietario aprueba la simulación y pide aplicar todos los cambios al sitio.
El generador publica los ocho módulos y sus cinco páginas auxiliares en la raíz,
conservando copias compatibles en `/nueva/`. La portada de espera se sustituye por
Inicio y la escena aprobada del astronauta. El chat de cristal se aplica por
defecto en todos los módulos y abre solo al pulsar el acceso habitual; enlaces de
simulación anteriores pueden seguir abriéndolo al entrar. Tipografía nativa,
distintivo propio de Efy, menú de atención y contactos corregidos se conservan.

Los formularios publicados usan el mismo endpoint `/nueva/api/siniestros.php`:
el código del correo y su configuración no se duplican. JavaScript obtiene la
ruta del `action` del formulario. La sesión segura se conserva en el endpoint.
Las páginas raíz admiten indexación y canonical hacia su ruta publicada; la copia
`/nueva/` conserva `noindex`. El generador mantiene versión en recursos y enlaces.
CRM y estados siguen pendientes de sus APIs; opiniones de demostración permanecen
identificadas como tales, hasta disponer de reseñas reales.

Revisión de publicación: 13 páginas raíz en móvil y escritorio (26 vistas),
con los ocho módulos ordenados, cristal activo, fuente de sistema y distintivo
propio de Efy. Sin errores ni desbordamiento; se conservan servicios, socios,
contactos, historia y preguntas verificadas. Las dos copias suman 362 enlaces y
anclas locales válidos. Las rutas de reporte raíz y previa cargan la configuración
del mismo endpoint, comprobado con tres GET simulados y sin enviar reportes.

## WhatsApp, ubicación y preparación de consultas de estado

El propietario entrega el saludo exacto con emojis y saltos de línea. Se guarda
en `contactos.json` y se aplica a todos los enlaces de WhatsApp de Efy: botones
del sitio, servicios, chat, consultas preparadas y teléfonos comerciales u
operativos. Los WhatsApp de aseguradoras externas conservan sus propios destinos.
El botón de Maps usa el enlace de ubicación facilitado por el propietario.

La consulta manual permite escribir cédula o placa (esta última solo en un
siniestro vehicular), validar el formato y preparar un resumen para copiar y
compartir con el equipo operativo. Ningún identificador se envía automáticamente
ni se incorpora al enlace de WhatsApp. No se afirma una búsqueda de estados.
La integración sigue pendiente del nombre y acceso al sistema del propietario,
que se han solicitado nuevamente por tratarse del bloqueo de la consulta real.

EVIA y Ayuda incorporan nueve opciones de salud y fuentes oficiales. Saludsa,
Humana, BMI, Ecuasanitas, Confiamed y Bupa tienen documentación detallada.
Privilegio tiene datos del formulario confirmado, pero no una lista exhaustiva
de anexos; Mediken publica pasos y carga de documentos en su portal. VidaSana
no tiene una lista pública que se haya podido verificar, y se remite al equipo.
No se generalizan requisitos ni plazos entre compañías o productos.

## Navegación azul cristalizada · 15 de octubre de 2026

Se integra esta actualización sobre `13430af`, conservando las mejoras recientes
de imágenes, servicios, tipografía y borradores por correo. Los nombres de los
ocho módulos mantienen enlaces directos a sus páginas; los submenús son listas
verticales con viñetas «•», superficie azul de marca cristalizada y una entrada
vertical breve. En móvil y dispositivos táctiles se añade una flecha independiente
para desplegar las opciones, sin interceptar el enlace del módulo. Se conservan
foco visible, cierre por Escape, navegación por teclado y movimiento reducido.

La consulta de estados conserva el borrador por correo aprobado el 13 de octubre,
y añade copiar el resumen y un enlace al WhatsApp operativo con el saludo exacto
del propietario. No hay búsqueda automática de estados ni envío de datos al
preparar el borrador. El saludo común se conserva también en la consulta comercial
preparada; su texto específico se puede copiar desde el resumen.

Revisión: nueve pruebas de navegación (incluido submenú táctil), catálogo y consultas
en raíz y copia previa a 320, 390 y 1440 px. 32 pruebas de acceso a módulos y 944
enlaces/anclas locales válidos. Mensaje de WhatsApp exacto, cuatro números, Maps,
nueve opciones de reembolso y sus fuentes, preguntas libres y apertura de FAQ
comprobados en navegador. El test de consultas excluye únicamente la carga tardía
del icono del sitio; sigue rechazando solicitudes de red de los borradores.

## Destinos coherentes dentro de cada módulo

Se corrigen submenús que salían del contexto del módulo: Conócenos/EVIA ya no
apunta a Ayuda; Socios y Reseñas mantienen sus accesos en sus propias páginas.
Inicio enlaza a secciones de Inicio, y Contáctanos incorpora anclas específicas
para ambos equipos, ubicación y redes. Asistencias y Ayuda conservan sus páginas
auxiliares bajo la misma categoría activa. Los títulos de los ocho módulos
continúan abriendo sus páginas, y los elementos de los desplegables llevan a la
sección nombrada. Se conserva la navegación azul cristalizada y las viñetas.
