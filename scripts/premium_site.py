"""The cinematic homepage is deliberately short; complete journeys live in their modules."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def premium_home(partners, about, contacts, arrow, selector, phone_url, contact_module, experience_stats):
    cinema = (ROOT / 'tooling/efy/templates/cinema-hero.html').read_text()
    # Coverage remains in the carousel; avoid repeating a full module above it.
    selector = re.sub(r'<aside class="coverage-concierge".*?</aside>', '', selector, flags=re.S)
    return ('<div class="premium-home cinema-home cinema-home-compact">' + cinema + selector +
            '<section class="home-essentials shell" aria-labelledby="home-essentials-title">'
            '<div><p class="eyebrow">Cerca de ti</p><h2 id="home-essentials-title">¿Necesitas ayuda?</h2>'
            '<p>Encuentra el canal que necesitas para dar el siguiente paso.</p></div>'
            '<div class="actions"><a class="button primary" href="asistencia.html">Necesito asistencia ' + arrow + '</a>'
            '<a class="text-action" href="contactos.html">Contactar a Efy ' + arrow + '</a></div></section></div>')
