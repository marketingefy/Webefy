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
    social = {item['platform']: item for item in contacts.get('social_profiles', [])}
    instagram = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
    facebook = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.8 22v-9.1h3.1l.5-3.5h-3.6V7.1c0-1 .3-1.7 1.8-1.7h1.9V2.3c-.3 0-1.5-.1-2.8-.1-2.8 0-4.6 1.7-4.6 4.8v2.4H7v3.5h3.1V22Z"/></svg>'
    contact_art = ('<figure class="contact-evia-figure" aria-label="EVIA te conecta con los canales de Efy">'
        '<div class="contact-evia-film" data-transparent-film>'
        '<img src="../assets/evia-contacto-transparente-20261109.png" alt="EVIA con su mano abierta presenta los canales de contacto" width="720" height="960" decoding="async">'
        '<canvas aria-hidden="true"></canvas><video muted loop playsinline preload="none" data-source="../assets/evia-contacto-alpha-20261109.mp4" aria-hidden="true" tabindex="-1"></video></div>'
        f'<a class="evia-phone-panel" href="{escape(phone_url(contacts["departments"][0]["phones"][0]), quote=True)}" aria-label="Conversar por WhatsApp con Efy"><span class="phone-camera"></span><span class="phone-screen">{PHONE}<span>Hablemos.</span><small>Efy Seguros</small></span></a>'
        f'<a class="evia-social-chip evia-instagram" href="{escape(social["instagram"]["url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Instagram de Efy Seguros">{instagram}<span>@efyseguros</span></a>'
        f'<a class="evia-social-chip evia-facebook" href="{escape(social["facebook"]["url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Facebook de Efy Seguros">{facebook}<span>Efy Seguros</span></a>'
        '<span class="evia-contact-orbit" aria-hidden="true"></span></figure>')
    return f'''<div class="contact-premium">
<section class="contact-premium-hero"><div class="container contact-premium-grid">
 <div><p class="eyebrow light">Contáctanos</p><h1 id="page-title">Conversemos.<br><span>Estamos cerca de ti.</span></h1><p class="large-copy">Elige el equipo que necesitas o visítanos en Quito.</p><div class="actions"><a class="button primary" href="#contacto-comercial">Hablar con Comercial {arrow}</a><a class="contact-operating-link" href="#contacto-operativo">Ya soy cliente {arrow}</a></div></div>
 {contact_art}
</div></section>
<nav class="container contact-shortcuts" aria-label="Canales de contacto"><a href="#contacto-comercial">Comercial {arrow}</a><a href="#contacto-operativo">Operativo {arrow}</a><a href="#contacto-correos">Correos {arrow}</a><a href="#social-title">Conecta con Efy {arrow}</a></nav>
<section class="container contact-premium-directory" aria-label="Contacta al equipo de Efy"><div class="contact-team-grid">{''.join(teams)}<section class="contact-email-panel" id="contacto-correos"><div class="contact-team-title"><span class="contact-symbol">{MAIL}</span><p class="eyebrow">También por correo</p></div>{emails}</section></div>
 <aside class="contact-office" id="oficina-quito"><span class="contact-office-icon">{PIN}</span><p class="eyebrow light">Nos encontramos aquí</p><h2>Quito.<br><span>Cerca de ti.</span></h2><address>{office_address}</address><a class="button primary" href="{escape(contacts['maps_url'], quote=True)}" target="_blank" rel="noopener noreferrer">Buscar dirección en Maps {arrow}</a><div class="contact-office-help"><p>¿Por dónde empezar?</p><button class="text-link" type="button" data-open-chat>Conversa con EVIA {arrow}</button></div></aside>
</section><div class="container contact-social-premium">{social_section}</div></div>'''
