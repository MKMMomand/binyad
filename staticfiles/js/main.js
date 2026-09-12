(function () {
  'use strict';

  var toggle = document.querySelector('.menu-toggle');
  var mobileNav = document.getElementById('mobileNav');

  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      if (open) {
        mobileNav.setAttribute('hidden', '');
      } else {
        mobileNav.removeAttribute('hidden');
      }
    });

    // Close on navigation
    mobileNav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mobileNav.setAttribute('hidden', '');
        toggle.setAttribute('aria-expanded', 'false');
      });
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
    onScroll();
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Guard double-submit
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


/* Products filter tabs (progressive enhancement) */
(function () {
  var tabs = document.querySelectorAll('.filter-tab');
  var grid = document.getElementById('productsGrid');
  var emptyMsg = document.getElementById('filterEmpty');

  if (!tabs.length || !grid) return;

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var filter = tab.getAttribute('data-filter');

      tabs.forEach(function (t) {
        t.classList.toggle('is-active', t === tab);
        t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
      });

      var visible = 0;
      grid.querySelectorAll('.product-card').forEach(function (card) {
        var status = card.getAttribute('data-status');
        var show = filter === 'all' || status === filter;
        card.style.display = show ? '' : 'none';
        if (show) visible++;
      });

      if (emptyMsg) {
        emptyMsg.hidden = visible > 0;
      }
    });
  });
})();