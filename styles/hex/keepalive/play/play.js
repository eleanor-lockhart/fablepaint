// KEEPALIVE: the whole game. Stills in sixteen registers, colour cycling for the sea, a dissolve made of pixels.
(async function () {
  const W = 640, H = 360, cv = document.getElementById('c'), cx = cv.getContext('2d'), logEl = document.getElementById('log');
  const G = await (await fetch('game.json')).json(), PAL = G.palette, cache = {};
  const S = { node: 'jetty', lamp: 0, lever: 0, dial: 0, lit: 0, linked: 0, sent: 3, waiting: 0 };
  let tick = 0, busy = false, cur = null, prev = null, fade = 5, started = false, lines = [];
  const thr = new Float32Array(W * H); { const r = new Float32Array((W / 2) * (H / 2)).map(Math.random); for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) thr[y * W + x] = r[(y >> 1) * (W / 2) + (x >> 1)]; }
  const snd = {}; for (const n of ['press', 'move', 'lever', 'lamp', 'dial', 'her', 'me', 'no', 'yes', 'sea']) { snd[n] = new Audio('snd/' + n + '.mp3'); } snd.sea.loop = true; snd.sea.volume = .7;
  const play = n => { if (!started) return; const a = snd[n].cloneNode(); a.volume = n === 'yes' || n === 'no' ? .9 : .7; a.play().catch(() => {}); };
  const key = () => ({ jetty: 'jetty_' + S.lamp, path: 'path_' + S.lamp, shelter: 'shelter', book: 'book_' + S.linked, beacon: 'beacon_' + S.lamp + S.lever + S.dial, lookout: 'lookout_' + S.lamp + S.lit, glass: 'glass_' + S.lit })[S.node];
  const pixels = src => new Promise(ok => { const im = new Image(); im.onload = () => { const o = document.createElement('canvas'); o.width = W; o.height = H; const c = o.getContext('2d'); c.drawImage(im, 0, 0); ok(c.getImageData(0, 0, W, H).data); }; im.src = src; });
  async function still(k) {
    if (!cache[k]) { const rgb = await pixels('img/' + k + '.png'), tb = G.cycles[k]; cache[k] = { rgb, tb, slot: tb ? await pixels('img/' + k + '_c.png') : null }; }
    return cache[k];
  }
  function paint(st, out) {            // one still at this tick, colour cycling applied
    out.set(st.rgb);
    if (st.tb) for (let i = 0; i < W * H; i++) { const s = st.slot[i * 4]; if (s) { const g = (s - 1) >> 3, c = PAL[st.tb[g][((s - 1 & 7) + tick) % 8]]; out[i * 4] = c[0]; out[i * 4 + 1] = c[1]; out[i * 4 + 2] = c[2]; } }
  }
  const img = cx.createImageData(W, H), a = new Uint8ClampedArray(W * H * 4), b = new Uint8ClampedArray(W * H * 4);
  function draw() {
    if (!cur) return; paint(cur, a);
    if (prev && fade < 5) { paint(prev, b); const p = [.5, .68, .82, .92, .97][fade]; for (let i = 0; i < W * H; i++) if (thr[i] >= p) { a[i * 4] = b[i * 4]; a[i * 4 + 1] = b[i * 4 + 1]; a[i * 4 + 2] = b[i * 4 + 2]; } }
    img.data.set(a); cx.putImageData(img, 0, 0);
  }
  async function show(dissolve) { const nx = await still(key()); if (dissolve) { prev = cur; fade = 0; } cur = nx; draw(); }
  setInterval(() => { tick++; draw(); }, 1000 / 6); setInterval(() => { if (fade < 5) { fade++; draw(); } }, 42);
  function log(s, her) { lines.unshift([s, her]); logEl.innerHTML = '<span class="' + (her ? 'her' : '') + '">' + s + '</span>' + (lines[1] ? '<span class="old">' + lines[1][0] + '</span>' : ''); }
  const wait = ms => new Promise(ok => setTimeout(ok, ms));
  async function go(n) { play('move'); S.node = n; await show(true); if ((n === 'lookout' || n === 'glass') && S.waiting && !S.linked) hers(); }
  async function blink(who, n, word) {  // her window on, or the beacon off, for a quarter of a second, n times
    for (let k = 1; k <= n; k++) { if (who === 'her') S.lit ^= 1; else S.lamp ^= 1; play(who); log((who === 'her' ? '< ' : '> ') + (word || k), who === 'her'); await show(false); await wait(250); if (who === 'her') S.lit ^= 1; else S.lamp ^= 1; await show(false); await wait(250); }
  }
  async function hers() { if (busy) return; busy = true; await wait(900); if (S.node === 'lookout' || S.node === 'glass') await blink('her', S.sent); busy = false; }
  async function lever() {
    if (!S.lamp) { S.lamp = 1; S.lever = 1; S.waiting = 1; play('lever'); play('lamp'); log('> HELLO'); return show(false); }
    if (S.linked) return log('THE LINK IS UP.  NOTHING TO SEND.');
    busy = true; S.lever = 0; play('lever'); await show(false); await wait(250); S.lever = 1; await show(false); await wait(250);
    await blink('me', S.dial); await wait(700);
    if (S.dial === S.sent + 1) { S.linked = 1; S.lit = 1; play('yes'); log('< YES.  LINK UP.', true); }
    else { S.lamp = 0; S.lever = 0; S.waiting = 0; S.sent = S.sent >= 7 ? 3 : S.sent + 2; play('no'); log('< NO.', true); setTimeout(() => log('YOUR LAMP IS OUT.'), 800); }
    await show(false); busy = false;
  }
  async function alive() {              // every eight seconds, for as long as both are there
    if (!S.linked || busy) return; busy = true; await blink('her', 1, 'STILL HERE.'); await wait(250); await blink('me', 1, 'STILL HERE.'); busy = false;
  }
  setInterval(alive, 8000);
  const spot = e => { const r = cv.getBoundingClientRect(), x = (e.clientX - r.left) * W / r.width, y = (e.clientY - r.top) * H / r.height; for (const [n, q] of Object.entries(G.spots[S.node] || {})) if (x >= q[0] && x <= q[2] && y >= q[1] && y <= q[3]) return n; return y > H - 34 || S.node === 'book' ? 'back' : null; };
  cv.addEventListener('mousemove', e => { cv.style.cursor = spot(e) ? 'pointer' : 'default'; });
  async function act(n) {
    if (!started) { started = true; snd.sea.play().catch(() => {}); }
    if (busy || !n) return; play('press');
    if (n === 'back') { if (G.back[S.node]) await go(G.back[S.node]); }
    else if (n === 'lever') await lever();
    else if (n === 'dial') { S.dial = (S.dial + 1) % 10; play('dial'); await show(false); }
    else if (n === 'her') { log('> (YOU WAVE.)'); busy = true; await wait(1800); log('<', true); busy = false; }
    else await go(n);
  }
  cv.addEventListener('click', e => act(spot(e))); document.getElementById('back').addEventListener('click', () => act('back'));
  await show(false);
  if (location.hash === '#test') {      // a walk through the whole thing, for checking: the log ends up in the page title
    for (const s of ['path', 'beacon', 'lever', 'lookout', 'W5000', 'back', 'dial', 'dial', 'dial', 'dial', 'lever', 'W7000', 'lookout', 'W1500', 'glass', 'her', 'W2500']) {
      if (s[0] === 'W') await wait(+s.slice(1)); else { while (busy) await wait(100); await act(s); }
    }
    document.title = 'TEST ' + key() + ' :: ' + lines.map(l => l[0]).reverse().join(' | ');
  }
})();
