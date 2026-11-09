"""Consistent, softly blended EVIA media for the company and review modules."""
from html import escape


def evia_film(module, description, identifier=''):
    stem = 'evia-conocenos-corporativo-20261029' if module == 'conocenos' else f'evia-{module}-preview'
    anchor = f' id="{escape(identifier, quote=True)}"' if identifier else ''
    return (f'<figure class="evia-film evia-film-{module}" data-evia-clip{anchor}>'
            f'<img class="evia-film-poster" src="../assets/site/{stem}.webp" '
            f'alt="{escape(description, quote=True)}" width="720" height="960" decoding="async">'
            f'<video muted playsinline loop preload="none" data-source="../assets/site/{stem}.mp4" '
            'aria-hidden="true" tabindex="-1"></video></figure>')
