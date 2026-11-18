/* Grupa Martex — main.js */
(() => {
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch {} }
  };

  // ---------- Motyw: domyślnie jasny ----------
  const root = document.documentElement;
  const metaTheme = document.querySelector('meta[name="theme-color"]');
  const applyTheme = t => {
    if (t === 'dark') root.setAttribute('data-theme', 'dark'); else root.removeAttribute('data-theme');
    if (metaTheme) metaTheme.content = t === 'dark' ? '#0e0e0e' : '#faf7f2';
  };
  applyTheme(store.get('martex-grupa-theme'));
  document.querySelectorAll('.theme').forEach(b => b.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next); store.set('martex-grupa-theme', next);
  }));

  // ---------- Menu ----------
  const nav = document.querySelector('.nav');
  const burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
  });
  document.querySelectorAll('.nav__links a').forEach(a => a.addEventListener('click', () => nav.classList.remove('is-open')));

  // ---------- Wejścia sekcji ----------
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));

  // ---------- Katalog: filtr + szukaj ----------
  const grid = document.querySelector('[data-products]');
  if (grid) {
    const cards = [...grid.querySelectorAll('.pcard')];
    const chips = [...document.querySelectorAll('[data-filter]')];
    const input = document.querySelector('[data-search]');
    const empty = document.querySelector('.empty-msg');
    const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l');
    let cat = 'all';
    const run = () => {
      const q = input ? norm(input.value.trim()) : '';
      let shown = 0;
      cards.forEach(c => {
        const ok = (cat === 'all' || c.dataset.cat === cat) && (!q || norm(c.dataset.name).includes(q));
        c.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.classList.toggle('show', shown === 0);
    };
    chips.forEach(ch => ch.addEventListener('click', () => {
      cat = ch.dataset.filter;
      chips.forEach(x => { x.classList.toggle('on', x === ch); x.setAttribute('aria-pressed', x === ch); });
      run();
      history.replaceState(null, '', cat === 'all' ? location.pathname : '#' + cat);
    }));
    if (input) input.addEventListener('input', run);
    const start = chips.find(c => '#' + c.dataset.filter === location.hash);
    if (start) start.click();
  }

  // ---------- Program lotowy: zakładki + dzisiejszy dzień ----------
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  if (tabs.length) {
    const show = t => {
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      document.querySelectorAll('.plan').forEach(p => p.classList.toggle('on', p.id === t.getAttribute('aria-controls')));
    };
    tabs.forEach(t => t.addEventListener('click', () => { show(t); history.replaceState(null, '', '#' + t.dataset.key); }));
    const start = tabs.find(t => '#' + t.dataset.key === location.hash);
    if (start) show(start);
    const wd = new Date().getDay(); // 0 = niedziela
    document.querySelectorAll('.plan tr[data-d]').forEach(tr => tr.classList.toggle('today', +tr.dataset.d === wd));
  }
  document.querySelectorAll('[data-print]').forEach(b => b.addEventListener('click', () => print()));

  // ---------- Do góry ----------
  const totop = document.querySelector('.totop');
  if (totop) {
    const t = () => totop.classList.toggle('show', scrollY > 700);
    addEventListener('scroll', t, { passive: true }); t();
    totop.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ---------- Cookies + mapa Google ----------
  const loadMaps = () => document.querySelectorAll('[data-map]').forEach(m => {
    if (m.classList.contains('loaded')) return;
    const f = document.createElement('iframe');
    f.src = m.dataset.map; f.loading = 'lazy'; f.title = m.dataset.title || 'Mapa dojazdu';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    m.prepend(f); m.classList.add('loaded');
  });
  const banner = document.querySelector('.cookies');
  const consent = store.get('martex-grupa-consent');
  if (consent === 'all') loadMaps();
  if (banner && !consent) setTimeout(() => banner.classList.add('show'), 900);
  document.querySelectorAll('[data-consent]').forEach(b => b.addEventListener('click', () => {
    store.set('martex-grupa-consent', b.dataset.consent);
    banner.classList.remove('show');
    if (b.dataset.consent === 'all') loadMaps();
    else document.querySelectorAll('[data-map].loaded').forEach(m => { m.querySelector('iframe')?.remove(); m.classList.remove('loaded'); });
  }));
  document.querySelectorAll('[data-cookie-settings]').forEach(b => b.addEventListener('click', () => banner && banner.classList.add('show')));
  document.querySelectorAll('[data-map-load]').forEach(b => b.addEventListener('click', () => {
    store.set('martex-grupa-consent', 'all'); banner && banner.classList.remove('show'); loadMaps();
  }));

  // ---------- Rok ----------
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
