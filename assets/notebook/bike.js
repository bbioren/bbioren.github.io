// Footer bike: while you hover the dashed line, the bike accelerates toward
// the cursor, brakes as it gets close, and the wheels turn with the distance
// travelled. Moving off the line sends it back to the start.
(function () {
  var track = document.getElementById("track");
  var bike = document.getElementById("bike");
  if (!track || !bike) return;
  var wheels = bike.querySelectorAll(".wheel");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var BIKE_W = 64;
  var WHEEL_R = 10;
  var x = 0; // left edge of the bike, px
  var v = 0; // velocity, px/s
  var target = 0;
  var spin = 0; // wheel angle, degrees
  var last = null;
  var raf = null;

  function maxX() {
    return Math.max(0, track.clientWidth - BIKE_W);
  }

  function draw() {
    bike.style.transform = "translateX(" + x.toFixed(1) + "px)";
    wheels.forEach(function (w) {
      w.setAttribute("transform", "rotate(" + spin.toFixed(1) + " " + w.dataset.cx + " " + w.dataset.cy + ")");
    });
  }

  function step(t) {
    if (last === null) last = t;
    var dt = Math.min(0.05, (t - last) / 1000);
    last = t;
    // damped spring toward the target: accelerates, coasts, brakes
    var k = 18;
    var c = 2 * Math.sqrt(k) * 0.9;
    var a = k * (target - x) - c * v;
    var maxA = 2200;
    a = Math.max(-maxA, Math.min(maxA, a));
    v += a * dt;
    v = Math.max(-900, Math.min(900, v));
    var dx = v * dt;
    x = Math.max(0, Math.min(maxX(), x + dx));
    spin += (dx / (2 * Math.PI * WHEEL_R)) * 360;
    draw();
    if (Math.abs(target - x) < 0.3 && Math.abs(v) < 2) {
      x = target;
      v = 0;
      draw();
      raf = null;
      last = null;
      return;
    }
    raf = requestAnimationFrame(step);
  }

  function go(to) {
    target = Math.max(0, Math.min(maxX(), to));
    if (reduce) {
      x = target;
      draw();
      return;
    }
    if (raf === null) raf = requestAnimationFrame(step);
  }

  track.addEventListener("pointermove", function (e) {
    var r = track.getBoundingClientRect();
    go(e.clientX - r.left - BIKE_W / 2);
  });
  track.addEventListener("pointerleave", function () {
    go(0);
  });
})();
