# Webefy · EFY Seguros

Web con páginas estáticas y recepción de siniestros en PHP, publicada en https://www.efyseguros.com/ mediante GitHub Actions y
SFTP a HostGator. Los cambios del sitio incorporados a `main` se publican automáticamente.

- Sitio: `public/`.
- Vista previa de la nueva web: `public/nueva/` (Inicio, Servicios, Contactos, Conócenos, Socios estratégicos, Ayuda y Siniestros).
- Catálogo de seguros confirmado: `tooling/efy/servicios.json`; pendiente de la lista del propietario.
- Aseguradoras asociadas: `tooling/efy/socios.json`; pendiente de los nombres del propietario.
- Regenerar sus páginas compartidas: `python3 scripts/build_site.py`.
- Diseño y contenido de la vista previa: [brief de la web](tooling/efy/WEB-BRIEF.md).
- Recepción de reportes: [módulo de siniestros](tooling/efy/SINIESTROS.md).
- Desarrollo local: `python3 -m http.server 8080 --bind 127.0.0.1 --directory public`.
- Identidad y página de espera: [DESIGN.md](DESIGN.md).
- Publicación y diagnóstico: [PUBLICACION.md](PUBLICACION.md).
- Habilidades y runtimes incluidos: [instalación EFY](tooling/efy/INSTALACION.md).

Las credenciales permanecen en GitHub Secrets y no se incluyen en el repositorio.
