// Teaching shelf: clicking a spine pulls it up and opens that notebook below.
(function () {
  var shelf = document.getElementById("shelf");
  if (!shelf) return;
  var spines = shelf.querySelectorAll(".spine");
  function open(i) {
    spines.forEach(function (s) {
      s.setAttribute("aria-expanded", String(s.dataset.i === i));
    });
    document.querySelectorAll("#opened > [id^='leaf-']").forEach(function (el) {
      el.hidden = el.id !== "leaf-" + i;
    });
  }
  spines.forEach(function (s) {
    s.addEventListener("click", function () {
      open(s.getAttribute("aria-expanded") === "true" ? "0" : s.dataset.i);
    });
  });
})();
