# Reportes de siniestros desde la web de Efy

El propietario pidió un módulo de reporte y confirmó el destinatario
`siniestros@efyseguros.com`. El módulo se llama Asistencia y está en
`/asistencia.html`, con el reporte en `/reportar-siniestro.html` y copias compatibles en `/nueva/`. Figura en la navegación, portada y guía de EVIA.
La antigua URL `/nueva/siniestros.html` conserva el mismo contenido y formulario.
La web completa está publicada en la raíz del dominio.

## Consulta de estados y líneas de asistencia

El registro de estados aún no está conectado a la web. El 13 de octubre de 2026
el propietario confirmó que, por ahora, se debe preparar la consulta al equipo.
La interfaz en `/consultas.html` y `/nueva/consultas.html` permite escoger siniestro
vehicular, otro siniestro o reembolso. Recibe la cédula o, sólo para un siniestro
vehicular, la placa. Activa y valida únicamente el campo elegido y prepara un
resumen con un enlace `mailto:` al destinatario fijo `siniestros@efyseguros.com`.
El visitante debe abrir su correo y enviar el mensaje; preparar el resumen no
envía solicitudes de red ni guarda identificadores en la web o el almacenamiento
del navegador. Cambiar los datos invalida el borrador anterior. No hace búsquedas,
no consulta el endpoint de reportes y no inventa estados.

La integración futura debe verificar la identidad y autorización del cliente antes
de mostrar información del caso. Una cédula o placa no constituye autenticación.
La referencia de recepción y sus metadatos privados tampoco son estados del
siniestro o reembolso. Este flujo permite solicitar seguimiento al equipo por correo.
También se puede copiar el resumen y abrir el WhatsApp operativo con el saludo
aprobado. El identificador no se incorpora al enlace de WhatsApp.

El directorio de 26 socios en `/nueva/lineas-asistencia.html` se filtra por nombre sin enviar datos. Teléfonos,
etiquetas y fuentes proceden de `socios.json`, documentados en
[SOCIOS-Y-ASISTENCIA.md](SOCIOS-Y-ASISTENCIA.md). Distingue asistencia vehicular,
médica, hogar y atención al cliente. Cuando no se pudo confirmar una línea,
enlaza al sitio oficial. Incluye ECU 911 para emergencias en Ecuador.

## Flujo

Contacto → evento y adjuntos → revisión y autorización → envío → referencia y
comprobante descargable. Teléfono obligatorio; correo, aseguradora y póliza
opcionales. Hasta tres fotos JPG/PNG/WebP o PDF. El límite por archivo es el menor
entre 2 MB y el límite PHP del servidor; el tamaño total también se adapta.

El cliente ve una referencia sólo después de que `mail()` acepta el mensaje.
Esa aceptación no prueba llegada a la bandeja ni lectura del equipo. No emitir
números de siniestro de la aseguradora, promesas de cobertura o tiempos de atención.
Si falla el correo, el formulario conserva los datos y ofrece reintentar o escribir
al correo oficial. Si no se puede confirmar un intento, no afirmar que falló o llegó.

## Recepción

`public/nueva/api/siniestros.php` usa PHP nativo de HostGator y su transporte local
de correo. Tanto el destinatario como el remitente de servicio están fijados al
correo autorizado. El correo del cliente sólo puede formar un Reply-To validado.
No hay correos automáticos al cliente ni destinos proporcionados por el visitante.

GET comprueba disponibilidad y devuelve el token de sesión y los límites reales.
POST valida los datos y el contenido de los adjuntos en el servidor, construye el
correo con los adjuntos, y devuelve la referencia cuando el transporte acepta el
envío. No registrar cuerpos de solicitudes en logs ni imprimir datos personales.

La sesión utiliza token CSRF, cookie HttpOnly/SameSite y Secure en HTTPS. Sólo se
aceptan los orígenes HTTPS de Efy; localhost se permite exclusivamente con el
servidor PHP de desarrollo. Hay un campo antibot y límite de diez intentos válidos
por IP/hora. La IP se transforma con HMAC y una clave privada local; no se guarda
su valor original. Las referencias y hashes de intentos previenen reenvíos duplicados.

## Datos y almacenamiento

Los reportes y sus adjuntos se entregan al correo; no se archivan en la web ni hay
rutas públicas para descargarlos. Los archivos temporales de carga son gestionados
por PHP durante la solicitud. El comprobante del visitante se genera sólo al
pulsar Descargar.

Los metadatos de reintentos (referencia, hash, estado y fecha) se guardan en
`/home1/brayanez/.efy-siniestros`, fuera de `public_html`, con directorio 0700 y
archivos 0600. No contienen nombre, teléfono, correo, póliza, texto del evento ni
adjuntos. Los JSON de más de siete días se eliminan tras un envío aceptado. La
variable opcional `EFY_CLAIMS_STATE_DIR` sólo sirve para elegir otra carpeta privada;
el endpoint rechaza carpetas dentro de la raíz pública.

La conservación de reportes en el buzón y su gestión corresponde al equipo de Efy.
No se ha comprobado la entrega de un correo real al buzón en estas pruebas.

## Pruebas

`tests/claims/test_api.py` requiere dos contenedores llamados `efy-claims-test` y
`efy-claims-fail`, accesibles sólo en localhost:8088/8089. Comprueba que su comando
use el transporte simulado antes de probar o limpiar las carpetas temporales.
El workflow de publicación prepara esos contenedores y ejecuta los seis casos:

- Correo con destinatario fijo, Reply-To validado, datos y adjunto real, renombrado
  seguro, referencia y metadatos privados sin datos del cliente.
- Reintento sin duplicado y rechazo de datos distintos para la misma clave.
- Datos inválidos, fecha futura, falta de autorización, inyección de encabezados,
  token CSRF incorrecto y origen externo: no envían correo.
- Archivos con contenido inválido, demasiado grandes o demasiados adjuntos.
- Fallo del transporte: no emite confirmación de recepción.
- Límite de frecuencia.

Playwright comprobó 320/390/768/1440 px, el recorrido de tres pasos, la revisión,
un adjunto, envío con referencia, descarga y conservación de los campos ante un
fallo del correo. Todos los envíos de pruebas usaron transporte simulado.

La verificación de publicación descarga las páginas y assets y compara hashes.
Para PHP comprueba por HTTPS la respuesta GET, destino, versión, disponibilidad,
token, límites y cookies; no envía reportes ni correos reales.

`tests/ui/lookup.spec.cjs` comprueba captura de cédula y placa, validación, cambio
de método y tipo, resumen y destino del borrador, ausencia de almacenamiento y
de solicitudes de red. Se ejecuta contra las dos rutas en 320, 390 y 1440 px,
con identificadores sintéticos; nunca abre el correo ni envía consultas reales.
