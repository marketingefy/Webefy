# Navegación, servicios y consultas — 13 de octubre de 2026

Cambios solicitados por la persona encargada de marketing, sobre la versión
publicada `8964911`. Se mantienen los colores, fuentes, contactos, textos del
catálogo, videos de EVIA, chat y recepción de reportes existentes.

| Antes | Ahora | Propósito |
| --- | --- | --- |
| El menú sólo mostraba enlaces. | Cada módulo muestra una lista vertical de accesos al pasar el puntero o recibir foco en escritorio. | Orientar antes de entrar, conservando el enlace principal. |
| Los 16 seguros formaban una lista larga en móvil. | Un carrusel manual con imágenes, categorías, contador, flechas y deslizamiento. | Explorar una opción cada vez. |
| Cédula, placa y búsqueda estaban deshabilitadas. | Campos editables con validación y un borrador de consulta al equipo. | Permitir solicitar seguimiento mientras no hay un registro conectado. |

## Navegación

Los paneles funcionan con ratón y teclado en escritorio desde 1181 px; sólo uno
permanece abierto. Escape cierra el panel y devuelve el foco al enlace principal.
Se cierran al salir, pulsar fuera o cambiar a una pantalla compacta. En pantallas
de hasta 1180 px se mantiene el menú existente y la selección directa de módulos.
La apertura usa 180 ms, sin animación para teclado o movimiento reducido.

## Servicios

Las ilustraciones editoriales se generaron para los 16 ramos y se entregan en un
atlas WebP de 1200 × 1200, 87.490 bytes. La asociación usa el ID de cada seguro,
de modo que reordenar los datos no cambia su imagen. La ventana 4:3 mantiene las
proporciones y conserva los objetos completos.

El catálogo mantiene el orden anterior por categoría, las anclas de grupos y
seguros, los detalles desplegables y los enlaces de consulta. No tiene avance
automático. Flechas, Home y End funcionan al enfocar el carrusel; el teclado y
el movimiento reducido desplazan de inmediato. Las imágenes y el texto pueden
explorarse también sin JavaScript, mediante desplazamiento horizontal nativo.

Comparación local con las mismas fuentes a 390 px: el catálogo pasa de 6.130 a
944 px de alto, conservando las 16 opciones. La orientación inicial se presenta
en un desplegable para mantener más compacto el módulo.

## Consulta de siniestros y reembolsos

El propietario confirmó que todavía no hay un registro de estados conectado.
El formulario activa sólo el identificador seleccionado: cédula de 10 dígitos
o placa para un siniestro vehicular. Valida antes de preparar el resumen y
normaliza espacios, guiones y mayúsculas de la placa.

Preparar la consulta no hace búsquedas, no envía correo, no accede a la API de
reportes y no guarda datos. El visitante revisa el resumen y abre su correo para
enviarlo a `siniestros@efyseguros.com`. Editar datos invalida el borrador. Se anuncia
la preparación mediante una región de estado accesible. El detalle del flujo
está en [SINIESTROS.md](tooling/efy/SINIESTROS.md).

## Comprobación

- Las 13 páginas a 320, 390, 768 y 1440 px: sin desbordamientos ni errores JS.
- Navegación: 8 pruebas, incluyendo 1101/1180/1181/1280/1440 px, puntero, teclado,
  Escape, enlaces originales, touch y conservación del chat EVIA.
- Servicios: ambas rutas a 320/390/1440 px; carga de las 16 imágenes, categorías,
  flechas, deslizamiento, enlaces directos, detalles y preferencias de movimiento.
- Consultas: ambas rutas a 320/390/1440 px; escritura, validación, cambio de tipo,
  borrador y ausencia de solicitudes de red, almacenamiento y cambios de URL.
- Lighthouse local de Servicios: rendimiento 91, accesibilidad 100, buenas
  prácticas 100 y SEO 100; CLS 0. Es una medición local, no de usuarios reales.
- Mismo conjunto de colores CSS y mismos archivos de contactos, contenido del
  catálogo, chat, reportes y videos.

Las pruebas están en `tests/ui/`. Requieren Playwright y Chromium y aceptan
`PLAYWRIGHT_MODULE`, `CHROMIUM_PATH` y `UI_BASE_URL`. Para la prueba de navegación,
arrancar primero un servidor local; las otras dos pueden iniciarlo automáticamente.
Nunca visitan producción ni envían correos reales.

La publicación conserva el workflow automático de HostGator, su validación de
reportes con correo simulado y la comparación HTTPS de los recursos publicados.

## Ajuste a la referencia visual del propietario

Los desplegables se compactaron a 260 px y se alinean debajo de cada módulo,
como en la referencia aportada. Mantienen sus destinos, teclado, Escape y
selección directa en móvil; los tres últimos se alinean al borde derecho para
quedar dentro de la pantalla. Se revisaron los ocho menús a 1181, 1280, 1440 y
1920 px, además de las pruebas existentes de navegación y las 13 páginas.

Las tarjetas y paneles interiores reciben un blanco cristalizado con brillo
suave, borde claro y sombra discreta. Los acentos de azul y rosa, la tipografía,
el chat y los formularios permanecen. La preferencia de transparencia reducida
y los navegadores sin desenfoque usan una superficie blanca opaca.

Se retiraron de la portada el rótulo rosa «EFY SEGUROS · TU MEJOR ELECCIÓN» y
«Una nueva experiencia de Efy, desde Quito.». El logo conserva su composición.
