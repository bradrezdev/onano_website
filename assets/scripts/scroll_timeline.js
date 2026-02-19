/**
 * ONANO Scroll Timeline v1.0
 *
 * Controlador maestro de scroll para la experiencia narrativa del HERO.
 * Lee el progreso de scroll sobre #scroll-hero-root y:
 *
 *  1. Pasa el progreso normalizado (0–1) a la API de partículas.
 *  2. Controla el fade-in/out de los slides de texto (.scroll-slide-N).
 *  3. Gestiona el fade del canvas al salir de la sección.
 *  4. Implementa el smooth-scroll para el CTA button.
 *
 * Sin dependencias externas. Compatible con Safari iOS.
 *
 * @version 1.0.0
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────
     CONSTANTES
     ───────────────────────────────────────────────────── */
  var ROOT_ID   = 'scroll-hero-root';
  var SLIDES_ID = 'scroll-slides';
  var CTA_ID    = 'scroll-cta';

  /**
   * Ventanas de visibilidad por slide (fracción del progreso 0–1).
   * Orden: [slide-hero, slide-science-1, slide-science-2, slide-science-3]
   */
  var SLIDE_WINDOWS = [
    { fadeIn: -0.1, peak: 0.0, fadeOut: 0.08, gone: 0.20 },  // slide-0: hero
    { fadeIn: 0.12, peak: 0.22, fadeOut: 0.44, gone: 0.56 }, // slide-1: aglomerado
    { fadeIn: 0.48, peak: 0.58, fadeOut: 0.74, gone: 0.84 }, // slide-2: dispersión
    { fadeIn: 0.78, peak: 0.88, fadeOut: 1.10, gone: 1.20 }, // slide-3: encapsulación
  ];

  /* ─────────────────────────────────────────────────────
     UTILIDADES
     ───────────────────────────────────────────────────── */
  function lerp(a, b, t)   { return a + (b - a) * t; }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function easeInOut(t)    { return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; }
  function easeOut(t)      { return 1 - (1 - t) * (1 - t); }

  function opacity01(p, win) {
    if (p < win.fadeIn)  return 0;
    if (p < win.peak)    return easeOut((p - win.fadeIn) / (win.peak - win.fadeIn));
    if (p <= win.fadeOut) return 1;
    if (p < win.gone)    return 1 - easeInOut((p - win.fadeOut) / (win.gone - win.fadeOut));
    return 0;
  }

  /* ─────────────────────────────────────────────────────
     ESTADO INTERNO
     ───────────────────────────────────────────────────── */
  var root, slides, canvasWrap, ctaEl;
  var rawProgress      = 0;
  var smoothProgress   = 0;
  var rafId;
  var initialized      = false;

  /* ─────────────────────────────────────────────────────
     CÁLCULO DE PROGRESO
     ───────────────────────────────────────────────────── */
  function computeRawProgress() {
    if (!root) return 0;
    var rect  = root.getBoundingClientRect();
    var total = root.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    return clamp(-rect.top / total, 0, 1);
  }

  /* ─────────────────────────────────────────────────────
     APLICAR SLIDES
     ───────────────────────────────────────────────────── */
  function applySlides(p) {
    if (!slides) return;
    for (var i = 0; i < SLIDE_WINDOWS.length; i++) {
      var el = slides.querySelector('.scroll-slide-' + i);
      if (!el) continue;
      var op = opacity01(p, SLIDE_WINDOWS[i]);
      el.style.opacity = op;
      /* translateY: entra desde +40px, sale hacia -40px */
      var ty = 0;
      var w  = SLIDE_WINDOWS[i];
      if (p < w.peak && p > w.fadeIn) {
        ty = (1 - easeOut((p - w.fadeIn) / (w.peak - w.fadeIn))) * 40;
      } else if (p > w.fadeOut && p < w.gone) {
        ty = -easeInOut((p - w.fadeOut) / (w.gone - w.fadeOut)) * 40;
      }
      el.style.transform = 'translateY(' + ty + 'px)';
    }
  }

  /* ─────────────────────────────────────────────────────
     APLICAR CANVAS FADE
     Fade-out cuando el scroll root empieza a salir del viewport.
     ───────────────────────────────────────────────────── */
  function applyCanvasFade(p) {
    if (!canvasWrap) return;
    if (!root) { canvasWrap.style.opacity = 1; return; }

    /* Fade in al entrar (por si el canvas empieza oculto) */
    var rectTop = root.getBoundingClientRect().top;
    if (rectTop > window.innerHeight * 0.2) {
      canvasWrap.style.opacity = 0;
      return;
    }

    /* Fade out al salir (bottom del root pasa de la pantalla) */
    var rectBottom = root.getBoundingClientRect().bottom;
    if (rectBottom < window.innerHeight * 0.5) {
      var fade = clamp(rectBottom / (window.innerHeight * 0.5), 0, 1);
      canvasWrap.style.opacity = easeInOut(fade);
      return;
    }

    canvasWrap.style.opacity = 1;
  }

  /* ─────────────────────────────────────────────────────
     RAF LOOP
     ───────────────────────────────────────────────────── */
  function tick() {
    rafId = requestAnimationFrame(tick);

    rawProgress    = computeRawProgress();
    smoothProgress = lerp(smoothProgress, rawProgress, 0.09);

    /* Umbral mínimo para evitar micro-updates */
    var delta = Math.abs(smoothProgress - rawProgress);
    var p     = delta < 0.0004 ? rawProgress : smoothProgress;

    /* Partículas */
    if (window.__oParticleHero) {
      window.__oParticleHero.setScrollProgress(p);
    }

    /* Texto + canvas */
    applySlides(p);
    applyCanvasFade(p);
  }

  /* ─────────────────────────────────────────────────────
     SMOOTH SCROLL  (CTA "Conocer más")
     Interpolación manual con easing — no depende de CSS scroll-behavior.
     ───────────────────────────────────────────────────── */
  function smoothScrollTo(targetY, durationMs) {
    var startY     = window.scrollY;
    var delta      = targetY - startY;
    var startTime  = null;

    function step(time) {
      if (!startTime) startTime = time;
      var elapsed = time - startTime;
      var t       = clamp(elapsed / durationMs, 0, 1);
      var ease    = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOut cubic
      window.scrollTo(0, startY + delta * ease);
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function bindCTA() {
    if (!ctaEl || ctaEl.dataset.ctaBound) return;
    ctaEl.dataset.ctaBound = '1';
    ctaEl.addEventListener('click', function (e) {
      e.preventDefault();
      if (!root) return;
      /* Desplazar al 28% de la sección (pico visible de slide-1) */
      var targetScroll = root.offsetTop + (root.offsetHeight - window.innerHeight) * 0.28;
      /* ⏱ VELOCIDAD DEL CTA — ajusta este valor para cambiar la duración:
         900 ms = rápido | 1200 ms = normal | 1600 ms = lento             */
      smoothScrollTo(targetScroll, 150);
    });
  }

  /* ─────────────────────────────────────────────────────
     BOOT — espera que el DOM esté listo
     ───────────────────────────────────────────────────── */
  function boot() {
    root       = document.getElementById(ROOT_ID);
    slides     = document.getElementById(SLIDES_ID);
    ctaEl      = document.getElementById(CTA_ID);
    canvasWrap = document.getElementById('particle-hero-canvas')
                 ? document.getElementById('particle-hero-canvas').parentElement
                 : null;

    if (!root || !slides) return;
    if (initialized) return;
    initialized = true;

    bindCTA();
    cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(tick);
  }

  var obs = new MutationObserver(boot);
  obs.observe(document.documentElement, { childList: true, subtree: true });
  boot();

  /* Rebind en caso de navegación SPA */
  window.addEventListener('popstate', function () {
    initialized = false;
    boot();
  });

})();
