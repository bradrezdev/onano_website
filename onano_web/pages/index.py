import reflex as rx

from ..components.ui import particle_hero_bg
from ..components.buttons import btn_nav
from ..components.layout.navbar import navbar
from ..components.layout.footer import footer
from ..styles.colors import *
from ..styles.fonts import *


# ── CSS ──────────────────────────────────────────────────────────────────────
# Solo lo que Reflex NO puede hacer:
#   - @property (custom property animada)
#   - @keyframes
#   - conic-gradient en .cta-glow-wrap (no hay equiv en Reflex)
#   - will-change + transition en clases que JS manipula por nombre
#   - pseudo-selector :hover para botones de nav
_HERO_CSS = f"""
@property --glow-angle {{
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}}
@keyframes spin-glow {{
  to {{ --glow-angle: 360deg; }}
}}
/* Wrapper del CTA — solo conic-gradient y animación */
.cta-glow-wrap {{
  position: relative;
  display: inline-flex;
  border-radius: 32px;
  padding: 2px;
  background: conic-gradient(
    from var(--glow-angle),
    transparent 0%,
    {BRAND_LIGHT_BLUE} 8%,
    {BRAND_SECONDARY_80} 12%,
    transparent 22%,
    transparent 100%
  );
  animation: spin-glow 3s linear infinite;
  cursor: pointer;
  transition: filter 0.3s ease;
  pointer-events: auto;
}}
.cta-glow-wrap:hover {{
  filter: brightness(1.3) drop-shadow(0 0 14px rgba(12, 188, 229, 0.45));
}}
/* Transición de slides — manipuladas por JS via class_name */
.scroll-slide-0, .scroll-slide-1,
.scroll-slide-2, .scroll-slide-3 {{
  will-change: opacity, transform;
  transition: opacity 0.6s ease, transform 0.6s ease;
  pointer-events: none;
}}
/* Hover de botones de navegación (pseudo-selector, no reemplazable en Reflex) */
.btn-nav:hover {{
  background: rgba(12, 188, 229, 0.12) !important;
  border-color: {BRAND_SECONDARY_80} !important;
}}
"""


# ── Helpers ────────────────────────────────────────────────────

# Nota: btn_nav() viene de ..components.buttons (DRY — Design System centralizado)

def _slide_wrap(idx: int, content: rx.Component, initial_opacity: str = "0") -> rx.Component:
    """
    Capa absolutamente posicionada sobre #scroll-slides (contenedor sticky).
    scroll_timeline.js gestiona opacity/transform vía inline style.
    """
    return rx.box(
        content,
        class_name=f"scroll-slide-{idx}",
        position="absolute",
        top="0",
        left="0",
        width="100%",
        height="100%",
        style={"opacity": initial_opacity},
    )


# ── SLIDE 0 — Hero ─────────────────────────────────────────────

def slide_hero() -> rx.Component:
    """Diapositiva inicial: título principal + CTA con glow giratorio."""
    return _slide_wrap(
        0,
        rx.flex(
            rx.vstack(
                rx.heading(
                    "Nanotecnología",
                    style=STYLE_H3,
                    color=BRAND_SECONDARY_40,
                    text_align="center",
                ),
                rx.text(
                    "Mejorando lo invisible,",
                    style=STYLE_H1,
                    color=BRAND_WHITE,
                    text_align="center",
                ),
                rx.text(
                    "transformando lo visible.",
                    style=STYLE_H1,
                    color=BRAND_WHITE,
                    text_align="center",
                ),
                align="center",
                spacing="0",
                max_width="640px",
            ),
            # ── CTA glow — solo el wrapper necesita CSS (conic-gradient)
            # El botón interior es un componente Reflex nativo.
            rx.box(
                rx.button(
                    "Conocer más",
                    style=STYLE_CTA,
                    color=BRAND_WHITE,
                    background=BRAND_DARK_BLUE,
                    border="none",
                    border_radius="32px",
                    height="64px",
                    padding_x="2.5em",
                    cursor="pointer",
                    white_space="nowrap",
                    pointer_events="auto",
                    letter_spacing="0.02em",
                    _hover={"filter": "none"},  # el hover lo maneja .cta-glow-wrap
                ),
                class_name="cta-glow-wrap",
                id="scroll-cta",
            ),
            direction="column",
            align="center",
            justify="end",
            gap="2.5em",
            width="100%",
            height="100%",
            padding_bottom="10vh",
            padding_x="1.5em",
        ),
        initial_opacity="1",
    )


# ── SLIDES 1-3 — Narrativa Científica ─────────────────────────
# Validado por Dr. Alexander Vance — NanoNutrición Aplicada, IEIA.

def _science_slide(
    idx: int,
    tag: str,
    title: str,
    body: str,
    show_next_btn: bool = False,
    show_prev_btn: bool = False,
) -> rx.Component:
    """
    Slide de narrativa científica alineada a la fase de partículas.
    Botones prev/next con rx.icon (chevrons Lucide) y estilos Reflex nativos.
    Design System — Botón Estándar: h 48px, border-radius 24px.
    """
    nav_row = rx.hstack(
        btn_nav(f"slide-prev-{idx}", "chevron-left") if show_prev_btn else rx.fragment(),
        btn_nav(f"slide-next-{idx}", "chevron-right") if show_next_btn else rx.fragment(),
        spacing="3",
    ) if (show_prev_btn or show_next_btn) else rx.fragment()

    return _slide_wrap(
        idx,
        rx.flex(
            rx.vstack(
                rx.heading(
                    tag,
                    style=STYLE_H3,
                    color=BRAND_SECONDARY_40,
                    text_align="start",
                ),
                rx.text(
                    title,
                    style=STYLE_H1,
                    color=BRAND_WHITE,
                    text_align="start",
                ),
                rx.text(
                    body,
                    style=STYLE_BODY,
                    color=BRAND_WHITE,
                    text_align="start",
                    max_width="520px",
                    padding_top="0.5em",
                ),
                nav_row,
                align="start",
                spacing="0",
                max_width="600px",
            ),
            align="end",
            justify="end",
            width="100%",
            height="100%",
            padding_bottom="10vh",
            padding_x=["1.5em", "3em", "6em", "8em"],
        ),
    )


# ── SCROLL ROOT — 400 vh master container ─────────────────────

def hero_scroll_root() -> rx.Component:
    """
    Contenedor scroll de 400 vh — arquitectura scroll-driven.

    Capas:
      1. Canvas position:fixed  → persiste sin desmontarse mientras se navega.
      2. #scroll-slides sticky  → apilado de diapositivas visibles a 100 vh.
      3. 4 slides superpuestos  → scroll_timeline.js decide cuál es visible
                                  según el porcentaje de scroll en este root.

    Fases del canvas (particle_hero.js v2):
      0  – 33%  →  agglomerated    (vibración moderada)
      33 – 66%  →  dispersing      (sub-clústeres de 3-5 partículas)
      66 – 100% →  encapsulating   (arco de encapsulación por clúster)
    """
    return rx.box(
        # CSS injection
        rx.el.style(_HERO_CSS),

        # Canvas + scripts (position: fixed — persiste en viewport)
        particle_hero_bg(),

        # ── Sticky slide container ─────────────────────────────
        rx.box(
            slide_hero(),
            _science_slide(
                1,
                "Aglomeración",
                "Máxima concentración bioactiva",
                (
                    "Las nanopartículas se organizan en estructuras compactas "
                    "de alta densidad molecular. Esta arquitectura garantiza "
                    "estabilidad química y concentración óptima de principios "
                    "activos antes de la liberación terapéutica."
                ),
                show_next_btn=True,
                show_prev_btn=False,
            ),
            _science_slide(
                2,
                "Dispersión",
                "Liberación en sub-clústeres nanométricos",
                (
                    "Bajo condiciones fisiológicas específicas, los agregados "
                    "se fragmentan en sub-clústeres de 3–5 partículas. Este "
                    "proceso incrementa la superficie activa de contacto celular "
                    "hasta 300 veces, optimizando la biodisponibilidad."
                ),
                show_next_btn=True,
                show_prev_btn=True,
            ),
            _science_slide(
                3,
                "Nanoencapsulación",
                "Recubierta de nueva generación",
                (
                    "Cada sub-aglomeración queda recubierta por una capa "
                    "protectora nanométrica de precisión: biodisponibilidad "
                    "sostenida, protección contra degradación enzimática y "
                    "liberación programada en el sitio terapéutico."
                ),
                show_next_btn=False,
                show_prev_btn=True,
            ),
            id="scroll-slides",
            position="sticky",
            top="0",
            height="100vh",
            z_index="2",
            overflow="hidden",
            pointer_events="none",
        ),

        id="scroll-hero-root",
        height="400vh",
        position="relative",
        bg=BRAND_HERO_BG,
    )


# ── Sección: Valores institucionales ──────────────────────────
# Agente: Bryan (UI) + Adrian (QA Design System)
#
# Pausa visual limpia que contrasta con la estimulación de partículas.
# Fondo neutro BRAND_BACKGROUND_ALT — sin gradientes, sin animaciones.
# Design System:
#   - Contenedor inner: border-radius 24px (h > 48px, regla oficial)
#   - Encabezados: BRAND_DARK_BLUE (#062A63)
#   - Cuerpo: BRAND_TEXT_DARK (#383A3F)
#   - Acento: BRAND_SECONDARY_100 (#0CBCE5)
#   - Fondo sección: BRAND_BACKGROUND_ALT (#F2F4F9)
# Fuente: valores_ONANO.md + brief_estrategico_ONANO.md

_VALORES = [
    (
        "Ciencia Aplicada",
        "Motor de evolución. Desarrollamos cada solución desde la "
        "investigación hasta el resultado, con respaldo científico "
        "verificable en cada etapa.",
    ),
    (
        "Innovación Consciente",
        "Avanzamos sin perder el rumbo. Cada formulación es "
        "intencional, medible y orientada al beneficio real de quien "
        "confía en nuestros productos.",
    ),
    (
        "Liderazgo Responsable",
        "Construimos oportunidades sostenibles con ética, visión de "
        "largo plazo y transparencia total en cada proceso y decisión.",
    ),
    (
        "Respeto por el Entorno",
        "Procesos formulados con respeto al cuerpo y al planeta. "
        "La precisión científica es nuestra forma de responsabilidad.",
    ),
    (
        "Visión Internacional",
        "Estándares globales de calidad en cada producto. Una marca "
        "diseñada para crecer con coherencia más allá de fronteras.",
    ),
]


def _valor_card(nombre: str, descripcion: str) -> rx.Component:
    """
    Tarjeta individual de valor institucional.
    h > 48px → border-radius: 16px per Design System (escala de cards).
    Fondo blanco sobre BRAND_BACKGROUND_ALT — contraste sutil.
    """
    return rx.box(
        rx.vstack(
            # Acento visual — barra corta BRAND_SECONDARY_100
            rx.box(
                width="28px",
                height="3px",
                background=BRAND_SECONDARY_100,
                border_radius="2px",
                flex_shrink="0",
            ),
            rx.heading(
                nombre,
                as_="h3",
                style=STYLE_H3,
                color=BRAND_DARK_BLUE,
            ),
            rx.text(
                descripcion,
                style=STYLE_BODY,
                color=BRAND_TEXT_DARK,
                opacity="0.82",
            ),
            align="start",
            spacing="3",
        ),
        padding_x=["1.25em", "1.5em"],
        padding_y=["1.25em", "1.5em"],
        background=BRAND_WHITE,
        #border_radius="16px",
        #border=f"1px solid {BRAND_BORDER_SOFT}",
        min_height="160px",
    )


def valores_section() -> rx.Component:
    """
    Sección Valores Institucionales — página Inicio (sitemap_ONANO.md).

    Objetivo UX: "reset" visual limpio que permita al usuario respirar
    después de la estimulación del hero scroll-driven de partículas.
    Estética: premium, elegante, respirable. Solo texto. Sin claims técnicos.

    Content source: valores_ONANO.md + brief_estrategico_ONANO.md
    """
    return rx.box(
        # ── Inner card — border-radius 24px per Design System ──
        rx.box(
            # Header del bloque
            rx.vstack(
                rx.text(
                    "SOMOS ONANO",
                    style=STYLE_LABEL,
                    color=BRAND_SECONDARY_100,
                ),
                rx.heading(
                    "Valores institucionales",
                    as_="h2",
                    style=STYLE_H1,
                    color=BRAND_DARK_BLUE,
                ),
                rx.text(
                    "ONANO fundamenta cada decisión en principios que van más allá "
                    "del producto: ciencia aplicada, liderazgo responsable, innovación "
                    "consciente y una visión que trasciende fronteras.",
                    style=STYLE_BODY,
                    color=BRAND_TEXT_DARK,
                    max_width="540px",
                    opacity="0.85",
                ),
                align="start",
                spacing="0",
                width="100%",
            ),
            # Grid de valores — 1 col mobile → 2 col tablet → 3 col desktop
            rx.grid(
                *[_valor_card(n, d) for n, d in _VALORES],
                columns=rx.breakpoints(initial="1", sm="1", md="2", lg="2", xl="3"),
                spacing="4",
                width="100%",
                margin_top="2.5em",
            ),
            # Container inner: border-radius 24px per Design System
            width="100%",
            max_width="1200px",
            margin="0 auto",
            margin_top=["32px", "2em", "3em", "4em", "5em"], # responsive margin-top [mobile, sm, md, lg, xl]
        ),
        position="relative",
        z_index="10",
        id="valores",
        width="100%",
        background=BRAND_WHITE,
        padding_y=["3em", "3.5em", "4.5em"],
        padding_x=["1em", "1.5em", "2em", "2em", "3em"],
    )


# ── Sección: Productos ──────────────────────────
# Agente: Bryan (UI) + Adrian (QA Design System)
# Slider horizontal con cards de productos (nombre + descripción breve + botón para más información).
# Fondo neutro BRAND_BACKGROUND_ALT — sin gradientes, sin animaciones.
# Design System:
#   - Contenedor inner: border-radius 24px (h > 48px, regla oficial)
#   - Encabezados: BRAND_DARK_BLUE (#062A63)
#   - Cuerpo: BRAND_TEXT_DARK (#383A3F)
#   - Acento: BRAND_SECONDARY_100 (#0CBCE5)
#   - Fondo sección: BRAND_BACKGROUND_ALT (#F2F4F9)
# Fuente: productos_ONANO.md

_PRODUCTOS = [
    (
        "Producto 1",
        "Descripción breve del producto 1. Destaca su innovación y beneficio principal sin entrar en detalles técnicos.",
    ),
    (
        "Producto 2",
        "Descripción breve del producto 2. Enfócate en el valor que aporta al usuario final, manteniendo un tono aspiracional.",
    ),
    (
        "Producto 3",
        "Descripción breve del producto 3. Resalta su diferencia clave y cómo mejora la experiencia del cliente.",
    ),
    (
        "Producto 4",
        "Descripción breve del producto 4. Destaca su innovación y beneficio principal sin entrar en detalles técnicos.",
    ),
]


def _product_card(nombre: str, descripcion: str) -> rx.Component:
    """
    Tarjeta individual de producto.
    h > 48px → border-radius: 16px per Design System (escala de cards).
    Fondo blanco sobre BRAND_BACKGROUND_ALT — contraste sutil.
    """
    return rx.box(
        rx.vstack(
            # Acento visual — barra corta BRAND_SECONDARY_100
            rx.vstack(
                rx.heading(
                    nombre,
                    as_="h3",
                    style=STYLE_H3,
                    color=BRAND_DARK_BLUE,
                ),
                rx.image(
                    src="placeholder-producto.svg",
                    alt=f"Imagen de {nombre}",
                    width="100%",
                    border_radius="24px",
                ),
                rx.text(
                    descripcion,
                    style=STYLE_BODY,
                    color=BRAND_TEXT_DARK,
                    opacity="0.82",
                ),
            ),
            rx.button(
                "Más información",
                variant="outline",
                color_scheme="blue",
                size="2",
                radius="full",
                _hover={"bg": f"{BRAND_LIGHT_BLUE}12", "border_color": BRAND_SECONDARY_80},
            ),
            height="100%",
            align="start",
            justify="between",
        ),
        padding_x=["1.25em", "1.5em"],
        padding_y=["1.25em", "1.5em"],
        background=BRAND_WHITE,
        border_radius="24px",
        border=f"1px solid {BRAND_BORDER_SOFT}",
        min_height="160px",
        margin_bottom="1em",
    )


def products_section() -> rx.Component:
    """
    Sección Productos — página Inicio (sitemap_ONANO.md).

    Objetivo UX: "reset" visual limpio que permita al usuario respirar
    después de la estimulación del hero scroll-driven de partículas.
    Estética: premium, elegante, respirable. Solo texto. Sin claims técnicos.

    Content source: productos_ONANO.md + brief_estrategico_ONANO.md
    """
    return rx.box(
        # ── Inner card — border-radius 24px per Design System ──
        rx.box(
            # Header del bloque
            rx.vstack(
                rx.text(
                    "PRODUCTOS",
                    style=STYLE_LABEL,
                    color=BRAND_SECONDARY_100,
                ),
                rx.heading(
                    "Innovación real con nanotecnología certificada",
                    as_="h2",
                    style=STYLE_H1,
                    color=BRAND_DARK_BLUE,
                ),
                align="start",
                spacing="0",
                width="100%",
            ),
            # Grid de productos — 1 col mobile → 2 col tablet → 3 col desktop
            rx.scroll_area(
                rx.grid(
                    *[_product_card(n, d) for n, d in _PRODUCTOS],
                    columns=rx.breakpoints(initial="4", sm="1", md="2", lg="2", xl="3"),
                    spacing="4",
                    width="240%",
                    margin_top="2.5em",
                ),
                direction="horizontal",
                width="100%",
            ),
            # Container inner: border-radius 24px per Design System
            width="100%",
            margin="0 auto",
            margin_top=["32px", "2em", "3em", "4em", "5em"], # responsive margin-top [mobile, sm, md, lg, xl]
        ),
        position="relative",
        z_index="10",
        id="productos",
        width="100%",
        background=BRAND_WHITE,
        padding_y=["3em", "3.5em", "4.5em"],
        padding_x=["1em", "1.5em", "2em", "2em", "3em"],
    )


def index() -> rx.Component:
    """Página de inicio — experiencia narrativa scroll-driven."""
    return rx.box(
        navbar(),
        hero_scroll_root(),
        valores_section(),
        products_section(),
        footer(),
        width="100%",
    )