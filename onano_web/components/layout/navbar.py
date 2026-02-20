import reflex as rx

from ..ui import Isologo
from ..ui import Isotipo
from ...styles.colors import *
from ...styles.fonts import STYLE_BODY, STYLE_CTA


# ── Progressive Backdrop Blur ──────────────────────────────────
# Técnica: apilar N capas con blur creciente, cada una visible solo
# en su "banda" vertical mediante mask-image (gradiente).
# Resultado visual: blur(1px) abajo → blur(10px) arriba.

_BLUR_STEPS: list[tuple[int, str]] = [
    # (blur_px, mask-image gradient)
    # Capa 0 — Fondo: blur suave, visible en el cuarto inferior
    (1,  "linear-gradient(to bottom, transparent 60%, black 80%, black 100%)"),
    # Capa 1 — blur medio-bajo, banda central-baja
    (4,  "linear-gradient(to bottom, transparent 35%, black 50%, black 60%, transparent 80%)"),
    # Capa 2 — blur medio-alto, banda central-alta
    (7,  "linear-gradient(to bottom, transparent 10%, black 25%, black 40%, transparent 60%)"),
    # Capa 3 — Tope: blur fuerte, visible en el cuarto superior
    (10, "linear-gradient(to bottom, black 0%, black 20%, transparent 45%)"),
]


def _blur_layer(blur_px: int, gradient: str) -> rx.Component:
    """Una capa individual del progressive blur."""
    return rx.box(
        position="absolute",
        inset="0",
        backdrop_filter=f"blur({blur_px}px)",
        style={
            "maskImage": gradient,
            "WebkitMaskImage": gradient,
        },
        pointer_events="none",
    )


def _progressive_blur() -> rx.Component:
    """Apila capas de blur progresivo: 10 px arriba → 1 px abajo."""
    return rx.fragment(
        *[_blur_layer(b, g) for b, g in _BLUR_STEPS]
    )


# ── Componentes de navegación ──────────────────────────────────

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, style=STYLE_BODY, color=BRAND_TEXT_DARK),
        href=url,
        text_decoration="none",
        _hover={"opacity": 0.7},
    )

def navbar() -> rx.Component:
    return rx.box(
        # Capas de blur progresivo (reemplazan al backdrop_filter uniforme)
        #_progressive_blur(),
        # Contenido visible
        rx.hstack(
            # Logo
            rx.link(
                Isologo.dark(),
                href="/",
            ),
            rx.spacer(),
            # Desktop Menu
            rx.hstack(
                navbar_link("Inicio", "/"),
                navbar_link("Quiénes somos", "/quienes-somos"),
                navbar_link("Productos", "/productos"),
                navbar_link("Contacto", "/contacto"),
                spacing="5", # Reflex spacing 1-9 (5 ~ 2em)
                display=["none", "none", "flex", "flex"],
            ),
            rx.spacer(),
            # CTA Button - Login
            rx.link(
                rx.button(
                    "Iniciar Sesión",
                    color=BRAND_LIGHT_BLUE,
                    radius="full",
                    style=STYLE_CTA,
                    size="3",
                    padding_x="1.5em",
                ),
                href="https://my.onanoglobal.com", # External link placeholder
                is_external=True,
                display=["none", "none", "flex", "flex"],
            ),
            # Mobile Menu Trigger (Hamburger - Implementation pending state logic)
            rx.icon("menu", color=BRAND_LIGHT_BLUE, display=["flex", "flex", "none", "none"]),
            
            width="100%",
            align_items="center",
            padding_x=["1em", "2em", "4em"],
            position="relative",
            z_index="1",  # Contenido sobre las capas de blur
        ),
        position="fixed",
        align="center",
        justify="center",
        top="10px",
        z_index="999",
        width="100%",
    )
