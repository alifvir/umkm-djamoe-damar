// Menu mobile. Tidak ada animasi lain, sesuai dial MOTION 1.
(function () {
  var tombol = document.querySelector("[data-nav-tombol]");
  var nav = document.querySelector("[data-nav]");
  if (!tombol || !nav) return;

  function tutup() {
    nav.setAttribute("data-terbuka", "false");
    tombol.setAttribute("aria-expanded", "false");
  }

  function buka() {
    nav.setAttribute("data-terbuka", "true");
    tombol.setAttribute("aria-expanded", "true");
  }

  tombol.addEventListener("click", function () {
    if (nav.getAttribute("data-terbuka") === "true") {
      tutup();
    } else {
      buka();
    }
  });

  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) tutup();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      tutup();
      tombol.focus();
    }
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target) && !tombol.contains(e.target)) tutup();
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth >= 960) tutup();
  });
})();
