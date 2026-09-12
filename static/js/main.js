(function () {
  'use strict';

  // Mobile menu toggle
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Back to top
  var btn = document.getElementById('backToTop');
  if (btn) {
    var onScroll = function () {
      if (window.scrollY > 400) btn.classList.add('is-visible');
      else btn.classList.remove('is-visible');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Lazy-load native fallback (only if supported)
  if ('loading' in HTMLImageElement.prototype) {
    // Browser handles loading="lazy" automatically
  }

  // Form double-submit guard
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      var submit = form.querySelector('button[type=submit]');
      if (submit) {
        submit.disabled = true;
        setTimeout(function () { submit.disabled = false; }, 5000);
      }
    });
  });
})();