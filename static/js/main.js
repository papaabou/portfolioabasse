(function () {
  "use strict";

  // Scroll-reveal animation (discrete, respects reduced-motion)
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealTargets = document.querySelectorAll(".reveal");

  if (revealTargets.length) {
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      revealTargets.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );
      revealTargets.forEach(function (el) { observer.observe(el); });
    }
  }

  // Back-to-top button
  var backToTop = document.querySelector(".back-to-top");
  if (backToTop) {
    var toggleBackToTop = function () {
      backToTop.classList.toggle("is-visible", window.scrollY > 480);
    };
    window.addEventListener("scroll", toggleBackToTop, { passive: true });
    toggleBackToTop();
    backToTop.addEventListener("click", function (event) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  }

  // Navbar background solidifies after scrolling past the hero
  var navbar = document.querySelector(".navbar-abasse");
  if (navbar) {
    var toggleNavbarState = function () {
      navbar.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    window.addEventListener("scroll", toggleNavbarState, { passive: true });
    toggleNavbarState();
  }

  // Gallery filter (client-side, no external library)
  var filterButtons = document.querySelectorAll("[data-gallery-filter]");
  var galleryItems = document.querySelectorAll("[data-gallery-item]");
  if (filterButtons.length && galleryItems.length) {
    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var target = button.getAttribute("data-gallery-filter");
        filterButtons.forEach(function (btn) { btn.classList.remove("active"); });
        button.classList.add("active");
        galleryItems.forEach(function (item) {
          var matches = target === "all" || item.getAttribute("data-category") === target;
          item.style.display = matches ? "" : "none";
        });
      });
    });
  }

  // Gallery lightbox (Bootstrap modal content swap)
  var lightboxModalEl = document.getElementById("galleryLightbox");
  if (lightboxModalEl && window.bootstrap) {
    var lightboxImg = lightboxModalEl.querySelector("img");
    var lightboxCaption = lightboxModalEl.querySelector(".lightbox-caption");
    document.querySelectorAll("[data-lightbox-src]").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        lightboxImg.src = trigger.getAttribute("data-lightbox-src");
        lightboxImg.alt = trigger.getAttribute("data-lightbox-caption") || "";
        if (lightboxCaption) {
          lightboxCaption.textContent = trigger.getAttribute("data-lightbox-caption") || "";
        }
      });
    });
  }
})();
