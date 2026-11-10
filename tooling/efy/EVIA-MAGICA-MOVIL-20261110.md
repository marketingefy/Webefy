# EVIA dinámica, marcas legibles y Contacto móvil

La versión b3498fd aprobada fue publicada y verificada en producción. Durante ese despliegue el propietario pidió más movimiento natural en EVIA, destellos como una varita desde el dedo, los fondos azules de BMI/AIG y corregir la transparencia de Contacto en celular. Esta nueva revisión se prepara por separado para mostrarla antes de publicar.

## Inicio

Se generaron ocho segundos nuevos en Higgsfield, usando la misma EVIA y la mesa como referencia: inclinación del torso, orientación del casco, articulación de hombro/codo/muñeca y presentación de tres opciones. La fuente original se conserva en `tooling/efy/media/evia-native-magica-20261110.mp4` (job `a9c4e714-effb-43c1-afa8-138a8c56824c`).

Se extrae la transparencia desde un fondo de croma uniforme; casco, traje, manos, mesa y botas permanecen completos. Los huecos reales entre brazo y torso se mantienen transparentes. No se rellenan todos los huecos de la silueta: eso conservaría fondo verde en esos espacios. La revisión ampliada detectó ese problema antes de publicar, y se agregó una comprobación de color además de la comparación de alfa.

El dedo se sigue con anclajes y flujo óptico, refinando la posición sobre los píxeles del guante. Los destellos son deterministas, blancos, azules y rosa magenta; salen del punto de contacto, acompañan el gesto y producen una respuesta breve del icono. Los hologramas se colocan por debajo del dedo para conservarlo visible. La secuencia va y regresa sin corte durante 16 segundos y respeta el modo de movimiento reducido mediante un PNG estático.

Para reconstruir con Python/OpenCV/numpy/scipy/Pillow, ffmpeg y Playwright/Chromium:

```sh
python tooling/efy/prepare-hero-native.py --out=/tmp/efy-magic
node tooling/efy/render-hero-magic.cjs --render --out=/tmp/efy-magic
python tooling/efy/encode-hero-magic.py --out=/tmp/efy-magic
python scripts/build_site.py
```

## BMI y AIG

Las marcas oficiales blancas y su indicador `on-dark` ya existían; una regla posterior de la escena imponía blanco a todos los fondos de logos. Se restauran fondos azules explícitos para estas dos tarjetas en todos los tamaños. No se modifican los archivos de marca. También se aclara el texto del desplegable de teléfonos para hacerlo legible sobre el panel oscuro.

## Contacto en celular

Se conserva el reproductor de video transparente de escritorio. En pantallas móviles, Contacto usa una animación WebP RGBA nativa y un fondo de animación transparente. No depende de subir fotogramas de un video oculto a WebGL en Safari. En movimiento reducido, `picture` selecciona el PNG estático. En móvil no se descarga el MP4 empaquetado. El helper `tooling/efy/encode-contact-mobile.py` reconstruye el archivo y su metadato de fondo transparente.

## Validación

- 384 fotogramas de inicio contrastados con las siluetas completas de la fuente nativa y vuelta al mismo fotograma.
- Comprobación adicional de color para impedir restos verdes opacos entre cuerpo y brazos.
- 180 fotogramas de Contacto con alfa transparente en sus cuatro esquinas y fondo de animación RGBA cero.
- Chromium y WebKit, 390 y 1440 px: marcas visibles sobre azul, Contacto con alfa, sin desbordamientos ni errores JavaScript. En móvil se selecciona el WebP; en movimiento reducido, el PNG.
- Recorrido guiado de 78 vistas más comprobaciones de las marcas y de Contacto móvil en ambas rutas.

Vistas e intermedios: `/workspace/output/efy-evia-magica-20261110/`.


Resultado final: 384 fotogramas completos sin pérdida de alfa, 96 muestras de color sin restos verdes opacos (la exportación intermedia fallaba con 4 871 píxeles verdes), 180 fotogramas móviles transparentes, recorrido guiado de 78 vistas y pruebas de Contacto/Aliados en Chromium y WebKit a 390/1440 px. Se conserva la reproducción estática en movimiento reducido. Las comprobaciones de Contacto y fondos de marca se incorporan también al despliegue automático con Chromium. La nueva vista previa de la varita se mostró en la conversación antes de continuar la publicación que el propietario solicitó y fue ampliando con estas correcciones.
