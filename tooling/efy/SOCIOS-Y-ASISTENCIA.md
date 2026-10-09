# Socios estratégicos y líneas de asistencia

Lista de 26 socios confirmada por el propietario el 9 de octubre de 2026.
Las asociaciones proceden de esa confirmación; las fuentes oficiales aportan los
logos y los canales de atención. No se deducen productos, coberturas ni contratos.

## Mantenimiento

`tooling/efy/socios.json` contiene el nombre, sitio oficial, logo local original,
fuente y fecha de revisión de cada socio. `logo_dark` coloca las versiones blancas
sobre una superficie oscura. Los archivos originales se descargan sin recolorear,
recortar ni reconstruir. Se presentan como imágenes locales y se comprueba su
carga en el navegador. `python3 scripts/build_site.py` genera Socios, Asistencia y
las respuestas de EVIA a partir de estos datos.

Cada línea contiene `phone`, `label`, `source` y, para WhatsApp, `channel`.
La etiqueta conserva el servicio: una oficina, citas o autorizaciones médicas no
se presentan como asistencia vehicular o atención de emergencia. Los números
se contrastaron con el texto del servicio y no sólo con enlaces `tel:`: algunos
sitios incluyen destinos de plantilla o destinos que discrepan del número visible.

Ecuasanitas confirma su call center 24/7 en su perfil oficial de LinkedIn. El logo
corresponde a la identidad presentada en 2025, con el símbolo de cintas y el
nombre EcuaSanitas, en su archivo oficial de la web actual. Se conserva la versión
blanca original sobre una superficie oscura. Se retiró el antiguo logo verde y
azul, que su archivo heredado todavía denominaba «nuevo». Referencia del cambio:
[anuncio oficial de Ecuasanitas](https://es.linkedin.com/posts/ecuasanitas_evoluci%C3%B3nqueinspira-tubienestarnuestraprioridad-activity-7323751621824319488-Wwmu).

Assist Card usa su SVG oficial con el cuadrado rojo y la marca blanca; Alianza usa
la versión naranja y gris enlazada por la cabecera de su web. No se recolorean las
versiones blancas ni se reconstruyen los símbolos. Los tres assets corregidos
tienen nombres nuevos para evitar conservar las imágenes anteriores en caché.

Assist Card muestra su WhatsApp de
asistencia en viaje y reintegros en el listado oficial; se usa el número visible
confirmado en su documentación, pues el enlace móvil de la página difiere.
Aseguradora del Sur documenta la línea de asistencia hogar en el folleto Mi Hogar;
no se generaliza esa línea a vehículos. El logo procede de la imagen configurada
como «Aseguradora logo» en su aplicación pública, no de iconos de la plantilla.

No se confirmó un teléfono vigente y apropiado para Generali o Mediken en las
fuentes revisadas. Ambas fichas enlazan a su sitio oficial y a la recomendación de
revisar la póliza. No se copian teléfonos de páginas de desarrollo, directorios de
terceros ni datos del área de privacidad como líneas de asistencia.

Consulta: los números se revisaron el 9 de octubre de 2026; pueden cambiar.
Cada ficha de Asistencia incluye la fuente para comprobar condiciones y canal.
La disponibilidad depende de la póliza o plan. ECU 911 figura por separado para
emergencias en Ecuador. La consulta de estados sigue pendiente del sistema de
origen: véase [SINIESTROS.md](SINIESTROS.md).

## Fuentes de logos

| Socio | Fuente original | Sitio oficial |
| --- | --- | --- |
| Sweaden | [Logo](https://sweadenseguros.com/wp-content/uploads/2020/01/logo-sweaden.png) | [Web](https://sweadenseguros.com/) |
| Chubb | [Logo](https://www.chubb.com/content/dam/chubb-sites/chubb/us-en/home_page/chubb-logo-black.png) | [Web](https://www.chubb.com/ec-es/) |
| Aseguradora del Sur | [Logo](https://aseguradoradelsur.com/static/images/logoCP.png) | [Web](https://aseguradoradelsur.com/) |
| Zurich | [Logo](https://amicovered.zurich.com/images/zurichLogo_EN.svg) | [Web](https://www.zurichseguros.com.ec/) |
| Seguros Unidos | [Logo](https://segurosunidos.ec/wp-content/uploads/2022/08/Seguros-Unidos.svg) | [Web](https://segurosunidos.ec/) |
| MAPFRE | [Logo](https://www.mapfre.com.ec/media/logo-mapfre.png) | [Web](https://www.mapfre.com.ec/) |
| Seguros Atlántida | [Logo](https://www.segurosatlantida.ec/_next/static/media/logo-rojo.2fpq9u-mq4ix8.webp) | [Web](https://www.segurosatlantida.ec/) |
| Ecuasanitas | [Logo](https://www.ecuasanitas.com/ecuasanitas-web/assets/img/ecuasanitas/Logo-Ecuasanitas-Blanco.svg) | [Web](https://www.ecuasanitas.com/) |
| Saludsa | [Logo](https://www.saludsa.com/wp-content/uploads/2021/03/logo_saludsa_home.svg) | [Web](https://www.saludsa.com/) |
| Humana | [Logo](https://humana.med.ec/wp-content/uploads/2025/03/humana-medicina-prepagada-logo-2025.png) | [Web](https://humana.med.ec/) |
| BMI | [Logo](https://www.bmicos.com/ecuador/wp-content/uploads/sites/9/2024/05/Logo-BMI_RGB_blanco.png) | [Web](https://www.bmicos.com/ecuador/) |
| Seguros Alianza | [Logo](https://www.segurosalianza.com/wp-content/uploads/2023/08/logoalianza_color.webp) | [Web](https://www.segurosalianza.com/) |
| Seguros del Pichincha | [Logo](https://segurosdelpichincha.com/images/shared/logo-sdp.png) | [Web](https://segurosdelpichincha.com/) |
| Interoceánica | [Logo](https://segurosinteroceanica.com/wp-content/themes/interoceanica/images/logo-default.png) | [Web](https://segurosinteroceanica.com/) |
| Generali | [Logo](https://www.generali.com/.resources/generalicom-templating-light/webresources/images/generali-logo-small.svg) | [Web](https://www.generali.com.ec/) |
| Equisuiza | [Logo](https://equisuiza.com/wp-content/uploads/2025/09/logo.svg) | [Web](https://equisuiza.com/) |
| Bupa | [Logo](https://www.bupasalud.com.ec/sites/default/files/2025-06/media/bupa-seguro-medico.svg) | [Web](https://www.bupasalud.com.ec/) |
| Assist Card | [Logo](https://www.assistcard.com/ImagesIT/assistcard.svg) | [Web](https://www.assistcard.com/ec) |
| Hispana | [Logo](https://www.hispanadeseguros.com/wp-content/uploads/2024/08/Logo-hispana-transparente-1.png) | [Web](https://www.hispanadeseguros.com/) |
| Latina Seguros | [Logo](https://latinaseguros.com.ec/wp-content/uploads/2021/11/logotipo-latina.png) | [Web](https://latinaseguros.com.ec/) |
| AIG | [Logo](https://www.aig.com.ec/content/experience-fragments/aig/lac/ecuador/es/header-nextgen/master/_jcr_content/root/responsivegrid_19588/responsivegrid_copy/container_copy_copy_/container_897891850/image_409587976.coreimg.png/1778871201638/icon-aig-logo-white.png) | [Web](https://www.aig.com.ec/) |
| VAZ Seguros | [Logo](https://vazseguros.com/wp-content/uploads/2022/01/logoVAZ.svg) | [Web](https://vazseguros.com/) |
| VidaSana | [Logo](https://vidasana.ec/images/logo_main.png) | [Web](https://vidasana.ec/) |
| Confiamed | [Logo](https://www.confiamed.com/wp-content/uploads/2025/12/confiamed.svg) | [Web](https://www.confiamed.com/) |
| Privilegio | [Logo](https://www.privilegioseguros.com.ec/wp-content/uploads/2025/12/logo-privilegio-cia-de-seguros-2.png) | [Web](https://www.privilegioseguros.com.ec/) |
| Mediken | [Logo](https://www.mediken.com.ec/assets/img/logo-mediken.png) | [Web](https://www.mediken.com.ec/) |

## Líneas verificadas

| Socio | Servicio | Número | Fuente |
| --- | --- | --- | --- |
| Sweaden | Asistencia vehicular · Claro | 099 714 3551 | [Fuente oficial](https://sweadenseguros.com/servicios/sweaden-assistance/) |
| Sweaden | Asistencia vehicular · Claro | 099 734 5298 | [Fuente oficial](https://sweadenseguros.com/servicios/sweaden-assistance/) |
| Sweaden | Asistencia vehicular · Movistar | 098 389 9042 | [Fuente oficial](https://sweadenseguros.com/servicios/sweaden-assistance/) |
| Chubb | Asistencia vehicular | 04 259 8212 | [Fuente oficial](https://www.chubb.com/ec-es/contactanos.html) |
| Chubb | Asistencia vehicular | 099 114 7216 | [Fuente oficial](https://www.chubb.com/ec-es/contactanos.html) |
| Aseguradora del Sur | Asistencia hogar · Mi Hogar | 099 555 3333 | [Fuente oficial](https://fms.aseguradoradelsur.com/asegsur/v1/fms/uploads/5ff56117-5bbe-49c9-a966-ebf694df1c58.pdf) |
| Zurich | Asistencia vehicular | 099 938 2238 | [Fuente oficial](https://www.zurichseguros.com.ec/servicios-clientes/contactanos) |
| Seguros Unidos | Asistencia en caso de siniestro | 1800 786436 | [Fuente oficial](https://segurosunidos.ec/servicios/asistencia/) |
| MAPFRE | Asistencia vehicular y hogar | 1700 627373 | [Fuente oficial](https://www.mapfre.com.ec/servicios-cliente/que-hacer/) |
| MAPFRE | Asistencia vehicular | 098 181 8182 | [Fuente oficial](https://www.mapfre.com.ec/servicios-cliente/que-hacer/) |
| Seguros Atlántida | Atención de siniestros · Línea nacional | 1800 54 23 78 | [Fuente oficial](https://www.segurosatlantida.ec/siniestros) |
| Seguros Atlántida | Atención de siniestros · WhatsApp | +593 98 490 0754 | [Fuente oficial](https://www.segurosatlantida.ec/siniestros) |
| Ecuasanitas | Call center · 24/7 | 02 395 6280 | [Fuente oficial](https://www.linkedin.com/company/ecuasanitas/) |
| Saludsa | Asistencia médica · Opción 1 · 24/7 | 02 602 0920 | [Fuente oficial](https://www.saludsa.com/contactos) |
| Saludsa | Asistencia médica · Opción 1 · 24/7 | 04 602 0920 | [Fuente oficial](https://www.saludsa.com/contactos) |
| Humana | Afiliados · Asistencia médica | 1800 486262 | [Fuente oficial](https://servicio.humana.med.ec/hc/es/articles/4417432981389--Qu%C3%A9-hacer-en-caso-de-una-emergencia) |
| Humana | Afiliados · Asistencia médica | 02 401 7000 | [Fuente oficial](https://servicio.humana.med.ec/hc/es/articles/4417432981389--Qu%C3%A9-hacer-en-caso-de-una-emergencia) |
| BMI | Autorizaciones médicas · Opción 1, subopción 1 | 1800 264264 | [Fuente oficial](https://www.bmicos.com/ecuador/directorio-de-contacto-de-clientes/) |
| BMI | Autorizaciones médicas · Opción 1, subopción 1 | 02 400 0081 | [Fuente oficial](https://www.bmicos.com/ecuador/directorio-de-contacto-de-clientes/) |
| Seguros Alianza | Asistencia vehicular y hogar · 24/7 | 02 516 9932 | [Fuente oficial](https://www.segurosalianza.com/contactos-asistencia/) |
| Seguros Alianza | Asistencia vehicular y hogar · 24/7 | 04 515 8022 | [Fuente oficial](https://www.segurosalianza.com/contactos-asistencia/) |
| Seguros del Pichincha | Atención y aviso de asistencia | 1800 400400 | [Fuente oficial](https://segurosdelpichincha.com/aviso-asistencia) |
| Interoceánica | Agenda de citas médicas | 1800 787787 | [Fuente oficial](https://segurosinteroceanica.com/) |
| Interoceánica | Servicio al cliente · Quito | 02 297 7500 | [Fuente oficial](https://segurosinteroceanica.com/) |
| Equisuiza | Asistencia · Opción 1; siniestros · Opción 2 | 1800 787878 | [Fuente oficial](https://equisuiza.com/contacto/) |
| Bupa | USA Medical Services · Asistencia médica internacional · 24/7 | +1 (305) 275 1500 | [Fuente oficial](https://www.bupasalud.com.ec/contactenos) |
| Bupa | Servicio al cliente · Ecuador | 02 401 8945 | [Fuente oficial](https://www.bupasalud.com.ec/contactenos) |
| Assist Card | Asistencia en viaje y reintegros · WhatsApp | +54 9 11 2703 9665 | [Fuente oficial](https://www.assistcard.com/listadotelefonico) |
| Hispana | Atención al cliente | 1800 447726 | [Fuente oficial](https://www.hispanadeseguros.com/) |
| Latina Seguros | Asistencia vial Latina | +593 99 230 4130 | [Fuente oficial](https://latinaseguros.com.ec/) |
| AIG | Asistencia vehicular · 24/7 | 02 395 5200 | [Fuente oficial](https://www.aig.com.ec/home/siniestros/vehiculos) |
| VAZ Seguros | Atención al cliente · Quito PBX | 02 450 4292 | [Fuente oficial](https://vazseguros.com/vazasistencia/) |
| VidaSana | Servicio al cliente · WhatsApp | +593 98 760 1828 | [Fuente oficial](https://vidasana.ec/contact) |
| Confiamed | Atención nacional · 24/7 | 1700 303030 | [Fuente oficial](https://www.confiamed.com/contactanos/) |
| Confiamed | Atención nacional · 24/7 | 1800 306030 | [Fuente oficial](https://www.confiamed.com/contactanos/) |
| Confiamed | Atención nacional · 24/7 | 02 294 3030 | [Fuente oficial](https://www.confiamed.com/contactanos/) |
| Privilegio | Servicio al cliente | 02 223 1908 | [Fuente oficial](https://www.privilegioseguros.com.ec/) |
| Privilegio | Servicio al cliente | 02 600 0700 | [Fuente oficial](https://www.privilegioseguros.com.ec/) |
