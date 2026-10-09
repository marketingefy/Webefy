# EFY Seguros: página temporal y publicación

El sitio está en `public/`. No requiere instalar paquetes ni un servidor de aplicaciones.

## Vista local

Desde el checkout existente (no crear otro worktree):

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory public
```

## Publicación manual inicial

Subir `EFY-proximamente.zip` a `public_html` y extraerlo allí usando cPanel.
`index.html` y `assets/nuevo-comienzo.png` deben quedar directamente en esa carpeta,
sin una carpeta `public` intermedia. Comprobar por HTTPS el texto «Próximamente» y la imagen.
La carpeta raíz del dominio se confirmó en las capturas de cPanel.

## Publicación automática por GitHub Actions

El workflow `Publicar EFY en HostGator` permanece desactivado hasta verificar la conexión
y configurar `DEPLOY_ENABLED=true`.

Confirmar con HostGator que SSH/SFTP esté habilitado y obtener hostname, puerto y la
clave pública o huella del servidor. «Manage SSH Keys» por sí solo no confirma acceso activo.
No asumir el puerto predeterminado.

Autorizar la clave pública dedicada en cPanel → SSH Access → Manage SSH Keys → Import Key.
Importar únicamente la parte pública y autorizarla. La clave privada se guarda como GitHub
Secret, nunca en el repositorio ni en el chat.

En GitHub: Settings → Secrets and variables → Actions.

Variables:

- `SSH_HOST`: hostname de conexión confirmado, sin esquema.
- `SSH_PORT`: puerto SSH confirmado por HostGator.
- `SSH_USER`: usuario cPanel confirmado.
- `SSH_DIRECTORY`: ruta absoluta confirmada del sitio, terminada en `/public_html`.
- `DEPLOY_ENABLED`: `true` únicamente después de verificar los datos y el acceso.

Secrets:

- `SSH_PRIVATE_KEY`: clave privada dedicada a este despliegue.
- `SSH_KEY_PASSPHRASE`: contraseña que protege esa clave, si se generó cifrada en cPanel.
  No es la contraseña de la cuenta HostGator. Se utiliza mediante un agente SSH temporal.
- `SSH_KNOWN_HOSTS`: entrada OpenSSH cuya huella se haya verificado con una fuente confiable
  de HostGator. Para puerto distinto de 22 debe incluir `[host]:puerto`.

La verificación de identidad del servidor es obligatoria. No usar `StrictHostKeyChecking=no`
ni confiar en `ssh-keyscan` sin verificar la huella. El script no borra archivos ajenos y
publica la página de entrada después de transferir los recursos.

Primera ejecución: Actions → Publicar EFY en HostGator → Run workflow.
Después, los cambios incorporados a `main` se publican automáticamente.
El workflow comprueba la página y la imagen por HTTPS. Hasta ese primer éxito, el despliegue
automático no está validado.

Si SSH/SFTP no está disponible, usar la publicación manual mientras se prepara una
alternativa con FTPS verificado. FTP sin cifrado no es la alternativa recomendada.

La página temporal no recopila datos. Los formularios del futuro sitio deben desarrollarse
y verificarse antes de publicarlos.
