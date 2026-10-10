# Mejoras de interfaz de Efy Seguros

Aplicación de las 16 skills de diseño y animación solicitadas el 10 de octubre
de 2026, sobre la web completa del commit `94b683b`. El alcance es la presentación
compartida por las 13 páginas y sus rutas de vista previa en `/nueva/`.

## Resultado

- Encabezado más compacto, con el mismo logo, distribución y navegación.
- Tipografía en `rem`, conservando su tamaño habitual y respetando el aumento
  de texto configurado por la persona. Se mantienen las fuentes existentes.
- Chat EVIA más legible: texto de conversación de 15 px equivalentes,
  interlineado de 1,65, opciones de 14 px y acciones rápidas de al menos 44 px.
- Márgenes que respetan las zonas seguras del teléfono y mejor ajuste de textos
  y botones en pantallas estrechas. El diálogo conserva su altura disponible.
- Entrada del chat de 200 ms con escala de 0,98 a 1, desplazamiento de 6 px a 0
  y opacidad de 0 a 1; respuesta al pulsar de 160 ms. Los mensajes mantienen
  su entrada de 180 ms y las estadísticas usan 320 ms.
- Curva compartida `cubic-bezier(.23,1,.32,1)` y hover limitado a un puntero
  preciso. Las preferencias de movimiento reducido desactivan las transiciones.
- Alternativa opaca usando el color existente `--surface` cuando el sistema
  solicita reducir la transparencia; el diseño de cristal habitual se conserva.
- Bordes de acento más discretos, con el mismo color.
- Logo y retratos entregados como WebP a escala mediante `picture`, con el
  archivo original como alternativa. El logo habitual pasa de 492 KB a 20–59 KB
  según la pantalla. Se anticipa la carga de la fuente del cuerpo de texto.

## Aplicación de cada skill

| Skill | Aplicación concreta |
| --- | --- |
| `frontend-design` | Afinar jerarquía, encabezado y composición compartida sin reemplazar la dirección visual vigente. |
| `ui-ux-pro-max` | Contrastar legibilidad, tamaños táctiles, ajuste móvil y preferencias de accesibilidad con sus recomendaciones. |
| `impeccable` | Revisar y simplificar el acabado: bordes menos pesados, espaciado y tipografía. Su detector señaló los bordes de acento de 3 px; se redujeron a 1 px. |
| `taste-skill` | Conservar la composición espacial de EVIA, el contraste entre secciones y la identidad propia de Efy al pulir componentes. |
| `emil-design-eng` | Aplicar respuesta breve a la pulsación y una entrada suave del diálogo, con animación de transformación y opacidad. |
| `apple-design` | Respetar texto ampliado, zonas seguras, controles cómodos y preferencias del sistema, manteniendo la tipografía de plataforma del chat. |
| `web-design-guidelines` | Revisar teclado, foco, dimensiones de imágenes, tipografía flexible, movimiento reducido y comportamiento sin JavaScript. |
| `find-animation-opportunities` | Elegir la entrada del diálogo y la pulsación de controles como puntos útiles de movimiento; conservar el contenido de lectura estable. |
| `improve-animations` | Registrar alcance, valores exactos, límites y comprobaciones en `plans/001-shared-interface-motion.md`. |
| `review-animations` | Revisar duración, curva, propiedades animadas, controles deshabilitados y ausencia de movimiento bajo la preferencia correspondiente. |
| `animation-vocabulary` | Definir la entrada como escala y desvanecimiento, y la pulsación como compresión breve, con estados iniciales y finales explícitos. |
| `hyperframes` | Ejecutar una comprobación técnica estricta del bucle existente de EVIA en una composición aislada, fuera de la web publicada. |
| `hyperframes-animation` | Revisar los estados del bucle con muestras temporales y conservar la reproducción de ida y vuelta ya aprobada. |
| `hyperframes-keyframes` | Comprobar encuadre, identidad y estados visibles en el inicio, el retorno y el final mediante snapshots en tiempos explícitos. |
| `hyperframes-creative` | Contrastar la escena con `DESIGN.md`: identidad de EVIA, composición, paleta y continuidad del plano aprobado. |
| `efy-analyzer-visual` | Aplicar sus criterios de consistencia visual y límites de alcance a este sitio: fuentes, marca, componentes compartidos y preservación de flujos. |

Las herramientas HyperFrames se usaron para revisar el medio existente. Sus
dependencias, composición de prueba y snapshots quedan fuera de `public/`;
la web mantiene su implementación estática y sus videos originales.

## Verificación

- 13 páginas a 320, 390, 768 y 1440 px: 52 casos aprobados, sin desbordamiento
  horizontal ni errores JavaScript.
- Menú móvil y chat con Escape y devolución de foco; respuesta de EVIA a una
  pregunta; búsquedas de socios, asistencia y ayuda; resumen de consulta.
- Escenarios adicionales: ausencia de JavaScript, reproducción bloqueada y
  tamaño de texto al 200 %. El póster sigue disponible.
- Entrada del diálogo observada en el navegador: transiciones nativas de
  opacidad y transformación, ambas de 200 ms.
- Lighthouse local, Chromium, portada móvil: rendimiento 95, accesibilidad 100,
  buenas prácticas 100 y SEO 100. CLS 0 y tiempo de bloqueo 0 ms. Esta medición
  corresponde al servidor local, no a una medición de usuarios en HostGator.
- HyperFrames: comprobación estricta de lint, runtime y geometría sin hallazgos;
  snapshots a 0, 0,25, 6, 6,042 y 12,042 segundos.
- Comparación con la versión base: mismo conjunto de colores CSS, textos,
  enlaces, IDs y atributos de formularios y controles. JavaScript, PHP y MP4
  conservan exactamente sus hashes SHA-256.

La publicación utiliza el workflow existente de HostGator. Este valida la API
de siniestros con un envío de correo simulado y compara por HTTPS los archivos
publicados con los del commit; no envía consultas reales durante las pruebas.
