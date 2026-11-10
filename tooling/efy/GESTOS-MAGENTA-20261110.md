# Gestos del inicio y trayectoria en magenta cristalino

EVIA mantiene el PNG regenerado aprobado. La mano y el antebrazo ahora siguen tres poses distintas, sincronizadas con la activación de Vehículo, Hogar y Salud. El brazo conserva una pose intermedia durante la transición, sin volver bruscamente al reposo entre iconos. El casco acompaña la selección con una pequeña inclinación y la luz sigue la punta del dedo. La mesa permanece fija. El film conserva Full HD, transparencia y 25 segundos de ida y vuelta.

La animación se compone mediante deformación continua del PNG, con transición suave en el codo, sin cortar piezas ni volver a segmentar el casco/traje sobre un fondo. El movimiento, el compositor, el atlas de iconos y la curva temporal quedan versionados para futuras correcciones.

Los dos cuadros de trayectoria usan magenta translúcido con reflejo superior, borde rosa y desenfoque de 22 px. Cifras blanco rosado y descripciones claras reemplazan el azul/rosa oscuro anterior. Se conserva el contador de 5 y 15 y se respeta la preferencia de movimiento reducido.

## Reproducir la exportación

```sh
node tooling/efy/render-hero-gesture.cjs --render --out=/tmp/efy-hero
python tooling/efy/encode-hero-gesture.py --out=/tmp/efy-hero
python scripts/build_site.py
```

Requiere Chromium, Playwright, ffmpeg y Pillow. La prueba de alfa también usa numpy/scipy. No necesita Higgsfield ni genera nuevos personajes.

## Comprobaciones

- `node tests/media/hero-gesture.test.cjs`: gesto visible en cada icono, sincronización, transición continua y retorno suave.
- `python tests/media/check_png_source.py --previous`: reproduce la falta de movimiento en el film anterior; la palma no sigue la nueva trayectoria en el fotograma 33.
- `python tests/media/check_png_source.py`: 600 fotogramas, 202 330 píxeles estables del PNG y seguimiento de la palma articulada; pérdida interior 0 %. La comprobación de Servicios también sigue pasando.
- Recorrido guiado de 78 vistas con IBM Plex real. Revisión del inicio en cuatro poses y tamaños de 390/1440 px. Sin errores JavaScript ni desbordamientos.
- En Conócenos, ambos contadores llegan a 5 y 15. Las dos vistas confirman el cristal magenta, desenfoque y colores claros; pruebas de caché y sintaxis correctas.

Las vistas previas están en `/workspace/output/efy-gestos-magenta-20261110/`. Esta versión se prepara para revisión antes de publicar, conforme a la preferencia del propietario.
