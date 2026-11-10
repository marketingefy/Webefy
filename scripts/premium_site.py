"""The cinematic homepage is deliberately short; complete journeys live in their modules."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]


def premium_home(partners, about, contacts, arrow, selector, phone_url, contact_module, experience_stats):
    cinema = (ROOT / 'tooling/efy/templates/cinema-hero.html').read_text()
    # Coverage remains in the carousel; avoid repeating a full module above it.
    selector = re.sub(r'<aside class="coverage-concierge".*?</aside>', '', selector, flags=re.S)
    coop = ('<section class="home-coop-shortcut shell" aria-labelledby="home-coop-title">'
            '<div><p class="eyebrow">Para socios de cooperativas</p><h2 id="home-coop-title">Tu cooperativa<br><span>Tu cobertura</span></h2>'
            '<p>Consulta los datos de tu seguro y encuentra el acompañamiento de Efy.</p>'
            '<a class="button primary" href="coberturas-cooperativas.html">Consultar mi cobertura ' + arrow + '</a></div>'
            '<img src="../assets/site/needs/cooperativas-hq-20261109.png" alt="" width="1254" height="1254" decoding="async"></section>')
    phone_groups = ''.join('<div><h3>' + escape(team['name']) + '</h3>' + ''.join('<a href="' + escape(phone_url(number), quote=True) + '">' + number[:3] + ' ' + number[3:6] + ' ' + number[6:] + '</a>' for number in team['phones']) + '</div>' for team in contacts['departments'])
    social_links = ''.join('<a href="' + escape(item['url'], quote=True) + '" target="_blank" rel="noopener noreferrer">' + escape(item['name']) + ' · ' + escape(item['label']) + '</a>' for item in contacts.get('social_profiles', []))
    emails = ''.join('<a href="mailto:' + escape(item['address'], quote=True) + '">' + escape(item['address']) + '</a>' for item in contacts['emails'])
    brief = ('<section class="home-contact-brief shell" aria-labelledby="home-contact-brief-title">'
             '<div class="brief-intro"><p class="eyebrow">Hablemos</p><h2 id="home-contact-brief-title">Conecta con Efy</h2></div>'
             '<div class="brief-grid"><div><h3>Visítanos en Quito</h3><address>' + escape(contacts['address']) + '</address>'
             '<a href="' + escape(contacts['maps_url'], quote=True) + '" target="_blank" rel="noopener noreferrer">Cómo llegar ' + arrow + '</a></div>'
             + phone_groups + '<div><h3>Correo y redes</h3>' + emails + social_links + '</div></div></section>')
    return ('<div class="premium-home cinema-home cinema-home-compact">' + cinema + coop + selector +
            '<section class="home-essentials shell" aria-labelledby="home-essentials-title">'
            '<div><p class="eyebrow">Cerca de ti</p><h2 id="home-essentials-title">¿Necesitas ayuda?</h2>'
            '<p>Encuentra el canal que necesitas para dar el siguiente paso.</p></div>'
            '<div class="actions"><a class="button primary" href="asistencia.html">Necesito asistencia ' + arrow + '</a>'
            '<a class="text-action" href="contactos.html">Contactar a Efy ' + arrow + '</a></div></section>' + brief + '</div>')
