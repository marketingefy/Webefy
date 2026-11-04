# Homepage services and cooperative coverage carousel — preview only

Replace only the homepage need-selector grid with a six-card horizontal carousel:
cooperative coverage first, then Auto, Salud, Vida, Hogar and Empresa. Add a
persistent coverage link beside the section heading; both coverage links route
to the existing coberturas-cooperativas.html within root or /nueva as appropriate.
No new lookup backend, coverage promises or production form submissions.
Services-page selector stays as the original five-card grid. EVIA media unchanged.

Responsive: 3 cards desktop, 2 tablet, 1 plus a partial next card mobile. Native
horizontal touch scrolling, snap alignment, manual arrows, visible position,
keyboard Home/End/arrow keys, disabled boundary buttons, reduced-motion support.
No automatic rotation: the coverage card remains discoverable.
Scoped CSS and homepage JS; bumped site asset version for subsequent publication.

Checks: 320/390/768/1440 widths, root and /nueva, six cards, no page overflow,
forward/back navigation, keyboard boundaries and actual coverage destination.
Guided UI suite passed 78 views with IBM Plex Sans fonts. Regression assertions
added for the home carousel. Self-contained preview also checked for carousel
navigation and the coverage route at 390/1440. External requests were blocked;
the existing coverage page attempted only an optional third-party provider logo.
No queries or form submissions were sent.

Artifacts: /workspace/output/efy-carrusel-cooperativas-20261104
No push to main or deployment: owner requested a preview before publication.
