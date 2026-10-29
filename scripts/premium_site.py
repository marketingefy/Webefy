"""Render the approved premium homepage with production destinations and owner data."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def premium_home(partners, about, contacts, arrow, selector, phone_url):
    template = (ROOT / 'tooling/efy/templates/premium-home.html').read_text()
    logos = ''.join(f'<a class="ally-logo" href="socios.html#socio-{item["id"]}"><img src="../{item["logo"]}" alt="{escape(item["name"], quote=True)}" width="180" height="80" loading="lazy"></a>' for item in partners if item.get('logo'))
    departments = []
    for item in contacts['departments']:
        identifier = item['name'].lower()
        phones = ''.join(f'<a href="{escape(phone_url(phone), quote=True)}">{phone[:3]} {phone[3:6]} {phone[6:]}</a>' for phone in item['phones'])
        departments.append(f'<article id="{identifier}"><p class="small-title">{escape(item["name"])}</p><h3>{"Tu próxima elección." if identifier == "comercial" else "Te acompañamos."}</h3>{phones}</article>')
    emails = ''.join(f'<a href="mailto:{escape(item["address"], quote=True)}">{escape(item["address"])}</a>' for item in contacts['emails'])
    departments.append(f'<article id="correos"><p class="small-title">Correos</p>{emails}</article>')
    socials = ''.join(f'<a href="{escape(item["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(item["name"])} · {escape(item["label"])}</a>' for item in contacts['social_profiles'])
    departments.append(f'<article id="conecta"><p class="small-title">Conecta con Efy</p><h3>Nos encontramos aquí.</h3><p>{escape(contacts["address"])} · {escape(contacts["city"])}</p><a href="{escape(contacts["maps_url"], quote=True)}">Buscar dirección en Maps {arrow}</a>{socials}</article>')
    for key, value in {'PROTECTION_SELECTOR': selector, 'PARTNER_LOGOS': logos, 'CONTACT_CARDS': ''.join(departments), 'ABOUT_PARAGRAPH': escape(about['paragraphs'][0])}.items():
        template = template.replace('{{' + key + '}}', value)
    return template
