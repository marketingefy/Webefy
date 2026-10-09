# Memoria funcional y límites de EfyAnalyzer

## Responsabilidades

- Claude y otros agentes funcionales construyen lógica, flujos, Supabase, permisos, APIs, notificaciones, correo e infraestructura.
- Codex preserva esa funcionalidad y trabaja por defecto en estética, UX, responsive, accesibilidad, animaciones, recursos de marca y consistencia visual.

## Funcionalidad existente que debe preservarse

- Sesiones y perfiles con roles `ADMIN`, `INTERNO` y `CLIENTE`.
- `CARTERAS` agrupa Validar, Historial, Alertas y Dashboard como un solo módulo concedible.
- Soporte incluye tickets, adjuntos, comentarios, notas internas, asignaciones, bitácora, recordatorios, menciones, visibilidad y papelera.
- Notificaciones funcionan en tiempo real y mediante push; el service worker no cachea la aplicación, solo la pantalla sin conexión.
- Existen Reportería, Perfil, administración de usuarios/aseguradoras/cooperativas/pólizas y portal de clientes.

## Decisiones técnicas que no se deben revertir

- `PageTransition` no usa `AnimatePresence` ni salida: al volver con App Router podía dejar la pantalla invisible.
- Páginas y layouts usan `usuarioDeSesion()`; endpoints de escritura conservan `getUser()`.
- Adjuntos se descargan por el dominio de la aplicación para no sacar al iPhone de la PWA.
- `xlsx-js-style` se importa dinámicamente para mantener ligero el bundle inicial.
- Proteger `safe-area`, pantalla completa y comportamiento instalado por plataforma; separar correcciones de iOS y Android.

## Papelera

- Cada persona ve sus propios tickets eliminados; administración puede ver el conjunto y filtrar por quién borró.
- Mantener intactos restauración, eliminación personal, período de vaciado y el significado de quién borró o puede ver cada ticket.
- Si hay conflicto en `app/(app)/soporte/papelera/PapeleraClient.tsx`, conservar la lógica de Claude y superponer sólo presentación, animación, avisos, estado vacío y tipografía.

## Evia y recursos de marca

- Antes de tocar Evia, revisar `components/EviaEntrada.tsx`, `components/PwaSetup.tsx`, `components/RefrescoAlVolver.tsx` y los assets existentes en `public/brand`.
- Mantener la entrada aproximada de 3 segundos y no cambiar autenticación ni navegación del login.
- No asumir que existe un video final de Higgsfield ni que rutas de otra Mac siguen disponibles; verificar primero.
- Preservar el símbolo oficial como favicon, icono de pestaña, icono PWA y `apple-touch-icon`; no sustituirlo por recursos genéricos.

## Publicación

- Producción se despliega desde `main` en Vercel.
- Flujo acordado: rama y PR, preview `Ready`, fusión a `main` y verificación de producción.
- Producción: `https://app.latamyanez.com`; repositorio: `brazio1994/efy-analyzer`.
- Última publicación visual registrada: PR #57, merge `6c35d63`, “Polish EFY interface motion and typography”.
- Proyecto Vercel: `efy-analyzer`; equipo: `fabrizio-yanez-s-projects`.
- Proyecto Supabase: `edzedlicbwrwpocoveip` en `us-west-2`.
- No tocar Supabase, Resend, Vercel, GitHub u otras integraciones por trabajo visual salvo orden explícita.
