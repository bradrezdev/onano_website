import reflex as rx
from ...styles.colors import BRAND_DARK_BLUE, BRAND_WHITE, BRAND_TEXT_DARK
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
                rx.image(src="/logotipo-onano.svg", height="2.5em"),
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
                    bg=BRAND_DARK_BLUE,
                    color=BRAND_WHITE,
                    radius="full",
                    style=STYLE_CTA,
                    size="3",
                    padding_x="1.5em",
                ),
                href="https://office.onanoglobal.com", # External link placeholder
                is_external=True,
                display=["none", "none", "flex", "flex"],
            ),
            # Mobile Menu Trigger (Hamburger - Implementation pending state logic)
            rx.icon("menu", color=BRAND_DARK_BLUE, display=["flex", "flex", "none", "none"]),
            
            width="100%",
            align_items="center",
            padding_x=["1em", "2em", "4em"],
            padding_y="1em",
        ),
        position="sticky",
        top="0",
        z_index="999",
        background="rgba(255, 255, 255, 0.95)",
        backdrop_filter="blur(10px)",
        border_bottom=f"1px solid {BRAND_DARK_BLUE}1A", # 10% opacity
        width="100%",
    )
