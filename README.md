# Webefy · EFY Seguros

Web con páginas estáticas y recepción de siniestros en PHP, publicada en https://www.efyseguros.com/ mediante GitHub Actions y
SFTP a HostGator. Los cambios del sitio incorporados a `main` se publican automáticamente.

- Sitio: `public/`.
- Módulos publicados en la raíz, con copia de revisión compatible en `public/nueva/` (Inicio, Servicios, Socios estratégicos, Conócenos, Asistencias, Reseñas, Contáctanos y Ayuda).
- Catálogo de seguros confirmado: `tooling/efy/servicios.json`; 16 apartados confirmados, organizados en cuatro grupos, incluidos Hogar y Pymes. Finanzas se mantiene distinto de Fianzas.
- Socios estratégicos: `tooling/efy/socios.json`; 26 confirmados por el propietario, con logos oficiales y canales de atención. [Fuentes y mantenimiento](tooling/efy/SOCIOS-Y-ASISTENCIA.md).
- Contactos confirmados: `tooling/efy/contactos.json`; WhatsApp comercial y operativo, correos, dirección única de Quito e Instagram/Facebook facilitados por el propietario.
- Conócenos: `tooling/efy/conocenos.json`; trayectoria y texto facilitados por el propietario, cifras animadas y video de EVIA en bucle. [Contenido y medios](tooling/efy/WEB-BRIEF.md).
- Ayuda: `reportar-error.html` prepara un reporte y abre el correo del cliente para enviarlo a `info@efyseguros.com`. La web no confirma un envío automático.
- Reseñas reales de clientes: `tooling/efy/resenas.json`; pendientes del propietario o de una fuente oficial. `resenas-demo.json` contiene diez ejemplos ficticios bajo el rótulo «Opiniones de demostración» mientras no haya reseñas reales.
- Cotizaciones: las consultas actuales se preparan en el navegador y continúan por WhatsApp comercial. El CRM facilitado es `https://app.latamyanez.com/login`; su recepción de solicitudes depende del acceso a la API o repo.
- Preguntas de EVIA: base de Ayuda y `tooling/efy/preguntas-frecuentes.json`; preguntas investigadas en fuentes oficiales, con nueve guías de documentos de reembolso por compañía, con enlaces y variantes para el chat.
- EVIA: burbujas de conversación y menú de atención para cotizaciones, pólizas, asistencia y asesores. Panel de cristal difuminado, fucsia de la marca y botón flotante translúcido y disponible en todos los módulos. IBM Plex Sans con jerarquía 400/500/600 también dentro del chat y distintivo propio de Efy junto al nombre. Los enlaces internos conservan la versión del sitio.
- Regenerar sus páginas compartidas: `python3 scripts/build_site.py`.
- Consulta de seguros de Coopartamos: `coberturas-cooperativas.html`, conectada desde el PHP propio con EfyAnalyzer. [Configuración privada y alcance](tooling/efy/COBERTURAS-COOPERATIVAS.md).
- Vistas previas, catálogo deslizante y consultas: [mejoras de interacción](MEJORAS-INTERACCION.md).
- Diseño y contenido del sitio: [brief de la web](tooling/efy/WEB-BRIEF.md).
- Asistencia: reporte de siniestros, líneas oficiales y preparación de consultas al equipo por cédula o placa. El registro de estados aún no está conectado. [Recepción e integración](tooling/efy/SINIESTROS.md).
- Desarrollo local: `python3 -m http.server 8080 --bind 127.0.0.1 --directory public`.
- Identidad y página de espera: [DESIGN.md](DESIGN.md).
- Publicación y diagnóstico: [PUBLICACION.md](PUBLICACION.md).
- Habilidades y runtimes incluidos: [instalación EFY](tooling/efy/INSTALACION.md).

Las credenciales permanecen en GitHub Secrets y no se incluyen en el repositorio.
