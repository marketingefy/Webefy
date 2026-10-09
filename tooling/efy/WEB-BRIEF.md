# Primera web Efy: Inicio, Contactos, Nosotros, Ayuda y Siniestros

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
Nosotros:  navegación / identidad / EVIA / principios / acceso a contacto
Ayuda:     navegación / búsqueda / categorías / respuestas / acceso a contacto
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

## Validación

Navegación entre cuatro páginas y menú móvil, búsqueda y filtros de preguntas,
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
