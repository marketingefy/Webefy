# Webefy · EFY Seguros

Sitio estático publicado en https://www.efyseguros.com/ mediante GitHub Actions y
SFTP a HostGator. Los cambios del sitio incorporados a `main` se publican automáticamente.

- Sitio: `public/`.
- Desarrollo local: `python3 -m http.server 8080 --bind 127.0.0.1 --directory public`.
- Identidad y página de espera: [DESIGN.md](DESIGN.md).
- Publicación y diagnóstico: [PUBLICACION.md](PUBLICACION.md).
- Habilidades y runtimes incluidos: [instalación EFY](tooling/efy/INSTALACION.md).

Las credenciales permanecen en GitHub Secrets y no se incluyen en el repositorio.
