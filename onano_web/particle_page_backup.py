"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from .components.particles import particles_background

class State(rx.State):
    """The app state."""

# --- COLORES DE MARCA ---
BRAND_DARK_BLUE = "#22439B"
BRAND_LIGHT_BLUE = "#00ACFF"
# Degradado oficial para botones y acentos llamativos
BRAND_GRADIENT = f"linear-gradient(180deg, {BRAND_LIGHT_BLUE} -90%, {BRAND_DARK_BLUE} 100%)"

def logo() -> rx.Component:
    """ONANO logo con tamaño responsivo."""
    return rx.image(
        #src="logotipoBlanco-onano.svg",
        src="logotipo-onano.svg",
        alt="ONANO Logo",
        # Tamaño responsivo: más pequeño en móvil (50%), controlado en escritorio (25em)
        width=["60%", "40%", "25em"], 
        padding_bottom="1em",
    )

def simulation_card() -> rx.Component:
    """Tarjeta destacada para invitar a la simulación."""
    return rx.box(
        rx.vstack(
            rx.heading("Simulador de Ingresos", size="4", weight="bold", color=BRAND_DARK_BLUE),
            rx.text(
                "Proyecta tu libertad financiera. Simula estructuras personalizadas "
                "y visualiza el potencial de tu red.",
                size="2",
                color="gray",
                text_align="center"
            ),
            rx.link(
                rx.button(
                    "Calcular mis Ganancias",
                    bg=BRAND_DARK_BLUE,
                    color="white",
                    size="3",
                    width="100%",
                    radius="full",
                    _hover={
                        "opacity": 0.9,
                        "cursor": "pointer"
                    },
                ),
                href="https://onanoglobal.github.io/calculadora/",
                is_external=True,
                width="100%",
                margin_top="1em",
            ),
            align="center",
            spacing="3",
            padding="1em",
        ),
        bg="white",
        box_shadow="0 4px 14px 0 rgba(0, 172, 255, 0.08)", # Sombra con el azul claro
        width=["90%", "80%", "400px"], # Ancho adaptativo
        border=f"1px solid {BRAND_LIGHT_BLUE}16", # Borde sutil transparente
        border_radius="3em",
    )

def blur_overlay() -> rx.Component:
    """Capa de desenfoque elegante (Glassmorphism)."""
    return rx.box(
        position="fixed",
        top="0",
        left="0",
        width="100%",
        height="100%",
        z_index="1",
        backdrop_filter="blur(20px)",
        background="rgba(255, 255, 255, 0.1)", # Muy sutil para dejar pasar la luz
        style={"pointer_events": "none"}, # Permitir clicks a través
    )

def liquid_background() -> rx.Component:
    """Fondo líquido animado con CSS."""
    return rx.box(
        # Blob 1
        rx.box(
            position="absolute",
            top="-10%",
            left="-10%",
            width="50vw",
            height="50vw",
            background=BRAND_LIGHT_BLUE,
            filter="blur(80px)",
            opacity="0.6",
            border_radius="50%",
            animation="moveBlob1 20s infinite alternate",
        ),
        # Blob 2
        rx.box(
            position="absolute",
            bottom="-10%",
            right="-10%",
            width="60vw",
            height="60vw",
            background=BRAND_DARK_BLUE,
            filter="blur(100px)",
            opacity="0.5",
            border_radius="50%",
            animation="moveBlob2 25s infinite alternate-reverse",
        ),
        # Blob 3 (Accent)
        rx.box(
            position="absolute",
            top="40%",
            left="40%",
            width="40vw",
            height="40vw",
            background="#F1F5F8",
            filter="blur(60px)",
            opacity="0.3",
            border_radius="50%",
            animation="moveBlob3 18s infinite alternate",
        ),
        rx.el.style(
            """
            @keyframes moveBlob1 {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(20vw, 20vh) scale(1.2); }
            }
            @keyframes moveBlob2 {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(-20vw, -10vh) scale(0.9); }
            }
            @keyframes moveBlob3 {
                0% { transform: translate(0, 0) rotate(0deg); }
                50% { transform: translate(-10vw, 20vh) rotate(180deg); }
                100% { transform: translate(10vw, -10vh) rotate(360deg); }
            }
            """
        ),
        position="fixed",
        top="0",
        left="0",
        width="100%",
        height="100%",
        z_index="0",
        background="#0a1128", # Fondo base oscuro
        overflow="hidden",
    )

def liquid_test_page() -> rx.Component:
    """Página de prueba para el fondo líquido."""
    return rx.center(
        liquid_background(),
        blur_overlay(), # Capa intermedia
        rx.vstack(
            logo(),
            rx.heading("Prueba de Fondo Líquido", size="8", color="white", padding_x="1em", text_align="center"),
            rx.text("Efecto fluido + Blur Glassmorphism", size="5", color="white", margin_top="-0.5em", text_align="center"),
            rx.spacer(margin_top="2em"),
            simulation_card(),
            align="center",
            spacing="4",
            width="100%",
            z_index=2,
            position="relative",
        ),
        height="100dvh",
        width="100%",
        overflow="hidden",
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        particles_background(),
        blur_overlay(), # NUEVO: Capa Blur sobre partículas
        rx.vstack(
            logo(),
            
            # --- SECCIÓN HERO ---
            rx.heading(
                "El Futuro de la Nanotecnología",
                size="8",
                text_align="center",
                color=BRAND_DARK_BLUE,
                padding_x="1em",
            ),
            rx.text(
                "Innovación en Bienestar.",
                size="5",
                color=BRAND_DARK_BLUE,
                weight="medium",
                margin_top="-0.5em",
                text_align="center"
            ),
            
            rx.spacer(margin_top="2em"),

            # --- LLAMADO A LA ACCIÓN ---
            simulation_card(),

            # --- FOOTER / AVISO ---
            rx.box(
                rx.text("Próximamente lanzamiento oficial", size="1", color="gray"),
                rx.text("® ONANO 2026", size="1", color="gray", weight="bold"),
                position="fixed",
                text_align="center",
                width="100%",
                bottom="2em",
                z_index=1000,
            ),
            align="center",
            spacing="4",
            width="100%",
            z_index=2, # Content above particles
            position="relative", # Ensure z-index works
        ),
        # Removed background from here to avoid hiding particles
        height="100dvh",
        width="100%",
        overflow="hidden", 
        # Fix: Prevent scroll interference on mobile 
        style={"touch-action": "none"},
    )