import reflex as rx

from ..components.ui import Isologo, Isotipo

from ..components.layout.navbar import navbar
from ..components.layout.footer import footer
from ..components.ui import molecule_background
from ..styles.colors import (
    BRAND_LIGHT_BLUE,
    BRAND_DARK_BLUE,
    BRAND_WHITE,
)
from ..styles.fonts import STYLE_DISPLAY, STYLE_H2, STYLE_CTA


def hero_section() -> rx.Component:
    """Hero con fondo molecular interactivo y CTA centrado."""
    return rx.box(
        # Contenido superpuesto
        rx.center(
            molecule_background(),
            rx.vstack(
                rx.vstack(
                    rx.heading(
                        "Ciencia que transforma",
                        style=STYLE_DISPLAY,
                        color=BRAND_DARK_BLUE,
                        text_align="center",
                        width="100%",
                    ),
                    rx.text(
                        "Mejorando lo invisible para transformar lo visible.",
                        style=STYLE_H2,
                        color=BRAND_DARK_BLUE,
                        text_align="center",
                        width="100%",
                    ),
                ),
                Isotipo.light(),
                rx.button(
                    "Conoce Más",
                    size="3",
                    radius="full",
                    bg=BRAND_DARK_BLUE,
                    color=BRAND_WHITE,
                    style=STYLE_CTA,
                    padding_x="2.5em",
                    padding_y="1.2em",
                    box_shadow=f"0 8px 30px {BRAND_DARK_BLUE}40",
                    _hover={
                        "transform": "scale(1.05)",
                        "box_shadow": f"0 12px 40px {BRAND_DARK_BLUE}55",
                    },
                    transition="all 0.3s ease",
                    cursor="pointer",
                    margin_top="1em",
                ),
                spacing="9",
                align="center",
                z_index="2",
                padding_x="1.5em",
                max_width="700px",
            ),
            width="100%",
            height="93%",
            z_index="2",
            style={"pointer_events": "auto"},
        ),
        position="relative",
        width="100%",
        height="120dvh",
        overflow="hidden",
    )


def index() -> rx.Component:
    """Página de inicio con fondo molecular interactivo."""
    return rx.box(
        navbar(),
        hero_section(),
        footer(),
        width="100%",
    )