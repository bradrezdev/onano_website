import reflex as rx

from ..ui import Isologo
from ..ui import Isotipo
from ...styles.colors import *
from ...styles.fonts import STYLE_BODY, STYLE_CTA


# ── Navbar Component (Pill Style) ──────────────────────────────
# Modificado: Estilo "Pildora" flotante con padding lateral de 10px
# respecto al ancho total de la página.

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, style=STYLE_BODY, color=BRAND_TEXT_DARK, weight="medium"),
        href=url,
        text_decoration="none",
        _hover={"opacity": 0.7},
    )

def navbar() -> rx.Component:
    return rx.box(
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
                spacing="6",
                display=["none", "none", "flex", "flex"],
            ),
            rx.spacer(),
            # CTA Button - Login
            rx.link(
                rx.button(
                    "Iniciar Sesión",
                    variant="surface", # Mas sutil para el navbar
                    color_scheme="gray",
                    high_contrast=True,
                    radius="full",
                    size="2",
                    style=STYLE_CTA,
                    padding_x="1.2em",
                ),
                href="https://my.onanoglobal.com",
                is_external=True,
                display=["none", "none", "flex", "flex"],
            ),
            # Mobile Menu Trigger
            rx.icon("menu", color=BRAND_SECONDARY_20, display=["flex", "flex", "none", "none"]),
            
            width="100%",
            align_items="center",
            height="100%",
        ),
        # Wrapper "Pildora"
        position="fixed",
        top="16px",
        left="50%",
        transform="translateX(-50%)", # Centrado absoluto
        width="calc(100% - 20px)",     # Padding 10px a cada lado (total 20px)
        max_width="1200px",            # Límite para pantallas muy anchas
        height="64px",                 # Altura fija tipo botón estándar
        padding_x="1.5em",
        # Estilo Visual Pildora
        background=NAVBAR_BG,                      # Fondo blanco con opacidad
        backdrop_filter="blur(4px)",           # Blur intenso para efecto glassmorphism
        border_radius="9999px",                 # Pildora completa
        box_shadow="0 4px 24px rgba(0,0,0,0.06)",
        z_index="999",
    )
