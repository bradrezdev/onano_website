import reflex as rx
from ...styles.colors import *
from ...styles.fonts import STYLE_BODY, STYLE_CTA

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, style=STYLE_BODY, color=BRAND_TEXT_DARK),
        href=url,
        text_decoration="none",
        _hover={"opacity": 0.7},
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.image(src="/isologo-dark.svg", height="2.5em"),
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
            padding_y="1em",
        ),
        position="fixed",
        top="0",
        z_index="999",
        backdrop_filter="blur(10px)",
        width="100%",
    )
