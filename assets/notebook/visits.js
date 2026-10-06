// Footer visit count from GoatCounter's public counter
// (needs "Allow adding visitor counts on your website" turned on in GoatCounter settings).
// If the counter is off or unreachable, nothing is shown.
(function () {
  var el = document.getElementById("visits");
  if (!el || !window.fetch) return;
  fetch("https://bbioren.goatcounter.com/counter/TOTAL.json")
    .then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(function (d) {
      if (!d || !d.count) return;
      el.textContent = "this notebook has been opened " + d.count + " times";
      el.hidden = false;
    })
    .catch(function () {});
})();
