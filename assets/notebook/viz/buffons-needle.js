(function () {
  "use strict";
  var root = document.getElementById("buffons-needle");
  if (!root) return;

  var ORANGE = "#dd6b20";
  var ROWS = 5; // gaps between lines; canvas height = ROWS * d
  var COLS = ROWS / 0.6; // width in units of d
  var MAX_DRAWN = 4000;

  function token(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) || fallback;
  }

  var style = document.createElement("style");
  style.textContent =
    "#buffons-needle{font-family:var(--f-mono,monospace);font-size:13px;max-width:680px;margin:1.5rem auto}" +
    "#buffons-needle canvas{display:block;width:100%}" +
    "#buffons-needle .bn-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}" +
    "#buffons-needle button{font:inherit;padding:4px 10px;border:1px solid var(--grid,#ccc);background:transparent;color:var(--ink,#1d2a44);border-radius:3px;cursor:pointer}" +
    "#buffons-needle button:hover{border-color:var(--pen,#2456a6)}" +
    "#buffons-needle input[type=range]{accent-color:var(--pen,#2456a6);flex:1;min-width:120px}" +
    "#buffons-needle .bn-stats{font-variant-numeric:tabular-nums;color:var(--ink,#1d2a44)}" +
    "#buffons-needle .bn-stats b{color:var(--pen,#2456a6)}" +
    "#buffons-needle .bn-x{color:" +
    ORANGE +
    "}";
  root.appendChild(style);

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text) e.textContent = text;
    return e;
  }

  var board = el("canvas", { "aria-label": "Needles dropped on parallel lines" });
  var plot = el("canvas", { "aria-label": "Running estimate of pi" });
  var stats = el("div", { class: "bn-row bn-stats", "aria-live": "polite" });
  var row1 = el("div", { class: "bn-row" });
  var b1 = el("button", { type: "button" }, "drop 1");
  var b100 = el("button", { type: "button" }, "drop 100");
  var bAuto = el("button", { type: "button", "aria-pressed": "false" }, "auto-drop");
  var bReset = el("button", { type: "button" }, "reset");
  row1.appendChild(b1);
  row1.appendChild(b100);
  row1.appendChild(bAuto);
  row1.appendChild(bReset);
  var row2 = el("div", { class: "bn-row" });
  var lab = el("label", { for: "bn-len" }, "needle length ℓ/d = ");
  var lenOut = el("span", { class: "bn-stats" });
  var slider = el("input", { id: "bn-len", type: "range", min: "0.2", max: "1", step: "0.05", value: "0.8" });
  lab.appendChild(lenOut);
  row2.appendChild(lab);
  row2.appendChild(slider);
  root.appendChild(board);
  root.appendChild(stats);
  root.appendChild(row1);
  root.appendChild(row2);
  root.appendChild(plot);

  var L, needles, N, C, hist;

  function reset() {
    L = parseFloat(slider.value);
    needles = [];
    N = 0;
    C = 0;
    hist = [];
    lenOut.textContent = L.toFixed(2);
  }

  // One needle: center (x, y) in units of d, angle t uniform in [0, pi).
  // Lines sit at y = 0, 1, ..., ROWS, so y uniform on [0, ROWS] is uniform mod 1.
  function drop() {
    var x = Math.random() * COLS;
    var y = Math.random() * ROWS;
    var t = Math.random() * Math.PI;
    var h = (L / 2) * Math.sin(t); // vertical half-extent
    var hit = Math.floor(y - h) !== Math.floor(y + h);
    N++;
    if (hit) C++;
    needles.push([x, y, t, hit]);
    if (needles.length > MAX_DRAWN) needles.shift();
    if (C > 0) {
      hist.push([N, (2 * L * N) / C]);
      if (hist.length > 1500)
        hist = hist.filter(function (_, i) {
          return i % 2 === 0;
        });
    }
  }

  function dropMany(k) {
    for (var i = 0; i < k; i++) drop();
    draw();
  }

  function fit(cv, ratio) {
    var w = Math.min(root.clientWidth || 680, 680);
    var dpr = window.devicePixelRatio || 1;
    var h = Math.round(w * ratio);
    cv.style.height = h + "px";
    cv.width = Math.round(w * dpr);
    cv.height = Math.round(h * dpr);
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function drawBoard() {
    var f = fit(board, ROWS / COLS),
      ctx = f.ctx,
      d = f.h / ROWS;
    ctx.fillStyle = token("--paper", "#fff");
    ctx.fillRect(0, 0, f.w, f.h);
    ctx.strokeStyle = token("--ink", "#1d2a44");
    ctx.lineWidth = 1.5;
    for (var k = 0; k <= ROWS; k++) {
      var yy = Math.min(Math.max(k * d, 0.75), f.h - 0.75);
      ctx.beginPath();
      ctx.moveTo(0, yy);
      ctx.lineTo(f.w, yy);
      ctx.stroke();
    }
    var pen = token("--pen", "#2456a6");
    ctx.lineCap = "round";
    ctx.lineWidth = Math.max(1.2, d * 0.03);
    var dense = needles.length > 600;
    ctx.globalAlpha = dense ? 0.55 : 0.9;
    for (var pass = 0; pass < 2; pass++) {
      ctx.strokeStyle = pass ? ORANGE : pen;
      ctx.beginPath();
      for (var i = 0; i < needles.length; i++) {
        var n = needles[i];
        if (n[3] !== !!pass) continue;
        var dx = (L / 2) * Math.cos(n[2]) * d,
          dy = (L / 2) * Math.sin(n[2]) * d;
        ctx.moveTo(n[0] * d - dx, n[1] * d - dy);
        ctx.lineTo(n[0] * d + dx, n[1] * d + dy);
      }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function drawPlot() {
    var f = fit(plot, 0.28),
      ctx = f.ctx;
    var soft = token("--ink-soft", "#667");
    var padL = 34,
      padR = 8,
      padT = 8,
      padB = 18;
    var pw = f.w - padL - padR,
      ph = f.h - padT - padB;
    var lo = 2.6,
      hi = 3.7;
    var maxN = Math.max(10, N),
      lmax = Math.log(maxN);
    function X(n) {
      return padL + (Math.log(n) / lmax) * pw;
    }
    function Y(v) {
      return padT + (1 - (Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo)) * ph;
    }
    ctx.clearRect(0, 0, f.w, f.h);
    ctx.font = "11px " + (token("--f-mono", "monospace") || "monospace");
    ctx.fillStyle = soft;
    ctx.strokeStyle = token("--grid", "#ccd");
    ctx.lineWidth = 1;
    ctx.strokeRect(padL, padT, pw, ph);
    ctx.textAlign = "right";
    ctx.fillText(hi.toFixed(1), padL - 4, padT + 8);
    ctx.fillText(lo.toFixed(1), padL - 4, padT + ph);
    ctx.textAlign = "left";
    ctx.fillText("N = 1", padL, f.h - 4);
    ctx.textAlign = "right";
    ctx.fillText("N = " + maxN + " (log scale)", padL + pw, f.h - 4);
    ctx.strokeStyle = ORANGE;
    ctx.setLineDash([5, 4]);
    ctx.beginPath();
    ctx.moveTo(padL, Y(Math.PI));
    ctx.lineTo(padL + pw, Y(Math.PI));
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.textAlign = "left";
    ctx.fillStyle = ORANGE;
    ctx.fillText("π", padL + 4, Y(Math.PI) - 4);
    ctx.strokeStyle = token("--pen", "#2456a6");
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var i = 0; i < hist.length; i++) {
      var px = X(hist[i][0]),
        py = Y(hist[i][1]);
      if (i) ctx.lineTo(px, py);
      else ctx.moveTo(px, py);
    }
    ctx.stroke();
  }

  function drawStats() {
    var est = C > 0 ? ((2 * L * N) / C).toFixed(5) : "—";
    var err = C > 0 ? Math.abs((2 * L * N) / C - Math.PI).toFixed(5) : "—";
    stats.innerHTML =
      "<span>N = " +
      N +
      "</span><span class='bn-x'>C = " +
      C +
      "</span>" +
      "<span>π̂ = 2ℓN/(dC) = <b>" +
      est +
      "</b></span>" +
      "<span>π = 3.14159</span><span>error = " +
      err +
      "</span>";
  }

  function draw() {
    drawBoard();
    drawPlot();
    drawStats();
  }

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var auto = false,
    raf = 0;
  function setAuto(on) {
    auto = on;
    bAuto.setAttribute("aria-pressed", String(on));
    bAuto.textContent = on ? "pause auto-drop" : "auto-drop";
    if (on && !raf) raf = requestAnimationFrame(tick);
  }
  function tick() {
    raf = 0;
    if (!auto) return;
    if (!document.hidden) dropMany(N < 200 ? 2 : N < 2000 ? 10 : 40);
    raf = requestAnimationFrame(tick);
  }

  b1.addEventListener("click", function () {
    dropMany(1);
  });
  b100.addEventListener("click", function () {
    dropMany(100);
  });
  bAuto.addEventListener("click", function () {
    setAuto(!auto);
  });
  bReset.addEventListener("click", function () {
    reset();
    draw();
  });
  slider.addEventListener("input", function () {
    reset();
    dropMany(20);
  });
  window.addEventListener("resize", draw);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && auto && !raf) raf = requestAnimationFrame(tick);
  });
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", draw);
  }
  new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "class"] });

  reset();
  dropMany(20);
  if (!reduce) setAuto(true);
})();
