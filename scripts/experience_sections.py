"""Shared content for Efy's guided insurance and client journeys."""
from html import escape


NEEDS = [
    ('vehiculos', 'Auto', 'Para cada nuevo camino.', 2),
    ('asistencia-medica', 'Salud', 'Tu bienestar, más cerca.', 5),
    ('vida', 'Vida', 'Por quienes más quieres.', 8),
    ('hogar', 'Hogar', 'Donde empieza tu historia.', 11),
    ('pymes', 'Empresa', 'Lo que estás construyendo.', 12),
]


def need_selector(arrow, carousel=False):
    cards = ''.join(
        f'<a class="protect-card protection-card" href="cotizar.html?ramo={key}" style="--delay:-{i * 1.7}s">'
        f'<span class="product-stage"><span class="floor-ring"></span><span class="model model-single"><img src="../assets/site/needs/{key}.webp" alt="" width="300" height="300" decoding="async"></span>'
        f'<span class="product-symbol">{arrow}</span></span><div class="product-body"><h3 class="product-title">{title}</h3><p class="product-copy">{description}</p><span class="product-action">Solicitar cotización {arrow}</span></div></a>'
        for i, (key, title, description, _tile) in enumerate(NEEDS)
    )
    if carousel:
        coverage = f'''<a class="protect-card service-shortcut coverage-shortcut" href="coberturas-cooperativas.html"><span class="product-stage coverage-stage"><span class="coverage-orbit"></span><svg class="coverage-emblem" viewBox="0 0 180 160" fill="none" aria-hidden="true"><defs><linearGradient id="coverage-shield" x1="35" y1="15" x2="140" y2="145" gradientUnits="userSpaceOnUse"><stop stop-color="#91b8ff"/><stop offset=".5" stop-color="#445ea5"/><stop offset="1" stop-color="#24376c"/></linearGradient></defs><path d="M90 16 143 36v40c0 31-23 53-53 67-30-14-53-36-53-67V36Z" fill="url(#coverage-shield)" stroke="#dce8ff" stroke-width="2"/><path d="m90 28 42 16v32c0 24-17 43-42 56-25-13-42-32-42-56V44Z" stroke="#c8d7ff" stroke-opacity=".5"/><circle cx="90" cy="65" r="14" fill="#fff"/><path d="M66 106v-9c0-15 48-15 48 0v9" fill="#fff"/><circle cx="132" cy="111" r="25" fill="#f25c9d" stroke="#ffd9eb" stroke-width="3"/><path d="m121 111 8 8 15-17" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="coverage-tag">Para socios</span><span class="product-symbol">{arrow}</span></span><div class="product-body"><p class="coverage-kicker">Consulta tu cobertura</p><h3 class="product-title">Cooperativas</h3><p class="product-copy">Encuentra la consulta de tu seguro en un solo lugar.</p><span class="product-action">Consultar mi cobertura {arrow}</span></div></a>'''
        return f'''<div class="premium-home premium-selector home-services-carousel"><section class="protection section shell protection-section" id="que-proteger" aria-labelledby="protection-title"><div class="section-top protection-heading"><div><p class="eyebrow">Servicios y consultas</p><h2 id="protection-title">¿Qué necesitas <span>hoy?</span></h2><p class="carousel-intro">Tu seguro y tus consultas, a un paso.</p></div><a class="coverage-direct" href="coberturas-cooperativas.html">Consulta tu cobertura · Cooperativas {arrow}</a></div><div class="protection-grid home-services-rail" id="home-services-rail" tabindex="0" role="region" aria-roledescription="carrusel" aria-label="Servicios y consulta de cobertura de cooperativas">{coverage}{cards}</div><div class="home-carousel-controls"><p>Desliza para explorar <span aria-hidden="true">↔</span></p><div><span id="home-services-position" role="status" aria-live="polite" aria-atomic="true">1 de 6</span><button type="button" id="home-services-prev" aria-label="Servicios anteriores" aria-controls="home-services-rail" disabled>←</button><button type="button" id="home-services-next" aria-label="Más servicios" aria-controls="home-services-rail">→</button></div></div><div class="catalog-bottom"><p>Protección para personas, familias y empresas.</p><a class="text-action" href="servicios.html#catalogo">Explorar nuestros seguros {arrow}</a></div></section></div>'''
    return f'''<div class="premium-home premium-selector"><section class="protection section shell protection-section" id="que-proteger" aria-labelledby="protection-title"><div class="section-top protection-heading"><div><p class="eyebrow">Una elección muy tuya</p><h2 id="protection-title">¿Qué quieres <span>proteger?</span></h2></div></div><div class="protection-grid">{cards}</div><div class="catalog-bottom"><p>Protección para personas, familias y empresas.</p><a class="text-action" href="servicios.html#catalogo">Explorar nuestros seguros {arrow}</a></div></section></div>'''


def quote_page(services, arrow, whatsapp):
    options = ''.join(f'<option value="{s["id"]}">{escape(s["name"])}</option>' for s in services)
    return f'''<section class="page-intro quote-intro"><div class="container"><p class="eyebrow">Solicita tu cotización</p><h1 id="page-title">Tu protección.<br><span>Comienza contigo.</span></h1><p class="large-copy">Tres pasos para preparar tu solicitud y conversar con un asesor de Efy.</p></div></section>
    <section class="section container quote-layout">
      <aside class="quote-guide"><p class="eyebrow">A tu medida</p><h2>Un buen seguro<br>empieza escuchándote.</h2><p>Cuéntanos qué quieres proteger. El asesor revisará contigo las opciones, sus coberturas y condiciones.</p><ul><li>Elige un ramo.</li><li>Cuéntanos tu prioridad.</li><li>Revisa y continúa por WhatsApp.</li></ul><a class="text-link" href="asistencia.html">¿Ya tienes un seguro y necesitas asistencia? {arrow}</a></aside>
      <div class="quote-workspace"><noscript><p>Para preparar una solicitud por pasos, activa JavaScript o <a href="{whatsapp}">conversa con un asesor por WhatsApp</a>.</p></noscript>
      <form id="quote-form" hidden>
        <p class="quote-step-label" id="quote-step-label" aria-live="polite">Paso 1 de 3 · Tu seguro</p>
        <progress id="quote-progress" max="3" value="1" aria-label="Avance de tu solicitud">1 de 3</progress>
        <fieldset class="quote-step" data-quote-step="0"><legend tabindex="-1">¿Qué quieres proteger?</legend><p>Selecciona el tipo de seguro que deseas consultar.</p><label for="quote-branch">Ramo del seguro</label><select id="quote-branch" name="branch" required><option value="">Elige una opción</option>{options}</select></fieldset>
        <fieldset class="quote-step" data-quote-step="1" hidden><legend tabindex="-1">¿Qué necesitas de tu seguro?</legend><p>Ayúdanos a entender en qué momento estás.</p><label for="quote-goal">Mi prioridad es</label><select id="quote-goal" name="goal" required><option value="">Selecciona tu prioridad</option><option>Contratar mi primer seguro</option><option>Comparar mi seguro actual</option><option>Renovar o mejorar mi protección</option><option>Proteger a mi empresa o equipo</option><option>Recibir orientación antes de elegir</option></select><label for="quote-notes">¿Algo más que quieras contarnos? <span>(opcional)</span></label><textarea id="quote-notes" name="notes" maxlength="600" rows="3" placeholder="Por ejemplo: busco una opción para mi familia."></textarea><p class="form-hint">Evita incluir cédulas, historias médicas o documentos en este campo.</p></fieldset>
        <fieldset class="quote-step" data-quote-step="2" hidden><legend tabindex="-1">Tu consulta, lista para conversar.</legend><p>Revisa el resumen antes de continuar.</p><label for="quote-summary">Resumen de tu solicitud</label><textarea id="quote-summary" rows="6" readonly></textarea><label for="quote-advisor">Equipo comercial</label><select id="quote-advisor" name="advisor"></select><p class="form-hint">El siguiente botón abre WhatsApp con tu solicitud preparada. Tú decides cuándo enviarla. El equipo confirmará la recepción y las opciones disponibles.</p><div class="actions quote-share"><a id="quote-whatsapp" class="button primary" href="{whatsapp}" target="_blank" rel="noopener noreferrer">Continuar por WhatsApp {arrow}</a><button class="text-link" id="quote-copy" type="button">Copiar resumen {arrow}</button></div><p id="quote-copy-status" role="status"></p></fieldset>
        <div class="quote-controls"><button class="text-link" type="button" id="quote-back" hidden>Volver</button><button class="button blue" type="submit" id="quote-next">Continuar {arrow}</button></div>
      </form></div>
    </section>'''


def business_page(services, arrow):
    ids = ['pymes', 'responsabilidad-civil', 'transporte-pesado', 'caucion', 'fidelidad-privada', 'finanzas']
    cards = ''.join(f'<article class="business-card"><h3>{escape(s["name"])}</h3><p>{escape(s["description"])}</p><a class="text-link" href="cotizar.html?ramo={s["id"]}">Solicitar asesoría {arrow}</a><a class="business-detail" href="servicios.html#seguro-{s["id"]}">Ver detalle del ramo</a></article>' for key in ids for s in services if s['id'] == key)
    return f'''<section class="page-intro"><div class="container"><p class="eyebrow">Seguros para empresas</p><h1 id="page-title">Tu negocio avanza.<br><span>Tu protección, también.</span></h1><p class="large-copy">Cada actividad tiene sus propios riesgos. Encuentra por dónde empezar y revisa con Efy lo que necesita tu empresa.</p><a class="button primary" href="cotizar.html?ramo=pymes">Asesoría para mi empresa {arrow}</a></div></section><section class="section container" aria-labelledby="business-title"><div class="section-heading"><p class="eyebrow">Lo que estás construyendo</p><h2 id="business-title">Protección para tu actividad.</h2></div><div class="business-grid">{cards}</div></section>'''


def clients_page(arrow, whatsapp):
    actions = [
        ('coberturas-cooperativas.html', 'Mi cobertura de cooperativa', 'Si eres socio de Coopartamos, consulta el registro de tu seguro de asistencia médica.'),
        ('consultas.html', 'Consultar mi caso', 'Prepara una consulta de siniestro o reembolso para el equipo operativo.'),
        ('reportar-siniestro.html', 'Reportar un siniestro', 'Envía el reporte y sus documentos al equipo de siniestros de Efy.'),
        ('lineas-asistencia.html', 'Necesito asistencia', 'Encuentra los canales oficiales de atención de tu aseguradora.'),
        ('ayuda.html#faq-reembolso-documentos', 'Preparar un reembolso', 'Revisa los documentos y formularios según tu aseguradora de salud.'),
        ('contactos.html#contacto-operativo', 'Pólizas y renovaciones', 'Solicita una copia de tus documentos o consulta tu próxima renovación con el equipo.'),
        ('ayuda.html#faq-search', 'Entender mi póliza', 'Resuelve dudas sobre coberturas, deducibles, exclusiones y vigencia.'),
    ]
    cards = ''.join(f'<a class="client-action" href="{url}"><div><h3>{title}</h3><p>{text}</p></div>{arrow}</a>' for url, title, text in actions)
    return f'''<section class="page-intro"><div class="container"><p class="eyebrow">Clientes Efy</p><h1 id="page-title">Contigo, también<br><span>después de elegir.</span></h1><p class="large-copy">Tus accesos de atención, reunidos en un solo lugar.</p></div></section><section class="section container" aria-labelledby="client-title"><div class="section-heading"><p class="eyebrow">¿Qué necesitas hoy?</p><h2 id="client-title">Encuentra ayuda para tu seguro.</h2></div><div class="client-grid">{cards}</div><div class="client-access-note"><h3>La atención sigue siendo personal.</h3><p>Para recibir copias de tus pólizas o confirmar fechas de renovación, comunícate con el equipo. El seguimiento de siniestros y reembolsos se consulta con nuestros asesores.</p><a class="text-link" href="{whatsapp}">Hablar con una persona {arrow}</a></div></section>'''
