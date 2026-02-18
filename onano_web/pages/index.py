import reflex as rx
from ..components.ui import liquid_background, blur_overlay, logo, simulation_card
from ..components.layout.navbar import navbar
from ..components.layout.footer import footer
from ..styles.colors import BRAND_LIGHT_BLUE, BRAND_DARK_BLUE, BRAND_WHITE, BRAND_GRAY_100
from ..styles.fonts import STYLE_H1, STYLE_H2, STYLE_BODY, STYLE_DISPLAY

def hero_section() -> rx.Component:
    """Sección Hero Corporativo con fondo líquido."""
    return rx.box(
        liquid_background(),
        blur_overlay(),
        rx.vstack(
            rx.heading(
                "Innovación Cuántica para tu Bienestar", 
                style=STYLE_DISPLAY,
                color=BRAND_WHITE,
                text_align="center",
            ),
            rx.text(
                "Descubre la nanotecnología que está revolucionando la salud y la libertad financiera.",
                style=STYLE_H2,
                color=BRAND_LIGHT_BLUE,
                text_align="center",
                max_width="600px",
            ),
            rx.spacer(height="2em"),
            simulation_card(),
            
            align="center",
            justify="center",
            height="100%",
            width="100%",
            spacing="5",
            z_index=2,
            padding_x="1em",
        ),
        position="relative",
        height="100vh",
        width="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="hidden",
    )

def science_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Ciencia Aplicada", style=STYLE_H1, color=BRAND_DARK_BLUE),
            rx.text(
                "Nuestra tecnología se basa en principios de física cuántica y nanotecnología avanzada...",
                style=STYLE_BODY,
                color="black",
            ),
            align="center",
            spacing="4",
            padding="4em 2em",
            max_width="1200px",
            margin="0 auto",
        ),
        bg=BRAND_GRAY_100,
        width="100%",
    )

def values_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Nuestros Valores", style=STYLE_H1, color=BRAND_DARK_BLUE),
            rx.text("Innovación • Integridad • Comunidad", style=STYLE_BODY),
            align="center",
            spacing="4",
            padding="4em 2em",
        ),
        width="100%",
        bg=BRAND_WHITE,
    )

def products_preview_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Productos Destacados", style=STYLE_H1, color=BRAND_DARK_BLUE),
            rx.text("Próximamente...", style=STYLE_BODY),
            align="center",
            spacing="4",
            padding="4em 2em",
        ),
        width="100%",
        bg=BRAND_GRAY_100,
    )

def index() -> rx.Component:
    """Página de inicio (Landing Page) según Sitemap."""
    return rx.box(
        navbar(),
        hero_section(),
        science_section(),
        values_section(),
        products_preview_section(),
        footer(),
        width="100%",
    )
