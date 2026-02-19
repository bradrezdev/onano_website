/**
 * ONANO Particle Hero — Nanoparticle Agglomeration → Dispersion
 *
 * Simula científicamente la transición de una aglomeración compacta
 * de partículas hacia pequeñas aglomeraciones de nanopartículas.
 *
 * Estados:
 *   1. AGGLOMERATED  — Clúster central compacto con micro-vibración
 *   2. DISPERSING    — Transición (burst outward)
 *   3. DISPERSED     — Pequeños clústeres de 3-5 partículas flotando
 *
 * Interacción: click / tap sobre la aglomeración activa la dispersión.
 * Auto-inicializable con MutationObserver (Reflex SPA).
 *
 * @version 1.0.0
 */

function initParticleHero(canvasId, opts) {
  'use strict';

  /* ═══════════════════════════════════════════════════════
     CONFIGURACIÓN
     ═══════════════════════════════════════════════════════ */
  var D = {
    particleCount:       120,
    clusterMin:          3,
    clusterMax:          5,
    /* Colores  (RGB arrays para rgba() rápida) */
    cyan:        [12, 188, 229],     // #0CBCE5
    cyanLight:   [61, 201, 234],     // #3DC9EA
    cyanPale:    [206, 242, 250],    // #CEF2FA
    darkBlue:    [6,  42,  99],      // #062A63
    bg:          '#070D1A',
    /* Aglomeración */
    agglomRadius:   0.10,           // fracción de min(W,H)
    agglomGlow:     0.18,           // radio del glow central
    /* Vibración */
    vibAmp:         2.8,            // px
    vibSpeedMin:    0.6,
    vibSpeedMax:    2.0,
    /* Dispersión */
    impulseMin:     5,
    impulseMax:     11,
    transitionMs:   1800,
    /* Física (post-dispersión) */
    attraction:     0.028,
    friction:       0.974,
    containerForce: 0.009,
    drift:          0.006,
    /* Contención elíptica (fracción viewport) */
    containX:       0.42,           // semi-eje X  (~84 % ancho)
    containY:       0.20,           // semi-eje Y  (~40 % alto ≈ 50 vh visual)
    /* Render */
    glowMul:        3.5,
    connAlphaAgg:   0.055,
    connAlphaDisp:  0.22,
    /* Pulso visual (hint interactividad) */
    pulseSpeed:     0.0012,
    pulseAmp:       0.25,
  };

  if (opts) { for (var k in opts) { if (opts.hasOwnProperty(k)) D[k] = opts[k]; } }

  /* ═══════════════════════════════════════════════════════
     CANVAS
     ═══════════════════════════════════════════════════════ */
  var canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  var ctx    = canvas.getContext('2d');
  var W = 0, H = 0, dpr = 1;
  var animId;

  /* ═══════════════════════════════════════════════════════
     ESTADO
     ═══════════════════════════════════════════════════════ */
  var STATE = 'agglomerated';   // 'agglomerated' | 'dispersing' | 'dispersed'
  var particles   = [];
  var clusterMeta = [];         // { targetX, targetY, driftVx, driftVy }

  /* ═══════════════════════════════════════════════════════
     UTILIDADES
     ═══════════════════════════════════════════════════════ */
  function rgba(c, a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
  function rand(lo, hi) { return lo + Math.random() * (hi - lo); }
  function gaussRand() {
    var u = 1 - Math.random(), v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  /* ═══════════════════════════════════════════════════════
     PARTÍCULA
     ═══════════════════════════════════════════════════════ */
  function Particle(x, y, cid) {
    this.x  = x;   this.y  = y;
    this.hx = x;   this.hy = y;       // home (agglomerated)
    this.vx = 0;   this.vy = 0;
    this.r  = rand(1.4, 4.6);
    this.op = rand(0.45, 0.95);
    this.cid = cid;                     // cluster id
    /* vibración */
    this.vPhase = Math.random() * Math.PI * 2;
    this.vSpd   = rand(D.vibSpeedMin, D.vibSpeedMax);
    this.vDirX  = (Math.random() - 0.5) * 2;
    this.vDirY  = (Math.random() - 0.5) * 2;
  }

  /* ═══════════════════════════════════════════════════════
     CREAR ESCENA
     ═══════════════════════════════════════════════════════ */
  function createScene() {
    var cx = W / 2, cy = H / 2;
    var baseR = Math.min(W, H) * D.agglomRadius;

    /* Asignar cluster IDs */
    particles   = [];
    clusterMeta = [];
    var assignments = [];
    var cid = 0;
    while (assignments.length < D.particleCount) {
      var sz = D.clusterMin + Math.floor(Math.random() * (D.clusterMax - D.clusterMin + 1));
      for (var s = 0; s < sz && assignments.length < D.particleCount; s++) {
        assignments.push(cid);
      }
      cid++;
    }
    /* Shuffle */
    for (var i = assignments.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = assignments[i]; assignments[i] = assignments[j]; assignments[j] = tmp;
    }

    /* Crear partículas — distribución gaussiana */
    for (var i = 0; i < D.particleCount; i++) {
      var ang  = Math.random() * Math.PI * 2;
      var dist = Math.min(Math.abs(gaussRand()) * baseR * 0.45, baseR * 1.2);
      particles.push(new Particle(
        cx + Math.cos(ang) * dist,
        cy + Math.sin(ang) * dist,
        assignments[i]
      ));
    }

    /* Metadata de clústeres */
    for (var c = 0; c < cid; c++) {
      clusterMeta.push({ targetX: cx, targetY: cy, driftVx: 0, driftVy: 0 });
    }
  }

  /* ═══════════════════════════════════════════════════════
     DISPERSIÓN
     ═══════════════════════════════════════════════════════ */
  function disperse() {
    if (STATE !== 'agglomerated') return;
    STATE = 'dispersing';

    var cx = W / 2, cy = H / 2;
    var ellA = W * D.containX;
    var ellB = H * D.containY;

    /* Posiciones objetivo para cada clúster */
    for (var c = 0; c < clusterMeta.length; c++) {
      var ang = (c / clusterMeta.length) * Math.PI * 2 + rand(-0.4, 0.4);
      var rf  = rand(0.25, 0.82);
      clusterMeta[c].targetX = cx + Math.cos(ang) * ellA * rf;
      clusterMeta[c].targetY = cy + Math.sin(ang) * ellB * rf;
      clusterMeta[c].driftVx = rand(-0.15, 0.15);
      clusterMeta[c].driftVy = rand(-0.15, 0.15);
    }

    /* Impulso de salida a cada partícula */
    for (var i = 0; i < particles.length; i++) {
      var p   = particles[i];
      var ang = Math.atan2(p.y - cy, p.x - cx) + rand(-0.45, 0.45);
      var imp = rand(D.impulseMin, D.impulseMax);
      p.vx = Math.cos(ang) * imp;
      p.vy = Math.sin(ang) * imp;
    }

    setTimeout(function () { STATE = 'dispersed'; }, D.transitionMs);
  }

  /* ═══════════════════════════════════════════════════════
     UPDATE
     ═══════════════════════════════════════════════════════ */
  function update(t) {
    var cx = W / 2, cy = H / 2;
    var i, p, cl;

    if (STATE === 'agglomerated') {
      /* ── Micro-vibración + atracción suave al centro ── */
      for (i = 0; i < particles.length; i++) {
        p = particles[i];
        var vib = Math.sin(t * 0.001 * p.vSpd + p.vPhase);
        p.x = p.hx + vib * p.vDirX * D.vibAmp;
        p.y = p.hy + vib * p.vDirY * D.vibAmp;
        /* Atracción leve hacia el centro (cohesión) */
        var dx = cx - p.hx, dy = cy - p.hy;
        var d  = Math.sqrt(dx * dx + dy * dy);
        if (d > 2) {
          p.hx += dx * 0.0004;
          p.hy += dy * 0.0004;
        }
      }
    } else {
      /* ── Dispersing / Dispersed — física ── */
      var ellA = W * D.containX;
      var ellB = H * D.containY;

      /* Drift orgánico de clústeres */
      for (i = 0; i < clusterMeta.length; i++) {
        cl = clusterMeta[i];
        cl.targetX += cl.driftVx;
        cl.targetY += cl.driftVy;
        /* Contención suave */
        var nx = (cl.targetX - cx) / ellA;
        var ny = (cl.targetY - cy) / ellB;
        var nd = nx * nx + ny * ny;
        if (nd > 0.82) {
          var push = (nd - 0.82) * 0.025;
          cl.driftVx -= nx * push;
          cl.driftVy -= ny * push;
        }
        cl.driftVx += (Math.random() - 0.5) * D.drift;
        cl.driftVy += (Math.random() - 0.5) * D.drift;
        cl.driftVx *= 0.996;
        cl.driftVy *= 0.996;
      }

      /* Actualizar partículas */
      for (i = 0; i < particles.length; i++) {
        p  = particles[i];
        cl = clusterMeta[p.cid];

        /* Atracción hacia target del clúster */
        var dx = cl.targetX - p.x;
        var dy = cl.targetY - p.y;
        var dd = Math.sqrt(dx * dx + dy * dy);
        if (dd > 1) {
          var force = D.attraction * Math.min(dd * 0.12, 1);
          p.vx += (dx / dd) * force;
          p.vy += (dy / dd) * force;
        }

        /* Micro-vibración residual */
        var vib = Math.sin(t * 0.001 * p.vSpd + p.vPhase);
        p.vx += vib * p.vDirX * 0.018;
        p.vy += vib * p.vDirY * 0.018;

        /* Fricción */
        p.vx *= D.friction;
        p.vy *= D.friction;

        /* Integrar posición */
        p.x += p.vx;
        p.y += p.vy;

        /* Contención elíptica individual */
        var enx = (p.x - cx) / (ellA * 1.08);
        var eny = (p.y - cy) / (ellB * 1.08);
        var end = enx * enx + eny * eny;
        if (end > 1) {
          var ef = (end - 1) * D.containerForce * 9;
          p.vx -= enx * ef;
          p.vy -= eny * ef;
        }
      }
    }
  }

  /* ═══════════════════════════════════════════════════════
     RENDER
     ═══════════════════════════════════════════════════════ */
  function draw(t) {
    /* Fondo */
    ctx.fillStyle = D.bg;
    ctx.fillRect(0, 0, W, H);

    /* Viñeta radial sutil */
    var vigR = Math.max(W, H) * 0.7;
    var vig  = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, vigR);
    vig.addColorStop(0, rgba(D.cyan, 0.018));
    vig.addColorStop(0.5, rgba(D.darkBlue, 0.008));
    vig.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = vig;
    ctx.fillRect(0, 0, W, H);

    if (STATE === 'agglomerated') {
      drawAgglomerated(t);
    } else {
      drawDispersed();
    }
  }

  /* ── Render: aglomeración ─────────────────────────────── */
  function drawAgglomerated(t) {
    var cx = W / 2, cy = H / 2;

    /* Glow central pulsante (hint de interactividad) */
    var pulse = 1 + Math.sin(t * D.pulseSpeed) * D.pulseAmp * 0.35;
    var glR   = Math.min(W, H) * D.agglomGlow * pulse;
    var glow  = ctx.createRadialGradient(cx, cy, 0, cx, cy, glR);
    glow.addColorStop(0,   rgba(D.cyan, 0.065));
    glow.addColorStop(0.4, rgba(D.cyan, 0.025));
    glow.addColorStop(1,   rgba(D.cyan, 0));
    ctx.beginPath();
    ctx.arc(cx, cy, glR, 0, Math.PI * 2);
    ctx.fillStyle = glow;
    ctx.fill();

    /* Conexiones internas (bonds moleculares, muy sutiles) */
    var baseR = Math.min(W, H) * D.agglomRadius;
    var thresh = baseR * baseR * 0.12;
    ctx.beginPath();
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var dx = particles[i].x - particles[j].x;
        var dy = particles[i].y - particles[j].y;
        if (dx * dx + dy * dy < thresh) {
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
        }
      }
    }
    ctx.strokeStyle = rgba(D.cyan, D.connAlphaAgg);
    ctx.lineWidth   = 0.4;
    ctx.stroke();

    /* Partículas */
    drawParticles();
  }

  /* ── Render: dispersión ───────────────────────────────── */
  function drawDispersed() {
    var i, c, m, a, b;

    /* Por cada clúster: glow compartido + conexiones internas */
    for (c = 0; c < clusterMeta.length; c++) {
      var members = [];
      for (i = 0; i < particles.length; i++) {
        if (particles[i].cid === c) members.push(particles[i]);
      }
      if (members.length < 2) continue;

      /* Centro del clúster */
      var avgX = 0, avgY = 0;
      for (m = 0; m < members.length; m++) { avgX += members[m].x; avgY += members[m].y; }
      avgX /= members.length;
      avgY /= members.length;

      /* Glow compartido (refuerza apariencia de aglomeración) */
      var cgR  = 28 + members.length * 3;
      var cGlow = ctx.createRadialGradient(avgX, avgY, 0, avgX, avgY, cgR);
      cGlow.addColorStop(0, rgba(D.cyan, 0.03));
      cGlow.addColorStop(1, rgba(D.cyan, 0));
      ctx.beginPath();
      ctx.arc(avgX, avgY, cgR, 0, Math.PI * 2);
      ctx.fillStyle = cGlow;
      ctx.fill();

      /* Conexiones intra-clúster */
      ctx.beginPath();
      for (a = 0; a < members.length; a++) {
        for (b = a + 1; b < members.length; b++) {
          var dx = members[a].x - members[b].x;
          var dy = members[a].y - members[b].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 90) {
            ctx.moveTo(members[a].x, members[a].y);
            ctx.lineTo(members[b].x, members[b].y);
          }
        }
      }
      ctx.strokeStyle = rgba(D.cyan, D.connAlphaDisp * 0.7);
      ctx.lineWidth   = 0.6;
      ctx.stroke();
    }

    /* Partículas */
    drawParticles();
  }

  /* ── Render: partículas individuales ──────────────────── */
  function drawParticles() {
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      /* Glow / halo */
      var gr   = p.r * D.glowMul;
      var grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, gr);
      grad.addColorStop(0, rgba(D.cyan, p.op * 0.22));
      grad.addColorStop(1, rgba(D.cyan, 0));
      ctx.beginPath();
      ctx.arc(p.x, p.y, gr, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      /* Núcleo */
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = rgba(D.cyanLight, p.op);
      ctx.fill();
    }
  }

  /* ═══════════════════════════════════════════════════════
     RESIZE
     ═══════════════════════════════════════════════════════ */
  function resize() {
    var par = canvas.parentElement;
    W   = par.clientWidth;
    H   = par.clientHeight;
    dpr = window.devicePixelRatio || 1;
    canvas.width  = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* ═══════════════════════════════════════════════════════
     EVENTOS
     ═══════════════════════════════════════════════════════ */
  function onClick(e) {
    if (STATE !== 'agglomerated') return;
    var rect = canvas.getBoundingClientRect();
    var mx = e.clientX - rect.left;
    var my = e.clientY - rect.top;
    var dx = mx - W / 2, dy = my - H / 2;
    if (Math.sqrt(dx * dx + dy * dy) < Math.min(W, H) * 0.22) {
      disperse();
    }
  }

  function onTouchEnd(e) {
    if (STATE !== 'agglomerated') return;
    var t = e.changedTouches && e.changedTouches[0];
    if (!t) return;
    var rect = canvas.getBoundingClientRect();
    var mx = t.clientX - rect.left;
    var my = t.clientY - rect.top;
    var dx = mx - W / 2, dy = my - H / 2;
    if (Math.sqrt(dx * dx + dy * dy) < Math.min(W, H) * 0.22) {
      disperse();
    }
  }

  var resizeTimer;
  function onResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var oW = W || 1, oH = H || 1;
      resize();
      var sx = W / oW, sy = H / oH;
      for (var i = 0; i < particles.length; i++) {
        particles[i].x  *= sx;  particles[i].y  *= sy;
        particles[i].hx *= sx;  particles[i].hy *= sy;
      }
      for (var c = 0; c < clusterMeta.length; c++) {
        clusterMeta[c].targetX *= sx;
        clusterMeta[c].targetY *= sy;
      }
    }, 100);
  }

  /* ═══════════════════════════════════════════════════════
     LOOP DE ANIMACIÓN
     ═══════════════════════════════════════════════════════ */
  function animate(t) {
    animId = requestAnimationFrame(animate);
    update(t);
    draw(t);
  }

  /* ═══════════════════════════════════════════════════════
     ARRANQUE
     ═══════════════════════════════════════════════════════ */
  canvas.addEventListener('click',    onClick);
  canvas.addEventListener('touchend', onTouchEnd, { passive: true });
  window.addEventListener('resize',   onResize);

  resize();
  createScene();
  animate(0);

  return {
    destroy: function () {
      cancelAnimationFrame(animId);
      canvas.removeEventListener('click',    onClick);
      canvas.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('resize',   onResize);
    },
    disperse: disperse,
  };
}

/* ═══════════════════════════════════════════════════════
   AUTO-INICIALIZACIÓN  (Reflex SPA)
   ═══════════════════════════════════════════════════════ */
(function () {
  var ID    = 'particle-hero-canvas';
  var _inst = null;

  function boot() {
    var c = document.getElementById(ID);
    if (!c || c.dataset.heroInit === '1') return;
    c.dataset.heroInit = '1';
    if (_inst && _inst.destroy) _inst.destroy();
    _inst = initParticleHero(ID);
  }

  var obs = new MutationObserver(boot);
  obs.observe(document.documentElement, { childList: true, subtree: true });
  boot();
})();
