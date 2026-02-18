"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

from .components.ui import liquid_background, blur_overlay, logo, simulation_card, BRAND_LIGHT_BLUE, BRAND_DARK_BLUE

class State(rx.State):
    """The app state."""

def index() -> rx.Component:
    """Página de prueba para el fondo líquido."""
    return rx.center(
        liquid_background(),
        blur_overlay(), # Capa intermedia
        rx.vstack(
            logo(),
            
            # --- SECCIÓN HERO ---
            rx.heading(
                "El Futuro de la Nanotecnología",
                size="8",
                text_align="center",
                color="white",
                padding_x="1em",
            ),
            rx.text(
                "P R Ó X I M A M E N T E …",
                size="5",
                color=BRAND_LIGHT_BLUE,
                weight="medium",
                margin_top="-0.5em",
                text_align="center"
            ),
            
            rx.spacer(margin_top="2em"),

            # --- LLAMADO A LA ACCIÓN ---
            simulation_card(),

            # --- FOOTER / AVISO ---
            #rx.box(
            #    rx.text("Próximamente lanzamiento oficial", size="1", color="white", weight="bold"),
            #    rx.text("® ONANO 2026", size="1", color="white", weight="bold"),
            #    position="fixed",
            #    text_align="center",
            #    width="100%",
            #    bottom="2em",
            #    z_index=1000,
            #),
            align="center",
            spacing="4",
            width="100%",
            z_index=2, # Content above particles
            position="relative", # Ensure z-index works
        ),
        height="100vh",
        width="100%",
        overflow="hidden",
        # Fix: Prevent scroll interference on mobile
        style={"touch-action": "none"},
    )

head_config = [
    # Enlace al manifest para PWA
    rx.el.link(
        rel="manifest",
        href="manifest.json"
    ),

    # Icono para iOS (Safari)
    rx.el.link(
        rel="apple-touch-icon",
        href="apple-touch-icon.png"
    ),
],

# Meta tags para PWA, SEO y redes sociales
meta = [
    {"name": "viewport", "content": "initial-scale=1, viewport-fit=cover, width=device-width"},
    {"name": "apple-mobile-web-app-status-bar-style", "content": "black-translucent"}, 
    {"name": "apple-mobile-web-app-capable", "content": "yes"},
    {"name": "theme-color", "content": BRAND_DARK_BLUE}, 
    
    # --- SEO & DESCRIPTION ---
    {"name": "description", "content": "ONANO | Nanotecnología aplicada al bienestar y la libertad financiera. Únete a la revolución de la nanotecnología y proyecta tu éxito."},
    {"name": "keywords", "content": "nanotecnología, bienestar, simulador financiero, onano, red de mercadeo, salud, tecnología cuántica"},
    {"name": "author", "content": "ONANO Global"},

    # --- OPEN GRAPH (Facebook, WhatsApp, LinkedIn) ---
    {"property": "og:type", "content": "website"},
    {"property": "og:url", "content": "https://onano-web-teal-apple.reflex.run"}, # URL placeholder
    {"property": "og:title", "content": "ONANO | Proyecta tu Éxito"},
    {"property": "og:description", "content": "Innovación en bienestar y libertad financiera. Descubre el futuro de la nanotecnología."},
    {"property": "og:image", "content": "https://onano-web-teal-apple.reflex.run/logotipo-onano.svg"},
]

app = rx.App(
    theme=rx.theme(
        appearance="light",
        head_components=head_config, # Aquí se añaden las etiquetas
    )
)

app.add_page(
    index,
    title="ONANO | Proyecta tu Éxito", # Título más atractivo para el navegador
    meta=meta,
)