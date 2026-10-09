# EFY Seguros: desarrollo y publicación automática

El sitio está en `public/`. Las páginas no requieren paquetes ni un servidor de
aplicaciones. El módulo de siniestros usa el PHP nativo y correo local de HostGator. La portada de espera no recopila datos. La vista previa `/nueva/` incluye una guía
de preguntas frecuentes y un formulario que prepara consultas sólo en el navegador;
no envía ni almacena información. El módulo Siniestros sí envía datos y adjuntos
al correo autorizado `siniestros@efyseguros.com`, con validación del servidor y
referencia después de la aceptación del transporte de correo. Véase [Siniestros](tooling/efy/SINIESTROS.md). WhatsApp se incorporará cuando el propietario
confirme el número.

## Desarrollo local

Usar el checkout existente en `/workspace/Webefy`; no crear worktrees adicionales.

```sh
cd /workspace/Webefy
python3 -m http.server 8080 --bind 127.0.0.1 --directory public
```

Comprobar el mensaje principal, la carga de la imagen y el diseño en móvil.
La nueva web se revisa en `/nueva/`; sus páginas compartidas se regeneran con
`python3 scripts/build_site.py`. El script de publicación incluye los `index.html`
de subdirectorios y reemplaza la portada raíz al finalizar.

## Publicación en HostGator

El workflow `Publicar EFY en HostGator` se ejecuta cuando se incorporan cambios a
`main` en los archivos del sitio, scripts de publicación o configuración del workflow.
También puede ejecutarse manualmente desde GitHub Actions → Run workflow.

Antes de subir archivos comprueba la autenticación SFTP y el acceso al directorio.
No borra archivos ajenos; sube los recursos primero y reemplaza `index.html` tras
transferirlo completamente. Después comprueba por HTTPS el contenido de cada archivo
frente a esta versión para detectar fallos de publicación o caché.

La conexión SFTP y el directorio del dominio se validaron desde GitHub Actions.
Datos no secretos predeterminados, obtenidos del cPanel del usuario y pruebas reales:

- Host: `162.241.61.73`
- Puerto: `2222`
- Usuario: `brayanez`
- Directorio: `/home1/brayanez/public_html`

Las variables opcionales `SSH_HOST`, `SSH_PORT`, `SSH_USER` y `SSH_DIRECTORY` de GitHub
Actions permiten cambiar esos datos si HostGator traslada la cuenta.

## Credenciales y confianza del servidor

En GitHub Settings → Secrets and variables → Actions están los secretos:

- `SSH_PRIVATE_KEY`: clave privada dedicada, creada y autorizada por el usuario en cPanel.
- `SSH_KEY_PASSPHRASE`: contraseña de esa clave.

El script desbloquea la clave mediante un agente temporal. No imprime claves ni contraseñas.
Nunca guardar valores secretos en el repositorio o en el chat.

La clave pública ED25519 del servidor está en `.github/hostgator_known_hosts`.
Su huella se verificó comparando la observación desde GitHub con una consulta a
`127.0.0.1` ejecutada por el usuario dentro de su cPanel autenticado:

`SHA256:Qj34DMRb4Ys/Ek8ctq5pS5K97hHcjHPGyihSntn4w/0`

La verificación estricta de identidad del servidor permanece activada. Si cambia la
clave del servidor, detener la publicación y verificar la nueva con una fuente confiable
antes de actualizarla. El secreto opcional `SSH_KNOWN_HOSTS` puede sobrescribir el archivo;
no es necesario configurarlo para esta instalación.

`Comprobar acceso a HostGator` queda disponible para ejecución manual: consulta puertos,
valida la clave e inicia una sesión de solo lectura para diagnosticar problemas.
No interpreta una respuesta a `ssh-keyscan` como una clave confiable por sí sola.

## Publicación manual de respaldo

El paquete actualizado `EFY-espera-limpia.zip` contiene `index.html`, el logo y las fuentes en `assets/`.
Subirlo y extraerlo directamente en `public_html`, sin una carpeta `public` intermedia.
No usar ese paquete antiguo para sobrescribir una versión posterior del sitio.
