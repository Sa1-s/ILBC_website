/* I Love Being Catholic v2 — navigation without reloads, journey tracker, interactions. No dependencies. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- safe storage (works even when localStorage is blocked) ---------- */
  var mem = {};
  function load() { try { return JSON.parse(localStorage.getItem('ilbc.journey') || '{}'); } catch (e) { return mem; } }
  function save(s) { mem = s; try { localStorage.setItem('ilbc.journey', JSON.stringify(s)); } catch (e) {} }
  var state = load();
  state.pages = state.pages || {}; state.units = state.units || []; state.setting = !!state.setting; state.checks = state.checks || {}; state.done = !!state.done;

  /* ---------- journey quests ---------- */
  var QUESTS = [
    ['hello', 'Say hello on the home page', function () { return state.pages.index; }, 'index.html'],
    ['invite', 'Read the invitation', function () { return state.pages.invitation; }, 'invitation.html'],
    ['units', 'Explore all five units', function () { return state.units.length >= 5; }, 'units.html'],
    ['setting', 'Pick a setting for your parish', function () { return state.setting; }, 'settings.html'],
    ['resources', 'See the resources', function () { return state.pages.resources; }, 'resources.html'],
    ['pathway', 'Follow the pathway', function () { return state.pages.beginning; }, 'beginning.html'],
    ['start', 'Plan your next step', function () { return state.pages['get-started']; }, 'get-started.html']
  ];
  var jbtn, jpanel, ring, toastEl;
  function buildJourney() {
    jbtn = document.createElement('button'); jbtn.className = 'jbtn'; jbtn.setAttribute('aria-expanded', 'false'); jbtn.setAttribute('aria-controls', 'jpanel');
    jbtn.innerHTML = '<span class="ring" data-t="0"></span><span class="t">Your journey</span>';
    jpanel = document.createElement('div'); jpanel.className = 'jpanel'; jpanel.id = 'jpanel'; jpanel.setAttribute('role', 'dialog'); jpanel.setAttribute('aria-label', 'Your journey');
    toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status');
    document.body.appendChild(jbtn); document.body.appendChild(jpanel); document.body.appendChild(toastEl);
    ring = $('.ring', jbtn);
    jbtn.addEventListener('click', function () { var o = !jpanel.classList.contains('open'); jpanel.classList.toggle('open', o); jbtn.setAttribute('aria-expanded', o); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { jpanel.classList.remove('open'); jbtn.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('click', function (e) { if (!jpanel.contains(e.target) && !jbtn.contains(e.target)) { jpanel.classList.remove('open'); jbtn.setAttribute('aria-expanded', 'false'); } });
    jpanel.addEventListener('click', function (e) {
      if (e.target.closest('a')) { jpanel.classList.remove('open'); jbtn.setAttribute('aria-expanded', 'false'); }
      if (e.target.closest('.reset')) { state = { pages: {}, units: [], setting: false, checks: {}, done: false }; save(state); markPage(); renderJourney(); refreshPageUI(); }
    });
  }
  function toast(msg) {
    /* Announce for screen readers, and show the note inside the Journey pill so it never covers page text. */
    toastEl.textContent = msg; var t = $('.t', jbtn);
    if (!toast.orig) toast.orig = t.textContent;
    t.textContent = msg.length > 34 ? 'Journey complete' : msg; jbtn.classList.add('flash');
    clearTimeout(toast.t); toast.t = setTimeout(function () { t.textContent = toast.orig; jbtn.classList.remove('flash'); }, 3000);
  }
  function confetti() {
    if (reduce) return;
    var cols = ['#a20e2b', '#d4a73f', '#efd0c6', '#f5e4cb', '#fcf5e6', '#241a1b'];
    for (var i = 0; i < 46; i++) {
      var c = document.createElement('i'); c.className = 'confetti';
      c.style.left = Math.random() * 100 + 'vw'; c.style.background = cols[i % cols.length];
      c.style.borderRadius = i % 3 === 0 ? '50%' : '3px';
      c.style.setProperty('--x', (Math.random() * 240 - 120) + 'px'); c.style.setProperty('--r', (Math.random() * 720 - 360) + 'deg');
      c.style.setProperty('--t', (1.6 + Math.random() * 1.6) + 's');
      document.body.appendChild(c); setTimeout(function (n) { n.remove(); }.bind(null, c), 3600);
    }
  }
  function renderJourney() {
    var done = QUESTS.filter(function (q) { return q[2](); }).length, pct = Math.round(done / QUESTS.length * 100);
    ring.style.setProperty('--p', pct); ring.setAttribute('data-t', done + '/' + QUESTS.length);
    jpanel.innerHTML = '<h4>Your journey</h4><p>' + (done === QUESTS.length ? 'You have seen it all. Your parish is ready to begin.' : 'Explore the site, one stop at a time. Progress stays on this device only.') + '</p><ol>' +
      QUESTS.map(function (q, i) { var d = q[2](); return '<li class="' + (d ? 'done' : '') + '"><a href="' + q[3] + '"><i>' + (d ? '✓' : i + 1) + '</i><span>' + q[1] + '</span></a></li>'; }).join('') +
      '</ol>' + (done === QUESTS.length ? '<a class="btn small" href="get-started.html#contact">Contact Liguori</a> ' : '') + '<button class="reset" type="button">Start over</button>';
    if (done === QUESTS.length && !state.done) { state.done = true; save(state); confetti(); toast('Journey complete — you are ready to bring this to your parish.'); }
    if (done < QUESTS.length && state.done) { state.done = false; save(state); }
  }
  function progress(msg) { save(state); renderJourney(); if (msg) toast(msg); }
  function pageKey() { var f = location.pathname.split('/').pop().replace('.html', ''); return f || 'index'; }
  function markPage() { var k = pageKey(); if (!state.pages[k]) { state.pages[k] = 1; save(state); } }

  /* ---------- persistent: header, scroll progress, burger ---------- */
  var header = $('.header'), bar = $('.progress'), toTop = $('.to-top'), burger = $('.burger'), nav = $('.nav');
  var lastY = 0, ticking = false;
  function onScroll() {
    var y = window.scrollY, max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (toTop) toTop.classList.toggle('show', y > 700); if (toNext) toNext.classList.toggle('show', y > 300); if (toPrev) toPrev.classList.toggle('show', y > 300);
    if (header && !(nav && nav.classList.contains('open'))) header.classList.toggle('hide', y > lastY && y > 260);
    lastY = y;
    if (!reduce) $$('[data-parallax]').forEach(function (el) { var r = el.parentElement.getBoundingClientRect(); if (r.bottom > 0 && r.top < innerHeight) el.style.setProperty('--py', (y * 0.16).toFixed(1) + 'px'); });
    updatePath(); ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  var ORDER = ['index.html', 'invitation.html', 'settings.html', 'units.html', 'resources.html', 'beginning.html', 'get-started.html'];
  var NAMES = ['Home', 'Welcome', 'Formats', 'Lessons', 'Library', 'Pathway', 'Get started'];
  var toNext = $('.to-next'), toPrev = $('.to-prev');
  function setNext() {
    if (!toNext) return; var f = location.pathname.split('/').pop() || 'index.html', i = ORDER.indexOf(f);
    if (i < 0) i = 0;
    var last = i === ORDER.length - 1, k = last ? 0 : i + 1;
    toNext.setAttribute('href', ORDER[k]); toNext.setAttribute('aria-label', (last ? 'Back to ' : 'Next page: ') + NAMES[k]);
    $('.nx-t', toNext).textContent = (last ? 'Back to ' : 'Next: ') + NAMES[k];
  }
  function setPrev() {
    if (!toPrev) return; var f = location.pathname.split('/').pop() || 'index.html', i = ORDER.indexOf(f);
    if (i < 0) i = 0;
    var first = i === 0, k = first ? ORDER.length - 1 : i - 1;
    toPrev.setAttribute('href', ORDER[k]); toPrev.setAttribute('aria-label', 'Previous page: ' + NAMES[k]);
    $('.pv-t', toPrev).textContent = NAMES[k];
  }
  setNext(); setPrev(); window.addEventListener('popstate', function () { setNext(); setPrev(); });
  if (toTop) toTop.addEventListener('click', function () { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  function setNav(o) { if (!nav) return; nav.classList.toggle('open', o); document.body.classList.toggle('nav-on', o); burger.setAttribute('aria-expanded', o); document.body.style.overflow = o ? 'hidden' : ''; header.classList.remove('hide'); }
  var scrim = document.createElement('div'); scrim.className = 'nav-scrim'; document.body.appendChild(scrim);
  scrim.addEventListener('click', function () { setNav(false); });
  if (nav) nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
  if (burger) { burger.addEventListener('click', function () { setNav(!nav.classList.contains('open')); }); document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); }); }

  /* ---------- per-page ---------- */
  var observers = [];
  function updatePath() { var p = $('.path'), f = $('.path-line i'); if (!p || !f) return; var r = p.getBoundingClientRect(); f.style.setProperty('--h', Math.max(0, Math.min(1, (innerHeight * 0.6 - r.top) / r.height)) * 100 + '%'); }
  function countUp(el) { var end = +el.getAttribute('data-count'), t0 = null; if (reduce) { el.textContent = end; return; } (function s(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / 1400, 1); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(s); })(performance.now()); }

  function refreshPageUI() {
    var meter = $('[data-units-meter]'); if (meter) {
      var n = state.units.length; $('.bar-meter', meter).style.setProperty('--w', n / 5 * 100 + '%'); $('.mtxt', meter).textContent = n + ' of 5 units explored';
      $$('.badge').forEach(function (b) { b.classList.toggle('on', state.units.indexOf(+b.getAttribute('data-u')) > -1); });
      $$('.step-btn').forEach(function (b) { b.classList.toggle('done', state.units.indexOf(+b.getAttribute('data-u')) > -1); });
    }
    $$('.checks input').forEach(function (i) { i.checked = !!state.checks[i.getAttribute('data-k')]; });
    var cm = $('[data-checks-meter]'); if (cm) { var all = $$('.checks input'), c = all.filter(function (i) { return i.checked; }).length; $('.bar-meter', cm).style.setProperty('--w', c / all.length * 100 + '%'); $('.mtxt', cm).textContent = c + ' of ' + all.length + ' ready'; }
  }

  function initPage() {
    observers.forEach(function (o) { o.disconnect(); }); observers = [];
    markPage(); renderJourney();
    var rev = $$('[data-reveal],.cross-box');
    if ('IntersectionObserver' in window && !reduce) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
      rev.forEach(function (e) { io.observe(e); }); observers.push(io);
    } else rev.forEach(function (e) { e.classList.add('in'); });
    var cs = $$('[data-count]');
    if ('IntersectionObserver' in window) { var co = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } }); }, { threshold: .6 }); cs.forEach(function (c) { co.observe(c); }); observers.push(co); } else cs.forEach(function (c) { c.textContent = c.getAttribute('data-count'); });
    $$('.cross-box path').forEach(function (p) { try { p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 2); } catch (e) {} });

    /* units stepper */
    var sb = $$('.step-btn');
    function pick(u, fromUser) {
      sb.forEach(function (b) { b.setAttribute('aria-selected', +b.getAttribute('data-u') === u); });
      $$('.unit-panel').forEach(function (p) { var on = +p.getAttribute('data-u') === u; p.hidden = !on; p.classList.toggle('show', on && fromUser !== 'init'); });
      if (state.units.indexOf(u) < 0) { state.units.push(u); progress(fromUser === 'init' ? null : (state.units.length === 5 ? 'All five units explored!' : 'Unit ' + u + ' explored')); }
      refreshPageUI();
    }
    sb.forEach(function (b) { b.addEventListener('click', function () { pick(+b.getAttribute('data-u'), true); }); });
    if (sb.length) { var h = /^#u(\d)$/.exec(location.hash); pick(h ? +h[1] : 1, 'init'); }
    $$('[data-next-unit]').forEach(function (b) { b.addEventListener('click', function () { pick(+b.getAttribute('data-next-unit'), true); $('.units-board').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }); });

    /* format tabs + quiz */
    var ft = $$('.fmt-tab');
    function pickFmt(f, user) {
      ft.forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-f') === f); });
      $$('.fmt-panel').forEach(function (p) { var on = p.getAttribute('data-f') === f; p.hidden = !on; p.classList.toggle('show', on); });
      if (user && !state.setting) { state.setting = true; progress('Setting picked'); }
    }
    ft.forEach(function (t) { t.addEventListener('click', function () { pickFmt(t.getAttribute('data-f'), true); }); });
    if (ft.length) pickFmt('sundays', false);
    var quiz = $('.quiz');
    if (quiz) initQuiz(quiz, pickFmt);

    /* resource toggles */
    $$('.tog').forEach(function (b) { b.addEventListener('click', function () { var m = b.nextElementSibling, o = !m.classList.contains('open'); m.classList.toggle('open', o); b.setAttribute('aria-expanded', o); b.innerHTML = o ? 'Show less' : 'Learn more'; }); });

    /* checklists */
    $$('.checks input').forEach(function (i) { i.addEventListener('change', function () { state.checks[i.getAttribute('data-k')] = i.checked; save(state); refreshPageUI(); }); });
    refreshPageUI();

    /* countdown */
    $$('[data-countdown]').forEach(function (el) { var d = Math.ceil((new Date(el.getAttribute('data-countdown') + 'T00:00:00') - new Date()) / 864e5); el.textContent = d > 0 ? d : 0; });

    /* contact form -> email app */
    var f = $('form.compose');
    if (f) f.addEventListener('submit', function (e) { e.preventDefault(); var d = new FormData(f); location.href = 'mailto:' + f.getAttribute('data-to') + '?subject=' + encodeURIComponent('I Love Being Catholic — parish enquiry') + '&body=' + encodeURIComponent('Name: ' + d.get('name') + '\nParish: ' + d.get('parish') + '\nEmail: ' + d.get('email') + '\nFormat of interest: ' + d.get('format') + '\n\n' + d.get('message')); });
    onScroll();
  }

  function initQuiz(root, pickFmt) {
    var Q = [
      ['When can your people gather most easily?', [['After Sunday Mass', 'sundays'], ['Over one weekend', 'retreat'], ['Weekday evenings', 'mission']]],
      ['What sounds most like your parish?', [['Learning that grows out of Mass and the homily', 'sundays'], ['A weekend away from routine, close to home', 'retreat'], ['An evening of hymns, music and prayer', 'mission']]],
      ['Who would lead it?', [['Our priest, with small-group hosts', 'sundays'], ['A parish formation team', 'retreat'], ['A visiting missionary', 'mission']]]
    ];
    var NAMES = { sundays: 'A parish preaching event over five Sundays', retreat: 'A parish retreat weekend', mission: 'A parish mission over five nights' };
    var i = 0, score = {};
    var box = $('.quiz-body', root);
    function render() {
      if (i >= Q.length) {
        var best = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; })[0];
        box.innerHTML = '<div class="result"><span class="sticker gold" style="--rot:-2deg">Your match</span><h3 style="margin-top:14px">' + NAMES[best] + '</h3><p>A starting point for the conversation with your parish team. Every format covers the same five units.</p><div style="display:flex;gap:12px;flex-wrap:wrap"><button class="btn small" type="button" data-show="' + best + '">See this format</button><button class="btn light small" type="button" data-again>Try again</button></div></div>';
        state.setting = true; progress('Setting picked'); return;
      }
      box.innerHTML = '<div class="q-progress">' + Q.map(function (_, k) { return '<i class="' + (k <= i ? 'on' : '') + '"></i>'; }).join('') + '</div><div class="q-step">Question ' + (i + 1) + ' of ' + Q.length + '</div><h3>' + Q[i][0] + '</h3><div class="opts">' + Q[i][1].map(function (o) { return '<button class="opt" type="button" data-v="' + o[1] + '">' + o[0] + '</button>'; }).join('') + '</div>';
    }
    box.addEventListener('click', function (e) {
      var o = e.target.closest('.opt'), s = e.target.closest('[data-show]'), a = e.target.closest('[data-again]');
      if (o) { score[o.getAttribute('data-v')] = (score[o.getAttribute('data-v')] || 0) + 1; i++; render(); }
      if (s) { pickFmt(s.getAttribute('data-show'), true); $('.fmt-tabs').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); }
      if (a) { i = 0; score = {}; render(); }
    });
    render();
  }

  /* ---------- navigation without reloads ---------- */
  var cache = {}, busy = false;
  function key(u) { return u.origin + u.pathname + u.search; }
  function fetchPage(u) { var k = key(u); if (!cache[k]) { cache[k] = fetch(k).then(function (r) { if (!r.ok) throw 0; return r.text(); }); cache[k].catch(function () { delete cache[k]; }); } return cache[k]; }
  function internal(a) { if (!a || !a.href || a.target === '_blank' || a.hasAttribute('download')) return false; var u = new URL(a.href, location.href); return u.origin === location.origin && location.protocol !== 'file:' && /(\.html?$|\/$)/.test(u.pathname); }
  function setActive(u) { var f = u.pathname.split('/').pop() || 'index.html'; $$('.nav a').forEach(function (a) { var g = new URL(a.href, location.href).pathname.split('/').pop() || 'index.html'; if (g === f) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); }); }
  function swap(u, push) {
    if (busy) return; busy = true; setNav(false); jpanel.classList.remove('open');
    var main = $('#main'); if (!reduce) main.classList.add('is-leaving');
    Promise.all([fetchPage(u), new Promise(function (r) { setTimeout(r, reduce ? 0 : 240); })]).then(function (r) {
      var doc = new DOMParser().parseFromString(r[0], 'text/html'), nm = doc.getElementById('main'); if (!nm) throw 0;
      document.title = doc.title; var md = doc.querySelector('meta[name=description]'), cd = $('meta[name=description]'); if (md && cd) cd.setAttribute('content', md.getAttribute('content'));
      main.innerHTML = nm.innerHTML; if (push) history.pushState({}, '', u.href); setActive(u); setNext(); setPrev(); scrollTo(0, 0); header.classList.remove('hide');
      main.classList.remove('is-leaving'); if (!reduce) { main.classList.remove('is-entering'); void main.offsetWidth; main.classList.add('is-entering'); }
      initPage(); if (u.hash && !/^#u\d$/.test(u.hash)) setTimeout(function () { var t = $(u.hash); if (t) t.scrollIntoView(); }, 80);
      main.focus({ preventScroll: true }); busy = false;
    }).catch(function () { busy = false; location.href = u.href; });
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a'); if (!internal(a)) return;
    var u = new URL(a.href, location.href), same = u.pathname === location.pathname;
    e.preventDefault();
    if (same) { setNav(false); if (u.hash) { var t = $(u.hash); if (t) t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); history.pushState({}, '', u.href); } else scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); setNav(false); return; }
    swap(u, true);
  });
  function pre(e) { var a = e.target.closest && e.target.closest('a'); if (internal(a)) { try { fetchPage(new URL(a.href, location.href)); } catch (x) {} } }
  document.addEventListener('mouseover', pre); document.addEventListener('touchstart', pre, { passive: true });
  addEventListener('popstate', function () { swap(new URL(location.href), false); });
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  buildJourney(); var m0 = $('#main'); if (m0) m0.setAttribute('tabindex', '-1'); initPage();

  // cookie notice: only essential storage is used; the choice is remembered
  (function () {
    var box = document.getElementById('cookie'); if (!box) return;
    var KEY = 'ilbc-cookie';
    function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    function show() { box.hidden = false; requestAnimationFrame(function () { box.classList.add('on'); }); }
    function hide() { box.classList.remove('on'); setTimeout(function () { box.hidden = true; }, 350); }
    if (!get()) setTimeout(show, 900);
    box.addEventListener('click', function (e) { var b = e.target.closest('[data-ck]'); if (!b) return; set(b.getAttribute('data-ck')); hide(); });
    document.addEventListener('click', function (e) { if (e.target.closest('.cookie-manage')) show(); });
  })();
  /* tap the ticker to pause or resume it */
  document.addEventListener('click', function (e) { var m = e.target.closest && e.target.closest('.marquee'); if (m) m.classList.toggle('paused'); });
})();
