"""
Sistema de color oficial - ONANO
Basado en design_system_ONANO.md
"""

# --- COLORES PRIMARIOS (AZUL ONANO) ---
BRAND_PRIMARY_100 = "#062A63"
BRAND_PRIMARY_80 = "#355078"
BRAND_PRIMARY_60 = "#677C9A"
BRAND_PRIMARY_40 = "#9AA7BB"
BRAND_PRIMARY_20 = "#CCD3DD"

# Alias para compatibilidad y uso general
BRAND_DARK_BLUE = BRAND_PRIMARY_100

# --- COLORES SECUNDARIOS (AZUL TECNOLÓGICO) ---
BRAND_SECONDARY_100 = "#0CBCE5"
BRAND_SECONDARY_80 = "#3DC9EA"
BRAND_SECONDARY_60 = "#6DD7EF"
BRAND_SECONDARY_40 = "#9EE4F5"
BRAND_SECONDARY_20 = "#CEF2FA"

# Alias para compatibilidad y uso general
BRAND_LIGHT_BLUE = BRAND_SECONDARY_100

# --- COLORES NEUTRALES ---
BRAND_WHITE = "#FFFFFF"
BRAND_BACKGROUND_ALT = "#F2F4F9"  # Fondo alternativo suave
BRAND_TEXT_DARK = "#383A3F"       # Texto oscuro UI
BRAND_BORDER_SOFT = "#EAECF0"     # Separadores y bordes suaves

# Escala de grises complementarios
BRAND_GRAY_100 = "#F0F0F0"
BRAND_GRAY_200 = "#F3F3F3"
BRAND_GRAY_300 = "#F6F6F6"
BRAND_GRAY_400 = "#F9F9F9"
BRAND_GRAY_500 = "#FCFCFC"

# --- DEGRADADOS ---
# Degradado oficial para botones y acentos llamativos (Ajustado con los colores oficiales)
# NOTA: Ajustamos el ángulo y los colores para coincidir mejor con la identidad visual
BRAND_GRADIENT = f"linear-gradient(180deg, {BRAND_LIGHT_BLUE} 0%, {BRAND_DARK_BLUE} 100%)"
