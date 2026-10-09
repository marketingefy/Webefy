# PWA y móviles de EfyAnalyzer

## Requisitos

- La aplicación instalada debe sentirse a pantalla completa y respetar las zonas seguras superior e inferior.
- Evitar fondo gris o negro residual al abrir y cerrar el menú lateral.
- Evitar zoom de campos en iOS, barras inesperadas, cortes de pantalla y desplazamiento horizontal global.
- Mantener `viewportFit: 'cover'` y no revertir ajustes de PWA sin probarlos.

## Problema histórico del menú en iPhone

- El fallo aparece al abrir y cerrar el menú con el botón de tres líneas: puede quedar una capa gris o negra sobre la aplicación o en la zona superior.
- Revisar primero overlay de `Sidebar`, `z-index`, estado `open`, composición del backdrop y `safe-area-inset-top`.
- No cambiar rutas ni navegación para corregirlo.
- Probar varias aperturas y cierres en PWA instalada; Chromium de escritorio no demuestra por sí solo que iOS está corregido.

## Componentes sensibles

- `PwaSetup`, `RefrescoAlVolver` y `EviaEntrada` se incluyen desde `app/layout.tsx`.
- Los adjuntos deben seguir descargándose por el dominio de la aplicación para no sacar al iPhone de la PWA.
- El manifest mantiene icono maskable en Android.
- iOS puede imponer restricciones propias; no prometer pantalla completa absoluta si el sistema no la permite.
