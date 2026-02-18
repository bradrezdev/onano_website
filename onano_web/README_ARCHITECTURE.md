# 🏗️ ONANO Software Architecture

Este documento describe la arquitectura de carpetas y archivos implementada para la fase 1 del proyecto ONANO, diseñada para ser escalable y modular.

## 📂 Estructura de Carpetas (`onano_web/`)

### `components/`
Componentes UI reutilizables.
- `layout/`: Componentes estructurales (Navbar, Footer, Sidebar).
- `shared/` (Sugerido): Átomos y moléculas (Botones, Inputs, Cards genéricas).
- `ui.py`: Archivo legacy con componentes específicos (se recomienda refactorizar a subcarpetas a futuro).

### `pages/`
Definición de las rutas y páginas de la aplicación.
- `index.py`: Página de inicio (Landing Page).
- Cada archivo aquí debería corresponder a una ruta o conjunto de rutas relacionadas.

### `state/`
Lógica de negocio y estado de la aplicación (Backend de Reflex).
- `base_state.py`: Estado base de la aplicación.
- Aquí irán los estados específicos como `auth.py`, `dashboard_state.py`, etc.

### `styles/`
Sistema de diseño y estilos globales.
- `colors.py`: Paleta de colores oficial (SSOT - Single Source of Truth).
- `fonts.py`: Definiciones de tipografía.
- `theme.py`: Configuración del tema de Reflex.

### `services/`
Integraciones externas y lógica de datos pura.
- `supabase.py`: (Futuro) Cliente y funciones para interactuar con Supabase.
- Separar la lógica de base de datos del estado de la UI.

### `utils/`
Funciones auxiliares y herramientas transversales.
- Formateadores de fecha, validadores, helpers de strings, etc.

## 🚀 Flujo de Trabajo
1.  **Nuevos Estilos:** Definir variables en `styles/`.
2.  **Nuevos Componentes:** Crear en `components/`.
3.  **Nueva Lógica:** Agregar al `state/`.
4.  **Nueva Página:** Crear archivo en `pages/` y registrar en `onano_web.py`.

---
*Documento generado por el equipo de Agentes ONANO (Adrian, Bryan, Jazmin).*
