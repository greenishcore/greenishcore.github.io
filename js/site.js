/* Navigation behaviour for handheld viewports.
   The menu is only collapsed when this script runs, so the links stay
   reachable if scripting is unavailable. */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) { return; }

  var mobile = window.matchMedia('(max-width: 719px)');

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
  }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  nav.addEventListener('click', function (event) {
    if (event.target.tagName === 'A' && mobile.matches) { setOpen(false); }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      setOpen(false);
      toggle.focus();
    }
  });

  function sync() {
    if (!mobile.matches) { setOpen(false); }
  }

  if (typeof mobile.addEventListener === 'function') {
    mobile.addEventListener('change', sync);
  } else if (typeof mobile.addListener === 'function') {
    mobile.addListener(sync);
  }
})();
