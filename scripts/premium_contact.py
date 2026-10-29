"""Contact preview: a glass connection hub and direct, department-specific channels."""
from html import escape

PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5H5l-3 2v-9.5A9.5 9.5 0 0 1 21 11.5Z"/><path d="M8 7c0 5 4 9 8 9l1-3-3-1-1 1-3-3 1-1-1-3Z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="4"/><path d="m3 6 9 7 9-7"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 10c0 6-7 12-7 12S5 16 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="9" r="2.5"/></svg>'


def premium_contact(contacts, arrow, phone_url, social_section, office_address):
    teams = []
    for team in contacts['departments']:
        identifier = team['name'].lower()
        phones = ''.join(
            f'<a class="contact-direct-phone" href="{escape(phone_url(phone), quote=True)}" '
            f'aria-label="WhatsApp {identifier}: {phone}"><span>{phone[:3]} {phone[3:6]} {phone[6:]}</span>{arrow}</a>'
            for phone in team['phones']
        )
        teams.append(f'<section class="contact-team" id="contacto-{identifier}">'
                     f'<div class="contact-team-title"><span class="contact-symbol">{PHONE}</span>'
                     f'<p class="eyebrow">{escape(team["name"])}</p></div>'
                     f'<h2>{"Encuentra tu seguro." if identifier == "comercial" else "Seguimos contigo."}</h2>'
                     f'<p>{escape(team["description"])}</p><div class="contact-direct-phones">{phones}</div>'
                     '<span class="contact-channel-label">Conversar por WhatsApp</span></section>')
    emails = ''.join(
        f'<a class="contact-mail-row" href="mailto:{escape(item["address"], quote=True)}">'
        f'<span><small>{escape(item["label"])}</small><strong>{escape(item["address"])}</strong></span>{arrow}</a>'
        for item in contacts['emails']
    )
    return f'''<div class="contact-premium">
<section class="contact-premium-hero"><div class="container contact-premium-grid">
 <div><p class="eyebrow light">Contáctanos</p><h1 id="page-title">Conversemos.<br><span>Estamos cerca de ti.</span></h1><p class="large-copy">Elige el equipo que necesitas o visítanos en Quito.</p><div class="actions"><a class="button primary" href="#contacto-comercial">Hablar con Comercial {arrow}</a><a class="contact-operating-link" href="#contacto-operativo">Ya soy cliente {arrow}</a></div></div>
 <div class="contact-hub" aria-label="Accesos a los canales de Efy"><div class="contact-hub-orbit" aria-hidden="true"></div><div class="contact-hub-orbit inner" aria-hidden="true"></div><div class="contact-hub-core"><span class="contact-hub-message">{PHONE}</span><p>Una conversación.<br><strong>Muchas formas de estar cerca.</strong></p></div><a class="contact-hub-port hub-commercial" href="#contacto-comercial">{PHONE}<span>Comercial</span></a><a class="contact-hub-port hub-operative" href="#contacto-operativo">{PHONE}<span>Operativo</span></a><a class="contact-hub-port hub-email" href="#contacto-correos">{MAIL}<span>Correos</span></a><a class="contact-hub-port hub-location" href="#oficina-quito">{PIN}<span>Quito</span></a></div>
</div></section>
<nav class="container contact-shortcuts" aria-label="Canales de contacto"><a href="#contacto-comercial">Comercial {arrow}</a><a href="#contacto-operativo">Operativo {arrow}</a><a href="#contacto-correos">Correos {arrow}</a><a href="#social-title">Conecta con Efy {arrow}</a></nav>
<section class="container contact-premium-directory" aria-label="Contacta al equipo de Efy"><div class="contact-team-grid">{''.join(teams)}<section class="contact-email-panel" id="contacto-correos"><div class="contact-team-title"><span class="contact-symbol">{MAIL}</span><p class="eyebrow">También por correo</p></div>{emails}</section></div>
 <aside class="contact-office" id="oficina-quito"><span class="contact-office-icon">{PIN}</span><p class="eyebrow light">Nos encontramos aquí</p><h2>Quito.<br><span>Cerca de ti.</span></h2><address>{office_address}</address><a class="button primary" href="{escape(contacts['maps_url'], quote=True)}" target="_blank" rel="noopener noreferrer">Buscar dirección en Maps {arrow}</a><div class="contact-office-help"><p>¿Por dónde empezar?</p><button class="text-link" type="button" data-open-chat>Conversa con EVIA {arrow}</button></div></aside>
</section><div class="container contact-social-premium">{social_section}</div></div>'''
