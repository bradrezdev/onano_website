import reflex as rx
from ..styles.colors import BRAND_DARK_BLUE, BRAND_LIGHT_BLUE, BRAND_GRADIENT

def logo() -> rx.Component:
    """ONANO logo con tamaño responsivo."""
    return rx.image(
        src="isologo-dark.svg",
        #src="logotipo-onano.svg",
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
            padding="1.25em",
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
    """Fondo líquido animado con CSS + Interactividad JS (Smooth)."""
    return rx.box(
        # Script externo para lógica de movimiento (Separation of Concerns)
        rx.script(src="/scripts/liquid_interaction.js"),
        
        # Blob 1 (Parallax opuesto)
        rx.box(
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
            style={
                "position": "absolute", 
                "top": "0", 
                "left": "0", 
                "width": "100%", 
                "height": "100%",
                # Transformación controlada por JS (lerp) mediante variables CSS
                "transform": "translate(calc((var(--mouse-x, 0.5) - 0.5) * -120px), calc((var(--mouse-y, 0.5) - 0.5) * -120px))",
                # IMPORTANTE: Sin transition aquí, el JS se encarga del suavizado (evita conflicto/jitter)
            }
        ),
        # Blob 2 (Parallax opuesto fuerte)
        rx.box(
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
            style={
                "position": "absolute", 
                "top": "0", 
                "left": "0", 
                "width": "100%", 
                "height": "100%",
                "transform": "translate(calc((var(--mouse-x, 0.5) - 0.5) * -180px), calc((var(--mouse-y, 0.5) - 0.5) * -180px))",
            }
        ),
        # Blob 3 Accent (Sigue al mouse suavemente)
        rx.box(
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
            style={
                "position": "absolute", 
                "top": "0", 
                "left": "0", 
                "width": "100%", 
                "height": "100%",
                "transform": "translate(calc((var(--mouse-x, 0.5) - 0.5) * 60px), calc((var(--mouse-y, 0.5) - 0.5) * 60px))",
            }
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
        style={"pointer-events": "none"}, # Asegurar que el fondo no bloquee nada
    )
