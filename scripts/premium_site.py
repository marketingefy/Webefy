"""Render the approved premium homepage with production destinations and owner data."""
from html import escape
from pathlib import Path
from evia_media import evia_film

ROOT = Path(__file__).resolve().parents[1]


def premium_home(partners, about, contacts, arrow, selector, phone_url, contact_module, experience_stats):
    template = (ROOT / 'tooling/efy/templates/premium-home.html').read_text()
    logos = ''.join(
        f'<a class="ally-logo" href="socios.html#socio-{item["id"]}"><span class="ally-mark{" on-dark" if item.get("logo_dark") else ""}"><img src="../{item["logo"]}" alt="{escape(item["name"], quote=True)}" width="180" height="80" loading="eager"></span><span class="ally-name">{escape(item["name"])}</span></a>'
        for item in partners if item.get('logo')
    )
    for key, value in {'PROTECTION_SELECTOR': selector, 'PARTNER_LOGOS': logos, 'CONTACT_MODULE': contact_module.replace('<h1 id="page-title">','<h2 id="home-contact-title">').replace('</h1>','</h2>'), 'EXPERIENCE_STATS': '<div class="experience-stats home-experience">' + experience_stats + '</div>', 'ABOUT_PARAGRAPH': escape(about['paragraphs'][0]), 'ABOUT_FILM': evia_film('conocenos', 'EVIA presenta la trayectoria de Efy'), 'REVIEWS_FILM': evia_film('resenas', 'EVIA escucha y agradece tus comentarios')}.items():
        template = template.replace('{{' + key + '}}', value)
    return template
