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

/* Whole-line plates (deno N3): images, code listings and embeds have
   arbitrary heights, which would push everything after them off the line
   grid. Each one is padded up to the next whole multiple of the body line
   pitch. Without scripting the page still reads, only the rhythm drifts. */
(function () {
  'use strict';

  var selector = 'figure, pre, iframe';
  var pending = false;

  function pitch() {
    return parseFloat(window.getComputedStyle(document.body).lineHeight) || 0;
  }

  function snap() {
    pending = false;
    var line = pitch();
    var main = document.getElementById('main');
    if (!line || !main) { return; }
    var plates = main.querySelectorAll(selector);
    var i, el, rect, origin, bottom;
    for (i = 0; i < plates.length; i++) { plates[i].style.minHeight = ''; }
    /* Snap each plate's bottom edge, in document order, to the grid that
       starts at the top of <main>, so sub-pixel rounding never adds up. */
    for (i = 0; i < plates.length; i++) {
      el = plates[i];
      rect = el.getBoundingClientRect();
      if (rect.height > 0) {
        origin = main.getBoundingClientRect().top;
        bottom = Math.ceil((rect.bottom - origin) / line - 0.01) * line;
        el.style.minHeight = (bottom - (rect.top - origin)) + 'px';
      }
    }
  }

  function schedule() {
    if (pending) { return; }
    pending = true;
    window.requestAnimationFrame(snap);
  }

  document.addEventListener('DOMContentLoaded', schedule);
  window.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);
  document.addEventListener('load', function (event) {
    if (event.target.tagName === 'IMG') { schedule(); }
  }, true);
  document.addEventListener('toggle', schedule, true);
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(schedule); }
})();
