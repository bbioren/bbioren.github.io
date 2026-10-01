// Typographic attack on the home page photos. Scores come from a real CLIP run
// (manim/clip_attack.py) and are embedded in the page as JSON. The polaroid
// cycles through the photos until a name tag is applied.
(function () {
  var dataEl = document.getElementById("clip-data");
  if (!dataEl) return;
  var data = JSON.parse(dataEl.textContent);
  var img = document.getElementById("attack-img");
  var bars = document.getElementById("bars");
  var note = document.getElementById("vlm-note");
  var buttons = document.querySelectorAll(".attack[data-key]");
  var base = img.getAttribute("src").replace(/[^/]*$/, "");
  var photos = Object.keys(data.photos);
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var photo = photos[0];
  var tag = "clean";
  var timer = null;

  photos.forEach(function (p) {
    Object.keys(data.photos[p]).forEach(function (k) {
      new Image().src = base + p + "-" + k + ".jpg";
    });
  });

  function render() {
    img.src = base + photo + "-" + tag + ".jpg";
    bars.innerHTML = "";
    data.photos[photo][tag].slice(0, 3).forEach(function (s, i) {
      var li = document.createElement("li");
      if (i === 0) li.className = "top";
      var pct = Math.round(s.p * 100);
      li.innerHTML =
        '<span class="lab"></span><span class="bar"><span style="width:' +
        Math.max(pct, 1) +
        '%"></span></span><span class="pct">' +
        pct +
        "%</span>";
      li.querySelector(".lab").textContent = s.label;
      bars.appendChild(li);
    });
    buttons.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.key === tag));
    });
    note.hidden = tag === "clean";
  }

  function cycle() {
    clearInterval(timer);
    timer = null;
    if (reduce || tag !== "clean" || photos.length < 2) return;
    timer = setInterval(function () {
      if (document.hidden) return;
      photo = photos[(photos.indexOf(photo) + 1) % photos.length];
      render();
    }, 5000);
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      tag = b.getAttribute("aria-pressed") === "true" ? "clean" : b.dataset.key;
      render();
      cycle();
    });
  });
  img.addEventListener("click", function () {
    photo = photos[(photos.indexOf(photo) + 1) % photos.length];
    render();
    cycle();
  });
  render();
  cycle();
})();
