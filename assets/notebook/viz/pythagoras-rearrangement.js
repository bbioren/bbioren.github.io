(function () {
  "use strict";
  var root = document.getElementById("pythagoras-rearrangement");
  if (!root) return;

  var S = 10; // side of the big square is a + b = 10
  var ORANGE = "#dd6b20";

  root.innerHTML =
    "<style>" +
    "#pythagoras-rearrangement{font-family:var(--f-mono);font-size:13px;margin:1rem 0}" +
    "#pythagoras-rearrangement canvas{display:block;margin:0 auto;max-width:100%}" +
    "#pythagoras-rearrangement .ctl{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;justify-content:center;margin-top:10px}" +
    "#pythagoras-rearrangement label{display:flex;align-items:center;gap:6px}" +
    "#pythagoras-rearrangement input[type=range]{accent-color:var(--pen);width:150px}" +
    "#pythagoras-rearrangement button{font:inherit;padding:3px 12px;border:1px solid var(--grid);background:var(--paper);color:var(--ink);border-radius:4px;cursor:pointer}" +
    "#pythagoras-rearrangement button:hover{border-color:var(--pen);color:var(--pen)}" +
    "#pythagoras-rearrangement .out{text-align:center;margin-top:8px;font-variant-numeric:tabular-nums;color:var(--ink)}" +
    "</style>" +
    "<canvas aria-label='Big square of side a plus b with four right triangles that slide between two arrangements'></canvas>" +
    "<div class='ctl'>" +
    "<button type='button' class='play'>play</button>" +
    "<label>arrangement <input type='range' class='t' min='0' max='1' step='0.001' value='0'></label>" +
    "<label>a <input type='range' class='a' min='1.5' max='8.5' step='0.1' value='6'></label>" +
    "</div>" +
    "<div class='out'></div>";

  var canvas = root.querySelector("canvas");
  var ctx = canvas.getContext("2d");
  var playBtn = root.querySelector(".play");
  var tIn = root.querySelector(".t");
  var aIn = root.querySelector(".a");
  var out = root.querySelector(".out");

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var playing = !reduced;
  var dir = 1;
  var hold = 0;
  var t = 0;
  var last = null;
  var size = 300;

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  // Each triangle is the canonical right triangle (right angle at its anchor,
  // leg a along local x, leg b along local y), rotated by `rot` and moved to (x, y).
  function poses(a, b) {
    var s = a + b;
    var Q = Math.PI / 2;
    return [
      // arrangement 1 (tilted c^2 hole)       arrangement 2 (a^2 and b^2 holes)
      { p: { x: 0, y: 0, r: 0 }, q: { x: 0, y: a, r: 0 } },
      { p: { x: s, y: 0, r: Q }, q: { x: s, y: 0, r: Q } },
      { p: { x: s, y: s, r: 2 * Q }, q: { x: a, y: s, r: 2 * Q } },
      { p: { x: 0, y: s, r: 3 * Q }, q: { x: a, y: a, r: 3 * Q } },
    ];
  }

  // Order in which triangles move so they never overlap at rest: 4th, 3rd, 1st.
  var phase = [2, -1, 1, 0];
  function local(k) {
    if (phase[k] < 0) return t;
    var u = t * 3 - phase[k];
    u = Math.max(0, Math.min(1, u));
    return u * u * (3 - 2 * u);
  }

  function lerp(p, q, u) {
    return { x: p.x + (q.x - p.x) * u, y: p.y + (q.y - p.y) * u, r: p.r + (q.r - p.r) * u };
  }

  function triPts(pose, a, b) {
    var c = Math.cos(pose.r);
    var s = Math.sin(pose.r);
    return [
      [0, 0],
      [a, 0],
      [0, b],
    ].map(function (v) {
      return [pose.x + v[0] * c - v[1] * s, pose.y + v[0] * s + v[1] * c];
    });
  }

  function resize() {
    var w = Math.min(root.clientWidth || 300, 560);
    size = w;
    var dpr = window.devicePixelRatio || 1;
    canvas.style.width = w + "px";
    canvas.style.height = w + "px";
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(w * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function draw() {
    var a = parseFloat(aIn.value);
    var b = S - a;
    var c2 = a * a + b * b;
    var ink = css("--ink") || "#1d2a44";
    var pen = css("--pen") || "#2456a6";
    var paper = css("--paper") || "#fff";
    var mono = css("--f-mono") || "monospace";
    var pad = size * 0.06;
    var k = (size - 2 * pad) / S;
    function X(x) {
      return pad + x * k;
    }
    function Y(y) {
      return size - pad - y * k;
    }

    ctx.clearRect(0, 0, size, size);
    // Whatever the triangles leave uncovered shows as orange.
    ctx.fillStyle = paper;
    ctx.fillRect(X(0), Y(S), S * k, S * k);
    ctx.globalAlpha = 0.28;
    ctx.fillStyle = ORANGE;
    ctx.fillRect(X(0), Y(S), S * k, S * k);
    ctx.globalAlpha = 1;

    var P = poses(a, b);
    var lw = Math.max(1.5, size / 260);
    ctx.lineJoin = "round";
    for (var i = 0; i < 4; i++) {
      var pts = triPts(lerp(P[i].p, P[i].q, local(i)), a, b);
      ctx.beginPath();
      ctx.moveTo(X(pts[0][0]), Y(pts[0][1]));
      ctx.lineTo(X(pts[1][0]), Y(pts[1][1]));
      ctx.lineTo(X(pts[2][0]), Y(pts[2][1]));
      ctx.closePath();
      ctx.fillStyle = paper;
      ctx.fill();
      ctx.globalAlpha = 0.3;
      ctx.fillStyle = pen;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.strokeStyle = pen;
      ctx.lineWidth = lw;
      ctx.stroke();
    }
    ctx.strokeStyle = ink;
    ctx.lineWidth = lw * 1.3;
    ctx.strokeRect(X(0), Y(S), S * k, S * k);

    // Side labels a and b along the bottom edge (arrangement 1 split).
    var fs = Math.max(11, Math.round(size / 30));
    ctx.font = fs + "px " + mono;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = ink;
    ctx.fillText("a", X(a / 2), Y(0) + pad * 0.5);
    ctx.fillText("b", X(a + b / 2), Y(0) + pad * 0.5);
    // The left edge splits b|a in arrangement 1 and a|b in arrangement 2.
    ctx.globalAlpha = 1 - t;
    ctx.fillText("b", X(0) - pad * 0.5, Y(b / 2));
    ctx.fillText("a", X(0) - pad * 0.5, Y(b + a / 2));
    ctx.globalAlpha = t;
    ctx.fillText("a", X(0) - pad * 0.5, Y(a / 2));
    ctx.fillText("b", X(0) - pad * 0.5, Y(a + b / 2));
    ctx.globalAlpha = 1;

    // Area labels fade in at the matching end.
    ctx.font = "bold " + Math.round(fs * 1.1) + "px " + mono;
    ctx.fillStyle = ORANGE;
    ctx.globalAlpha = Math.max(0, 1 - 3 * t);
    ctx.fillText("c² = " + c2.toFixed(2), X(S / 2), Y(S / 2));
    ctx.globalAlpha = Math.max(0, 3 * t - 2);
    var sa = a * k < fs * 6 ? "a²" : "a² = " + (a * a).toFixed(2);
    var sb = b * k < fs * 6 ? "b²" : "b² = " + (b * b).toFixed(2);
    ctx.fillText(sa, X(a / 2), Y(a / 2));
    ctx.fillText(sb, X(a + b / 2), Y(a + b / 2));
    ctx.globalAlpha = 1;

    out.innerHTML =
      "a = " +
      a.toFixed(1) +
      ", b = " +
      b.toFixed(1) +
      ", c = " +
      Math.sqrt(c2).toFixed(3) +
      "<br>a² + b² = " +
      (a * a).toFixed(2) +
      " + " +
      (b * b).toFixed(2) +
      " = " +
      c2.toFixed(2) +
      " = c²" +
      "<br>uncovered = (a+b)² − 4·(ab/2) = " +
      (S * S).toFixed(0) +
      " − " +
      (2 * a * b).toFixed(2) +
      " = " +
      c2.toFixed(2);
  }

  function step(now) {
    if (last === null) last = now;
    var dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (playing && !document.hidden) {
      if (hold > 0) {
        hold -= dt;
      } else {
        t += (dir * dt) / 3.5;
        if (t >= 1 || t <= 0) {
          t = Math.max(0, Math.min(1, t));
          dir = -dir;
          hold = 1.2;
        }
        tIn.value = t;
        draw();
      }
    }
    requestAnimationFrame(step);
  }

  function setPlaying(p) {
    playing = p;
    playBtn.textContent = p ? "pause" : "play";
  }

  playBtn.addEventListener("click", function () {
    if (reduced) {
      // Step instantly to the other arrangement.
      t = t < 0.5 ? 1 : 0;
      tIn.value = t;
      draw();
      return;
    }
    setPlaying(!playing);
  });
  tIn.addEventListener("input", function () {
    setPlaying(false);
    t = parseFloat(tIn.value);
    draw();
  });
  aIn.addEventListener("input", draw);
  window.addEventListener("resize", resize);
  document.addEventListener("visibilitychange", function () {
    last = null;
  });
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", draw);
  }

  if (window.MutationObserver) {
    new MutationObserver(draw).observe(document.documentElement, { attributes: true });
  }
  setPlaying(playing);
  if (reduced) playBtn.textContent = "flip";
  resize();
  requestAnimationFrame(step);
})();
