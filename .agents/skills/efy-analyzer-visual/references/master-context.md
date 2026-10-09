# Contexto maestro — EFY Analyzer / Efy Seguros

Memoria histórica entregada por Fabrizio. Usarla para recuperar antecedentes; confirmar siempre repositorio, sesiones, conectores y archivos reales antes de actuar. Las reglas operativas vigentes están en `SKILL.md` y en las referencias especializadas.

## Proyecto y responsabilidades

- Repositorio: `brazio1994/efy-analyzer`.
- Producción: `https://app.latamyanez.com`.
- Despliegue: Vercel conectado a GitHub.
- Producto: CRM/PWA para clientes y equipo interno de Efy Seguros.
- Claude trabaja lógica, funcionalidades, errores de código, Supabase, rutas, permisos e infraestructura.
- Codex trabaja estética, UX, animaciones, responsive visual y consistencia de diseño.
- Si existe duda entre visual y funcional, detenerse y preguntar.

No modificar por iniciativa propia rutas, negocio, autenticación, permisos, roles, Supabase, políticas, APIs, correo, variables, infraestructura, integraciones o datos. Tampoco alterar el comportamiento de tickets, papelera, notificaciones, archivos o perfil. Sí se permiten CSS/Tailwind, composición visual, tipografía, espaciado, color, estados vacíos, microinteracciones, transiciones, iconografía y accesibilidad visual.

## Flujo con Claude y publicación

1. Revisar `origin/main` y crear rama `agent/...` desde ahí.
2. Trabajar sólo en la rama aislada.
3. No publicar ni fusionar hasta que Fabrizio diga claramente “publícalo”.
4. Antes de publicar, incorporar lo último de `main`.
5. Ante conflictos, conservar siempre la lógica nueva de Claude y aplicar encima sólo el cambio visual.
6. Validar, crear PR hacia `main`, esperar Vercel `Ready`, fusionar sólo con autorización y verificar producción.
7. No usar Sites; la ruta real es GitHub + Vercel.

Mensaje estándar para Claude:

> Codex está trabajando sólo en la capa visual, en una rama aislada. No modifica rutas, lógica, datos, permisos ni integraciones. Antes de publicar integraremos tus cambios recientes de `main` para no sobrescribir nada.

Identidad Git verificada:

- `brazio1994`.
- `66549026+brazio1994@users.noreply.github.com`.

Usarla localmente antes de publicar para evitar rechazos de Vercel por correo no verificado. No usar `git add -A` cuando existan cambios ajenos; añadir sólo archivos autorizados.

## Dirección visual aprobada

- Tecnológica, moderna, elegante, minimalista, clara, amigable, profesional y propia de Efy.
- Azul `#445EA5`, magenta `#EC245B`, tinta `#0B1020`, fondo `#F7F8FB`.
- IBM Plex Sans para interfaz y títulos; títulos regulares `400`, datos/botones/estados normalmente `500`.
- Nunito Sans sólo para marca/display; el wordmark oficial conserva `font-extrabold`.
- Jerarquía mediante espacio, tamaño, color y composición, no mediante letras gruesas.
- Evitar tarjetas pesadas, gradientes ajenos, exceso de negrita, animaciones exageradas y desplazamiento lateral global.
- Motion de aproximadamente 160–420 ms, con opacidad, `clip-path`, color y transformaciones simples.
- Respetar `useReducedMotion` y `prefers-reduced-motion`.

## Publicación visual #57

- Fecha registrada: 31 de julio de 2026.
- PR: `https://github.com/brazio1994/efy-analyzer/pull/57`.
- Merge: `6c35d63`.
- Título: `Polish EFY interface motion and typography`.
- Integró después PR #55 (papelera personal/eliminación) y PR #56 (icono maskable Android).
- Compilación 41/41; preview Vercel `Ready`; producción verificada en `/login`.

Se ajustaron tipografía y estados en títulos, ticket, perfil, portal, login, dashboard, historial, validación, reportería, personas, papelera, versiones, novedades, notificaciones, navegación, etiquetas, badges y métricas.

Se añadieron transiciones en `PageTransition`, módulos, reportería, personas, restauración, estados vacíos, versiones, novedades, notificaciones, conversaciones, menciones, adjuntos, botones, filas, foco y selección.

Archivos relevantes del PR #57:

- `app/globals.css`.
- `components/PageTransition.tsx`, `PageHeader.tsx`, `StatCard.tsx`, `PortalShell.tsx`.
- `components/Navbar.tsx`, `Sidebar.tsx`, `NovedadesPopup.tsx`, `NotificacionesBell.tsx`.
- `components/TicketDetalle.tsx`, `TicketAdjuntos.tsx`, `TicketFila.tsx`, `BitacoraTicket.tsx`.
- `components/Avatar.tsx`, `AdminTabs.tsx`, `CambiarClave.tsx`, `PantallaError.tsx`, `AvisoNotificaciones.tsx`.

Módulos revisados: Validar, Historial, Dashboard, Reportería, Personas, Soporte, Analítica, Menciones, Papelera, Ticket/conversaciones, Versiones, Perfil, Administración, Login y Portal.

## PWA, iPhone, Android y menú

- Debe instalarse sin pasos adicionales y sentirse como aplicación a pantalla completa.
- Cuidar zonas superior e inferior; evitar zoom de inputs, barras inesperadas, cortes y scroll horizontal.
- Mantener `viewportFit: 'cover'`, soporte maskable Android y comportamiento instalado por plataforma.
- `PwaSetup`, `RefrescoAlVolver` y `EviaEntrada` están incluidos desde `app/layout.tsx`.
- No revertir ajustes de `safe-area`, fullscreen o barras sin probar en teléfonos reales.
- iOS puede imponer restricciones; no prometer fullscreen absoluto.

Problema histórico: al abrir/cerrar el menú con el botón de tres líneas en iPhone podía quedar una capa gris o negra; navegar a otro módulo la quitaba. Revisar primero overlay de `Sidebar`, `z-index`, estado `open`, `safe-area-inset-top` y composición. No alterar rutas ni navegación. Probar repetidamente en PWA instalada.

Fabrizio aclaró que iPhone antes usaba toda la pantalla sin franja negra; el negro se dejó para Android. El objetivo es recuperar pantalla completa en iPhone y evitar que el velo del menú permanezca al cerrarse.

## Evia y activos de marca

- Evia es la mascota/astronauta.
- Objetivo histórico: sustituir “Actualizando”, mostrarla en cargas/actualizaciones y al entrar, unos 3 segundos, idealmente trabajando/tecleando.
- Antes de tocarla revisar `EviaEntrada.tsx`, `PwaSetup.tsx`, `RefrescoAlVolver.tsx` y `public/brand`.
- No cambiar autenticación ni navegación del login.
- Hubo exploración con Higgsfield; no asumir que existe video final.

Rutas históricas de otra Mac:

- Evia: `/Users/fabrizioyanez/Downloads/ChatGPT Image 21 abr 2026, 06_33_33 p.m..png`.
- Símbolo EFY: `/Users/fabrizioyanez/Library/CloudStorage/OneDrive-Personal/DISEÑOS EFY/EFY REDISEÑADO/EFY-REMODELADO-SIN-SOMBRA-LOGO.png`.
- Logo completo: `/Users/fabrizioyanez/Library/CloudStorage/OneDrive-Personal/DISEÑOS EFY/EFY REDISEÑADO/EFY-REMODELADO-SIN-SOMBRA.jpg`.

El símbolo oficial debe conservarse como favicon, icono de pestaña, PWA y pantalla de inicio. Archivos vistos: `public/icon.png`, `public/icons/apple-touch-icon.png`, `public/manifest.json`, `public/brand/efy-mark.png`.

## Áreas funcionales sensibles

Papelera:

- Cada persona ve sus tickets eliminados; administración ve todos y filtra por quién borró.
- Conservar restauración, eliminación personal y período de vaciado.
- En conflictos de `app/(app)/soporte/papelera/PapeleraClient.tsx`, conservar lógica de Claude y superponer sólo animación, avisos, estado vacío, progreso y tipografía.
- No cambiar quién borró, quién puede ver ni a quién pertenece cada ticket.

Perfil: conservar toda la lógica de foto, contraseña y datos; mejorar sólo presentación cuando se solicite.

Decisiones que no se deben revertir:

- `PageTransition` sin `AnimatePresence` ni salida porque App Router podía dejar la pantalla invisible.
- Páginas/layouts usan `usuarioDeSesion()`; endpoints de escritura conservan `getUser()`.
- Adjuntos descargan por el dominio de la app para no sacar al iPhone de la PWA.
- `xlsx-js-style` se importa dinámicamente para mantener ligero el bundle inicial.

## Preview y conectores históricos

- Preview aislado: `/Users/fabrizioyanez/Documents/Codex/2026-07-29/prior-conversation-with-codex-conversation-role/efy-recent-modules-preview.html`.
- URL usada: `http://127.0.0.1:8768/efy-recent-modules-preview.html`.
- Era una maqueta local, no producción ni parte asegurada del repositorio.

Conectores consultados: Supabase, Vercel, Resend, Higgsfield y GitHub. No asumir sesiones o credenciales en otra computadora. Vercel despliega al fusionar `main`; Supabase/Resend no se tocan en trabajo visual sin orden.

- Proyecto Vercel: `efy-analyzer`; equipo `fabrizio-yanez-s-projects`.
- Supabase: `edzedlicbwrwpocoveip`, región `us-west-2`.

## Skills y validación

Usar Impeccable como auditoría principal; la versión actual consolida capacidades antes separadas como `ui-skills-root`, `baseline-ui`, motion y accesibilidad. Usar `ui-ux-pro-max` sólo cuando haga falta, `playwright-cli` o Browser para probar y `github:yeet` sólo después de “publícalo”.

Skills disponibles en esta Mac al guardar la memoria: `efy-analyzer-visual`, `impeccable`, `ui-ux-pro-max`, `frontend-design`, `playwright`, `playwright-cli`, `screenshot`, Browser/Chrome, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-deploy`, `github:yeet` e ImageGen.

Validación mínima:

```bash
npm run build
git diff --check
git status -sb
```

## Adjuntos y rutas temporales

- Adjunto histórico: `Imagen pegada 1.jpg`.
- Mostraba Soporte instalado en iPhone con franja gris/negra superior.
- Ruta temporal: `/tmp/codex-remote-attachments/019fcf22-db62-7280-8037-fa6bda2827f1/2C495987-01B5-4857-8BF3-54856C7EC42D/1-Imagen-pegada-1.jpg`.

No asumir que adjuntos, rutas temporales, logos, imágenes o videos siguen disponibles. Si un trabajo los necesita y no existen localmente, pedírselos nuevamente a Fabrizio.

## Último estado conocido al guardar

Fecha: 5 de agosto de 2026.

- Rama: `agent/blend-fullscreen-cutout`.
- Worktree: `/Users/fabrizioyanez/Documents/Codex/2026-07-29/prior-conversation-with-codex-conversation-role/work/efy-fullscreen-top`.
- Modificados: `app/layout.tsx` y `components/Sidebar.tsx`.
- Ajuste preparado: `statusBarStyle: 'black-translucent'` y overlay del menú limitado por debajo de la zona superior.
- Compilación local pasada: 39/39 páginas.
- Publicación pendiente en ese momento por autenticación de GitHub CLI.

Este último estado es histórico; comprobarlo con Git y GitHub antes de continuar.
