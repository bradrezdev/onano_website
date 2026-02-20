"""
Componentes de botones reutilizables — ONANO Design System.

Jerarquía según design_system_ONANO.md:

  Botón Estándar  → h ≤ 48px, border-radius 24px, acciones secundarias.
  Botón CTA       → h ≤ 64px, border-radius 32px, acción principal de pantalla.

Uso:
    from ..components.buttons import btn_nav
    btn_nav("slide-next-1", "chevron-right")
"""

import reflex as rx
from ..styles.colors import BRAND_WHITE, BRAND_SECONDARY_100, BRAND_SECONDARY_80
from ..styles.fonts import STYLE_CTA, STYLE_BODY


# ── Botón Estándar ─────────────────────────────────────────────
# h: 48px | border-radius: 24px | ghost outline | ícono Lucide

_BTN_STANDARD_STYLE: dict = {
    "height": "48px",
    "width": "48px",
    "padding": "0",
    "border": f"1.5px solid {BRAND_SECONDARY_100}",
    "border_radius": "24px",
    "background": "transparent",
    "color": BRAND_WHITE,
    "cursor": "pointer",
    "pointer_events": "auto",
    "transition": "background 0.25s ease, border-color 0.25s ease",
    "display": "inline-flex",
    "align_items": "center",
    "justify_content": "center",
}


def btn_nav(btn_id: str, icon_name: str) -> rx.Component:
    """
    Botón de navegación circular — Design System ONANO (Botón Estándar).
    - Dimensiones: 48 × 48 px, border-radius 24px.
    - Estilo: ghost (borde SECONDARY_100, fondo transparente).
    - Contenido: ícono Lucide (chevron-left / chevron-right).
    - hover definido en _HERO_CSS (.btn-nav:hover) vía CSS pseudo-selector.

    Args:
        btn_id:    ID del elemento HTML (vinculado por scroll_timeline.js).
        icon_name: Nombre del ícono Lucide, e.g. "chevron-left".
    """
    return rx.el.button(
        rx.icon(icon_name, size=20, color=BRAND_WHITE),
        id=btn_id,
        class_name="btn-nav",
        style=_BTN_STANDARD_STYLE,
    )


# ── Botón CTA (interior del wrapper con glow) ──────────────────
# h: 64px | border-radius: 32px | acción principal

_BTN_CTA_STYLE: dict = {
    **STYLE_CTA,
    "height": "64px",
    "padding": "0 2.5em",
    "border": "none",
    "border_radius": "32px",
    "background": "transparent",  # el wrapper .cta-glow-wrap da el fondo
    "color": BRAND_WHITE,
    "cursor": "pointer",
    "pointer_events": "auto",
    "white_space": "nowrap",
    "letter_spacing": "0.02em",
}


def btn_cta_inner(label: str = "Conocer más") -> rx.Component:
    """
    Interior del botón CTA — Design System ONANO (Botón CTA).
    - Dimensiones: h 64px, border-radius 32px.
    - Se usa DENTRO del wrapper .cta-glow-wrap que provee el glow animado.
    - El fondo real lo da el wrapper; este botón es transparente.

    Args:
        label: Texto del botón (default "Conocer más").
    """
    return rx.button(
        label,
        style=_BTN_CTA_STYLE,
        _hover={"filter": "none"},  # hover visual lo maneja .cta-glow-wrap:hover
    )
