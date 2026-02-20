# CHANGELOG — ONANO Website Hero & Ciencia

**Período**: Feb 19, 2026  
**Version**: v1.0-RC  
**Compilación**: 21/21 ✅

---

## v1.0-RC — Hero Scroll-Driven + Ciencia Slides Complete

### ✨ Features Nuevos

#### Hero Scroll-driven Experience
- **400vh scroll container** con 4 slides apilados (hero + 3 científicas)
- **Canvas position:fixed** con partículas sincronizadas al scroll
- **3 fases de partículas**: Aglomeración → Dispersión → Encapsulación
- **Snap automático** entre peaks de slides (0.0, 0.22, 0.58, 0.88)
- **CTA glow animado** con conic-gradient 360° rotation

#### Ciencia Narrativa
- **Slide 1**: Aglomeración — "Máxima concentración bioactiva"
- **Slide 2**: Dispersión — "Liberación sub-clústeres nanométricos"
- **Slide 3**: Encapsulación — "Recubierta de nueva generación"
- Validado por Dr. Alexander Vance (NanoNutrición Aplicada, IEIA)

#### Componentes Reutilizables (DRY)
- **`btn_nav()`** — Botones estándar (h:48px, r:24px, chevrons)
- **`btn_cta_inner()`** — Botones CTA (h:64px, r:32px)
- Centralizados en `onano_web/components/buttons.py`

### 🐛 Bugs Arreglados

| ID | Issue | Fix |
|----|-------|-----|
| 3️⃣ | CTA skip slide-1 → 2 | Target exacto (0.22) + immunity 600ms |
| 4️⃣ | Dead zone bottom click | `pointer-events: none` CSS + JS dinámico |
| 5️⃣ | Back button slide-2 fail | Removido `pointer_events="none"` hstack |
| 6️⃣ | Scroll-up no ancla hero | SNAP_TARGETS + [0.0] entry |

### 🔧 Technical Improvements

- **JavaScript**: scroll_timeline.js v1.0 con snap immunity + dynamic pointer-events
- **CSS**: @property custom, @keyframes spin-glow, conic-gradient CTA
- **Python**: Reflex components nativos + estilos Design System centralizados
- **QA**: 21/21 compilación exitosa, sin tracebacks

### 📊 Metrics

| Métrica | Valor |
|---------|-------|
| Componentes compilados | 21/21 ✅ |
| Archivos Python sin errores | 3/3 ✅ |
| Bugs arreglados | 4/4 ✅ |
| Slides científicas | 3/3 ✅ |
| Snap targets configurados | 4 (0.0, 0.22, 0.58, 0.88) |

### 🎯 Design System Compliance

- ✅ Botones Estándar: h 48px, r 24px
- ✅ Botones CTA: h 64px, r 32px
- ✅ Colors: BRAND primarios + SECONDARY gradients
- ✅ Tipografía: H1, H3, BODY per specs
- ✅ Mobile-first: Responsive breakpoints `["520px","768px","1024px","1280px","1640px"]`

---

## Breaking Changes

Ninguno — versión inicial compatible con futuras expansiones.

---

## Migration Guide

Para usar en desarrollo:

```bash
cd /Users/bradrez/Documents/bradrez_projects/onano/onano-web
source .venv/bin/activate
reflex run
# App running at: http://localhost:3000
```

**Nuevos imports disponibles**:
```python
from onano_web.components.buttons import btn_nav, btn_cta_inner
from onano_web.components import particle_hero_bg
```

---

## Known Limitations

- Canvas resize no optimizado (TODO: ResizeObserver)
- Touch gesture refinements necesarios para iPad (Phase 2)
- Performance audit pending (Lighthouse)

---

## Next Phase (Roadmap)

- [ ] Section "Descubre la Nanociencia" (Phase 2)
- [ ] E-commerce module + product grid
- [ ] Dashboard multinivel + comisiones
- [ ] Supabase auth integration
- [ ] Mobile gesture refinements

---

**Maintained by**: Adrian (Senior Dev & QA)  
**Contributors**: Bryan (Frontend), Jazmin (Backend)  
**Documentation**: [PROGRESS.md](.github/PROGRESS.md)
