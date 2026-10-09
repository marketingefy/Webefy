# Primera web Efy: Inicio, Servicios, Contactos, Conócenos, Socios estratégicos, Ayuda y Siniestros

Petición del propietario: comenzar la web pública con cuatro módulos. La vista de
trabajo está en `public/nueva/`; la portada de espera se mantiene en `public/index.html`
mientras se completan los datos oficiales. Esta versión no cambia el hosting.

## Dirección de diseño

Público: personas que quieren conocer Efy y entender cómo consultar por sus seguros.
Trabajo de la portada: presentar la marca y dirigir a la información o el contacto.

Tokens: grafito #080E1D, tinta secundaria #17233D, blanco #F8F9FC, lienzo #F7F8FB,
rosa de lectura #FF91B2, azul de acción #445EA5. Magenta #EC245B sólo como acento.
Nunito Sans 700 para titulares; IBM Plex Sans 400 para texto y navegación.

Firma: EVIA trabajando en el universo digital de Efy, integrada en una portada
cinematográfica; el resto de la web ofrece superficies claras y lectura sencilla.
La composición de la escena aprobada se conserva y no hay botón de pausa.

```
Inicio:    navegación / mensaje + taller EVIA / accesos a información / cierre
Contactos: navegación / introducción / canales oficiales / preparar consulta
Conócenos:  navegación / identidad / EVIA / principios / acceso a contacto
Ayuda:     navegación / búsqueda / categorías / respuestas / acceso a contacto
Servicios: navegación / introducción / catálogo / guía para comparar / consulta
Socios:    navegación / aseguradoras / guía de póliza / acceso a siniestros
```

Revisión previa: se descartó una parrilla genérica de pólizas, cifras y logos de
aseguradoras porque no hay ramos, cifras o asociaciones confirmados. La firma
visual está concentrada en EVIA y el taller. La jerarquía de contenido guía el resto.

## Contenido pendiente

El propietario confirmó Quito y pidió incorporar un apartado con chatbot.
WhatsApp se incorporará después. Se solicitaron correo, descripción oficial y ramos.
No inventar esos datos. No simular envíos ni confirmar consultas sin destino real.
EVIA responde con una base local de preguntas frecuentes; no es una integración
generativa ni recibe pólizas o reportes. Los borradores se preparan en el navegador, sin enviar ni almacenar
información. La vista previa requiere completar esos datos antes de pasar a portada.
El módulo Siniestros se añadió por petición posterior y envía al correo
`siniestros@efyseguros.com`, confirmado por el propietario. Su recepción, datos
y pruebas se documentan en [SINIESTROS.md](SINIESTROS.md).

## Servicios

El propietario pidió desglosar los tipos de seguros de Efy. Se ha solicitado su
lista; todavía no hay ramos confirmados. Servicios incluye un estado de catálogo
próximo, una guía para comparar propuestas y enlaces reales a Ayuda, Contactos y
EVIA. No publica los ejemplos de la pregunta como productos de Efy.

El catálogo se prepara en `tooling/efy/servicios.json` y se regenera con el resto
de páginas. Cada entrada contiene `id` (único, minúsculas y guiones), `name`,
`description` y `details` (lista de textos confirmados; puede estar vacía).
Los detalles se muestran en acordeones nativos y los textos se escapan como HTML.
La respuesta de EVIA sobre servicios usa esa misma lista y enlaza al catálogo.
No agregar precios, coberturas o condiciones que el propietario no haya confirmado.

## Socios estratégicos y Conócenos

El propietario pidió renombrar «Nosotros» a «Conócenos» y mostrar las aseguradoras
con las que trabaja Efy. El nombre se actualiza en todos los accesos, conservando
la URL `nosotros.html` para que los enlaces existentes sigan funcionando.

`socios.html` queda integrado en la navegación y la portada. Sus nombres proceden
de `tooling/efy/socios.json`: cada entrada contiene `id` único y `name` confirmado.
No hay aseguradoras confirmadas todavía; se solicitaron los nombres al propietario.
El estado próximo es explícito. No se inventan asociaciones ni logotipos. EVIA usa
la misma lista. Los logos oficiales se incorporarán cuando estén disponibles.

Dirección del módulo: el titular pone lo que el cliente quiere proteger primero;
un panel oscuro reúne las preguntas que debe resolver antes de decidir. Se
conservan los tokens y las tipografías compartidas. Se descartaron iconos de ramos
y tarjetas de productos ficticios; las fichas aparecerán con contenido real.

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
