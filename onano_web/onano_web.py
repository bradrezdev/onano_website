"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

from .pages.index import index
from .state.base_state import State
from .styles.colors import BRAND_DARK_BLUE

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
]

# Meta tags para PWA, SEO y redes sociales
meta = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"},
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
    ),
    head_components=head_config, # Aquí se añaden las etiquetas
)

app.add_page(
    index,
    title="ONANO | Proyecta tu Éxito", # Título más atractivo para el navegador
    meta=meta,
    route="/",
)
