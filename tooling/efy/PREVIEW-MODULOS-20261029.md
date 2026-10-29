# Efy: revisión de módulos, sin publicar

Petición vigente: mostrar estos cambios en vista previa antes de publicarlos.
Trabajo aislado en `/workspace/efy-module-preview-20261029`, rama local
`preview/efy-module-refinement-20261029`. La web publicada sigue en `a78c695`.
No se debe enviar esta rama a producción sin una nueva instrucción del propietario.

## Propuesta

- Inicio: recuperar «Elegir bien. Vivir con tranquilidad.» y «Protege lo que más
  importa. Encuentra tu seguro con asesoría cercana.». Nueva toma con la misma
  orientación y diseño de EVIA al pasar por el holograma de salud.
- Conócenos: video de bienvenida, trayectoria y escudo familiar; conserva los
  cinco años de Efy, más de quince de experiencia y los tres párrafos del propietario.
- Reseñas: video de escucha y agradecimiento con dos burbujas de conversación.
  Las opiniones de demostración existentes conservan su identificación; no se
  añaden valoraciones, nombres ni reseñas supuestamente reales.
- Ambos videos se integran sobre `#080e1d`, con mezcla `lighten` y máscara
  suave en los cuatro bordes. Sin tarjeta ni marco. Pausan fuera de vista y
  respetan movimiento reducido, pestaña oculta y ahorro de datos.
- Inicio incluye los 26 aliados, con sus nombres y archivos aprobados. Las cuatro
  versiones blancas (Zurich, BMI, AIG, VAZ) reciben soporte oscuro. No se recolorean.
  La carga explícita permite comprobarlos todos en la vista previa.
- Contacto: cabecera con conexiones de cristal, acceso por equipo, cuatro enlaces
  correctos a WhatsApp, correos, redes y ubicación. Dirección una sola vez.
- Menú: despliegue vertical con puntero en computadora, teclado y Escape; en táctil
  abre con toque. Servicios usa una sola columna con desplazamiento cuando falta altura.
- Logo blanco: 180 px en escritorio, 162 px intermedio y 148 px en celular,
  con ligera reducción de intensidad. Se conservan los colores e IBM Plex Sans.

## Medios

Referencias generadas, conservadas sin sustituir los originales:

- Conócenos: `/workspace/generated_images/exec-0a470734-4912-48cb-82da-02bfe1d2614a.png`.
- Reseñas: `/workspace/generated_images/exec-64876d54-54a3-4a83-84df-ce2253225409.png`.
- Medios confirmados: `0af89dea-3cfd-4134-8711-9316163aa291` y
  `ff86955a-7158-4b01-a286-d48862ede27d`.

Kling 3.0 Pro, sin sonido, primer y último fotograma con la misma referencia:

- Inicio: `5bc71bc6-e988-4351-a0ca-e847b9782f70`, 10 s, estimación de 15 créditos.
- Conócenos: `1a755518-bde9-4fb2-964d-012e776a97fc`, 8 s, 12 créditos.
- Reseñas: `cfba456f-0014-4045-a3f5-89dd8fec0561`, 8 s, 12 créditos.

Los originales están en `/workspace/output/efy-module-preview-20261029/`.
`prepare_review_films.py` produce H.264, 24 fps, sin audio, faststart, con una
disolución de 0,5 s entre extremos: 9,5 s para inicio y 7,5 s para cada módulo.
Inicio tiene encuadres independientes de 1280×720 y 720×800; módulos, 720×960.

## Revisión entregable

`package_module_preview.py` genera un único archivo de unos 5,2 MB:
`/workspace/output/efy-module-preview-20261029/Efy-vista-previa-interactiva.html`.
Integra 17 páginas, 60 recursos, fuentes, logos y videos. No requiere recursos
externos. Permite recorrer módulos y cambiar el ancho de revisión. Las peticiones
a servidores y los envíos de formularios quedan bloqueados en este artefacto;
esa limitación se informa en la barra de vista previa y no cambia el sitio real.

En la misma carpeta se encuentran el recorrido MP4, capturas de escritorio y
celular, los tres videos terminados y los originales. La generación no publica.

## Verificación

- 78 vistas de páginas raíz y `/nueva/`, navegación, cotización, tipografía real,
  reproducción en ambos formatos, pausa fuera de vista y alternativa estática.
- Hover en los seis desplegables; Servicios vertical en una columna.
- Artefacto sin peticiones externas, 26 logos decodificados, cuatro soportes
  oscuros, los cuatro WhatsApp y reproducción de los tres videos.
- Cinco módulos revisados a 390 px y sus composiciones de escritorio.
- Revisión visual de los tres videos y reinicios; archivos públicos de la
  copia de trabajo principal permanecen intactos.
