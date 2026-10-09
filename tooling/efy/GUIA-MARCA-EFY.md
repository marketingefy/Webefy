# Guía visual de EFY para la nueva página web

Preparada el 9 de octubre de 2026. Esta guía traslada la identidad visual vigente
de EFY a una web pública; no sustituye el brief del propietario ni un manual
corporativo aprobado. Las recomendaciones de composición son propuestas para
la web. Los colores de marca proceden del diseño actual del CRM.

## Paleta de marca confirmada

| Color | Código | Uso recomendado en la web |
| --- | --- | --- |
| Magenta principal | `#EC245B` | Identidad, detalles de marca, acentos y luces suaves |
| Magenta profundo | `#C61649` | Variante magenta para botones con texto blanco pequeño |
| Azul eléctrico | `#445EA5` | Acciones principales, enlaces en superficies claras, interacción |
| Azul profundo | `#344B88` | Variante azul para estados de interacción y profundidad |
| Tinta | `#0B1020` | Fondo oscuro principal y texto sobre superficies claras |
| Tinta secundaria | `#17233D` | Capas, zonas secundarias y superficies oscuras |
| Lienzo claro | `#F7F8FB` | Alternativa clara para lectura y secciones que la necesiten |
| Línea clara | `#DFE4EC` | Separadores sobre superficies claras |

La identidad combina **grafito translúcido, magenta y azul de EFY**. El fondo
aporta profundidad; los contenidos siguen siendo fáciles de leer. No convertir
cada sección en una tarjeta opaca ni introducir una paleta diferente por servicio.

Para materiales oscuros, el CRM usa además texto `#F8F9FC`, líneas
`rgb(255 255 255 / 0.16)` y superficies grafito en degradado. El archivo
`referencias-efy/tokens-efy.css` contiene una base opcional con estos valores.
Los tonos grafito de las superficies son tokens de interfaz, no colores nuevos
del logotipo. La transparencia debe comprobarse sobre el fondo final.

## Contraste y usos del color

Contrastes calculados con luminancia relativa WCAG sobre colores sólidos:

| Texto / fondo | Contraste | Aplicación |
| --- | --- | --- |
| Blanco / azul `#445EA5` | 6,19:1 | Apto para texto normal |
| Blanco / magenta profundo `#C61649` | 5,81:1 | Apto para texto normal |
| Blanco / magenta principal `#EC245B` | 4,23:1 | No alcanza 4,5:1 para texto normal; reservar para texto grande o acentos |
| Texto `#F8F9FC` / tinta `#0B1020` | 17,98:1 | Apto para lectura sobre fondo oscuro |
| Tinta `#0B1020` / lienzo `#F7F8FB` | 17,83:1 | Apto para lectura sobre fondo claro |
| Azul `#445EA5` / tinta `#0B1020` | 3,06:1 | Evitar como texto pequeño sobre fondo oscuro |

En fondos oscuros, usar texto claro para enlaces y expresar la interacción azul
mediante fondo, borde o subrayado. Verificar el foco y los estados reales en el
navegador, especialmente sobre cristal y fotografías. Los estados de éxito,
advertencia y error llevan texto e icono: el color por sí solo no comunica estado.

## Tipografía y logotipo

- **Nunito Sans, 600–800:** titulares destacados, hero y cifras principales.
- **IBM Plex Sans, 400–600:** lectura, navegación, botones, formularios y preguntas frecuentes.
- **IBM Plex Mono:** identificadores y datos que requieran alineación; uso puntual.

Mantener pocos tamaños y pesos, párrafos cómodos y una jerarquía clara. El CRM
combina encabezados con la familia de interfaz y componentes con fuente de
display; no es necesario forzar Nunito Sans en todos los encabezados de la web.
Obtener las fuentes de una distribución autorizada con su licencia; este paquete
no incluye archivos de fuentes.

Usar el logotipo oficial de **EFY Seguros** proporcionado para la página pública,
con proporciones intactas y espacio alrededor. Las variantes blancas funcionan
sobre oscuro; comprobar la legibilidad de la variante a color sobre cada fondo.
Los recursos de **EFY Analyzer / IA** pertenecen al producto: no asumir que su
wordmark es el logotipo corporativo de Seguros. No redibujar el símbolo ni
sustituirlo por una llama genérica. Este paquete no incluye logotipos ni vídeos.

## Dirección visual para una web pública

Transmitir confianza, claridad y atención humana con una estética tecnológica
sobria. Mantener aire entre secciones, tipografía protagonista y contenido breve.
Una web pública necesita más espacio y menos densidad que las tablas del CRM.

Usar el grafito como base, con luces magenta y azul discretas detrás del contenido.
Aplicar cristal en navegación, formularios o superficies destacadas cuando mejore
la composición. Evitar desenfoque en todas las filas, textos con opacidad muy baja,
brillos intensos y degradados que compitan con la lectura. El lienzo claro de la
marca puede servir para secciones de lectura, conservando la identidad común.

Reutilizar tokens y componentes para servicios, contacto, cotización, navegación
y pie de página. Tarjetas con radio moderado —14 px como punto de partida—,
botones en cápsula y bordes sutiles. Los botones que contienen **sólo un icono**
necesitan ancho y alto iguales, por ejemplo 44 × 44 px con radio 12 px, para evitar
óvalos alargados. El tamaño visible puede variar manteniendo un área táctil cómoda.

La acción principal puede ser azul; una llamada de marca puede usar magenta
profundo con texto blanco. Los secundarios usan cristal discreto. El hover de
elementos interactivos incorpora azul de EFY y el foco de teclado siempre es
visible. Mantener los estados de carga, éxito, error y deshabilitado coherentes.

## Experiencia, contenido y móvil

Como estructura inicial, considerar presentación, ramos o servicios, proceso de
asesoría, preguntas frecuentes y contacto. Ajustarla al brief y al contenido real;
no añadir secciones vacías por completar una plantilla. Llamadas claras como
«Solicitar asesoría» o «Pedir cotización» deben llevar a una acción que funcione.

No inventar aseguradoras asociadas, precios, coberturas, testimonios, estadísticas,
garantías ni condiciones. Identificar como pendientes los datos que falten. Usar
el dominio de la nueva web para SEO y enlaces cuando esté confirmado.

En móvil: contenido sin desbordamiento horizontal, menús accesibles, formularios
con etiquetas visibles y tipografía de entrada de al menos 16 px para evitar zoom
automático en iPhone. Reservar espacio para flechas de selectores y mensajes de
validación. Las opciones de activación pueden usar switches o botones segmentados
cuando corresponda, conservando la semántica y navegación por teclado.

Si hay adjuntos, mostrar progreso real cuando esté disponible y estados claros
de preparación, carga, descarga y error. Una animación no debe simular porcentajes
ni confirmar una operación que todavía no terminó. No afirmar que un archivo
quedó guardado en el dispositivo si el navegador no permite comprobarlo.

## Movimiento y rendimiento

Microinteracciones discretas de 160–220 ms y entradas breves de 220–250 ms como
punto de partida. Priorizar opacity y transform; respetar `prefers-reduced-motion`.
Evitar animación decorativa continua, rebotes en cada elemento y vídeos pesados
automáticos. El login y los vídeos aprobados de Evia no se trasladan a esta web.

Optimizar las imágenes y tamaños responsive, cargar diferidamente las imágenes
fuera de pantalla y priorizar la imagen principal si determina la carga inicial.
Usar fuentes con carga controlada y cargar sólo las bibliotecas que la web
necesite. Las skills y runtimes incluidos no justifican añadir dependencias al
frontend. Mantener navegación rápida y respuestas claras al enviar formularios.

## Comprobación antes de entregar

- Revisar vistas de 320 px, 390 px y escritorio, sin recortes ni solapamientos.
- Probar teclado, foco visible, etiquetas, contraste y movimiento reducido.
- Verificar navegación y estados de formularios sin enviar correos reales para probar diseño.
- Comprobar carga inicial, peso de imágenes y ausencia de errores del navegador.
- Revisar la misma identidad en todas las páginas y componentes.
- Confirmar contenido, dominio, logotipos y destinatarios antes de publicar.

## Fuentes y alcance

Valores de marca contrastados con `DESIGN.md` y `tailwind.config.js` de
`brazio1994/efy-analyzer`, checkout
`0a39d7cfb0ca161df052f443f0f3faada5ff2d7e`. Los materiales grafito proceden de
`.efy-operational-shell` en `app/globals.css`; su aplicación en la web es opcional
y debe validarse en el nuevo contexto. La copia completa del documento de diseño
está en `referencias-efy/DESIGN-CRM.md`.

Las instrucciones del nuevo repositorio y el brief del propietario gobiernan el
trabajo. Las reglas operativas, permisos, datos y hosting del CRM son contexto;
no son configuración de la nueva web. Las skills históricas se conservan tal
como fueron exportadas; esta guía aclara la identidad vigente cuando sus ejemplos
describen un diseño anterior.
