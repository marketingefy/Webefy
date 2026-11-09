"""Shared transparent EVIA video, with the approved reflective backdrop and native fallback."""
from html import escape

def evia_film(module, description, identifier=''):
    anchor = f' id="{escape(identifier, quote=True)}"' if identifier else ''
    return (f'<figure class="cinema-inline cinema-module-art" data-cinema-scene="{escape(module, quote=True)}"{anchor} '
            f'role="img" aria-label="{escape(description, quote=True)}">'
            '<canvas class="cinema-stars" data-cinema-stars aria-hidden="true"></canvas>'
            '<img class="cinema-fallback" src="../assets/evia-cinema-cutout-20261109.webp" '
            'alt="" width="880" height="720" decoding="async" loading="lazy"></figure>')
