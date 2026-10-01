(function () {
  "use strict";
  var root = document.getElementById("fourier-epicycles");
  if (!root) return;

  var N = 256,
    Q = 2048,
    MAXC = 100,
    M = 2048,
    TAU = Math.PI * 2,
    ORANGE = "#dd6b20";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var style = document.createElement("style");
  style.textContent =
    "#fourier-epicycles{font-family:var(--f-mono);font-size:13px;max-width:680px;margin:1.5rem auto;}" +
    "#fourier-epicycles .fe-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0;}" +
    "#fourier-epicycles canvas{display:block;width:100%;border:1px solid var(--grid);border-radius:4px;background:var(--paper);}" +
    "#fourier-epicycles button{font:inherit;padding:4px 10px;border:1px solid var(--grid);border-radius:4px;background:var(--paper);color:var(--ink);cursor:pointer;}" +
    "#fourier-epicycles button:hover,#fourier-epicycles button[aria-pressed=true]{border-color:var(--pen);color:var(--pen);}" +
    "#fourier-epicycles input[type=range]{accent-color:var(--pen);flex:1;min-width:120px;}" +
    "#fourier-epicycles output,#fourier-epicycles .fe-read{font-variant-numeric:tabular-nums;}" +
    "#fourier-epicycles .fe-read{color:var(--ink-soft);min-height:2.6em;}";
  document.head.appendChild(style);

  root.innerHTML =
    '<div class="fe-row" role="group" aria-label="shape">' +
    '<button type="button" data-shape="square">square wave</button>' +
    '<button type="button" data-shape="heart">heart</button>' +
    '<button type="button" data-shape="draw">draw your own</button>' +
    '<button type="button" class="fe-play"></button></div>' +
    '<canvas aria-label="rotating circles tracing a Fourier approximation of a closed curve"></canvas>' +
    '<div class="fe-row"><label for="fe-n">circles</label>' +
    '<input id="fe-n" type="range" min="1" max="' +
    MAXC +
    '" value="8"><output for="fe-n">8</output></div>' +
    '<div class="fe-read" aria-live="polite"></div>';

  var canvas = root.querySelector("canvas"),
    ctx = canvas.getContext("2d");
  var slider = root.querySelector("#fe-n"),
    out = root.querySelector("output");
  var read = root.querySelector(".fe-read"),
    playBtn = root.querySelector(".fe-play");
  var shapeBtns = root.querySelectorAll("[data-shape]");

  var W = 0,
    H = 0,
    S = 1,
    dpr = 1;
  var shape = "square",
    pts = null,
    c0 = null,
    terms = [],
    total = 0;
  var curve = [],
    peak = 0,
    nc = 8,
    t = 0;
  var raw = null,
    drawing = false;
  var running = !reduce,
    raf = 0,
    last = 0;

  function css(name, fb) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fb;
  }

  // ---- shapes, sampled at N points around one period ----
  function squarePts() {
    // x is a triangle wave, y a square wave: top edge left to right, jump down, bottom edge back, jump up.
    // Sampled finely (Q points) so the DFT matches the true Fourier coefficients for the first 100 terms.
    var p = [];
    for (var n = 0; n < Q; n++) {
      var u = n / Q,
        s = Math.sin(TAU * u);
      p.push([1 - 4 * Math.abs(u - 0.5), Math.abs(s) < 1e-9 ? 0 : s > 0 ? 1 : -1]);
    }
    return p;
  }
  function heartPts() {
    var p = [];
    for (var n = 0; n < N; n++) {
      var a = (TAU * n) / N,
        s = Math.sin(a);
      p.push([(16 * s * s * s) / 16, (13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a) + 2.5) / 16]);
    }
    return p;
  }
  function resample(r) {
    // evenly spaced points by arc length along the closed polygon
    var p = r.concat([r[0]]),
      L = [0],
      i,
      j = 0,
      o = [];
    for (i = 1; i < p.length; i++) L.push(L[i - 1] + Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]));
    var len = L[L.length - 1];
    for (var n = 0; n < N; n++) {
      var s = (len * n) / N;
      while (j < L.length - 2 && L[j + 1] < s) j++;
      var seg = L[j + 1] - L[j],
        u = seg > 0 ? (s - L[j]) / seg : 0;
      o.push([p[j][0] + u * (p[j + 1][0] - p[j][0]), p[j][1] + u * (p[j + 1][1] - p[j][1])]);
    }
    return o;
  }

  // ---- DFT: c_k = (1/N) sum_n z_n e^{-2 pi i k n / N}, k in [-N/2, N/2) ----
  function setPoints(p) {
    pts = p;
    var cs = [],
      N = p.length;
    for (var k = 0; k < N; k++) {
      var re = 0,
        im = 0;
      for (var n = 0; n < N; n++) {
        var a = (-TAU * k * n) / N,
          ca = Math.cos(a),
          sa = Math.sin(a);
        re += p[n][0] * ca - p[n][1] * sa;
        im += p[n][0] * sa + p[n][1] * ca;
      }
      re /= N;
      im /= N;
      cs.push({ f: k < N / 2 ? k : k - N, re: re, im: im, r: Math.hypot(re, im) });
    }
    c0 = cs[0];
    terms = cs.slice(1).sort(function (a, b) {
      return b.r - a.r;
    });
    total = 0;
    for (var i = 0; i < terms.length; i++) total += terms[i].r * terms[i].r;
    build();
  }
  function evalAt(u, count, arms) {
    var x = c0.re,
      y = c0.im;
    if (arms) arms.push([x, y]);
    for (var i = 0; i < count; i++) {
      var c = terms[i],
        a = TAU * c.f * u,
        ca = Math.cos(a),
        sa = Math.sin(a);
      x += c.re * ca - c.im * sa;
      y += c.re * sa + c.im * ca;
      if (arms) arms.push([x, y]);
    }
    return [x, y];
  }
  function build() {
    curve = [];
    peak = 0;
    if (!pts) return update();
    for (var j = 0; j <= M; j++) {
      var q = evalAt(j / M, nc);
      curve.push(q);
      peak = Math.max(peak, Math.abs(q[1]));
    }
    update();
  }
  function update() {
    out.textContent = nc;
    if (!pts) {
      read.textContent = "draw one closed loop on the canvas";
      return draw();
    }
    var e = 0;
    for (var i = 0; i < nc; i++) e += terms[i].r * terms[i].r;
    var txt = "energy captured " + (total ? (100 * e) / total : 100).toFixed(2) + "%";
    if (shape === "square")
      txt += "  ·  peak height " + peak.toFixed(3) + " (edge at 1), overshoot " + ((100 * (peak - 1)) / 2).toFixed(1) + "% of the jump";
    var top = terms
      .slice(0, Math.min(nc, 6))
      .map(function (c) {
        return c.f;
      })
      .join(", ");
    read.textContent = txt + "\nbiggest frequencies: " + top + (nc > 6 ? ", ..." : "");
    read.style.whiteSpace = "pre-line";
    draw();
  }

  // ---- drawing ----
  function X(x) {
    return W / 2 + x * S;
  }
  function Y(y) {
    return H / 2 - y * S;
  }
  function poly(p, close) {
    ctx.beginPath();
    for (var i = 0; i < p.length; i++) ctx[i ? "lineTo" : "moveTo"](X(p[i][0]), Y(p[i][1]));
    if (close) ctx.closePath();
    ctx.stroke();
  }
  function draw() {
    var ink = css("--ink", "#1d2a44"),
      soft = css("--ink-soft", "#555"),
      pen = css("--pen", "#2456a6"),
      grid = css("--grid", "#ccc");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = ctx.lineJoin = "round";
    if (drawing && raw) {
      ctx.strokeStyle = ORANGE;
      ctx.lineWidth = 2.5;
      return poly(raw, false);
    }
    if (!pts) return;
    ctx.strokeStyle = grid;
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    poly(pts, true);
    ctx.setLineDash([]);
    ctx.strokeStyle = pen;
    ctx.lineWidth = 2.5;
    poly(curve, false);
    var arms = [];
    evalAt(t, nc, arms);
    ctx.lineWidth = 1;
    for (var i = 1; i < arms.length; i++) {
      var r = terms[i - 1].r * S;
      if (r < 0.6) continue;
      ctx.strokeStyle = soft;
      ctx.globalAlpha = 0.45;
      ctx.beginPath();
      ctx.arc(X(arms[i - 1][0]), Y(arms[i - 1][1]), r, 0, TAU);
      ctx.stroke();
      ctx.globalAlpha = 1;
    }
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1.5;
    poly(arms, false);
    var tip = arms[arms.length - 1];
    ctx.fillStyle = ORANGE;
    ctx.beginPath();
    ctx.arc(X(tip[0]), Y(tip[1]), 4.5, 0, TAU);
    ctx.fill();
  }
  function resize() {
    W = Math.min(root.clientWidth || 680, 680);
    H = Math.round(W * 0.6);
    dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.height = H + "px";
    S = Math.min(W, H) / 2 / 1.32;
    draw();
  }

  // ---- animation ----
  function tick(ts) {
    if (!running || document.hidden) {
      raf = 0;
      return;
    }
    if (last) t = (t + Math.min(ts - last, 50) / 9000) % 1;
    last = ts;
    draw();
    raf = requestAnimationFrame(tick);
  }
  function start() {
    if (running && !raf && !document.hidden) {
      last = 0;
      raf = requestAnimationFrame(tick);
    }
  }
  function setPlay(on) {
    running = on;
    playBtn.textContent = on ? "pause" : "play";
    if (on) start();
  }

  // ---- controls ----
  function choose(s) {
    shape = s;
    for (var i = 0; i < shapeBtns.length; i++) shapeBtns[i].setAttribute("aria-pressed", shapeBtns[i].dataset.shape === s);
    canvas.style.touchAction = s === "draw" ? "none" : "auto";
    canvas.style.cursor = s === "draw" ? "crosshair" : "default";
    t = 0;
    if (s === "square") setPoints(squarePts());
    else if (s === "heart") setPoints(heartPts());
    else {
      pts = null;
      build();
    }
  }
  for (var i = 0; i < shapeBtns.length; i++)
    shapeBtns[i].addEventListener("click", function () {
      choose(this.dataset.shape);
    });
  slider.addEventListener("input", function () {
    nc = +slider.value;
    build();
  });
  playBtn.addEventListener("click", function () {
    setPlay(!running);
  });

  function world(e) {
    var b = canvas.getBoundingClientRect();
    return [(e.clientX - b.left - W / 2) / S, (H / 2 - (e.clientY - b.top)) / S];
  }
  canvas.addEventListener("pointerdown", function (e) {
    if (shape !== "draw") return;
    drawing = true;
    raw = [world(e)];
    canvas.setPointerCapture(e.pointerId);
    e.preventDefault();
    draw();
  });
  canvas.addEventListener("pointermove", function (e) {
    if (!drawing) return;
    var p = world(e),
      q = raw[raw.length - 1];
    if (Math.hypot(p[0] - q[0], p[1] - q[1]) * S > 2) {
      raw.push(p);
      draw();
    }
  });
  function finish() {
    if (!drawing) return;
    drawing = false;
    if (raw.length > 8) {
      t = 0;
      setPoints(resample(raw));
    } else draw();
  }
  canvas.addEventListener("pointerup", finish);
  canvas.addEventListener("pointercancel", finish);

  document.addEventListener("visibilitychange", start);
  window.addEventListener("resize", function () {
    resize();
  });
  if (window.MutationObserver)
    new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "class"] });

  resize();
  setPlay(running);
  choose("square");
})();
