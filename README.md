# Webefy · EFY Seguros

Web con páginas estáticas y recepción de siniestros en PHP, publicada en https://www.efyseguros.com/ mediante GitHub Actions y
SFTP a HostGator. Los cambios del sitio incorporados a `main` se publican automáticamente.

- Sitio: `public/`.
- Vista previa de la nueva web: `public/nueva/` (Inicio, Servicios, Contactos, Conócenos, Socios estratégicos, Reseñas, Ayuda y Asistencia).
- Catálogo de seguros confirmado: `tooling/efy/servicios.json`; pendiente de la lista del propietario.
- Socios estratégicos: `tooling/efy/socios.json`; 26 confirmados por el propietario, con logos oficiales y canales de atención. [Fuentes y mantenimiento](tooling/efy/SOCIOS-Y-ASISTENCIA.md).
- Reseñas reales de clientes: `tooling/efy/resenas.json`; pendientes del propietario o de una fuente oficial.
- Regenerar sus páginas compartidas: `python3 scripts/build_site.py`.
- Diseño y contenido de la vista previa: [brief de la web](tooling/efy/WEB-BRIEF.md).
- Asistencia: reporte de siniestros, líneas oficiales y consulta de estados pendiente de conectar al sistema del propietario. [Recepción e integración](tooling/efy/SINIESTROS.md).
- Desarrollo local: `python3 -m http.server 8080 --bind 127.0.0.1 --directory public`.
- Identidad y página de espera: [DESIGN.md](DESIGN.md).
- Publicación y diagnóstico: [PUBLICACION.md](PUBLICACION.md).
- Habilidades y runtimes incluidos: [instalación EFY](tooling/efy/INSTALACION.md).

Las credenciales permanecen en GitHub Secrets y no se incluyen en el repositorio.
