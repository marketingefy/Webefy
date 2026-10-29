> Actualización: el propietario autorizó publicar todos los cambios pendientes, con una respuesta más animada de los iconos.

# Señalamiento con luz y respuesta de iconos — vista previa

El propietario pidió una alternativa al giro: señalar, mover el icono y dar luz
a la punta del dedo. Se mantienen escena, traje, atlas de iconos y colores aprobados.

Toma de señalamientos Kling 3.0 Pro: cbacdf39-0acd-4665-8870-72ce6f17d8a9,
12 segundos sin sonido; estimación 18 créditos. Referencia sin modificar:
9a9b93a0-6a3e-4427-828b-9f37751553da.
Fuente: https://d8j0ntlcm91z4.cloudfront.net/user_33FNxc26zK65f40FTg5mKBmYy1R/hf_20261029_210630_cbacdf39-0acd-4665-8870-72ce6f17d8a9.mp4

track_pointing_finger.py analiza el guante en 288 fotogramas con segmentación
cromática, componente conectado y suavizado temporal. Produce finger-track.json;
se revisaron visualmente los tres señalamientos antes del render completo.
La luz sigue ese recorrido, con núcleo blanco y halo azul/rosa. Una señal curva
discreta enlaza el dedo con el icono activo. Los iconos no dan vueltas: flotan,
se acercan un 18%, inclinan suavemente y regresan. Misma respuesta normalizada
para Vehículo, Hogar y Salud, empezando a 1, 4 y 7 s de la toma original.

Render con EFY_HERO_OUTPUT=/workspace/output/efy-evia-dedo-luz-20261029.
Exportación en H.264 de 11,5 s, escritorio 1280x720 y móvil 720x800, silenciosa,
con posters y bucle enlazado. HTML autocontenido en la misma carpeta.
No se envía esta rama a producción sin revisar antes la propuesta.
