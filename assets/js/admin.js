/* I Love Being Catholic: site image editor.
   Visitors: reads images.json and swaps any replaced images in.
   Admin: the lock in the footer opens a password prompt. After sign-in, click any image
   to replace it, then Publish. Publishing commits the new image and images.json to the
   GitHub repository with the admin's own GitHub token, and GitHub Pages redeploys.
   The password only hides the editor. The GitHub token is what allows changes. */
(function () {
  'use strict';
  var REPO = 'Sa1-s/ILBC_website', BRANCH = 'main', MAP_PATH = 'images.json';
  var PASS_HASH = 'dfff47b4a2d0e6c24928c8779dd2cf4f28c312fa360e407db7a740bdb59dfa61';
  var K_SESSION = 'ilbc-admin', K_TOKEN = 'ilbc-gh-token';

  var map = {};            /* published slot -> image path */
  var pending = {};        /* slot -> {data, ext, preview} or {remove:true} */
  var editing = false, fails = 0, lockUntil = 0;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function ss(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); if (v === null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, v); } catch (e) { return null; } }
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; } }
  function page() { var p = location.pathname.split('/').pop(); return p && /\.html$/.test(p) ? p : 'index.html'; }

  /* ---------- sha-256 (works on http and https) ---------- */
  function sha256(str) {
    function r(n, x) { return (x >>> n) | (x << (32 - n)); }
    var K = [], H = [], i, j, primes = 0, c = 2;
    function isP(n) { for (var d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; }
    while (primes < 64) { if (isP(c)) { if (primes < 8) H[primes] = (Math.pow(c, 1 / 2) * 4294967296) | 0; K[primes] = (Math.pow(c, 1 / 3) * 4294967296) | 0; primes++; } c++; }
    var bytes = unescape(encodeURIComponent(str)), l = bytes.length, words = [];
    for (i = 0; i < l; i++) words[i >> 2] |= bytes.charCodeAt(i) << (24 - (i % 4) * 8);
    words[l >> 2] |= 0x80 << (24 - (l % 4) * 8); words[((l + 8) >> 6) * 16 + 15] = l * 8;
    for (j = 0; j < words.length; j += 16) {
      var W = [], a = H[0], b = H[1], cc = H[2], d = H[3], e = H[4], f = H[5], g = H[6], h = H[7];
      for (i = 0; i < 64; i++) {
        if (i < 16) W[i] = words[j + i] | 0;
        else { var s0 = r(7, W[i - 15]) ^ r(18, W[i - 15]) ^ (W[i - 15] >>> 3), s1 = r(17, W[i - 2]) ^ r(19, W[i - 2]) ^ (W[i - 2] >>> 10); W[i] = (W[i - 16] + s0 + W[i - 7] + s1) | 0; }
        var t1 = (h + (r(6, e) ^ r(11, e) ^ r(25, e)) + ((e & f) ^ (~e & g)) + K[i] + W[i]) | 0;
        var t2 = ((r(2, a) ^ r(13, a) ^ r(22, a)) + ((a & b) ^ (a & cc) ^ (b & cc))) | 0;
        h = g; g = f; f = e; e = (d + t1) | 0; d = cc; cc = b; b = a; a = (t1 + t2) | 0;
      }
      H[0] = (H[0] + a) | 0; H[1] = (H[1] + b) | 0; H[2] = (H[2] + cc) | 0; H[3] = (H[3] + d) | 0;
      H[4] = (H[4] + e) | 0; H[5] = (H[5] + f) | 0; H[6] = (H[6] + g) | 0; H[7] = (H[7] + h) | 0;
    }
    return H.map(function (x) { return ('00000000' + (x >>> 0).toString(16)).slice(-8); }).join('');
  }

  /* ---------- slots: every content image and banner on the page ---------- */
  function slots() {
    var main = $('#main'); if (!main) return [];
    var out = [], seen = {}, pg = page();
    $$('img', main).forEach(function (img) {
      if (!img.dataset.orig) img.dataset.orig = img.getAttribute('src');
      var o = img.dataset.orig, n = seen[o] = (seen[o] || 0) + 1;
      img.dataset.slot = pg + '|' + o + '|' + n; out.push({ el: img, slot: img.dataset.slot, kind: 'img' });
    });
    $$('.page-hero .bg', main).forEach(function (bg, i) {
      if (!bg.dataset.orig) { var m = /url\(["']?([^"')]+)/.exec(bg.style.backgroundImage || ''); bg.dataset.orig = m ? m[1] : ''; }
      bg.dataset.slot = pg + '|bg|' + bg.dataset.orig + '|' + (i + 1); out.push({ el: bg, slot: bg.dataset.slot, kind: 'bg' });
    });
    return out;
  }
  function setSrc(s, url) {
    if (s.kind === 'img') { s.el.removeAttribute('srcset'); if (s.el.getAttribute('src') !== url) s.el.setAttribute('src', url); }
    else s.el.style.backgroundImage = 'url("' + url + '")';
  }
  function apply() {
    slots().forEach(function (s) {
      var p = pending[s.slot];
      if (p && p.remove) setSrc(s, s.el.dataset.orig);
      else if (p) setSrc(s, p.preview);
      else if (map[s.slot]) setSrc(s, map[s.slot]);
    });
    if (editing) decorate();
  }
  function loadMap() {
    return fetch(MAP_PATH + '?t=' + Date.now(), { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : { slots: {} }; })
      .then(function (j) { map = (j && j.slots) || {}; apply(); })
      .catch(function () { apply(); });
  }

  /* ---------- UI ---------- */
  var css = '.ilbc-ed-modal{position:fixed;inset:0;z-index:1000;background:rgba(30,3,12,.55);display:grid;place-items:center;padding:16px}' +
    '.ilbc-ed-card{background:#fffaf2;color:#241a1b;border-radius:18px;padding:22px 22px 18px;width:min(420px,100%);box-shadow:0 20px 50px rgba(0,0,0,.3);font:400 .95rem/1.5 Montserrat,system-ui,sans-serif}' +
    '.ilbc-ed-card h3{font:700 1.35rem/1.2 "Crimson Pro",Georgia,serif;margin:0 0 6px;color:#a20e2b}' +
    '.ilbc-ed-card p{margin:0 0 12px;font-size:.88rem;color:#5b4a4c}' +
    '.ilbc-ed-card input[type=password],.ilbc-ed-card input[type=text]{width:100%;box-sizing:border-box;font:16px Montserrat,system-ui,sans-serif;padding:10px 12px;border:2px solid #e3c3bb;border-radius:10px;margin:0 0 10px;background:#fff}' +
    '.ilbc-ed-card label{display:flex;gap:8px;align-items:center;font-size:.82rem;margin:0 0 12px}' +
    '.ilbc-ed-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}' +
    '.ilbc-ed-btn{font:600 .85rem Montserrat,system-ui,sans-serif;border-radius:99px;padding:8px 16px;border:2px solid #a20e2b;background:#a20e2b;color:#fff;cursor:pointer}' +
    '.ilbc-ed-btn.l{background:#fff;color:#a20e2b}.ilbc-ed-btn:disabled{opacity:.5;cursor:default}' +
    '.ilbc-ed-err{color:#a20e2b;font-weight:600;font-size:.82rem;min-height:1.2em;margin:0 0 8px}' +
    '.ilbc-ed-prev{width:100%;max-height:200px;object-fit:contain;border-radius:10px;background:#f3e7df;margin:0 0 12px}' +
    '.ilbc-ed-bar{position:fixed;left:50%;transform:translateX(-50%);top:calc(var(--hh,90px) + 6px);z-index:999;display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;background:#241a1b;color:#fff;border-radius:99px;padding:7px 8px 7px 16px;box-shadow:0 10px 30px rgba(0,0,0,.3);font:600 .8rem Montserrat,system-ui,sans-serif;max-width:calc(100vw - 24px)}' +
    '.ilbc-ed-bar .ilbc-ed-btn{padding:5px 12px;font-size:.76rem}.ilbc-ed-bar .ilbc-ed-btn.l{background:transparent;color:#fff;border-color:rgba(255,255,255,.4)}' +
    'body.ilbc-editing #main img[data-slot]{outline:3px dashed #d4a73f;outline-offset:-3px;cursor:pointer}' +
    'body.ilbc-editing #main img[data-slot]:hover{outline-style:solid;filter:brightness(.92)}' +
    '.ilbc-ed-hero{position:absolute;right:16px;bottom:56px;z-index:5;font:600 .8rem Montserrat,system-ui,sans-serif;background:#241a1b;color:#fff;border:2px solid #d4a73f;border-radius:99px;padding:7px 14px;cursor:pointer}' +
    '.ilbc-ed-tag{position:absolute;z-index:6;pointer-events:none;font:700 .68rem Montserrat,system-ui,sans-serif;background:#d4a73f;color:#241a1b;border-radius:99px;padding:2px 8px}';
  function style() { if ($('#ilbc-ed-css')) return; var s = document.createElement('style'); s.id = 'ilbc-ed-css'; s.textContent = css; document.head.appendChild(s); }

  function modal(html) {
    style(); close();
    var m = document.createElement('div'); m.className = 'ilbc-ed-modal'; m.id = 'ilbc-ed-modal';
    m.innerHTML = '<div class="ilbc-ed-card" role="dialog" aria-modal="true">' + html + '</div>';
    m.addEventListener('click', function (e) { if (e.target === m) close(); });
    document.body.appendChild(m);
    var f = $('input,button', m); if (f) f.focus();
    return m;
  }
  function close() { var m = $('#ilbc-ed-modal'); if (m) m.remove(); }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  function login() {
    var m = modal('<h3>Site editor</h3><p>Enter the editor password to change images on this site.</p>' +
      '<form><input type="password" autocomplete="current-password" aria-label="Password" placeholder="Password">' +
      '<div class="ilbc-ed-err" aria-live="polite"></div>' +
      '<div class="ilbc-ed-row"><button type="button" class="ilbc-ed-btn l" data-x>Cancel</button><button class="ilbc-ed-btn">Sign in</button></div></form>');
    $('[data-x]', m).onclick = close;
    $('form', m).onsubmit = function (e) {
      e.preventDefault(); var err = $('.ilbc-ed-err', m);
      if (Date.now() < lockUntil) { err.textContent = 'Too many tries. Wait a moment.'; return; }
      if (sha256($('input', m).value) === PASS_HASH) { fails = 0; ss(K_SESSION, '1'); close(); startEdit(); }
      else { fails++; if (fails >= 5) { lockUntil = Date.now() + 30000; fails = 0; } err.textContent = 'Incorrect password.'; $('input', m).select(); }
    };
  }

  function bar() {
    var b = $('#ilbc-ed-bar');
    if (!b) {
      style(); b = document.createElement('div'); b.id = 'ilbc-ed-bar'; b.className = 'ilbc-ed-bar'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', 'Image editor');
      document.body.appendChild(b);
      b.addEventListener('click', function (e) {
        var t = e.target.closest('[data-a]'); if (!t) return; var a = t.dataset.a;
        if (a === 'pub') publish(); else if (a === 'discard') { pending = {}; apply(); bar(); }
        else if (a === 'gh') tokenDialog(); else if (a === 'out') stopEdit();
      });
    }
    var n = Object.keys(pending).length;
    b.innerHTML = '<span>Click an image to replace it</span>' +
      '<button class="ilbc-ed-btn" data-a="pub"' + (n ? '' : ' disabled') + '>Publish' + (n ? ' (' + n + ')' : '') + '</button>' +
      (n ? '<button class="ilbc-ed-btn l" data-a="discard">Discard</button>' : '') +
      '<button class="ilbc-ed-btn l" data-a="gh">GitHub key</button><button class="ilbc-ed-btn l" data-a="out">Sign out</button>';
  }
  function decorate() {
    $$('.ilbc-ed-hero').forEach(function (x) { x.remove(); });
    slots().forEach(function (s) {
      if (s.kind !== 'bg') return;
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'ilbc-ed-hero'; btn.textContent = 'Replace banner image';
      btn.onclick = function (e) { e.preventDefault(); e.stopPropagation(); pick(s); };
      s.el.parentNode.appendChild(btn);
    });
  }
  function onClick(e) {
    if (!editing) return;
    var img = e.target.closest && e.target.closest('#main img[data-slot]'); if (!img) return;
    e.preventDefault(); e.stopPropagation();
    var s = slots().filter(function (x) { return x.el === img; })[0]; if (s) pick(s);
  }
  function startEdit() { editing = true; document.body.classList.add('ilbc-editing'); bar(); apply(); }
  function stopEdit() {
    if (Object.keys(pending).length && !confirmDiscard()) return;
    editing = false; pending = {}; ss(K_SESSION, null); document.body.classList.remove('ilbc-editing');
    var b = $('#ilbc-ed-bar'); if (b) b.remove(); $$('.ilbc-ed-hero').forEach(function (x) { x.remove(); }); apply();
  }
  function confirmDiscard() { return window.confirm('Discard unpublished image changes?'); }

  function pick(s) {
    var cur = s.kind === 'img' ? s.el.currentSrc || s.el.src : (/url\(["']?([^"')]+)/.exec(s.el.style.backgroundImage) || [])[1];
    var changed = map[s.slot] || pending[s.slot];
    var m = modal('<h3>Replace image</h3><img class="ilbc-ed-prev" alt="Current image" src="' + cur + '">' +
      '<p>Choose a JPG, PNG or WebP. Large photos are resized to fit the web.</p>' +
      '<input type="file" accept="image/jpeg,image/png,image/webp" hidden>' +
      '<div class="ilbc-ed-err" aria-live="polite"></div>' +
      '<div class="ilbc-ed-row">' + (changed ? '<button type="button" class="ilbc-ed-btn l" data-r>Restore original</button>' : '') +
      '<button type="button" class="ilbc-ed-btn l" data-x>Cancel</button><button type="button" class="ilbc-ed-btn" data-u>Upload new image</button></div>');
    var input = $('input[type=file]', m);
    $('[data-x]', m).onclick = close;
    $('[data-u]', m).onclick = function () { input.click(); };
    if (changed) $('[data-r]', m).onclick = function () { if (map[s.slot]) pending[s.slot] = { remove: true }; else delete pending[s.slot]; close(); apply(); bar(); };
    input.onchange = function () {
      var f = input.files[0], err = $('.ilbc-ed-err', m); if (!f) return;
      if (!/^image\/(jpeg|png|webp)$/.test(f.type)) { err.textContent = 'Please choose a JPG, PNG or WebP image.'; return; }
      if (f.size > 20 * 1024 * 1024) { err.textContent = 'That file is over 20 MB. Please choose a smaller one.'; return; }
      err.textContent = 'Preparing image…';
      shrink(f).then(function (r) { pending[s.slot] = r; close(); apply(); bar(); })
        .catch(function () { err.textContent = 'That image could not be read.'; });
    };
  }
  function shrink(file) {
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), im = new Image();
      im.onload = function () {
        var max = 1800, w = im.naturalWidth, h = im.naturalHeight, k = Math.min(1, max / Math.max(w, h));
        var c = document.createElement('canvas'); c.width = Math.round(w * k); c.height = Math.round(h * k);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
        var png = file.type === 'image/png', d = c.toDataURL(png ? 'image/png' : 'image/jpeg', 0.86);
        res({ preview: d, data: d.split(',')[1], ext: png ? 'png' : 'jpg' });
      };
      im.onerror = function () { URL.revokeObjectURL(url); rej(); };
      im.src = url;
    });
  }

  /* ---------- publish through the GitHub API ---------- */
  function tokenDialog(after) {
    var m = modal('<h3>GitHub key</h3><p>Publishing saves images to the <b>' + REPO + '</b> repository. Paste a GitHub fine-grained token with <b>Contents: Read and write</b> access to that repository. It is kept only in this browser.</p>' +
      '<form><input type="text" autocomplete="off" spellcheck="false" aria-label="GitHub token" placeholder="github_pat_…" value="' + (ls(K_TOKEN) ? '••••••••' : '') + '">' +
      '<div class="ilbc-ed-err" aria-live="polite"></div>' +
      '<div class="ilbc-ed-row">' + (ls(K_TOKEN) ? '<button type="button" class="ilbc-ed-btn l" data-f>Forget key</button>' : '') +
      '<button type="button" class="ilbc-ed-btn l" data-x>Cancel</button><button class="ilbc-ed-btn">Save</button></div></form>');
    $('[data-x]', m).onclick = close;
    if ($('[data-f]', m)) $('[data-f]', m).onclick = function () { ls(K_TOKEN, null); close(); };
    $('form', m).onsubmit = function (e) {
      e.preventDefault(); var v = $('input', m).value.trim();
      if (v && v.indexOf('•') < 0) ls(K_TOKEN, v);
      if (!ls(K_TOKEN)) { $('.ilbc-ed-err', m).textContent = 'Paste a token first.'; return; }
      close(); if (after) after();
    };
  }
  function gh(method, path, body) {
    return fetch('https://api.github.com/repos/' + REPO + '/contents/' + path + (method === 'GET' ? '?ref=' + BRANCH + '&t=' + Date.now() : ''), {
      method: method, cache: 'no-store',
      headers: { 'Authorization': 'Bearer ' + ls(K_TOKEN), 'Accept': 'application/vnd.github+json' },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      if (r.status === 404 && method === 'GET') return null;
      if (!r.ok) return r.text().then(function (t) { var e = new Error(t); e.status = r.status; throw e; });
      return r.json();
    });
  }
  function b64(str) { return btoa(unescape(encodeURIComponent(str))); }
  function unb64(s) { return decodeURIComponent(escape(atob(s.replace(/\n/g, '')))); }

  function publish() {
    if (!ls(K_TOKEN)) return tokenDialog(publish);
    var keys = Object.keys(pending); if (!keys.length) return;
    var b = $('#ilbc-ed-bar'); b.innerHTML = '<span>Publishing ' + keys.length + ' change' + (keys.length > 1 ? 's' : '') + '…</span>';
    var stamp = Date.now(), uploads = {}, chain = Promise.resolve();
    keys.forEach(function (k, i) {
      var p = pending[k]; if (p.remove) return;
      var name = 'assets/uploads/' + k.split('|')[0].replace('.html', '') + '-' + stamp + '-' + (i + 1) + '.' + p.ext;
      chain = chain.then(function () { return gh('PUT', name, { message: 'Site editor: upload image', content: p.data, branch: BRANCH }); })
        .then(function () { uploads[k] = name; });
    });
    function writeMap(retry) {
      return gh('GET', MAP_PATH).then(function (f) {
        var cur = {}; try { cur = f ? JSON.parse(unb64(f.content)) : {}; } catch (e) {}
        var sl = cur.slots || {};
        keys.forEach(function (k) { if (pending[k].remove) delete sl[k]; else sl[k] = uploads[k]; });
        var body = { message: 'Site editor: update images', content: b64(JSON.stringify({ version: 1, slots: sl }, null, 2) + '\n'), branch: BRANCH };
        if (f) body.sha = f.sha;
        return gh('PUT', MAP_PATH, body).then(function () { return sl; });
      }).catch(function (e) { if (e.status === 409 && !retry) return writeMap(true); throw e; });
    }
    chain.then(function () { return writeMap(false); }).then(function (sl) {
      /* keep previews in view until GitHub Pages finishes redeploying */
      var keep = {}; keys.forEach(function (k) { if (!pending[k].remove) keep[k] = pending[k].preview; });
      map = sl; Object.keys(keep).forEach(function (k) { map[k] = keep[k]; });
      pending = {}; bar(); apply();
      modal('<h3>Published</h3><p>The new images are saved. Visitors will see them in about a minute, once GitHub Pages finishes updating.</p><div class="ilbc-ed-row"><button type="button" class="ilbc-ed-btn" data-x>Done</button></div>');
      $('#ilbc-ed-modal [data-x]').onclick = close;
    }).catch(function (e) {
      bar();
      var why = e.status === 401 ? 'GitHub did not accept the key. Check it and try again.'
        : e.status === 403 || e.status === 404 ? 'The key cannot write to ' + REPO + '. Give it Contents: Read and write access to that repository.'
        : 'Publishing failed. Check your connection and try again.';
      modal('<h3>Not published</h3><p>' + why + '</p><p>Your changes are still here, so you can try again.</p><div class="ilbc-ed-row"><button type="button" class="ilbc-ed-btn l" data-k>GitHub key</button><button type="button" class="ilbc-ed-btn" data-x>OK</button></div>');
      $('#ilbc-ed-modal [data-x]').onclick = close; $('#ilbc-ed-modal [data-k]').onclick = function () { tokenDialog(); };
    });
  }

  /* ---------- wire up ---------- */
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.ed-lock')) { e.preventDefault(); if (editing) bar(); else login(); } });
  document.addEventListener('click', onClick, true);
  window.addEventListener('beforeunload', function (e) { if (Object.keys(pending).length) { e.preventDefault(); e.returnValue = ''; } });
  var main = $('#main');
  if (main && 'MutationObserver' in window) new MutationObserver(function () { apply(); }).observe(main, { childList: true });
  loadMap();
  if (ss(K_SESSION) === '1') startEdit();
})();
