# Flujo de trabajo EFY

## Aislamiento

1. Revisar el worktree y actualizar la referencia de `origin/main`.
2. Crear una rama propia desde `origin/main`, por ejemplo `agent/nombre-del-ajuste-visual`.
3. Trabajar únicamente en la capa visual autorizada.
4. No publicar ni fusionar hasta que Fabrizio diga claramente “publícalo”.

## Integración con Claude

- Antes de publicar, traer lo último de `main`.
- Ante conflictos, conservar siempre la nueva lógica de Claude y aplicar encima sólo el cambio visual de Codex.
- No usar `git add -A` si existen cambios ajenos; añadir únicamente los archivos autorizados.

Mensaje estándar:

> Codex está trabajando sólo en la capa visual, en una rama aislada. No modifica rutas, lógica, datos, permisos ni integraciones. Antes de publicar integraremos tus cambios recientes de `main` para no sobrescribir nada.

## Validación y publicación

1. Ejecutar `npm run build`, `git diff --check` y `git status -sb`.
2. Configurar en otra Mac la identidad Git verificada si hace falta: `brazio1994` y `66549026+brazio1994@users.noreply.github.com`.
3. Hacer push de la rama y crear PR hacia `main` mediante `github:yeet`.
4. Esperar preview de Vercel en estado `Ready` y confirmar que el PR sea fusionable.
5. Fusionar sólo después de la autorización explícita y verificar producción en `https://app.latamyanez.com`.
6. Informar PR, commit, estado de Vercel y entregar un mensaje breve para Claude.

No usar Sites: este proyecto se publica mediante GitHub y Vercel.
