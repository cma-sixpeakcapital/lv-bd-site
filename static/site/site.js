/* LV Construction draft site. Source: tools/sitegen/site.js (copied to static/site/ by build_site.py).
   Four small behaviours, no dependencies except Leaflet for the map:
   1. figures marked data-count count up when they scroll into view
   2. the seven-step process graphic (data-lvp)
   3. the ROM to GMP explainer player (data-lvx)
   4. the project map and its filter tabs (data-lvmapwrap)
   Every page holds a desktop copy and a phone copy of its content, so each behaviour is set up per element. */
(function () {
  'use strict';
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var all = function (root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); };

  function onView(el, cb, opts) {
    if (!('IntersectionObserver' in window)) { cb(true, null); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { cb(e.isIntersecting, io); });
    }, opts || { threshold: 0.25 });
    io.observe(el);
  }

  /* ---------- 1. counting figures ---------- */
  function initCount(el) {
    var txt = el.textContent;
    var m = txt.match(/^(.*?)(\d[\d,]*(?:\.\d+)?)(.*)$/);
    if (!m || reduce) return;
    var pre = m[1], post = m[3], comma = m[2].indexOf(',') > -1;
    var dec = (m[2].split('.')[1] || '').length, target = parseFloat(m[2].replace(/,/g, ''));
    if (!target) return;
    function fmt(v) {
      var s = v.toFixed(dec);
      if (comma) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return pre + s + post;
    }
    el.textContent = fmt(0);
    var done = false;
    onView(el, function (visible, io) {
      if (!visible || done) return;
      done = true;
      if (io) io.disconnect();
      var dur = 1500, t0 = null;
      function frame(now) {
        if (t0 === null) t0 = now;
        var p = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
        el.textContent = p < 1 ? fmt(target * e) : txt;
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }, { threshold: 0.6 });
  }

  /* ---------- 2. seven-step process graphic ---------- */
  function initSteps(root) {
    var tiles = all(root, '.lvp-tile'), panels = all(root, '.lvp-panel'), dots = all(root, '.lvp-track i');
    var row = root.querySelector('.lvp-tiles'), count = root.querySelector('.lvp-count');
    var n = tiles.length, cur = 0, timer = null, auto = !reduce, DUR = 6500, inView = false, hover = false;
    root.style.setProperty('--dur', DUR + 'ms');

    function show(i, byUser) {
      cur = (i + n) % n;
      tiles.forEach(function (tile, k) {
        var on = k === cur;
        tile.classList.toggle('on', on);
        tile.setAttribute('aria-selected', on ? 'true' : 'false');
        tile.tabIndex = on ? 0 : -1;
        panels[k].hidden = !on;
        panels[k].classList.toggle('on', on);
        if (dots[k]) dots[k].className = k < cur ? 'done' : (on ? 'on' : '');
      });
      root.style.setProperty('--i', cur);
      if (count) count.textContent = 'Step ' + (cur + 1) + ' of ' + n;
      if (row.scrollWidth > row.clientWidth + 4) {   // phone: the tiles are a sideways strip
        var left = tiles[cur].offsetLeft - (row.clientWidth - tiles[cur].offsetWidth) / 2;
        if (row.scrollTo) row.scrollTo({ left: left, behavior: reduce ? 'auto' : 'smooth' }); else row.scrollLeft = left;
      }
      if (byUser) { auto = false; pause(); }
    }
    function pause() { if (timer) clearInterval(timer); timer = null; root.classList.remove('auto'); }
    function play() {
      if (!auto || timer || !inView || hover) return;
      root.classList.add('auto');
      timer = setInterval(function () {
        if (cur === n - 1) { auto = false; pause(); return; }   // one pass, then it rests on the last step
        show(cur + 1, false);
      }, DUR);
    }
    tiles.forEach(function (tile, k) {
      tile.addEventListener('click', function () { show(k, true); });
      tile.addEventListener('keydown', function (e) {
        var to = { ArrowRight: cur + 1, ArrowDown: cur + 1, ArrowLeft: cur - 1, ArrowUp: cur - 1, Home: 0, End: n - 1 }[e.key];
        if (to === undefined) return;
        e.preventDefault(); show(to, true); tiles[cur].focus();
      });
    });
    var prev = root.querySelector('.lvp-prev'), next = root.querySelector('.lvp-next');
    if (prev) prev.addEventListener('click', function () { show(cur - 1, true); });
    if (next) next.addEventListener('click', function () { show(cur + 1, true); });
    root.addEventListener('mouseenter', function () { hover = true; pause(); });
    root.addEventListener('mouseleave', function () { hover = false; play(); });
    show(0, false);
    onView(root, function (visible) { inView = visible; if (visible) play(); else pause(); }, { threshold: 0.35 });
  }

  /* ---------- 3. ROM to GMP explainer player ---------- */
  function initExplainer(root) {
    var STARTS = [0, 4.5, 11, 21, 31, 41, 51], END = 60;   // seconds: title, overview, four stages, closing line
    var pp = root.querySelector('.lvx-pp'), bar = root.querySelector('.lvx-prog i'), re = root.querySelector('.lvx-re'), stage = root.querySelector('.lvx-stage');
    var t = 0, playing = false, last = null, userPaused = false;

    function render() {
      var s = 0;
      for (var k = 0; k < STARTS.length; k++) if (t >= STARTS[k]) s = k;
      root.setAttribute('data-scene', s);
      bar.style.width = (Math.min(t / END, 1) * 100) + '%';
    }
    function tick(now) {
      if (!playing) return;
      if (last !== null) t += Math.min((now - last) / 1000, 0.1);
      last = now;
      if (t >= END) { t = END; render(); set(false); return; }
      render();
      requestAnimationFrame(tick);
    }
    function set(on) {
      playing = on; last = null;
      root.classList.toggle('playing', on);
      pp.setAttribute('aria-label', on ? 'Pause' : 'Play');
      if (on) requestAnimationFrame(tick);
    }
    function toggle() {
      if (!playing && t >= END) t = 0;
      userPaused = playing;
      set(!playing);
      render();
    }
    pp.addEventListener('click', toggle);
    stage.addEventListener('click', toggle);
    re.addEventListener('click', function () { t = 0; userPaused = false; render(); set(true); });
    if (reduce) { t = END; render(); return; }   // show the closing frame; Replay still plays it on request
    render();
    onView(root, function (visible) {
      if (visible && !playing && !userPaused && t < END) set(true);
      else if (!visible && playing) set(false);
    }, { threshold: 0.5 });
  }

  /* ---------- 4. project map ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function initMap(wrap) {
    var el = wrap.querySelector('[data-lvmap]'), tabs = all(wrap, '.lvtab'), note = wrap.querySelector('.lvmap-n');
    var pins = JSON.parse(el.getAttribute('data-pins')), filter = 'all', map = null, markers = [];
    var match = function (p) { return filter === 'all' || p.s === filter || p.p === filter; };

    function apply() {
      var shown = pins.filter(match).length;
      if (note) note.textContent = shown + (shown === 1 ? ' building shown' : ' buildings shown');
      if (!map) return;
      var pts = [];
      markers.forEach(function (mk) {
        if (match(mk.lvPin)) { mk.addTo(map); pts.push(mk.getLatLng()); } else { map.removeLayer(mk); }
      });
      if (pts.length) map.fitBounds(window.L.latLngBounds(pts), { padding: [48, 48], maxZoom: 14 });
    }
    function make() {
      if (map || !window.L) return;
      var L = window.L;
      map = L.map(el, { scrollWheelZoom: false, dragging: !L.Browser.mobile });
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 17, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      pins.forEach(function (p) {
        var mk = L.marker([p.la, p.lo], {
          title: p.n, alt: p.n,
          icon: L.divIcon({ className: '', html: '<span class="lvpin ' + p.s + '"></span>', iconSize: [18, 18], iconAnchor: [9, 9], popupAnchor: [0, -8] })
        });
        mk.bindPopup('<b>' + esc(p.n) + '</b>' + esc(p.h) + '<br>' + esc(p.l) + (p.u ? '<a class="lvmap-more" href="' + esc(p.u) + '">See the building</a>' : ''));
        mk.lvPin = p;
        markers.push(mk);
      });
      apply();
    }
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        filter = tab.getAttribute('data-filter');
        tabs.forEach(function (x) { x.setAttribute('aria-pressed', x === tab ? 'true' : 'false'); });
        apply();
      });
    });
    apply();
    onView(el, function (visible) {
      if (!visible) return;
      make();
      if (map) map.invalidateSize();
    }, { threshold: 0, rootMargin: '300px 0px' });
  }

  /* ---------- 5. contact form ---------- */
  function initForm(form) {
    var status = form.querySelector('.lvform-status'), button = form.querySelector('button[type="submit"]'), opened = Date.now();
    var FALLBACK = 'This did not send. Please email Tom at <a href="mailto:tpt@sixpeakcapital.com">tpt@sixpeakcapital.com</a> or call <a href="tel:+17242720182">(724) 272-0182</a>.';
    function say(html, bad) { status.innerHTML = html; status.style.color = bad ? '#B42318' : '#0B1833'; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = {}, i, el;
      for (i = 0; i < form.elements.length; i++) { el = form.elements[i]; if (el.name) data[el.name] = el.value.trim(); }
      if (!data.name) { say('Please add your name.', true); form.elements.name.focus(); return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email || '')) { say('Please add an email address Tom can reply to.', true); form.elements.email.focus(); return; }
      data.elapsed = Date.now() - opened;
      button.disabled = true; button.style.opacity = '0.6';
      say('Sending...');
      fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.ok }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error('not sent');
          all(form, 'div').forEach(function (d) { if (d.parentNode === form) d.style.display = 'none'; });
          say('<strong style="font-family: \'DM Sans\', Inter, sans-serif; font-size: 22px">Thank you. Your note is with Tom.</strong><br>He will reply to ' + esc(data.email) + '.');
        })
        .catch(function () { button.disabled = false; button.style.opacity = '1'; say(FALLBACK, true); });
    });
  }

  function start() {
    all(document, '[data-lvform]').forEach(initForm);
    all(document, '[data-count]').forEach(initCount);
    all(document, '[data-lvp]').forEach(initSteps);
    all(document, '[data-lvx]').forEach(initExplainer);
    all(document, '[data-lvmapwrap]').forEach(initMap);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
