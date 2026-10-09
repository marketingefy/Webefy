---
name: efy-analyzer-visual
description: Aplicar y verificar el sistema visual de EfyAnalyzer en cambios de interfaz React, Next.js y Tailwind, preservando la funcionalidad construida por Claude. Usar al modificar estética, composición, tipografía, responsive, accesibilidad, animaciones, navegación, PWA o comportamiento visual en iPhone y Android del repositorio efy-analyzer.
---

# EfyAnalyzer Visual

## Preparar el trabajo

1. Leer primero `AGENTS.md`, `DESIGN.md` y `CLAUDE.md` del repositorio cuando existan.
2. Leer [references/visual-system.md](references/visual-system.md) para decisiones de marca y composición.
3. Leer [references/functional-boundaries.md](references/functional-boundaries.md) antes de tocar componentes que mezclen presentación y lógica.
4. Leer [references/pwa-mobile.md](references/pwa-mobile.md) para cambios en navegación móvil, menú, `safe-area`, instalación o PWA.
5. Leer [references/project-workflow.md](references/project-workflow.md) antes de crear una rama o publicar.
6. Leer [references/master-context.md](references/master-context.md) cuando se necesiten antecedentes, activos históricos, áreas ya modificadas, conectores o decisiones de publicaciones anteriores.
7. Revisar `origin/main`, la rama y el diff; preservar cambios ajenos.

## Mantener el alcance

- Limitar los cambios a presentación, responsive, accesibilidad, animaciones y UX visual.
- No alterar rutas, autenticación, permisos, Supabase, consultas, APIs, correo, notificaciones, modelos de datos ni infraestructura sin una petición explícita.
- Si existe duda entre visual y funcional, detenerse y preguntar.
- Mantener intactos nombres accesibles, orden funcional y contratos de componentes.
- Preferir cambios mínimos y localizados sobre reescrituras amplias.

## Aplicar el sistema visual

- Reutilizar tokens, componentes, iconos y recursos de marca existentes.
- Reservar navegación oscura para identidad; mantener claras las superficies operativas.
- Expresar jerarquía mediante tamaño, espacio, color y composición; evitar construirla con negritas.
- Mantener objetivos táctiles cercanos a 44 px, foco visible y estados que no dependan solo del color.
- Respetar `prefers-reduced-motion` y animar principalmente `transform` y `opacity`.

## Usar las skills auxiliares

- Usar `impeccable` como auditoría y refinamiento principal; su versión actual consolida los antiguos `ui-skills-root`, `baseline-ui`, `fixing-motion-performance` y `fixing-accessibility`.
- Usar `ui-ux-pro-max` sólo cuando haga falta consultar patrones o decisiones adicionales.
- Usar `playwright-cli` o Browser para comprobar la interfaz real.
- Usar `github:yeet` únicamente cuando Fabrizio haya escrito claramente “publícalo”.

## Verificar

1. Ejecutar `npm run build`, `git diff --check` y `git status -sb`.
2. Usar `playwright-cli` o Browser para comprobar el comportamiento real desde 320 px y en un viewport de iPhone.
3. Confirmar que `scrollWidth <= clientWidth` y que tablas anchas contienen su propio desplazamiento.
4. En cambios PWA, probar apertura/cierre del menú, `safe-area`, notch/Dynamic Island, modo instalado y regreso desde segundo plano.
5. Usar la skill `screenshot` para comparar estados antes/después cuando el resultado sea visual.
6. No declarar corregido un problema específico de iOS basándose solo en Chromium; dejar indicada la verificación física pendiente.

## Publicar

- No publicar, hacer push ni fusionar hasta que Fabrizio escriba claramente “publícalo”.
- Publicar mediante una rama propia y un PR hacia `main`; no editar producción manualmente ni usar Sites.
- Traer los últimos cambios de `main`, conservar siempre la lógica nueva de Claude y aplicar encima únicamente el cambio visual de Codex.
- Esperar que el preview de Vercel quede en `Ready`, fusionar sólo con autorización y verificar `https://app.latamyanez.com`.
- No fusionar builds fallidos ni cambios incompletos.
