import reflex as rx
from ..components.layout.navbar import navbar
from ..components.layout.footer import footer
from ..components.ui import spline, SPLINE_SCENE
from ..styles.colors import (
    BRAND_LIGHT_BLUE,
    BRAND_DARK_BLUE,
    BRAND_WHITE,
    BRAND_RADIAL_GRADIENT,
)
from ..styles.fonts import STYLE_H1, STYLE_DISPLAY, STYLE_BODY, STYLE_CTA


def hero_section() -> rx.Component:
    """Sección Hero con Spline 3D interactivo y contenido centrado."""
    return rx.box(
        # Fondo con Spline 3D
        rx.box(
            spline(scene=SPLINE_SCENE),
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            z_index="1",
        ),
        # Overlay degradado radial
        rx.box(
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            background=BRAND_RADIAL_GRADIENT,
            opacity="0.3",
            z_index="2",
        ),
        # Contenido centrado
        rx.center(
            rx.vstack(
                rx.heading(
                    "Mejorando invisible, transformando",
                    style=STYLE_DISPLAY,
                    color=BRAND_WHITE,
                    text_align="center",
                    margin_bottom="120px",
                    width="100%",
                ),
                rx.button(
                    "Conoce Más",
                    size="3",
                    radius="full",
                    bg=BRAND_WHITE,
                    color=BRAND_DARK_BLUE,
                    style=STYLE_CTA,
                    padding_x="2em",
                    padding_y="1em",
                    box_shadow="0 10px 30px rgba(0, 0, 0, 0.3)",
                    _hover={
                        "transform": "scale(1.05)",
                        "box_shadow": "0 15px 40px rgba(0, 0, 0, 0.4)",
                    },
                    transition="all 0.3s ease",
                    cursor="pointer",
                ),
                align="center",
                z_index="3",
                padding_x="1em",
            ),
            width="100%",
            height="100%",
            z_index="3",
        ),
        position="relative",
        width="100%",
        height="120dvh",
        overflow="hidden",
    )


def index() -> rx.Component:
    """Página de inicio redesñada con Spline 3D."""
    return rx.box(
        navbar(),
        hero_section(),
        footer(),
        width="100%",
    )