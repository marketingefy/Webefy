# 001 — Afinar el movimiento de la interfaz compartida

- **Status**: DONE
- **Commit base**: `94b683b`
- **Severity**: LOW
- **Category**: Easing, cohesion, accessibility, missed opportunities
- **Estimated scope**: `public/assets/site/efy-site.css`; sin dependencias nuevas.

## Problema y alcance

La web completa comparte CSS y conserva el chat nativo, sus menús y los videos
aprobados. La persona solicitó aplicar las mejoras preservando colores y
funcionamiento. La revisión de `improve-animations` se limita a planificar;
la implementación se realiza con las skills de interfaz y la revisión posterior
con `review-animations`.

Valores de la versión base, en `public/assets/site/efy-site.css:5`, `:56` y `:61`
(la numeración puede variar tras la implementación):

```css
--ease:cubic-bezier(.2,.8,.2,1);
.chat-message{animation:evia-message-in 180ms ease-out}
.experience-stat{transition:transform 450ms ease,opacity 450ms ease}
```

El diálogo se abría de inmediato y varios controles carecían de respuesta al
pulsarlos. Son oportunidades de acabado, no fallos del flujo de conversación.

## Objetivo exacto

```css
:root{
  --ease:cubic-bezier(.23,1,.32,1);
  --duration-feedback:160ms;
  --duration-enter:200ms;
}
.evia-dialog[open]{
  opacity:1;
  transform:translateY(0) scale(1);
  transition:opacity var(--duration-enter) var(--ease),
             transform var(--duration-enter) var(--ease);
}
@starting-style{
  .evia-dialog[open]{opacity:0;transform:translateY(6px) scale(.98)}
}
```

La pulsación usa `scale(.97)` con 160 ms en menú, cierre, filtros, botón flotante,
opciones del chat, acciones rápidas, envío y controles de reseñas habilitados.
Los mensajes conservan 180 ms usando la curva compartida. La entrada existente
de estadísticas se reduce a 320 ms con la misma curva.

## Convenciones y pasos

1. Reutilizar `--ease` de `:root` y añadir los dos tokens de duración.
2. Mantener el keyframe existente `evia-message-in`; cambiar solamente su curva.
3. Afinar la transición existente de `.experience-stat` sin modificar sus
   disparadores ni el conteo de cifras.
4. Añadir la entrada CSS del diálogo con `@starting-style`. Los navegadores
   que no lo admitan conservan la apertura nativa inmediata.
5. Añadir respuesta a la pulsación. Excluir botones de reseñas deshabilitados.
6. Limitar hover a `(hover:hover) and (pointer:fine)`.
7. Añadir la anulación de transiciones y transformaciones nuevas en
   `@media(prefers-reduced-motion:reduce)` y asegurar opacidad final 1.

## Límites

- Conservar los eventos, foco, `showModal()`, Escape y cierre nativo inmediato.
- Mantener textos, navegación, formularios, contactos, colores y medios.
- Conservar el control de reproducción por visibilidad y ahorro de datos.
- No añadir animación a los títulos ni a la navegación con teclado.
- No introducir bibliotecas, retrasos de interacción ni cambios de alojamiento.

## Comprobación y resultado

- `python3 scripts/build_site.py` y `git diff --check`: correctos.
- Prueba de portada en 320, 390, 768 y 1440 px: menú, chat, respuesta, Escape
  y devolución de foco correctos.
- Apertura observada con `getAnimations()`: dos `CSSTransition`, de opacidad
  y transformación, con duración de 200 ms.
- Inspección visual de chat abierto en móvil y escritorio: el contenido termina
  estable y legible; no hay entrada desde una escala extrema.
- Movimiento reducido: sin reproducción automática del video ni transiciones
  nuevas. Con reproducción bloqueada se mantiene el póster.
- Hashes de JavaScript, PHP y MP4 idénticos a la base.

**Terminado cuando:** las nuevas respuestas visuales no impiden ninguna acción,
se desactivan con movimiento reducido y se conservan los contratos funcionales.
Estas condiciones quedaron verificadas.
