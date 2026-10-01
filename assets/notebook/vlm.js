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

  // Rows stay in one fixed order (by score on the clean photo) so you can
  // watch probability move between labels when a name tag goes on.
  var rows = {};
  function buildRows() {
    bars.innerHTML = "";
    rows = {};
    data.photos[photo].clean.forEach(function (s) {
      var li = document.createElement("li");
      li.innerHTML = '<span class="lab"></span><span class="bar"><span></span></span><span class="pct"></span>';
      li.querySelector(".lab").textContent = s.label;
      bars.appendChild(li);
      rows[s.label] = li;
    });
  }

  function render() {
    img.src = base + photo + "-" + tag + ".jpg";
    if (!bars.dataset.photo || bars.dataset.photo !== photo) {
      buildRows();
      bars.dataset.photo = photo;
    }
    var scores = data.photos[photo][tag];
    var best = scores[0].label;
    scores.forEach(function (s) {
      var li = rows[s.label];
      if (!li) return;
      var pct = Math.round(s.p * 100);
      li.querySelector(".bar span").style.width = Math.max(pct, 1) + "%";
      li.querySelector(".pct").textContent = pct + "%";
      li.className = s.label === best ? "top" : "";
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
