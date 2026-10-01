(function () {
  "use strict";
  var root = document.getElementById("galton-board");
  if (!root) return;

  var style = document.createElement("style");
  style.textContent =
    "#galton-board{font-family:var(--f-mono);font-size:13px;max-width:680px;margin:1.5rem auto;}" +
    "#galton-board canvas{display:block;width:100%;background:var(--paper);border:1px solid var(--grid);}" +
    "#galton-board .gb-row{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin-top:8px;}" +
    "#galton-board label{display:flex;align-items:center;gap:6px;}" +
    "#galton-board input[type=range]{accent-color:var(--pen);width:110px;}" +
    "#galton-board button{font:inherit;padding:3px 10px;background:var(--paper);color:var(--ink);border:1px solid var(--grid);border-radius:3px;cursor:pointer;}" +
    "#galton-board button:hover{border-color:var(--pen);color:var(--pen);}" +
    "#galton-board .gb-stats{font-variant-numeric:tabular-nums;color:var(--ink-soft);}" +
    "#galton-board .gb-stats b{color:var(--ink);font-weight:600;}" +
    "#galton-board .gb-key{display:inline-block;width:14px;height:0;border-top:3px solid;vertical-align:middle;margin-right:4px;}";
  document.head.appendChild(style);

  root.innerHTML =
    '<canvas aria-label="Galton board simulation"></canvas>' +
    '<div class="gb-row">' +
    '<label>rows <input type="range" id="gb-n" min="4" max="16" step="1" value="10"><span id="gb-nv"></span></label>' +
    '<label>bias p <input type="range" id="gb-p" min="0.05" max="0.95" step="0.05" value="0.5"><span id="gb-pv"></span></label>' +
    '<label>rate <input type="range" id="gb-r" min="1" max="60" step="1" value="20"><span id="gb-rv"></span></label>' +
    "</div>" +
    '<div class="gb-row">' +
    '<button type="button" id="gb-play"></button>' +
    '<button type="button" id="gb-add">+100 instantly</button>' +
    '<button type="button" id="gb-reset">reset</button>' +
    "</div>" +
    '<div class="gb-row gb-stats" id="gb-stats" aria-live="polite"></div>' +
    '<div class="gb-row gb-stats">' +
    '<span><span class="gb-key" style="border-color:#dd6b20"></span>binomial(n, p)</span>' +
    '<span><span class="gb-key" style="border-color:var(--ink-soft);border-top-style:dashed"></span>normal N(np, np(1&minus;p))</span>' +
    "</div>";

  var canvas = root.querySelector("canvas");
  var ctx = canvas.getContext("2d");
  var $ = function (id) {
    return document.getElementById(id);
  };
  var elN = $("gb-n"),
    elP = $("gb-p"),
    elR = $("gb-r"),
    btnPlay = $("gb-play");
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var n,
    p,
    counts,
    balls,
    total,
    sumX,
    sumX2,
    spawnAcc = 0,
    playing = !reduced,
    lastT = null;
  var W = 0,
    H = 0;
  var ROW_TIME = 0.09; // seconds per peg row

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || "#1d2a44";
  }
  function choose(a, b) {
    var r = 1;
    for (var i = 1; i <= b; i++) r = (r * (a - b + i)) / i;
    return r;
  }
  function binomPmf(k) {
    return choose(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
  }
  function normPdf(x) {
    var v = n * p * (1 - p);
    return Math.exp(-((x - n * p) * (x - n * p)) / (2 * v)) / Math.sqrt(2 * Math.PI * v);
  }
  function path() {
    var steps = [];
    for (var i = 0; i < n; i++) steps.push(Math.random() < p ? 1 : 0);
    return steps;
  }
  function land(k) {
    counts[k]++;
    total++;
    sumX += k;
    sumX2 += k * k;
  }

  function reset() {
    n = +elN.value;
    p = +elP.value;
    counts = [];
    for (var i = 0; i <= n; i++) counts.push(0);
    balls = [];
    total = 0;
    sumX = 0;
    sumX2 = 0;
    spawnAcc = 0;
    updateLabels();
    draw();
  }
  function addInstant(m) {
    for (var j = 0; j < m; j++) {
      var s = path(),
        k = 0;
      for (var i = 0; i < n; i++) k += s[i];
      land(k);
    }
    draw();
  }

  // geometry
  function geo() {
    var dx = (W * 0.92) / (n + 1);
    var top = H * 0.06,
      boardH = H * 0.5,
      histTop = top + boardH + H * 0.04;
    return { dx: dx, cx: W / 2, top: top, rowH: boardH / n, histTop: histTop, histBot: H - 4 };
  }
  function xAt(g, k, r) {
    return g.cx + (r - k / 2) * g.dx;
  }

  function draw() {
    if (!W) return;
    var ink = css("--ink"),
      pen = css("--pen"),
      soft = css("--ink-soft"),
      grid = css("--grid");
    var g = geo(),
      i,
      k;
    ctx.clearRect(0, 0, W, H);
    // pegs
    var pegR = Math.max(1.5, Math.min(3.5, g.dx * 0.09));
    ctx.fillStyle = ink;
    for (k = 0; k < n; k++)
      for (i = 0; i <= k; i++) {
        ctx.beginPath();
        ctx.arc(xAt(g, k, i), g.top + (k + 0.5) * g.rowH, pegR, 0, 2 * Math.PI);
        ctx.fill();
      }
    // bin walls + baseline
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (i = 0; i <= n + 1; i++) {
      var wx = g.cx + (i - 0.5 - n / 2) * g.dx;
      ctx.moveTo(wx, g.histTop);
      ctx.lineTo(wx, g.histBot);
    }
    ctx.stroke();
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(g.cx - (n / 2 + 0.5) * g.dx, g.histBot);
    ctx.lineTo(g.cx + (n / 2 + 0.5) * g.dx, g.histBot);
    ctx.stroke();
    // scale: fit both counts and expected curve
    var maxC = 1,
      N = Math.max(total, 1);
    for (i = 0; i <= n; i++) maxC = Math.max(maxC, counts[i], N * binomPmf(i), N * normPdf(n * p));
    var hH = (g.histBot - g.histTop) * 0.95;
    var yOf = function (c) {
      return g.histBot - (c / maxC) * hH;
    };
    // bars
    ctx.fillStyle = pen;
    ctx.globalAlpha = 0.35;
    for (i = 0; i <= n; i++) {
      var bx = xAt(g, n, i) - g.dx * 0.42;
      ctx.fillRect(bx, yOf(counts[i]), g.dx * 0.84, g.histBot - yOf(counts[i]));
    }
    ctx.globalAlpha = 1;
    if (total > 0) {
      // normal curve (dashed)
      ctx.strokeStyle = soft;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([5, 4]);
      ctx.beginPath();
      for (var s = 0; s <= 200; s++) {
        var x = -0.5 + (s / 200) * (n + 1);
        var px = xAt(g, n, x),
          py = yOf(total * normPdf(x));
        if (s) ctx.lineTo(px, py);
        else ctx.moveTo(px, py);
      }
      ctx.stroke();
      ctx.setLineDash([]);
      // binomial expected (orange ticks + dots)
      ctx.strokeStyle = "#dd6b20";
      ctx.fillStyle = "#dd6b20";
      ctx.lineWidth = 2.5;
      ctx.lineCap = "round";
      for (i = 0; i <= n; i++) {
        var ey = yOf(total * binomPmf(i)),
          ex = xAt(g, n, i);
        ctx.beginPath();
        ctx.moveTo(ex - g.dx * 0.3, ey);
        ctx.lineTo(ex + g.dx * 0.3, ey);
        ctx.stroke();
      }
      // np marker
      var mx = xAt(g, n, n * p);
      ctx.beginPath();
      ctx.moveTo(mx, g.histBot);
      ctx.lineTo(mx, g.histBot + 4);
      ctx.stroke();
    }
    // balls in flight
    ctx.fillStyle = pen;
    var br = Math.max(2, Math.min(4.5, g.dx * 0.14));
    for (var b = 0; b < balls.length; b++) {
      var ball = balls[b],
        t = ball.t / ROW_TIME,
        row = Math.floor(t),
        f = t - row,
        bxp,
        byp;
      if (row < n) {
        var r0 = ball.r[row],
          r1 = r0 + ball.s[row];
        bxp = xAt(g, row, r0) + (xAt(g, row + 1, r1) - xAt(g, row, r0)) * f;
        byp = g.top + (row + 0.5) * g.rowH - pegR - br + f * g.rowH - Math.sin(f * Math.PI) * g.rowH * 0.35;
      } else {
        bxp = xAt(g, n, ball.r[n]);
        byp = g.top + (n + 0.5) * g.rowH - pegR - br + (t - n) * g.rowH * 2;
      }
      ctx.beginPath();
      ctx.arc(bxp, byp, br, 0, 2 * Math.PI);
      ctx.fill();
    }
  }

  function spawn() {
    var s = path(),
      r = [0];
    for (var i = 0; i < n; i++) r.push(r[i] + s[i]);
    balls.push({ s: s, r: r, t: 0 });
  }

  function updateLabels() {
    $("gb-nv").textContent = elN.value;
    $("gb-pv").textContent = (+elP.value).toFixed(2);
    $("gb-rv").textContent = elR.value + "/s";
    btnPlay.textContent = playing ? "pause" : "play";
    var mean = total ? sumX / total : NaN;
    var vr = total > 1 ? (sumX2 - total * mean * mean) / (total - 1) : NaN;
    var f = function (v) {
      return isNaN(v) ? "  -  " : v.toFixed(2);
    };
    $("gb-stats").innerHTML =
      "<span>balls <b>" +
      total +
      "</b></span>" +
      "<span>sample mean <b>" +
      f(mean) +
      "</b> vs np = <b>" +
      (n * p).toFixed(2) +
      "</b></span>" +
      "<span>sample var <b>" +
      f(vr) +
      "</b> vs np(1&minus;p) = <b>" +
      (n * p * (1 - p)).toFixed(2) +
      "</b></span>";
  }

  function frame(ts) {
    var dt = lastT == null ? 0 : Math.min(0.05, (ts - lastT) / 1000);
    lastT = ts;
    if (playing && !document.hidden) {
      spawnAcc += dt * +elR.value;
      while (spawnAcc >= 1) {
        spawn();
        spawnAcc -= 1;
      }
      var endT = (n + 0.6) * ROW_TIME,
        landed = false;
      for (var b = balls.length - 1; b >= 0; b--) {
        balls[b].t += dt;
        if (balls[b].t >= endT) {
          land(balls[b].r[n]);
          balls.splice(b, 1);
          landed = true;
        }
      }
      if (landed) updateLabels();
      draw();
      requestAnimationFrame(frame);
    } else {
      lastT = null;
    }
  }
  function start() {
    if (playing) {
      lastT = null;
      requestAnimationFrame(frame);
    }
  }

  function resize() {
    var w = Math.min(root.clientWidth || 680, 680),
      dpr = window.devicePixelRatio || 1;
    W = w;
    H = Math.round(w * 0.62);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  elN.addEventListener("input", reset);
  elP.addEventListener("input", reset);
  elR.addEventListener("input", updateLabels);
  btnPlay.addEventListener("click", function () {
    playing = !playing;
    updateLabels();
    start();
  });
  $("gb-add").addEventListener("click", function () {
    addInstant(100);
    updateLabels();
  });
  $("gb-reset").addEventListener("click", reset);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) start();
  });
  window.addEventListener("resize", resize);
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", draw);
  }
  new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "class"] });

  reset();
  addInstant(200); // start with a real sample so the shape is visible at rest
  updateLabels();
  resize();
  start();
})();
