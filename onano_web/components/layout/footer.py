import reflex as rx
from ...styles.colors import BRAND_DARK_BLUE, BRAND_WHITE, BRAND_GRAY_400, BRAND_TEXT_DARK
from ...styles.fonts import STYLE_BODY, STYLE_MICRO, STYLE_H3

def footer_section_heading(text: str) -> rx.Component:
    return rx.heading(text, style=STYLE_H3, color=BRAND_WHITE, margin_bottom="1em")

def footer_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, style=STYLE_BODY, color=BRAND_GRAY_400, size="2"),
        href=url,
        text_decoration="none",
        _hover={"color": BRAND_WHITE},
    )

def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.flex(
                # Column 1: Brand
                rx.vstack(
                    rx.image(src="/logotipoBlanco-onano.svg", width="150px"),
                    rx.text(
                        "Ciencia aplicada al bienestar y futuro.",
                        style=STYLE_BODY,
                        color=BRAND_GRAY_400,
                        max_width="250px",
                    ),
                    align_items="start",
                    spacing="4",
                    flex="1",
                ),
                # Column 2: Links
                rx.vstack(
                    footer_section_heading("Empresa"),
                    footer_link("Quiénes somos", "/quienes-somos"),
                    footer_link("Productos", "/productos"),
                    footer_link("Oportunidad", "/oportunidad"),
                    align_items="start",
                    spacing="2",
                    flex="1",
                ),
                # Column 3: Legal
                rx.vstack(
                    footer_section_heading("Legal"),
                    footer_link("Términos y Condiciones", "/terminos"),
                    footer_link("Política de Privacidad", "/privacidad"),
                    footer_link("Descargo de Responsabilidad", "/disclaimer"),
                    align_items="start",
                    spacing="2",
                    flex="1",
                ),
                # Column 4: Contact
                rx.vstack(
                    footer_section_heading("Contacto"),
                    rx.text("soporte@onanoglobal.com", style=STYLE_BODY, color=BRAND_GRAY_400),
                    rx.text("CDMX, México", style=STYLE_BODY, color=BRAND_GRAY_400),
                    align_items="start",
                    spacing="2",
                    flex="1",
                ),
                width="100%",
                flex_direction=["column", "column", "row", "row"],
                spacing="8",
                padding_y="4em",
            ),
            rx.divider(opacity="0.2", border_color=BRAND_WHITE),
            rx.hstack(
                rx.text(
                    "© 2026 ONANO Global. Todos los derechos reservados.",
                    style=STYLE_MICRO,
                    color=BRAND_GRAY_400,
                ),
                rx.spacer(),
                # Social Icons
                rx.hstack(
                    rx.icon("facebook", color=BRAND_WHITE, size=18),
                    rx.icon("instagram", color=BRAND_WHITE, size=18),
                    rx.icon("linkedin", color=BRAND_WHITE, size=18),
                    spacing="4",
                ),
                width="100%",
                padding_y="2em",
                align_items="center",
                flex_direction=["column-reverse", "row"], # Stack on mobile
            ),
            max_width="1200px",
            margin="0 auto",
            padding_x="2em",
        ),
        bg=BRAND_DARK_BLUE,
        width="100%",
    )
