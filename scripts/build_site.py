"""Build the published Efy website and preview from shared navigation, services and FAQ data."""
import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE_VERSION = 'efy-web-glass-dropdowns-20261013'
OUT = ROOT / 'public' / 'nueva'
OUT.mkdir(exist_ok=True)
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
CONTACTS = json.loads((ROOT / 'tooling/efy/contactos.json').read_text())
for department in CONTACTS['departments']:
    if not department['name'].strip() or not all(re.fullmatch(r'0[0-9]{9}', phone) for phone in department['phones']):
        raise ValueError('Contact departments need a name and valid Ecuador phone numbers')
for email in [item['address'] for item in CONTACTS['emails']] + [CONTACTS['error_email']]:
    if not re.fullmatch(r'[a-z0-9._+-]+@efyseguros\.com', email):
        raise ValueError('Contact email must be an Efy address')
def display_phone(phone):
    return f'{phone[:3]} {phone[3:6]} {phone[6:]}'

COMMERCIAL = next(department for department in CONTACTS['departments'] if department['name'] == 'Comercial')
WHATSAPP = [{'phone': phone, 'label': display_phone(phone), 'url': 'https://wa.me/593' + phone[1:]} for phone in COMMERCIAL['phones']]
def whatsapp_url(message='', index=0):
    return WHATSAPP[index]['url'] + ('?text=' + quote(message) if message else '')

ABOUT = json.loads((ROOT / 'tooling/efy/conocenos.json').read_text())
for milestone in ABOUT['milestones']:
    if type(milestone['years']) is not int or milestone['years'] < 0 or milestone['prefix'] not in ('', '+'):
        raise ValueError('About milestones need owner-confirmed years and a supported prefix')

SERVICES = json.loads((ROOT / 'tooling/efy/servicios.json').read_text())
service_ids = set()
for service in SERVICES:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', service['id']) or service['id'] in service_ids:
        raise ValueError('Every service needs a unique URL-safe id')
    for field in ('name', 'description'):
        if not isinstance(service[field], str) or not service[field].strip():
            raise ValueError(f'Service {field} must contain confirmed text')
    if not isinstance(service.get('details'), list) or not all(isinstance(item, str) and item.strip() for item in service['details']):
        raise ValueError('Service details must be a list of confirmed text')
    service_ids.add(service['id'])
    if service.get('group') not in ('Movilidad', 'Salud', 'Vida y bienestar', 'Patrimonio y actividad'):
        raise ValueError('Service needs a supported catalogue group')
service_answer = ('En Servicios puedes consultar estos tipos de seguros: ' + ', '.join(service['name'] for service in SERVICES) + '. Revisa el detalle de cada uno y prepara tus preguntas para Efy. Las condiciones dependen de la propuesta y de la póliza.' if SERVICES else 'Estamos preparando el catálogo de seguros de Efy. En Servicios encontrarás el detalle de cada tipo cuando esté disponible. Mientras tanto, puedes revisar qué preguntar antes de elegir y preparar tu consulta en Contactos.')
PARTNERS = json.loads((ROOT / 'tooling/efy/socios.json').read_text())
partner_ids = set()
for partner in PARTNERS:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', partner['id']) or partner['id'] in partner_ids:
        raise ValueError('Every partner needs a unique URL-safe id')
    if not isinstance(partner['name'], str) or not partner['name'].strip():
        raise ValueError('Partner name must contain confirmed text')
    partner_ids.add(partner['id'])
partner_answer = ('Los socios estratégicos con los que trabaja Efy son: ' + ', '.join(partner['name'] for partner in PARTNERS) + '. Puedes conocerlos en Socios estratégicos y revisar sus canales oficiales en Asistencia.' if PARTNERS else 'Estamos preparando la presentación de los socios estratégicos con los que trabaja Efy. Si necesitas identificar tu aseguradora actual, revisa tu póliza o certificado.')
def official_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or any(char.isspace() or ord(char) < 32 for char in value):
        raise ValueError('Official source must be a valid HTTPS URL without credentials')

for partner in PARTNERS:
    if partner.get('website'):
        official_url(partner['website'])
    if partner.get('logo_source'):
        official_url(partner['logo_source'])
    if partner.get('logo'):
        if not re.fullmatch(r'assets/site/partners/[a-z0-9-]+\.(?:png|jpg|jpeg|webp|svg)', partner['logo']):
            raise ValueError('Partner logo must be a local image asset')
        if not (ROOT / 'public' / partner['logo']).is_file():
            raise ValueError('Partner logo asset is missing')
    for line in partner.get('assistance', []):
        if not re.fullmatch(r'\+?[0-9 ()-]{7,24}', line['phone']) or not 7 <= len(re.sub(r'\D', '', line['phone'])) <= 15:
            raise ValueError('Assistance line needs a valid phone number')
        official_url(line['source'])
        if not line['label'].strip():
            raise ValueError('Assistance line needs an official source and service label')
        if line.get('channel', 'phone') not in ('phone','whatsapp'):
            raise ValueError('Unsupported assistance channel')
REVIEW_DATA = json.loads((ROOT / 'tooling/efy/resenas.json').read_text())
REVIEWS = REVIEW_DATA['items']
def review_url(value):
    if value is None:
        return None
    if not isinstance(value, str) or any(char.isspace() or ord(char) < 32 for char in value):
        raise ValueError('Review source must be a valid HTTPS URL')
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Review source must be a valid HTTPS URL without credentials')
    return value

REVIEW_PROFILE = review_url(REVIEW_DATA.get('profile_url'))
review_ids = set()
for review in REVIEWS:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', review['id']) or review['id'] in review_ids:
        raise ValueError('Every review needs a unique URL-safe id')
    for field in ('author', 'text'):
        if not isinstance(review[field], str) or not review[field].strip():
            raise ValueError(f'Review {field} must contain real customer text')
    rating = review.get('rating')
    if rating is not None and (type(rating) is not int or not 1 <= rating <= 5):
        raise ValueError('Review rating must be an integer from 1 to 5, or omitted')
    if review.get('date') is not None:
        if date.fromisoformat(review['date']).isoformat() != review['date']:
            raise ValueError('Review date must use YYYY-MM-DD')
    review_url(review.get('source_url'))
    review_ids.add(review['id'])
review_answer = ('Puedes leer las opiniones de clientes en el apartado Reseñas.' if REVIEWS or REVIEW_PROFILE else 'El apartado Reseñas está preparado para compartir las opiniones de clientes de Efy. Estamos reuniendo las reseñas para publicarlas allí.')
DEMO_DATA = json.loads((ROOT / 'tooling/efy/resenas-demo.json').read_text())
DEMO_REVIEWS = DEMO_DATA['items'] if DEMO_DATA.get('simulation') is True and not REVIEWS else []
if DEMO_REVIEWS:
    if len(DEMO_REVIEWS) != 10 or any(not re.fullmatch(r'demo-[a-z-]+', item['id']) or type(item['rating']) is not int or not 1 <= item['rating'] <= 5 for item in DEMO_REVIEWS):
        raise ValueError('Review demonstration needs ten explicitly fictional examples')
    review_answer = 'Puedes ver una muestra del diseño en Reseñas, con diez comentarios y estrellas ficticios claramente identificados. Las opiniones reales de clientes se incorporarán cuando estén disponibles; esta muestra no procede de Google.'
FAQ = [
    {'id':'lineas','category':'Si ocurre un evento','question':'¿Dónde encuentro las líneas de asistencia?','answer':'En Asistencia puedes buscar tu aseguradora o proveedor y consultar sus canales oficiales. Cada línea indica a qué servicio corresponde y enlaza a su fuente. Si hay una emergencia en Ecuador, llama al 911. Verifica en tu póliza o plan las condiciones de la asistencia.'},
    {'id':'estado','category':'Si ocurre un evento','question':'¿Puedo consultar el estado de mi siniestro o reembolso?','answer':'En Asistencia puedes preparar una consulta al equipo por cédula o, para un siniestro vehicular, por placa. Revisa el resumen y abre tu correo para enviarlo a siniestros@efyseguros.com. La web todavía no consulta un registro de estados; el equipo debe verificar tu identidad antes de compartir información. EVIA no accede a los casos.'},
    {'id':'resenas','category':'Sobre Efy','question':'¿Dónde puedo leer las reseñas de clientes de Efy?','answer':review_answer},
    {'id':'socios','category':'Sobre Efy','question':'¿Cuáles son los socios estratégicos de Efy?','answer':partner_answer},
    {'id':'servicios','category':'Sobre Efy','question':'¿Qué tipos de seguros ofrece Efy?','answer':service_answer},
    {'id':'elegir','category':'Antes de elegir','question':'¿Por dónde empiezo para elegir un seguro?','answer':'Empieza por lo que quieres proteger y por los riesgos que te preocupan. Después compara coberturas, exclusiones, deducibles, límites y costo. Una propuesta debe ayudarte a entender qué incluye y qué queda fuera.'},
    {'id':'cotizar','category':'Antes de elegir','question':'¿Qué información preparo para pedir una cotización?','answer':'Anota qué quieres proteger, qué cobertura buscas y las preguntas que necesitas resolver. Los datos y documentos necesarios dependen del tipo de seguro y de la aseguradora. Confirma los requisitos por un canal oficial antes de enviar información personal.'},
    {'id':'cobertura','category':'Tu póliza','question':'¿Qué es una cobertura?','answer':'Es la protección que la póliza ofrece para un riesgo o una situación determinada. Su alcance depende de las condiciones, los límites y las exclusiones que aparecen en el contrato.'},
    {'id':'deducible','category':'Tu póliza','question':'¿Qué significa deducible?','answer':'Es la parte del costo de un evento cubierto que corresponde asumir al asegurado, cuando así lo establece la póliza. Puede expresarse como un valor, un porcentaje o una combinación. Revisa cuándo se aplica y cómo se calcula.'},
    {'id':'exclusiones','category':'Tu póliza','question':'¿Qué son las exclusiones?','answer':'Son las situaciones o los riesgos que la póliza no cubre. Antes de elegir, revisa las exclusiones junto con las coberturas y pregunta por cualquier condición que no entiendas.'},
    {'id':'renovar','category':'Tu póliza','question':'¿Qué reviso antes de renovar mi seguro?','answer':'Comprueba la fecha de vencimiento, las coberturas, los límites, los deducibles, el costo y los cambios en tus necesidades. Confirma las condiciones de la nueva vigencia antes de aceptarla.'},
    {'id':'siniestro','category':'Si ocurre un evento','question':'¿Qué hago si necesito reportar un siniestro?','answer':'Prioriza tu seguridad. Si hay una emergencia, llama al 911 en Ecuador. Puedes informar a Efy desde el apartado Asistencia; el reporte se envía a siniestros@efyseguros.com. También debes seguir los canales y plazos de tu aseguradora indicados en la póliza. Este aviso a Efy no confirma cobertura ni sustituye el aviso exigido por la aseguradora.'},
    {'id':'documentos','category':'Si ocurre un evento','question':'¿Dónde encuentro los canales de asistencia de mi seguro?','answer':'Consulta tu póliza, certificado o documentación de la aseguradora. Allí debes verificar los teléfonos y el procedimiento aplicable. La guía de EVIA no recibe reportes ni reemplaza los canales de asistencia de tu aseguradora.'},
    {'id':'ubicacion','category':'Sobre Efy','question':'¿Dónde está Efy?','answer':'Efy está en Quito. La dirección y los canales oficiales de atención se incorporarán cuando estén confirmados.'},
    {'id':'contacto','category':'Sobre Efy','question':'¿Cómo puedo contactar a Efy?','answer':'Estamos preparando los canales oficiales de contacto, incluido WhatsApp. Mientras tanto, puedes consultar esta guía o preparar tu consulta en el módulo Contactos. EVIA no envía mensajes ni solicitudes al equipo.'},
    {'id':'evia','category':'Sobre Efy','question':'¿Quién es EVIA y cómo funciona este chat?','answer':'EVIA es la guía digital de esta web. Este chat responde a partir de las preguntas frecuentes de Efy: ofrece información general y te ayuda a preparar preguntas. No consulta pólizas, no cotiza y no confirma coberturas particulares.'},
]

RESEARCH = json.loads((ROOT / 'tooling/efy/preguntas-frecuentes.json').read_text())
for item in RESEARCH['items']:
    if item['id'] in {question['id'] for question in FAQ} or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['id']):
        raise ValueError('Researched FAQ needs a unique URL-safe id')
    source = RESEARCH['sources'][item['source']]
    official_url(source['url'])
    FAQ.append({**item, 'source': source})

for faq in FAQ:
    if faq['id'] == 'ubicacion':
        faq['answer'] = f"Estamos en {CONTACTS['city']}: {CONTACTS['address']}. Encuentra nuestros canales en Contáctanos."
    if faq['id'] == 'contacto':
        faq['answer'] = f'Puedes hablar con el equipo comercial por WhatsApp al {" o al ".join(COMMERCIAL["phones"])}. Elige uno de los accesos para abrir la conversación. También puedes escribir a info@efyseguros.com. Para siniestros y reembolsos, escribe a siniestros@efyseguros.com.'

home = f'''
<section class="home-hero" aria-labelledby="page-title">
  <figure class="workshop" aria-hidden="true">
    <picture><source media="(max-width:760px)" srcset="../assets/evia-workshop-mobile.webp?v=evia-wide-restored-20261009"><img src="../assets/evia-workshop.webp?v=evia-wide-restored-20261009" alt="" width="1280" height="720" fetchpriority="high"></picture>
    <video class="workshop-video" muted playsinline loop preload="none" tabindex="-1"></video><div class="workshop-shade"></div>
  </figure>
  <div class="container hero-copy">
    <h1 id="page-title">Elegir bien.<br>Vivir con<br><span>tranquilidad.</span></h1>
    <p class="hero-lead">Elegir un seguro empieza por entenderlo.<br>Conoce Efy y encuentra el próximo paso para ti.</p>
    <div class="actions"><a class="button primary" href="nosotros.html">Conócenos {ARROW}</a><button class="button ghost" type="button" data-open-chat>Habla con EVIA</button></div>
  </div>
  <p class="scene-note"><span></span>EVIA, dando forma a nuestro universo digital.</p>
</section>
<section class="section container" aria-labelledby="start-title">
  <div class="section-heading"><p class="eyebrow">A TU RITMO</p><h2 id="start-title">La información que necesitas.<br><span>Un lugar para encontrarla.</span></h2></div>
  <div class="editorial-links">
    <a class="editorial-link" href="servicios.html"><div><p class="small-label">SERVICIOS</p><h3>Empieza por lo que quieres proteger.</h3><p>Conoce nuestro apartado de seguros y qué revisar antes de elegir.</p></div>{ARROW}</a>
    <a class="editorial-link" href="socios.html"><div><p class="small-label">SOCIOS ESTRATÉGICOS</p><h3>Las aseguradoras con las que trabajamos.</h3><p>Un espacio para conocer a nuestros socios estratégicos.</p></div>{ARROW}</a>
    <a class="editorial-link" href="nosotros.html"><div><p class="small-label">CONÓCENOS</p><h3>Conoce el mundo de Efy.</h3><p>Nuestra identidad, lo que nos mueve y EVIA, nuestra guía digital.</p></div>{ARROW}</a>
    <a class="editorial-link" href="asistencia.html#reportar"><div><p class="small-label">ASISTENCIAS</p><h3>Encuentra tu siguiente paso.</h3><p>Reporta un siniestro, consulta por tu caso y encuentra líneas de atención.</p></div>{ARROW}</a>
    <a class="editorial-link" href="resenas.html"><div><p class="small-label">RESEÑAS</p><h3>La experiencia de nuestros clientes.</h3><p>Un espacio para sus opiniones sobre Efy.</p></div>{ARROW}</a>
    <a class="editorial-link" href="contactos.html"><div><p class="small-label">CONTACTOS</p><h3>Encuentra tu siguiente paso.</h3><p>Prepara tus preguntas y conoce los canales de atención de Efy.</p></div>{ARROW}</a>
    <a class="editorial-link" href="ayuda.html"><div><p class="small-label">AYUDA</p><h3>Entiende antes de decidir.</h3><p>Respuestas sobre coberturas, deducibles y conceptos de tu póliza.</p></div>{ARROW}</a>
  </div>
</section>
<section class="guide-section"><div class="container guide-grid"><div><p class="eyebrow light">CONOCE A EVIA</p><h2>Una guía cercana.<br><span>Para preguntas reales.</span></h2><p>EVIA te ayuda a encontrar información general sobre seguros y a organizar lo que quieres consultar.</p><button class="button primary" type="button" data-open-chat>Iniciar una conversación {ARROW}</button></div><div class="chat-preview"><div class="avatar-row"><img src="../assets/site/evia-portrait.jpg" alt="" width="56" height="56" loading="lazy"><div><strong>EVIA</strong><span>Guía de preguntas frecuentes</span></div></div><p class="preview-message">Hola, soy EVIA. ¿Qué te gustaría entender mejor?</p><button type="button" class="suggestion" data-chat-question="¿Qué significa deducible?">¿Qué significa deducible? {ARROW}</button><button type="button" class="suggestion" data-chat-question="¿Por dónde empiezo para elegir un seguro?">¿Por dónde empiezo? {ARROW}</button></div></div></section>
'''

experience_stats = ''.join(f'<article class="experience-stat"><p class="experience-number"><span aria-hidden="true">{item["prefix"]}<span data-count="{item["years"]}">{item["years"]}</span> años</span><span class="sr-only">{item["prefix"]}{item["years"]} años</span></p><p>{escape(item["text"])}</p></article>' for item in ABOUT['milestones'])
about_story = ''.join(f'<p>{escape(paragraph)}</p>' for paragraph in ABOUT['paragraphs'])
about = f'''
<section class="about-hero"><div class="container about-grid"><div><p class="eyebrow light">CONÓCENOS</p><h1 id="page-title">Efy Seguros.<br><span>Tu mejor elección.</span></h1><p class="large-copy">La confianza se construye escuchando.<br>La tranquilidad, acompañándote.</p><a class="button primary" href="#nuestra-historia">Conoce nuestra historia {ARROW}</a></div><figure class="portrait-panel evia-motion"><img src="../assets/site/evia-about-poster.webp?v=evia-20261010" alt="EVIA, nuestra astronauta de traje crema y detalles magenta, interactuando con un panel holográfico azul sobre fondo grafito" width="720" height="960" fetchpriority="high"><video class="evia-portrait-video" muted playsinline loop preload="none" tabindex="-1" aria-hidden="true" data-source="../assets/site/evia-about-loop.mp4?v=evia-20261010"></video><figcaption>Nuestra guía digital.</figcaption></figure></div></section>
<section class="section container experience-section" id="nuestra-historia" aria-labelledby="experience-title"><div class="experience-stats">{experience_stats}</div><div class="experience-intro"><h2 id="experience-title">{escape(ABOUT['headline'])}</h2><p>{escape(ABOUT['intro'])}</p></div></section>
<section class="about-story-section"><div class="container about-story"><p class="eyebrow">LO QUE NOS MUEVE</p><div>{about_story}<a class="button primary" href="{whatsapp_url('Hola Efy, quisiera conversar con un asesor comercial.')}">Hablar con Efy por WhatsApp {ARROW}</a></div></div></section>
'''

consult_section = f'''
<section class="section container consult-section" aria-labelledby="consult-title"><div><p class="eyebrow">PREPARA TU CONSULTA</p><h2 id="consult-title">Ordena tus ideas.<br><span>Lleva las preguntas claras.</span></h2><p>Escribe qué necesitas y genera un resumen que puedas copiar para tu próxima conversación.</p></div><form id="consult-form"><label for="consult-topic">¿Sobre qué quieres consultar?</label><select id="consult-topic" name="topic" required><option value="">Selecciona un tema</option><option>Elegir un seguro</option><option>Solicitar información para una cotización</option><option>Entender mi póliza</option><option>Consultar una renovación</option><option>Otra consulta</option></select><label for="consult-question">¿Qué te gustaría saber?</label><textarea id="consult-question" name="question" rows="4" maxlength="1200" required placeholder="Por ejemplo: quiero saber qué revisar al comparar dos propuestas."></textarea><p class="form-hint">El resumen se prepara aquí, sin enviarlo ni guardarlo. Evita incluir datos personales.</p><button class="button blue" type="submit">Preparar mi consulta {ARROW}</button><div id="consult-result" class="consult-result" hidden><label for="consult-summary">Tu consulta preparada</label><textarea id="consult-summary" rows="5" readonly></textarea><a class="button blue" id="consult-whatsapp" href="{whatsapp_url()}">Consultar por WhatsApp {ARROW}</a><button class="text-link" type="button" id="copy-consult">Copiar consulta {ARROW}</button><p id="copy-status" role="status"></p></div></form></section>
'''

office_lines = [line[:1].upper() + line[1:] for line in CONTACTS['address'].split(', ', 2)]
office_address = ''.join(f'<span>{escape(line.replace(", oficina", " · Oficina"))}</span>' for line in office_lines)

department_rows = ''
for department in CONTACTS['departments']:
    phones = ''
    for phone in department['phones']:
        commercial = department['name'] == 'Comercial'
        destination = 'https://wa.me/593' + phone[1:] if commercial else 'tel:+593' + phone[1:]
        channel = 'WhatsApp comercial' if commercial else 'Llamar al equipo operativo'
        phones += f'<div class="contact-phone"><a href="{destination}" aria-label="{channel}: {display_phone(phone)}">{display_phone(phone)} {ARROW}</a><span>{channel}</span></div>'
    department_rows += f'<section class="contact-department"><p class="small-label">{escape(department["name"].upper())}</p><p>{escape(department["description"])}</p><div class="contact-phones">{phones}</div></section>'
email_rows = ''.join(f'<div class="contact-email"><span>{escape(item["label"])}</span><a href="mailto:{item["address"]}">{escape(item["address"])} {ARROW}</a></div>' for item in CONTACTS['emails'])
social_icons = {
    'instagram': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    'facebook': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.8 22v-9.1h3.1l.5-3.5h-3.6V7.1c0-1 .3-1.7 1.8-1.7h1.9V2.3c-.3 0-1.5-.1-2.8-.1-2.8 0-4.6 1.7-4.6 4.8v2.4H7v3.5h3.1V22Z"/></svg>',
}
social_cards = ''.join(f'<a class="contact-social-link" href="{escape(item["url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Efy Seguros en {escape(item["name"], quote=True)}: {escape(item["label"], quote=True)} (abre una nueva pestaña)"><span class="contact-social-icon {item["platform"]}">{social_icons[item["platform"]]}</span><span class="contact-social-text"><span>{escape(item["name"])}</span><strong>{escape(item["label"])}</strong></span>{ARROW}</a>' for item in CONTACTS.get('social_profiles', []))
social_section = f'<section class="contact-department contact-social" aria-labelledby="social-title"><h2 class="small-label" id="social-title">CONECTA CON EFY</h2><div class="contact-social-links">{social_cards}</div></section>' if social_cards else ''
contact = f'''
<section class="page-intro container"><p class="eyebrow">CONTÁCTANOS</p><h1 id="page-title">Conversemos.<br><span>Estamos cerca de ti.</span></h1><p class="large-copy intro-copy">Elige el equipo que necesitas o visítanos en Quito.</p></section>
<section class="container contact-directory" aria-label="Canales de Efy"><div class="contact-channel-list">{department_rows}<section class="contact-department"><p class="small-label">CORREOS</p>{email_rows}</section>{social_section}</div><aside class="office-panel"><p class="eyebrow light">ENCUÉNTRANOS</p><h2>{escape(CONTACTS['city'])}.</h2><address>{office_address}</address><a class="button primary" href="https://www.google.com/maps/search/?api=1&amp;query=Av.%2010%20de%20Agosto%20y%20Juan%20de%20Galindes%20Green%20Tower%20Quito" rel="noopener noreferrer">Buscar dirección en Maps {ARROW}</a><div class="office-chat"><p>¿Tienes una duda sobre seguros?</p><button class="text-link" type="button" data-open-chat>Conversa con EVIA {ARROW}</button></div></aside></section>
''' + consult_section

# Tile identity follows the service ID, so reordering the catalogue keeps each image.
service_illustrations = {
    'finanzas': 0, 'accidentes-personales': 1, 'vehiculos': 2, 'transporte-pesado': 3,
    'motos': 4, 'asistencia-medica': 5, 'gastos-medicos-mayores': 6, 'asistencia-viaje': 7,
    'vida': 8, 'vida-indexada': 9, 'dental': 10, 'hogar': 11,
    'pymes': 12, 'responsabilidad-civil': 13, 'caucion': 14, 'fidelidad-privada': 15,
}
if set(service_illustrations) != service_ids:
    raise ValueError('Every service needs a matching catalogue illustration')
service_cards = []
for service in SERVICES:
    illustration_index = service_illustrations[service['id']]
    details = ''.join(f'<li>{escape(item)}</li>' for item in service['details'])
    service_cards.append(f'''<article class="service-card" id="seguro-{service['id']}" data-service-group="{escape(service['group'], quote=True)}"><div class="service-visual" style="--tile-col:{illustration_index % 4};--tile-row:{illustration_index // 4}"><img src="../assets/site/service-illustrations.webp" alt="" width="1200" height="1200" loading="lazy" decoding="async"></div><div class="service-card-body"><p class="service-category">{escape(service['group'])}</p><h3>{escape(service['name'])}</h3><p>{escape(service['description'])}</p>{f'<details><summary>Conoce el detalle <span aria-hidden="true">+</span></summary><ul>{details}</ul></details>' if details else ''}<a class="text-link" href="{whatsapp_url('Hola Efy, quisiera información sobre ' + service['name'] + '.')}">Consultar este ramo {ARROW}</a></div></article>''')
service_groups = [('movilidad', 'Movilidad'), ('salud', 'Salud'), ('vida-bienestar', 'Vida y bienestar'), ('patrimonio-actividad', 'Patrimonio y actividad')]
catalog = '<div class="catalog-nav service-filters" role="group" aria-label="Filtrar seguros por categoría"><button type="button" data-service-category="Todas" aria-pressed="true">Todos los seguros</button>' + ''.join(f'<button type="button" id="{key}" data-service-category="{escape(name, quote=True)}" aria-pressed="false">{name}</button>' for key, name in service_groups) + '</div>'
catalog += '<div class="catalog-heading"><p>Desliza para descubrir cada opción.</p><div class="catalog-controls"><span id="service-position" role="status" aria-live="polite" aria-atomic="true"></span><div><button type="button" id="service-prev" aria-label="Ver seguro anterior" aria-controls="service-rail">' + ARROW + '</button><button type="button" id="service-next" aria-label="Ver siguiente seguro" aria-controls="service-rail">' + ARROW + '</button></div></div></div>'
catalog += '<div class="service-catalog service-rail" id="service-rail" role="region" aria-roledescription="carrusel" aria-label="Opciones de seguros" tabindex="0">' + ''.join(card for _, group in service_groups for card, service in zip(service_cards, SERVICES) if service['group'] == group) + '</div>'
catalog += '<p class="form-hint">El alcance, las coberturas y los requisitos se confirman con la propuesta y las condiciones de cada póliza o plan.</p>'
services_page = f'''
<section class="services-hero"><div class="container services-hero-grid"><div><p class="eyebrow light">SERVICIOS</p><h1 id="page-title">Empieza por<br>lo que quieres<br><span>proteger.</span></h1><p class="large-copy">Cada elección empieza con algo que importa. Aquí reunimos la información para ayudarte a dar el siguiente paso.</p><a class="button primary" href="#catalogo">Explorar servicios {ARROW}</a></div><aside class="services-compass"><details><summary><span class="small-label">ANTES DE DECIDIR</span><span class="compass-title">Una elección clara empieza contigo.</span><span class="compass-plus" aria-hidden="true">+</span></summary><div class="compass-content"><p>¿Qué quieres proteger?</p><p>¿Qué necesitas que incluya?</p><p>¿Qué condiciones debes revisar?</p><a class="text-link" href="ayuda.html#faq-elegir">Encuentra por dónde empezar {ARROW}</a></div></details></aside></div></section>
<section class="section container services-section" id="catalogo" aria-labelledby="catalog-title"><div class="section-heading"><p class="eyebrow">SEGUROS CON EFY</p><h2 id="catalog-title">Explora nuestros seguros.</h2></div>{catalog}</section>
<section class="soft-section"><div class="container"><div class="section-heading"><p class="eyebrow">PARA COMPARAR MEJOR</p><h2>Hay más que un precio<br><span>en cada propuesta.</span></h2></div><div class="principles service-checklist"><article><h3>Qué incluye.</h3><p>Revisa los riesgos cubiertos y los límites de cada cobertura. Pide que te expliquen cualquier concepto que no esté claro.</p><a class="text-link" href="ayuda.html#faq-cobertura">Entender las coberturas {ARROW}</a></article><article><h3>Qué asumes tú.</h3><p>Comprueba cómo se aplica el deducible y qué parte de un evento cubierto te corresponde pagar.</p><a class="text-link" href="ayuda.html#faq-deducible">Entender el deducible {ARROW}</a></article><article><h3>Qué queda fuera.</h3><p>Lee las exclusiones y las condiciones que debes cumplir. La protección concreta se define en la póliza.</p><a class="text-link" href="ayuda.html#faq-exclusiones">Revisar las exclusiones {ARROW}</a></article></div></div></section>
<section class="section container help-cta"><div><p class="eyebrow">TU SIGUIENTE PASO</p><h2>Lleva tus preguntas claras.</h2><p>Prepara tu consulta o conversa con EVIA sobre conceptos generales.</p></div><div class="actions"><a class="button blue" href="contactos.html#consult-title">Preparar mi consulta {ARROW}</a><button class="text-link" type="button" data-open-chat>Consultar a EVIA {ARROW}</button></div></section>
'''

def partner_logo(partner):
    if not partner.get('logo'):
        return ''
    background = ' on-dark' if partner.get('logo_dark') else ''
    return f'<div class="partner-logo{background}"><img src="../{partner["logo"]}" alt="{escape(partner["name"], quote=True)}" width="240" height="100" loading="lazy"></div>'

def partner_card(partner):
    website = (f'<a class="text-link" href="{escape(partner["website"], quote=True)}" rel="noopener noreferrer">Sitio oficial {ARROW}</a>' if partner.get('website') else '')
    name = escape(partner['name'])
    assistance = f'<details class="partner-assistance"><summary>Teléfonos de atención <span aria-hidden="true">+</span></summary>{provider_lines(partner)}</details>'
    return f'<li class="partner-card" id="socio-{partner["id"]}" data-provider="{escape(partner["name"], quote=True)}">{partner_logo(partner)}<h3>{name}</h3>{assistance}{website}</li>'

def provider_lines(partner):
    lines = []
    for line in partner.get('assistance', []):
        digits = re.sub(r'[^+0-9]', '', line['phone'])
        destination = 'https://wa.me/' + re.sub(r'\D', '', digits) if line.get('channel') == 'whatsapp' else 'tel:' + digits
        channel = 'WhatsApp' if line.get('channel') == 'whatsapp' else 'Llamar'
        lines.append(f'<div class="assistance-line"><p>{escape(line["label"])}</p><a href="{destination}">{channel}: {escape(line["phone"])} {ARROW}</a><a class="line-source" href="{escape(line["source"], quote=True)}" rel="noopener noreferrer">Ver fuente oficial</a></div>')
    return ''.join(lines) or '<p class="form-hint">Consulta los canales de atención en el sitio oficial o en tu póliza.</p>'

partner_rows = ''.join(partner_card(partner) for partner in PARTNERS)
partner_catalog = (f'<ul class="partner-list">{partner_rows}</ul>' if PARTNERS else '''<div class="catalog-pending"><p class="small-label">PRÓXIMAMENTE</p><h3>Conoce a nuestras<br>aseguradoras aliadas.</h3><p>Estamos preparando la presentación de los socios estratégicos con los que trabaja Efy.</p></div>''')
partners_page = f'''
<section class="page-intro container partners-intro"><p class="eyebrow">SOCIOS ESTRATÉGICOS</p><h1 id="page-title">Conoce a quienes<br><span>trabajan con Efy.</span></h1><p class="large-copy intro-copy">Seguros, salud y asistencia de viaje. Nuestros socios estratégicos, reunidos en un mismo lugar.</p></section>
<section class="container partner-section" aria-labelledby="partners-title"><h2 id="partners-title">Nuestros socios.</h2>{'<label for="partner-search">Encuentra un socio</label><input id="partner-search" type="search" placeholder="Escribe el nombre…" autocomplete="off"><p id="partner-count" class="form-hint" role="status"></p><p id="partner-empty" class="form-hint" hidden>No encontramos ese nombre. Prueba con otra palabra.</p>' if PARTNERS else ''}{partner_catalog}</section>
<section class="guide-section"><div class="container partner-guide"><div><p class="eyebrow light">TU ASEGURADORA Y TU PÓLIZA</p><h2>La información correcta.<br><span>En el lugar correcto.</span></h2></div><div><p>El nombre de tu aseguradora, las coberturas y los canales de asistencia se encuentran en tu póliza o certificado. Consúltalos para conocer las condiciones de tu seguro.</p><a class="button primary" href="ayuda.html#faq-documentos">Revisar la guía de asistencia {ARROW}</a></div></div></section>
<section class="section container help-cta"><div><p class="eyebrow">SI NECESITAS REPORTAR UN EVENTO</p><h2>Cuéntale a Efy lo ocurrido.</h2><p>Puedes enviar tu reporte desde Asistencia. Sigue también los canales y plazos indicados por tu aseguradora.</p></div><a class="button blue" href="asistencia.html#reportar">Reportar un siniestro {ARROW}</a></section>
'''

review_cards = []
months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
for review in REVIEWS:
    rating = (f'<p class="review-rating"><span aria-hidden="true">★</span> Calificación: {review["rating"]} de 5</p>' if review.get('rating') is not None else '')
    published = ''
    if review.get('date'):
        day = date.fromisoformat(review['date'])
        published = f'<time datetime="{day.isoformat()}">{day.day} de {months[day.month-1]} de {day.year}</time>'
    source = (f'<a class="text-link" href="{escape(review["source_url"], quote=True)}" rel="noopener noreferrer">Ver reseña original {ARROW}</a>' if review.get('source_url') else '')
    review_cards.append(f'<figure class="review-card" id="resena-{review["id"]}">{rating}<blockquote><p>{escape(review["text"])}</p></blockquote><figcaption><strong>{escape(review["author"])}</strong>{published}</figcaption>{source}</figure>')
review_catalog = ('<div class="review-grid">' + ''.join(review_cards) + '</div>' if REVIEWS else '''<div class="catalog-pending review-pending"><p class="small-label">PRÓXIMAMENTE</p><h3>Las experiencias de nuestros clientes,<br>en sus propias palabras.</h3><p>Estamos reuniendo opiniones para compartirlas aquí.</p></div>''')
if DEMO_REVIEWS:
    demo_cards = []
    for item in DEMO_REVIEWS:
        stars = ''.join('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.1 6.7 1-4.9 4.7 1.2 6.7-6-3.2-6 3.2 1.2-6.7L2.3 9.1l6.7-1Z"/></svg>' for _ in range(item['rating']))
        demo_cards.append(f'<article class="review-demo-card" id="resena-{item["id"]}"><div class="review-demo-author"><span class="review-avatar" aria-hidden="true">{escape(item["initials"])}</span><div><h3>{escape(item["author"])}</h3></div></div><div class="review-stars"><span class="sr-only">Calificación simulada: {item["rating"]} de 5 estrellas</span>{stars}</div><blockquote><p>{escape(item["text"])}</p></blockquote><p class="review-topic">{escape(item["topic"])}</p></article>')
    review_catalog = f'<div class="review-demo-rail" tabindex="0" aria-label="Explorar diez comentarios simulados" aria-describedby="reviews-demo-label">{"".join(demo_cards)}</div><div class="review-demo-controls"><p class="review-position" aria-live="polite" aria-atomic="true"></p><div><button class="review-prev" type="button" aria-label="Ver comentarios anteriores">{ARROW}</button><button class="review-next" type="button" aria-label="Ver comentarios siguientes">{ARROW}</button></div></div>'
review_profile_label = 'Ver más reseñas' if REVIEWS else 'Leer reseñas en el perfil de Efy'
review_profile_link = (f'<a class="button blue" href="{escape(REVIEW_PROFILE, quote=True)}" rel="noopener noreferrer">{review_profile_label} {ARROW}</a>' if REVIEW_PROFILE else '')
reviews_page = f'''
<section class="reviews-hero"><div class="container"><p class="eyebrow light">RESEÑAS DE CLIENTES</p><h1 id="page-title">Tu experiencia<br><span>también cuenta.</span></h1><p class="large-copy">La confianza se construye en cada conversación. Tu opinión nos ayuda a seguir acompañándote mejor.</p></div></section>
<section class="section container reviews-section" aria-labelledby="reviews-title"><div class="section-heading"><p class="eyebrow"{' id="reviews-demo-label"' if DEMO_REVIEWS else ''}>{'OPINIONES DE DEMOSTRACIÓN' if DEMO_REVIEWS else 'EN SUS PROPIAS PALABRAS'}</p><h2 id="reviews-title">{'Cercanía, en cada conversación.' if DEMO_REVIEWS else 'Voces de nuestros clientes.'}</h2></div>{review_catalog}{f'<div class="review-source">{review_profile_link}</div>' if REVIEW_PROFILE else ''}</section>
<section class="soft-section"><div class="container help-cta"><div><p class="eyebrow">CONOCE MÁS DE EFY</p><h2>Una conversación<br>puede ser el comienzo.</h2><p>Conoce nuestra marca o prepara lo que te gustaría consultar.</p></div><div class="actions"><a class="button blue" href="nosotros.html">Conócenos {ARROW}</a><a class="text-link" href="contactos.html">Ir a Contactos {ARROW}</a></div></div></section>
'''

categories = ['Todas', 'Antes de elegir', 'Tu póliza', 'Si ocurre un evento', 'Sobre Efy']
filters = ''.join(f'<button class="filter-button" type="button" data-category="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>' for i,c in enumerate(categories))
def faq_source(question):
    source = question.get('source')
    if not isinstance(source, dict):
        return ''
    return f'<a class="faq-source" href="{escape(source["url"], quote=True)}">Fuente: {escape(source["label"])}</a>'

faq_rows = ''.join(f'<details class="faq-item" data-category="{f["category"]}" id="faq-{f["id"]}"><summary>{escape(f["question"])}<span aria-hidden="true"></span></summary><div><p class="faq-category">{escape(f["category"])}</p><p>{escape(f["answer"])}</p>{faq_source(f)}</div></details>' for f in FAQ)
help_page = f'''
<section class="help-intro container"><p class="eyebrow">AYUDA</p><h1 id="page-title">Las buenas decisiones<br>empiezan con <span>claridad.</span></h1><p class="large-copy">Encuentra respuestas sobre seguros y sobre Efy.</p><form class="faq-search" role="search"><label class="sr-only" for="faq-search">Buscar en preguntas frecuentes</label><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><input id="faq-search" type="search" placeholder="Busca: cobertura, deducible, renovación…" autocomplete="off"><button type="button" id="clear-search" hidden aria-label="Borrar búsqueda">×</button></form></section>
<section class="container help-content" aria-label="Preguntas frecuentes"><div class="faq-filters" aria-label="Filtrar preguntas por tema">{filters}</div><p class="search-status" id="search-status" role="status">{len(FAQ)} preguntas para orientarte</p><div class="faq-list">{faq_rows}</div><div class="no-results" id="no-results" hidden><h2>No encontramos esa pregunta.</h2><p>Prueba con una palabra más breve, como «póliza» o «cobertura», o conversa con EVIA.</p><button class="button blue" type="button" data-open-chat>Consultar a EVIA {ARROW}</button></div><p class="help-disclaimer">Información general. Las coberturas, requisitos y procedimientos dependen de las condiciones de cada póliza y aseguradora.</p></section>
<section class="soft-section"><div class="container help-cta"><div><p class="eyebrow">UNA PREGUNTA MÁS</p><h2>EVIA también puede orientarte.</h2><p>Conversa con nuestra guía o prepara una consulta para Efy.</p></div><div class="actions"><button class="button blue" type="button" data-open-chat>Abrir el chat {ARROW}</button><a class="text-link" href="contactos.html">Ir a Contactos {ARROW}</a></div></div></section>
'''


assistance_cards = []
for partner in PARTNERS:
    content = provider_lines(partner)
    website = (f'<a class="text-link" href="{escape(partner["website"], quote=True)}" rel="noopener noreferrer">Sitio oficial {ARROW}</a>' if partner.get('website') else '<p class="form-hint">Canal oficial pendiente de confirmar.</p>')
    assistance_cards.append(f'<article class="assistance-card" data-provider="{escape(partner["name"], quote=True)}"><h3>{escape(partner["name"])}</h3>{content}{website}</article>')

assistance_directory = ('<div class="assistance-directory">' + ''.join(assistance_cards) + '</div>' if PARTNERS else '<p>Estamos preparando las líneas oficiales de nuestros socios.</p>')
lookup_content = f'''
<section class="section container lookup-section" id="consultar-estado" aria-labelledby="lookup-title">
  <div><p class="eyebrow">SINIESTROS Y REEMBOLSOS</p><h2 id="lookup-title">Consulta por<br><span>tu caso.</span></h2><p>Prepara tu consulta con la cédula o, para un siniestro vehicular, la placa del vehículo. El equipo de Efy te ayudará a dar seguimiento.</p><p class="form-hint">Aún no hay un registro de estados conectado a la web. El equipo confirmará tu identidad antes de compartir información del caso.</p><a class="text-link" href="mailto:siniestros@efyseguros.com">Escribir directamente al equipo {ARROW}</a></div>
  <div class="lookup-panel"><p id="lookup-availability" class="lookup-pending">CONSULTA AL EQUIPO DE EFY</p>
    <form id="lookup-form">
      <label for="lookup-type">¿Qué quieres consultar?</label><select id="lookup-type"><option value="vehicular">Siniestro vehicular</option><option value="siniestro">Otro siniestro</option><option value="reembolso">Reembolso</option></select>
      <fieldset class="lookup-method"><legend>Identificar mi caso por</legend><label><input type="radio" name="lookup-method" value="cedula" checked>Cédula</label><label id="lookup-plate-option"><input type="radio" name="lookup-method" value="placa">Placa del vehículo</label></fieldset>
      <div id="lookup-cedula-field"><label for="lookup-cedula">Número de cédula</label><input id="lookup-cedula" type="text" inputmode="numeric" autocomplete="off" minlength="10" maxlength="10" pattern="[0-9]{{10}}" placeholder="Escribe los 10 dígitos" required aria-describedby="lookup-data-hint"></div>
      <div id="lookup-plate-field" hidden><label for="lookup-plate">Placa del vehículo</label><input id="lookup-plate" type="text" autocomplete="off" autocapitalize="characters" maxlength="10" placeholder="Ejemplo: ABC-1234" disabled aria-describedby="lookup-data-hint"></div>
      <p class="form-hint" id="lookup-data-hint">Estos datos se usan para preparar el correo en tu dispositivo. En este paso no se envían ni se guardan en la web.</p><button class="button blue" type="submit">Preparar consulta al equipo {ARROW}</button>
    </form><p id="lookup-status" class="form-hint" role="status" aria-live="polite" aria-atomic="true"></p>
    <section id="lookup-result" class="lookup-result" aria-labelledby="lookup-result-title" hidden><h3 id="lookup-result-title">Tu consulta está preparada.</h3><p>Revisa el resumen y abre tu correo para enviarlo al equipo de siniestros. Aún no se ha enviado.</p><label for="lookup-summary">Resumen de la consulta</label><textarea id="lookup-summary" rows="5" readonly></textarea><a class="button primary" id="lookup-email" href="mailto:siniestros@efyseguros.com">Abrir correo para enviar {ARROW}</a></section>
    <noscript><p class="form-hint">Activa JavaScript para preparar el resumen o escribe directamente a siniestros@efyseguros.com.</p></noscript>
  </div>
</section>
'''
report_content = f'''
<section class="container claim-section-heading" id="reportar" aria-labelledby="report-title"><p class="eyebrow">REPORTAR UN SINIESTRO</p><h2 id="report-title">Cuéntanos lo ocurrido.<br><span>Empecemos por ayudarte.</span></h2><p>Envía tu reporte al equipo de Efy. Te pediremos los datos del evento y una forma de contactarte.</p></section>
<section class="container claim-layout" aria-label="Reporte de siniestro"><aside class="claim-guide"><div class="urgent-note"><p class="small-label">SI HAY UNA EMERGENCIA</p><h2>Tu seguridad<br>es lo primero.</h2><p>En Ecuador, llama al <a href="tel:911">911</a> si necesitas atención urgente. Este formulario no ofrece asistencia inmediata.</p></div><div class="claim-destination"><p class="small-label">TU REPORTE LLEGARÁ A</p><a href="mailto:siniestros@efyseguros.com">siniestros@efyseguros.com</a><p>El envío informa a Efy. Revisa también los canales y plazos de aviso exigidos por tu aseguradora.</p></div><p class="claim-note">La referencia que recibas corresponde al reporte para Efy; no confirma cobertura, indemnización ni aceptación por la aseguradora.</p><a class="text-link" href="ayuda.html#faq-siniestro">Revisa nuestra guía de siniestros {ARROW}</a></aside>
<div class="claim-workspace" id="claim-workspace" tabindex="-1"><ol class="claim-progress" aria-label="Pasos del reporte"><li aria-current="step"><span>1</span>Tu contacto</li><li><span>2</span>El evento</li><li><span>3</span>Revisar y enviar</li></ol><p id="claim-availability" class="form-hint" role="status">Comprobando disponibilidad del envío…</p><div id="claim-error" class="claim-error" role="alert" hidden></div>
<noscript><p class="claim-error">Para completar el formulario, activa JavaScript. También puedes enviar tu reporte a <a href="mailto:siniestros@efyseguros.com">siniestros@efyseguros.com</a>.</p></noscript>
<form id="claim-form" enctype="multipart/form-data" method="post" action="api/siniestros.php">
<fieldset class="claim-step" data-step="0"><legend>¿Cómo podemos contactarte?</legend><p class="step-intro">Estos datos permiten que el equipo de Efy identifique tu reporte y pueda comunicarse contigo.</p><label for="claim-name">Nombre y apellido <span class="required-label">(obligatorio)</span></label><input id="claim-name" name="name" autocomplete="name" minlength="2" maxlength="120" required><div class="claim-fields"><div><label for="claim-phone">Teléfono <span class="required-label">(obligatorio)</span></label><input id="claim-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="25" placeholder="Ej.: +593 99 123 4567" required></div><div><label for="claim-email">Correo electrónico <span class="required-label">(opcional)</span></label><input id="claim-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="tu@correo.com"></div></div><div class="claim-fields"><div><label for="claim-insurer">Aseguradora <span class="required-label">(opcional)</span></label><input id="claim-insurer" name="insurer" maxlength="100" placeholder="Si la conoces"></div><div><label for="claim-policy">Número de póliza <span class="required-label">(opcional)</span></label><input id="claim-policy" name="policy" maxlength="100" placeholder="Si lo tienes a mano"></div></div><div class="step-actions"><button class="button blue" type="button" data-claim-next>Continuar {ARROW}</button></div></fieldset>
<fieldset class="claim-step" data-step="1"><legend>¿Qué ocurrió?</legend><p class="step-intro">Describe los hechos con tus palabras. Puedes adjuntar fotos o documentos que ayuden a entender el evento.</p><label for="claim-type">Tipo de evento <span class="required-label">(obligatorio)</span></label><select id="claim-type" name="event_type" required><option value="">Selecciona una opción</option><option>Accidente</option><option>Daños</option><option>Robo</option><option>Otro evento</option></select><div class="claim-fields"><div><label for="claim-date">Fecha del evento <span class="required-label">(obligatorio)</span></label><input id="claim-date" name="event_date" type="date" required></div><div><label for="claim-time">Hora aproximada <span class="required-label">(opcional)</span></label><input id="claim-time" name="event_time" type="time"><p class="form-hint">Hora de Quito.</p></div></div><label for="claim-location">Lugar del evento <span class="required-label">(obligatorio)</span></label><input id="claim-location" name="location" maxlength="240" placeholder="Ciudad y dirección o referencia" required><label for="claim-description">Describe lo ocurrido <span class="required-label">(obligatorio)</span></label><textarea id="claim-description" name="description" rows="5" minlength="20" maxlength="4000" required placeholder="Indica qué pasó y qué daños observaste."></textarea><p class="form-hint">Incluye sólo información necesaria para el reporte. No escribas claves, datos bancarios ni detalles médicos.</p><label for="claim-files">Fotos o documentos <span class="required-label">(opcional)</span></label><input id="claim-files" name="attachments[]" type="file" accept="image/jpeg,image/png,image/webp,application/pdf" multiple aria-describedby="claim-file-hint"><p id="claim-file-hint" class="form-hint">Hasta 3 archivos JPG, PNG, WebP o PDF. Máximo 2 MB por archivo.</p><ul id="claim-file-list" class="claim-file-list" aria-label="Archivos seleccionados"></ul><div class="step-actions"><button class="text-link" type="button" data-claim-back>Volver</button><button class="button blue" type="button" data-claim-next>Revisar reporte {ARROW}</button></div></fieldset>
<fieldset class="claim-step" data-step="2"><legend>Revisa antes de enviar.</legend><p class="step-intro">Comprueba los datos. Tu reporte se enviará a <strong>siniestros@efyseguros.com</strong>.</p><dl id="claim-review" class="claim-review"></dl><label class="claim-consent" for="claim-consent"><input id="claim-consent" name="consent" type="checkbox" value="1" required><span>Autorizo a Efy a usar la información y los adjuntos de este reporte para gestionar mi caso y contactarme.</span></label><p class="form-hint">Los datos se envían al correo del equipo de siniestros. Los adjuntos no se publican en la web. Este aviso no sustituye los procedimientos de la aseguradora.</p><div class="step-actions"><button class="text-link" type="button" data-claim-back>Corregir datos</button><button id="claim-send" class="button blue" type="submit" disabled>Enviar reporte {ARROW}</button></div></fieldset><div class="claim-honeypot" aria-hidden="true"><label for="claim-website">Sitio web</label><input id="claim-website" name="website" tabindex="-1" autocomplete="off"></div></form>
<section id="claim-success" class="claim-success" aria-labelledby="claim-success-title" hidden><div class="receipt-icon" aria-hidden="true">✓</div><p class="eyebrow">REPORTE PARA EFY</p><h2 id="claim-success-title">Tu reporte fue enviado.</h2><p>El servidor aceptó el envío a <strong>siniestros@efyseguros.com</strong>. Conserva esta referencia para consultar al equipo.</p><p class="receipt-reference" id="claim-reference"></p><p class="form-hint" id="claim-received-at"></p><p class="claim-note">Esta referencia no es un número de siniestro emitido por la aseguradora ni confirma cobertura. Sigue también sus instrucciones de aviso.</p><div class="actions"><button id="claim-download" type="button" class="button blue">Descargar comprobante {ARROW}</button><a class="text-link" href="index.html">Volver al inicio</a></div></section></div></section>
'''
lines_content = f'''
<section class="soft-section" id="lineas-asistencia" aria-labelledby="lines-title"><div class="container"><div class="section-heading"><p class="eyebrow">LÍNEAS OFICIALES</p><h2 id="lines-title">Encuentra la atención<br><span>que necesitas.</span></h2></div><div class="emergency-line"><div><strong>Emergencias en Ecuador</strong><p>Si hay riesgo inmediato para la vida o la seguridad, llama al ECU 911.</p></div><a class="button blue" href="tel:911">Llamar al 911 {ARROW}</a></div><p class="assistance-intro">Elige el canal que corresponde a tu aseguradora o proveedor. La disponibilidad de cada asistencia depende de tu póliza o plan.</p><label for="assistance-search">Busca tu aseguradora o proveedor</label><input id="assistance-search" type="search" placeholder="Por ejemplo: Chubb, Saludsa o MAPFRE" autocomplete="off"><p id="assistance-count" class="form-hint" role="status"></p><p id="assistance-empty" class="form-hint" hidden>No encontramos ese nombre. Revisa tu póliza o prueba con otra palabra.</p>{assistance_directory}</div></section>
'''

def subpage_intro(section, title, description, parent='asistencia.html'):
    return f'<section class="page-intro container"><a class="breadcrumb" href="{parent}">← {section}</a><p class="eyebrow">{section.upper()}</p><h1 id="page-title">{title}</h1><p class="large-copy intro-copy">{description}</p></section>'

lookup_page = subpage_intro('Asistencias', 'Tu siniestro.<br><span>Tu reembolso.</span>', 'Un espacio para dar seguimiento a tu caso.') + lookup_content
report_page = subpage_intro('Asistencias', 'Reporta un siniestro.<br><span>Estamos para ayudarte.</span>', 'Informa lo ocurrido al equipo de Efy y conserva la referencia de tu reporte.') + report_content
lines_page = subpage_intro('Asistencias', 'La atención correcta.<br><span>A una llamada.</span>', 'Encuentra los canales oficiales de tu aseguradora o proveedor.') + lines_content
assistance_hub = f'''
<section class="assistance-hero"><div class="container"><p class="eyebrow light">ASISTENCIAS</p><h1 id="page-title">Cuando lo necesitas.<br><span>Efy, cerca de ti.</span></h1><p class="large-copy">Reporta lo ocurrido, consulta por tu caso o encuentra el canal de atención de tu aseguradora.</p></div></section>
<section class="section container assistance-hub" aria-label="Gestiones de asistencia">
<a class="assistance-option" id="reportar" href="reportar-siniestro.html"><span class="option-number" aria-hidden="true">01</span><div><p class="small-label">REPORTE</p><h2>Reportar un siniestro</h2><p>Cuéntanos lo ocurrido y envía los datos al equipo de Efy.</p><span class="option-action">Iniciar reporte {ARROW}</span></div></a>
<a class="assistance-option" id="consultar-estado" href="consultas.html"><span class="option-number" aria-hidden="true">02</span><div><p class="small-label">SEGUIMIENTO</p><h2>Estado de siniestros y reembolsos</h2><p>Prepara tu consulta por cédula o placa y envíala al equipo de Efy.</p><span class="option-action">Consultar por mi caso {ARROW}</span></div></a>
<a class="assistance-option" id="lineas-asistencia" href="lineas-asistencia.html"><span class="option-number" aria-hidden="true">03</span><div><p class="small-label">LÍNEAS OFICIALES</p><h2>Asistencia de tu aseguradora</h2><p>Teléfonos verificados, organizados por compañía y servicio.</p><span class="option-action">Buscar un teléfono {ARROW}</span></div></a>
</section><section class="soft-section"><div class="container emergency-line"><div><strong>Emergencias en Ecuador</strong><p>Si hay riesgo inmediato para la vida o la seguridad, llama al ECU 911.</p></div><a class="button blue" href="tel:911">Llamar al 911 {ARROW}</a></div></section>
'''

help_page += f'<section class="section container help-cta"><div><p class="eyebrow">MEJOREMOS ESTA WEB</p><h2>¿Encontraste un error?</h2><p>Cuéntanos qué ocurrió para que podamos revisarlo.</p></div><a class="button blue" href="reportar-error.html">Reportar un error {ARROW}</a></section>'
error_page = subpage_intro('Ayuda', 'Ayúdanos a mejorar.<br><span>Cuéntanos el error.</span>', 'Un enlace que no abre, un formulario o algo que no se ve bien. Tu reporte nos ayuda a revisarlo.', 'ayuda.html') + f'''
<section class="container error-layout" aria-label="Reporte de un error de la web"><aside><p class="small-label">EQUIPO DE EFY</p><h2>Lo revisamos contigo.</h2><p>Prepara el reporte y envíalo desde tu aplicación de correo a <a href="mailto:{CONTACTS['error_email']}">{CONTACTS['error_email']}</a>.</p><p class="form-hint">Este apartado es para errores de la web. Para un evento de tu seguro, utiliza el formulario de siniestros.</p><a class="text-link" href="reportar-siniestro.html">Reportar un siniestro {ARROW}</a></aside>
<div class="error-workspace"><form id="error-form" data-recipient="{CONTACTS['error_email']}"><label for="error-page">Página o apartado donde ocurrió</label><input id="error-page" maxlength="250" required placeholder="Por ejemplo: Servicios"><label for="error-type">¿Qué problema encontraste?</label><select id="error-type" required><option value="">Elige una opción</option><option>Un enlace no funciona</option><option>Un formulario no funciona</option><option>El contenido no se ve bien</option><option>Información que necesita corregirse</option><option>Otro error</option></select><label for="error-description">¿Qué ocurrió?</label><textarea id="error-description" rows="5" minlength="10" maxlength="1500" required placeholder="Describe qué intentabas hacer y qué pasó."></textarea><label for="error-device">Dispositivo o navegador (opcional)</label><input id="error-device" maxlength="120" placeholder="Por ejemplo: iPhone, Safari"><p class="form-hint">Evita incluir cédulas, información médica, contraseñas o datos de tu póliza.</p><button class="button blue" type="submit">Preparar reporte {ARROW}</button></form><div id="error-result" class="consult-result" hidden><label for="error-summary">Revisa tu reporte</label><textarea id="error-summary" rows="8" readonly></textarea><div class="actions"><a id="error-email" class="button blue" href="mailto:{CONTACTS['error_email']}">Abrir correo para enviarlo {ARROW}</a><button id="error-copy" class="text-link" type="button">Copiar reporte</button></div><p class="form-hint" id="error-status" role="status">El reporte está preparado. Envía el mensaje desde tu aplicación de correo; la web no lo ha enviado.</p></div><noscript><p>Puedes describir el error y la página donde ocurrió escribiendo a <a href="mailto:{CONTACTS['error_email']}">{CONTACTS['error_email']}</a>.</p></noscript></div></section>
'''


pages = [
    ('index.html','Inicio','Efy Seguros · Tu mejor elección',home),
    ('servicios.html','Servicios','Servicios · Efy Seguros',services_page),
    ('socios.html','Socios estratégicos','Socios estratégicos · Efy Seguros',partners_page),
    ('nosotros.html','Conócenos','Conócenos · Efy Seguros',about),
    ('asistencia.html','Asistencias','Asistencias · Efy Seguros',assistance_hub),
    ('resenas.html','Reseñas','Reseñas de clientes · Efy Seguros',reviews_page),
    ('contactos.html','Contáctanos','Contáctanos · Efy Seguros',contact),
    ('ayuda.html','Ayuda','Ayuda · Efy Seguros',help_page),
]
extras = [
    ('consultas.html','Asistencias','Estados y reembolsos · Efy Seguros',lookup_page),
    ('reportar-siniestro.html','Asistencias','Reportar un siniestro · Efy Seguros',report_page),
    ('siniestros.html','Asistencias','Reportar un siniestro · Efy Seguros',report_page),
    ('lineas-asistencia.html','Asistencias','Líneas de asistencia · Efy Seguros',lines_page),
    ('reportar-error.html','Ayuda','Reportar un error · Efy Seguros',error_page),
]
NAV_PREVIEWS = {
    'index.html': ('Bienvenido a Efy.', 'Encuentra lo que quieres proteger y el siguiente paso para acompañarte.', [('servicios.html', 'Explorar seguros', 'Opciones para cada etapa.'), ('asistencia.html', 'Necesito asistencia', 'Reportes, consultas y líneas de atención.'), ('contactos.html', 'Hablar con el equipo', 'Nuestros canales de contacto.')]),
    'servicios.html': ('Empieza por lo que importa.', 'Explora nuestros seguros por categoría y revisa cada opción a tu ritmo.', [('servicios.html#movilidad', 'Movilidad', 'Vehículos, motos y viajes.'), ('servicios.html#salud', 'Salud', 'Atención y gastos médicos.'), ('servicios.html#vida-bienestar', 'Vida y bienestar', 'Vida y accidentes personales.'), ('servicios.html#patrimonio-actividad', 'Patrimonio y actividad', 'Hogar, negocios y garantías.')]),
    'socios.html': ('Conoce a nuestros socios.', 'Las aseguradoras y proveedores con los que trabaja Efy, en un solo lugar.', [('socios.html', 'Explorar socios', 'Encuentra tu aseguradora o proveedor.'), ('lineas-asistencia.html', 'Líneas de asistencia', 'Consulta sus canales oficiales.')]),
    'nosotros.html': ('Conoce el mundo de Efy.', 'Nuestra trayectoria, lo que nos mueve y EVIA, tu guía digital.', [('nosotros.html', 'Nuestra historia', 'La experiencia detrás de Efy.'), ('ayuda.html#faq-evia', 'Conoce a EVIA', 'Cómo puede orientarte nuestra guía.')]),
    'asistencia.html': ('Estamos para acompañarte.', 'Elige lo que necesitas para dar seguimiento o encontrar asistencia.', [('reportar-siniestro.html', 'Reportar un siniestro', 'Informa al equipo lo ocurrido.'), ('consultas.html', 'Siniestros y reembolsos', 'Prepara tu consulta por cédula o placa.'), ('lineas-asistencia.html', 'Líneas de asistencia', 'Canales oficiales de los proveedores.')]),
    'resenas.html': ('La experiencia de elegir Efy.', 'Visita nuestro espacio de opiniones y conoce cómo está organizado.', [('resenas.html', 'Explorar reseñas', 'Conoce la sección de opiniones.'), ('contactos.html', 'Conversar con Efy', 'Encuentra al equipo que necesitas.')]),
    'contactos.html': ('Conversemos.', 'Encuentra al equipo adecuado o prepara tus preguntas antes de escribirnos.', [('contactos.html', 'Canales de contacto', 'Comercial, siniestros y atención.'), ('contactos.html#consult-title', 'Preparar una consulta', 'Organiza lo que quieres preguntar.'), ('consultas.html', 'Consultar por mi caso', 'Siniestros y reembolsos.')]),
    'ayuda.html': ('Entiende antes de decidir.', 'Respuestas claras para preparar tus preguntas y revisar tu seguro.', [('ayuda.html#faq-elegir', 'Elegir un seguro', 'Por dónde empezar.'), ('ayuda.html#faq-cobertura', 'Entender tu póliza', 'Coberturas y conceptos.'), ('reportar-error.html', 'Reportar un problema', 'Ayúdanos a mejorar la web.')]),
}

def navigation_item(filename, name, current):
    _, _, links = NAV_PREVIEWS[filename]
    panel_id = 'nav-preview-' + filename.removesuffix('.html')
    current_attribute = ' aria-current="page"' if current else ''
    destinations = ''.join(f'<li><a class="nav-preview-link" href="{escape(url, quote=True)}">{escape(label)}</a></li>' for url, label, _ in links)
    return (f'<div class="nav-item"><a class="nav-link" href="{filename}"{current_attribute} aria-expanded="false" aria-controls="{panel_id}">{escape(name)}<svg class="nav-chevron" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m3 4.5 3 3 3-3"/></svg></a>'
            f'<section class="nav-preview" id="{panel_id}" aria-label="Explorar {escape(name, quote=True)}" hidden><ul class="nav-preview-links">{destinations}</ul></section></div>')

for filename, label, title, content in pages + extras:
    content = content.replace('asistencia.html#reportar', 'reportar-siniestro.html').replace('asistencia.html#consultar-estado', 'consultas.html').replace('asistencia.html#lineas-asistencia', 'lineas-asistencia.html').replace('Ir a Contactos', 'Ir a Contáctanos').replace('>CONTACTOS<', '>CONTÁCTANOS<')
    nav = ''.join(navigation_item(file, name, name == label) for file,name,_,_ in pages)
    document = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#080e1d"><meta name="description" content="Conoce Efy Seguros, encuentra información útil y conversa con EVIA, nuestra guía de preguntas frecuentes."><title>{title}</title><link rel="icon" href="../assets/efy-seguros-transparent.png" type="image/png"><link rel="preload" href="../assets/fonts/ibm-plex-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="../assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../assets/site/efy-site.css?v=claims-20261009"><script src="../assets/site/efy-site.js?v=claims-20261009" defer></script></head>
<body data-page="{("asistencia" if label == "Asistencias" else label.lower())}"><a class="skip-link" href="#contenido">Ir al contenido</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html" aria-label="Efy Seguros, Inicio"><picture><source type="image/webp" srcset="../assets/efy-brand-360.webp 360w, ../assets/efy-brand-720.webp 720w" sizes="(max-width:760px) 144px, 178px"><img src="../assets/efy-seguros-transparent.png" alt="Efy Seguros · Tu mejor elección" width="1774" height="887" fetchpriority="high" decoding="async"></picture></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span>Menú</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button><nav id="site-nav" class="site-nav" aria-label="Navegación principal">{nav}</nav><button class="header-chat" type="button" data-open-chat>Conversa con EVIA {ARROW}</button></div></header>
<main id="contenido">{content}</main>
<footer class="site-footer"><div class="container"><div class="footer-bottom"><p>© 2026 Efy Seguros.</p><span>Tu mejor elección.</span></div></div></footer>
<button class="chat-fab" type="button" data-open-chat aria-controls="evia-dialog" aria-expanded="false"><img src="../assets/site/evia-portrait.jpg" alt="" width="40" height="40"><span>Habla con EVIA</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-8 8H5l-3 3V11.5a9 9 0 0 1 18 0Z"/></svg></button>
<dialog id="evia-dialog" class="evia-dialog is-glass" aria-labelledby="chat-title"><div class="chat-header"><div class="avatar-row"><img src="../assets/site/evia-portrait.jpg" alt="" width="44" height="44"><div><h2 id="chat-title">EVIA <svg class="chat-brand-badge" viewBox="0 0 24 24" role="img" aria-label="Distintivo de marca Efy"><title>Distintivo propio de Efy</title><circle cx="12" cy="12" r="11" fill="currentColor"/><path d="m7 12 3.2 3.2L17 8.5" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></h2><span>Asistente virtual de Efy</span></div></div><button id="close-chat" class="icon-button" type="button" aria-label="Cerrar chat">×</button></div><p class="chat-context">Información general de seguros. Evita compartir datos personales.</p><div id="chat-messages" class="chat-messages" role="log" aria-live="polite" aria-relevant="additions" aria-label="Conversación con EVIA"><div class="chat-message bot"><span>EVIA</span><p>Hola, soy EVIA, tu asistente virtual de Efy. ¿En qué puedo ayudarte?</p></div></div><div class="chat-quick-actions"><button id="chat-menu-toggle" type="button" aria-controls="chat-messages"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M8 6h12M8 12h12M8 18h12"/><circle cx="3" cy="6" r="1"/><circle cx="3" cy="12" r="1"/><circle cx="3" cy="18" r="1"/></svg>Ver opciones</button><a class="chat-team-link" href="{whatsapp_url('Hola Efy, quisiera hablar con el equipo comercial.')}">Abrir WhatsApp {ARROW}</a></div><form id="chat-form" class="chat-form"><label class="sr-only" for="chat-input">Tu pregunta para EVIA</label><input id="chat-input" type="text" maxlength="400" placeholder="Escribe un mensaje…" autocomplete="off" required><button class="icon-button send-button" type="submit" aria-label="Enviar pregunta a EVIA"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="m3 3 18 9-18 9 3-9-3-9Z"/><path d="M6 12h15"/></svg></button></form><a class="chat-help-link" href="ayuda.html">Preguntas frecuentes de Efy {ARROW}</a></dialog>
<script id="contact-data" type="application/json">{json.dumps({"whatsapp": WHATSAPP, "providers": [name for partner in PARTNERS for name in [partner['name'], partner['id'].replace('-', ' ')]]}, ensure_ascii=False).replace('<','\\u003c')}</script>
<script id="faq-data" type="application/json">{json.dumps(FAQ,ensure_ascii=False).replace('<','\\u003c')}</script>
</body></html>'''
    if filename in ('reportar-siniestro.html', 'siniestros.html'):
        document = document.replace('</head>', f'<script src="../assets/site/siniestros.js?v={SITE_VERSION}" defer></script></head>')
    if filename == 'nosotros.html':
        document = document.replace('</head>', '<script src="../assets/site/evia-about.js?v=evia-20261010" defer></script></head>')
    if filename == 'consultas.html':
        document = document.replace('</head>', f'<script src="../assets/site/asistencia.js?v={SITE_VERSION}" defer></script></head>')
    if filename == 'servicios.html':
        document = document.replace('</head>', f'<script src="../assets/site/services.js?v={SITE_VERSION}" defer></script></head>')
    document = document.replace('</head>', f'<script src="../assets/site/navigation.js?v={SITE_VERSION}" defer></script></head>')
    if filename == 'reportar-error.html':
        document = document.replace('</head>', '<script src="../assets/site/errores.js?v=info-20261010" defer></script></head>')
    document = document.replace('efy-site.css?v=claims-20261009', 'efy-site.css?v=' + SITE_VERSION).replace('efy-site.js?v=claims-20261009', 'efy-site.js?v=' + SITE_VERSION)
    document = document.replace('<meta name="robots"', f'<meta name="efy-site-version" content="{SITE_VERSION}"><meta name="robots"')
    document = re.sub(r'href="([a-z0-9-]+\.html)(#[^"]*)?"', lambda match: f'href="{match[1]}?v={SITE_VERSION}{match[2] or ""}"', document)
    def avatar_picture(match):
        image = re.sub(r'width="[0-9]+" height="[0-9]+"', 'width="960" height="1280"', match[1])
        return ('<span class="evia-avatar"><picture><source type="image/webp" '
                'srcset="../assets/site/evia-avatar-180.webp 180w, ../assets/site/evia-avatar-360.webp 360w" '
                'sizes="135px">' + image + '</picture></span>')
    document = re.sub(r'(<img src="../assets/site/evia-portrait.jpg" alt=""[^>]*>)', avatar_picture, document)
    document = document.replace('</head>', '<noscript><style>button[data-open-chat],.suggestion,.faq-search,.faq-filters,#search-status,#consult-form,#error-form,#claim-form,.claim-progress,#claim-availability,#lookup-form,.service-filters,label[for="partner-search"],#partner-search,#partner-count,label[for="assistance-search"],#assistance-search,#assistance-count{display:none}</style></noscript></head>')
    (OUT / filename).write_text(document)
    # The root is the published product; /nueva/ remains available for old review links.
    published = document.replace('../assets/', '/assets/').replace('content="noindex,nofollow"', 'content="index,follow"')
    published = published.replace('action="api/siniestros.php"', 'action="/nueva/api/siniestros.php"')
    canonical = 'https://www.efyseguros.com/' + ('' if filename == 'index.html' else filename)
    published = published.replace('</head>', f'<link rel="canonical" href="{canonical}"></head>')
    (ROOT / 'public' / filename).write_text(published)
    print('Built published page and preview:', filename)
