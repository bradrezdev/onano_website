import reflex as rx

from ..components.ui import particle_hero_bg

from ..components.layout.navbar import navbar
from ..components.layout.footer import footer
from ..styles.colors import *
from ..styles.fonts import *


# ── CSS: CTA glow + smooth scroll ─────────────────────────────
_HERO_CSS = f"""
html {{ scroll-behavior: smooth; }}

@property --glow-angle {{
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}}

@keyframes spin-glow {{
  to {{ --glow-angle: 360deg; }}
}}

.cta-glow-wrap {{
  position: relative;
  display: inline-flex;
  border-radius: 32px;
  padding: 2px;
  background: conic-gradient(
    from var(--glow-angle),
    transparent 0%,
    {BRAND_LIGHT_BLUE} 8%,
    {BRAND_SECONDARY_80} 12%,
    transparent 22%,
    transparent 100%
  );
  animation: spin-glow 3s linear infinite;
  cursor: pointer;
  transition: filter 0.3s ease;
}}

.cta-glow-wrap:hover {{
  filter: brightness(1.3) drop-shadow(0 0 14px rgba(12, 188, 229, 0.45));
}}

.cta-glow-inner {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 30px;
  background: {BRAND_DARK_BLUE};
  color: {BRAND_WHITE};
  padding: 1em 2.5em;
  font-family: 'Avenir Next', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}}
"""


def hero_section() -> rx.Component:
    """
    Hero: aglomeración de nanopartículas que se dispersa al click.
    Fondo oscuro, título con degradado 45°, CTA con glow rotativo.
    """
    return rx.box(
        # Inyección de CSS (glow + smooth scroll)
        rx.el.style(_HERO_CSS),

        # Canvas interactivo (z-index 0, recibe clicks)
        particle_hero_bg(),

        # Contenido superpuesto (pointer-events: none excepto CTA)
        rx.flex(
            # ── Bloque superior: título + subtítulo ──
            rx.vstack(
                rx.heading(
                    "Nanotecnología",
                    style=STYLE_H3,
                    color=BRAND_SECONDARY_40,
                    text_align="center",
                    opacity="0.85",
                    max_width="600px",
                ),
                rx.text(
                    "Mejorando lo invisible",
                    style=STYLE_H1,
                    color=BRAND_WHITE,
                    text_align="center",
                    max_width="600px",
                    white_space="pre-wrap", # Permite saltos de línea en el texto
                ),
                rx.text(
                    "para transformar lo visible.",
                    style=STYLE_H1,
                    color=BRAND_WHITE,
                    text_align="center",
                    max_width="600px",
                    white_space="pre-wrap", # Permite saltos de línea en el texto
                ),
                align="center",
                spacing="0",
            ),

            # ── Spacer → separa título del CTA ──
            rx.spacer(),

            # ── Bloque inferior: CTA glow button ──
            rx.link(
                rx.box(
                    rx.box(
                        "Conocer más",
                        class_name="cta-glow-inner",
                    ),
                    class_name="cta-glow-wrap",
                ),
                href="#section-next",
                text_decoration="none",
                pointer_events="auto",
            ),

            direction="column",
            align="center",
            justify="between",
            width="100%",
            height="100%",
            padding_y=["18vh", "20vh"],
            padding_x="1.5em",
            z_index="2",
            pointer_events="none",
        ),

        position="relative",
        width="100%",
        height="115dvh",
        overflow="hidden",
        bg=BRAND_HERO_BG,
    )


def science_section_placeholder() -> rx.Component:
    """Placeholder para la sección científica (destino del scroll CTA)."""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading(
                    "Descubre la Nanociencia",
                    style=STYLE_DISPLAY,
                    color=BRAND_DARK_BLUE,
                    text_align="center",
                ),
                rx.text(
                    "Próximamente: sección científica completa.",
                    style=STYLE_H2,
                    color=BRAND_DARK_BLUE,
                    text_align="center",
                    opacity="0.6",
                ),
                align="center",
                spacing="4",
            ),
            height="100%",
        ),
        id="section-next",
        width="100%",
        min_height="100vh",
        bg=BRAND_WHITE,
        padding="4em",
    )


def index() -> rx.Component:
    """Página de inicio con hero interactivo de nanopartículas."""
    return rx.box(
        navbar(),
        hero_section(),
        science_section_placeholder(),
        footer(),
        width="100%",
    )