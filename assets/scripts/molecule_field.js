/**
 * ONANO Molecule Field v3 — Single Organic Ring Molecule
 *
 * Concepto:
 *   - UNA sola molécula centrada en el canvas.
 *   - Círculo interno: nodos en reposo, posicionados irregularmente (orgánico).
 *   - Círculo externo: 5 % más grande, límite de expansión al hover / tap.
 *   - Sin rotación. Respiración radial sutil. Expansión suave al interactuar.
 *
 * Auto-inicializable con MutationObserver (compatible Reflex SPA).
 *
 * @version 3.0.0
 */

function initMoleculeField(canvasId, options) {
  'use strict';

  /* ════════════════════════════════════════════════════════
     CONFIGURACIÓN POR DEFECTO
     ════════════════════════════════════════════════════════ */
  var defaults = {
    colors: {
      primary:   '#062A63',
      secondary: '#0CBCE5',
      bgStart:   '#FFFFFF',
      bgEnd:     '#F2F4F9',
      dustMuted: '#9AA7BB',
    },
    /* Molécula */
    nodeCount:            24,
    innerRadiusFactor:    0.32,
    expansionPercent:     5,
    /* Conexiones */
    connectionMaxAngle:   Math.PI * 0.45,
    connectionCrossProb:  0.28,
    connectionOpacity:    0.12,
    connectionOpacityHover: 0.24,
    /* Nodos */
    glowSize:             14,
    /* Respiración */
    breathAmplitude:      0.010,
    breathSpeed:          0.0008,
    /* Interacción */
    hoverLerpIn:          0.05,
    hoverLerpOut:         0.028,
    touchHoldMs:          700,
    /* Polvo */
    dustCount:            35,
  };

  var cfg = _deepMerge(defaults, options || {});

  /* ════════════════════════════════════════════════════════
     CANVAS Y ESTADO
     ════════════════════════════════════════════════════════ */
  var canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  var ctx = canvas.getContext('2d');
  var W, H, dpr;
  var mouse = { x: -9999, y: -9999 };
  var touchActive = false;
  var touchTimeout;
  var molecule = null;
  var dustParticles = [];
  var animId;

  /* ════════════════════════════════════════════════════════
     UTILIDADES
     ════════════════════════════════════════════════════════ */
  function _deepMerge(t, s) {
    var o = Object.assign({}, t);
    for (var k in s) {
      if (s[k] && typeof s[k] === 'object' && !Array.isArray(s[k])) {
        o[k] = _deepMerge(o[k] || {}, s[k]);
      } else { o[k] = s[k]; }
    }
    return o;
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function hexToRgb(h) {
    return {
      r: parseInt(h.slice(1, 3), 16),
      g: parseInt(h.slice(3, 5), 16),
      b: parseInt(h.slice(5, 7), 16),
    };
  }
  function rgba(c, a) {
    return 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',' + a + ')';
  }

  var primaryRgb   = hexToRgb(cfg.colors.primary);
  var secondaryRgb = hexToRgb(cfg.colors.secondary);
  var dustRgb      = hexToRgb(cfg.colors.dustMuted);

  /* ════════════════════════════════════════════════════════
     MOLÉCULA  (Single Organic Ring)
     ════════════════════════════════════════════════════════ */
  function Molecule(cx, cy) {
    this.cx = cx;
    this.cy = cy;
    this.hoverT = 0;
    this.isHovered = false;
    this.innerRadius = 0;
    this.outerRadius = 0;
    this.hitRadius = 0;
    this.nodes = [];
    this.connections = [];
    this._nodeScale = 1;

    /* Semilla orgánica: se genera UNA vez para consistencia en resize */
    this._seed = [];
    this._connIndices = [];
    this._generateSeed();
    this.build();
  }

  /**
   * Genera los datos aleatorios del anillo (ángulos, jitter, tamaños).
   * Se llama UNA sola vez en el constructor.
   */
  Molecule.prototype._generateSeed = function () {
    var N = cfg.nodeCount;
    this._seed = [];
    this._connIndices = [];

    /* ── Ángulos base con jitter orgánico ── */
    var angles = [];
    for (var i = 0; i < N; i++) {
      var base = (i / N) * Math.PI * 2;
      var jitter = (Math.random() - 0.5) * (Math.PI * 2 / N) * 0.6;
      angles.push(base + jitter);
    }
    angles.sort(function (a, b) { return a - b; });

    /* ── Datos por nodo ── */
    for (var i = 0; i < N; i++) {
      var isAnchor = (i % 3 === 0);
      this._seed.push({
        angle:        angles[i],
        radialFactor: 1 + (Math.random() - 0.5) * 0.16,
        radius:       isAnchor
                        ? 3.5 + Math.random() * 3.0
                        : 2.0 + Math.random() * 2.0,
        isAnchor:     isAnchor,
        breathPhase:  Math.random() * Math.PI * 2,
        breathAmp:    0.6 + Math.random() * 0.8,
      });
    }

    /* ── Conexiones ── */
    // Anillo backbone
    for (var i = 0; i < N; i++) {
      this._connIndices.push([i, (i + 1) % N]);
    }
    // Cross-connections (triangulación parcial)
    for (var i = 0; i < N; i++) {
      for (var j = i + 2; j < N; j++) {
        if (j === N - 1 && i === 0) continue;
        var ad = Math.abs(this._seed[i].angle - this._seed[j].angle);
        if (ad > Math.PI) ad = Math.PI * 2 - ad;
        if (ad < cfg.connectionMaxAngle && Math.random() < cfg.connectionCrossProb) {
          this._connIndices.push([i, j]);
        }
      }
    }
  };

  /**
   * Calcula posiciones (rest / expanded) según W / H actuales.
   */
  Molecule.prototype.build = function () {
    var minDim = Math.min(W, H);
    this.innerRadius = minDim * cfg.innerRadiusFactor;
    this.outerRadius = this.innerRadius * (1 + cfg.expansionPercent / 100);
    this.hitRadius   = this.outerRadius * 1.35;
    this._nodeScale  = Math.max(0.75, Math.min(1.5, minDim / 800));

    var R        = this.innerRadius;
    var expRatio = this.outerRadius / this.innerRadius;

    this.nodes = [];
    for (var i = 0; i < this._seed.length; i++) {
      var s = this._seed[i];
      var r = R * s.radialFactor;

      var restX = Math.cos(s.angle) * r;
      var restY = Math.sin(s.angle) * r;
      var expandedX = restX * expRatio;
      var expandedY = restY * expRatio;

      this.nodes.push({
        restX:         restX,
        restY:         restY,
        expandedX:     expandedX,
        expandedY:     expandedY,
        radius:        s.radius * this._nodeScale,
        isAnchor:      s.isAnchor,
        renderX:       0,
        renderY:       0,
        currentRadius: s.radius * this._nodeScale,
        breathPhase:   s.breathPhase,
        breathAmp:     s.breathAmp,
      });
    }

    this.connections = this._connIndices;
  };

  /**
   * Update: interpolación hover + respiración radial.
   */
  Molecule.prototype.update = function (time) {
    var target = this.isHovered ? 1 : 0;
    var speed  = this.isHovered ? cfg.hoverLerpIn : cfg.hoverLerpOut;
    this.hoverT = lerp(this.hoverT, target, speed);
    if (Math.abs(this.hoverT - target) < 0.001) this.hoverT = target;

    var ht = this.hoverT;

    for (var i = 0; i < this.nodes.length; i++) {
      var n = this.nodes[i];

      /* Respiración radial */
      var breath = Math.sin(time * cfg.breathSpeed + n.breathPhase)
                   * this.innerRadius * cfg.breathAmplitude * n.breathAmp;

      /* Posición = lerp(rest, expanded) + breathing */
      var bx = lerp(n.restX, n.expandedX, ht);
      var by = lerp(n.restY, n.expandedY, ht);
      var ang = Math.atan2(by, bx);
      bx += Math.cos(ang) * breath;
      by += Math.sin(ang) * breath;

      n.renderX = this.cx + bx;
      n.renderY = this.cy + by;
      n.currentRadius = n.radius * (1 + ht * 0.25);
    }
  };

  /**
   * Render:  glow central  →  conexiones  →  nodos.
   */
  Molecule.prototype.draw = function (ctx) {
    var ht = this.hoverT;

    /* ── 1. Glow central sutil ── */
    var cgR = this.innerRadius * 0.55;
    var cg  = ctx.createRadialGradient(this.cx, this.cy, 0, this.cx, this.cy, cgR);
    cg.addColorStop(0, rgba(secondaryRgb, 0.025 + ht * 0.045));
    cg.addColorStop(1, rgba(secondaryRgb, 0));
    ctx.beginPath();
    ctx.arc(this.cx, this.cy, cgR, 0, Math.PI * 2);
    ctx.fillStyle = cg;
    ctx.fill();

    /* ── 2. Conexiones ── */
    var connAlpha = lerp(cfg.connectionOpacity, cfg.connectionOpacityHover, ht);
    for (var k = 0; k < this.connections.length; k++) {
      var ai = this.connections[k][0];
      var bi = this.connections[k][1];
      var a  = this.nodes[ai];
      var b  = this.nodes[bi];

      var dx   = a.renderX - b.renderX;
      var dy   = a.renderY - b.renderY;
      var dist = Math.sqrt(dx * dx + dy * dy);
      var fade = Math.max(0, 1 - dist / (this.innerRadius * 1.6));

      ctx.beginPath();
      ctx.moveTo(a.renderX, a.renderY);
      ctx.lineTo(b.renderX, b.renderY);
      ctx.strokeStyle = rgba(primaryRgb, connAlpha * fade);
      ctx.lineWidth   = (a.isAnchor || b.isAnchor) ? 1.0 : 0.6;
      ctx.stroke();
    }

    /* ── 3. Nodos ── */
    for (var i = 0; i < this.nodes.length; i++) {
      var n = this.nodes[i];

      /* Glow */
      var glowA = 0.04 + ht * 0.10;
      var glowR = ((n.isAnchor ? cfg.glowSize * 1.4 : cfg.glowSize) + ht * 8) * this._nodeScale;
      var grad  = ctx.createRadialGradient(n.renderX, n.renderY, 0, n.renderX, n.renderY, glowR);
      grad.addColorStop(0, rgba(secondaryRgb, glowA));
      grad.addColorStop(1, rgba(secondaryRgb, 0));
      ctx.beginPath();
      ctx.arc(n.renderX, n.renderY, glowR, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      /* Núcleo */
      var coreRgb   = ht > 0.05 ? secondaryRgb : primaryRgb;
      var coreAlpha = n.isAnchor ? (0.90 + ht * 0.10) : (0.70 + ht * 0.30);
      ctx.beginPath();
      ctx.arc(n.renderX, n.renderY, n.currentRadius, 0, Math.PI * 2);
      ctx.fillStyle = rgba(coreRgb, coreAlpha);
      ctx.fill();
    }
  };

  /**
   * Hit-test circular.
   */
  Molecule.prototype.hitTest = function (mx, my) {
    var dx = mx - this.cx;
    var dy = my - this.cy;
    return (dx * dx + dy * dy) <= this.hitRadius * this.hitRadius;
  };

  /* ════════════════════════════════════════════════════════
     POLVO AMBIENTAL
     ════════════════════════════════════════════════════════ */
  function Dust() { this.reset(true); }

  Dust.prototype.reset = function () {
    this.x  = Math.random() * W;
    this.y  = Math.random() * H;
    this.r  = 1 + Math.random() * 1.8;
    this.a  = 0.03 + Math.random() * 0.06;
    this.vx = (Math.random() - 0.5) * 0.10;
    this.vy = (Math.random() - 0.5) * 0.10;
  };

  Dust.prototype.update = function () {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x < -10 || this.x > W + 10 || this.y < -10 || this.y > H + 10) this.reset();
  };

  Dust.prototype.draw = function (ctx) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = rgba(dustRgb, this.a);
    ctx.fill();
  };

  /* ════════════════════════════════════════════════════════
     RESIZE
     ════════════════════════════════════════════════════════ */
  function resize() {
    var parent = canvas.parentElement;
    W   = parent.clientWidth;
    H   = parent.clientHeight;
    dpr = window.devicePixelRatio || 1;
    canvas.width  = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* ════════════════════════════════════════════════════════
     ESCENA
     ════════════════════════════════════════════════════════ */
  function createScene() {
    molecule = new Molecule(W / 2, H / 2);
    dustParticles = [];
    for (var i = 0; i < cfg.dustCount; i++) {
      dustParticles.push(new Dust());
    }
  }

  /* ════════════════════════════════════════════════════════
     FONDO
     ════════════════════════════════════════════════════════ */
  function drawBg() {
    var g = ctx.createRadialGradient(
      W * 0.5, H * 0.4, 0,
      W * 0.5, H * 0.5, Math.max(W, H) * 0.7
    );
    g.addColorStop(0, cfg.colors.bgStart);
    g.addColorStop(1, cfg.colors.bgEnd);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
  }

  /* ════════════════════════════════════════════════════════
     LOOP DE ANIMACIÓN
     ════════════════════════════════════════════════════════ */
  function animate(time) {
    animId = requestAnimationFrame(animate);
    drawBg();

    for (var i = 0; i < dustParticles.length; i++) {
      dustParticles[i].update();
      dustParticles[i].draw(ctx);
    }

    if (molecule) {
      molecule.isHovered = molecule.hitTest(mouse.x, mouse.y);
      molecule.update(time);
      molecule.draw(ctx);
    }
  }

  /* ════════════════════════════════════════════════════════
     EVENTOS
     ════════════════════════════════════════════════════════ */
  function onMouseMove(e) {
    var rect = canvas.getBoundingClientRect();
    mouse.x = (e.clientX !== undefined ? e.clientX : -9999) - rect.left;
    mouse.y = (e.clientY !== undefined ? e.clientY : -9999) - rect.top;
  }
  function onMouseLeave() { mouse.x = -9999; mouse.y = -9999; }

  function onTouchStart(e) {
    var t = e.touches && e.touches[0];
    if (t) {
      var rect = canvas.getBoundingClientRect();
      mouse.x = t.clientX - rect.left;
      mouse.y = t.clientY - rect.top;
      touchActive = true;
      clearTimeout(touchTimeout);
    }
  }

  function onTouchMove(e) {
    var t = e.touches && e.touches[0];
    if (t) {
      var rect = canvas.getBoundingClientRect();
      mouse.x = t.clientX - rect.left;
      mouse.y = t.clientY - rect.top;
    }
  }

  function onTouchEnd() {
    touchActive = false;
    touchTimeout = setTimeout(function () {
      if (!touchActive) { mouse.x = -9999; mouse.y = -9999; }
    }, cfg.touchHoldMs);
  }

  var resizeTimer;
  function onResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      resize();
      if (molecule) {
        molecule.cx = W / 2;
        molecule.cy = H / 2;
        molecule.build();
      }
      for (var i = 0; i < dustParticles.length; i++) {
        dustParticles[i].reset();
      }
    }, 120);
  }

  /* ════════════════════════════════════════════════════════
     ARRANQUE
     ════════════════════════════════════════════════════════ */
  document.addEventListener('mousemove',  onMouseMove);
  document.addEventListener('mouseleave', onMouseLeave);
  document.addEventListener('touchstart', onTouchStart, { passive: true });
  document.addEventListener('touchmove',  onTouchMove,  { passive: true });
  document.addEventListener('touchend',   onTouchEnd);
  window.addEventListener('resize', onResize);

  resize();
  createScene();
  animate(0);

  return {
    destroy: function () {
      cancelAnimationFrame(animId);
      clearTimeout(touchTimeout);
      document.removeEventListener('mousemove',  onMouseMove);
      document.removeEventListener('mouseleave', onMouseLeave);
      document.removeEventListener('touchstart', onTouchStart);
      document.removeEventListener('touchmove',  onTouchMove);
      document.removeEventListener('touchend',   onTouchEnd);
      window.removeEventListener('resize', onResize);
    },
  };
}

/* ════════════════════════════════════════════════════════
   AUTO-INICIALIZACIÓN  (compatible Reflex SPA)
   ════════════════════════════════════════════════════════ */
(function () {
  var ID    = 'molecule-canvas';
  var _inst = null;

  function boot() {
    var c = document.getElementById(ID);
    if (!c || c.dataset.molInit === '1') return;
    c.dataset.molInit = '1';
    if (_inst && _inst.destroy) _inst.destroy();
    _inst = initMoleculeField(ID);
  }

  var obs = new MutationObserver(boot);
  obs.observe(document.documentElement, { childList: true, subtree: true });
  boot();
})();
