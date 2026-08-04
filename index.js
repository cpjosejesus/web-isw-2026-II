/* ═══════════════════════════════════════════
   Jose Jesus — Portafolio & Blog
   ═══════════════════════════════════════════ */

/* ── Datos del blog ─────────────────────────
   Para publicar un artículo nuevo, agrega un
   objeto a este arreglo. `cat` debe coincidir
   con un data-filter de los botones del HTML.
   ─────────────────────────────────────────── */
const POSTS = [
  {
    title: 'Por qué dejé de optimizar antes de medir',
    excerpt: 'Pasé una semana reescribiendo una función que representaba el 0.4% del tiempo de ejecución. Esto fue lo que aprendí sobre priorizar.',
    cat: 'ingenieria',
    catLabel: 'Ingeniería',
    date: '2026-07-28',
    read: 6
  },
  {
    title: 'Diseñar para el estado vacío',
    excerpt: 'La primera pantalla que ve un usuario nuevo casi nunca tiene datos. Aun así, es la que menos diseñamos.',
    cat: 'diseno',
    catLabel: 'Diseño',
    date: '2026-07-14',
    read: 4
  },
  {
    title: 'Cómo leo un codebase que no escribí',
    excerpt: 'Un método repetible para orientarme en proyectos grandes sin ahogarme en archivos: entradas, límites y flujos.',
    cat: 'ingenieria',
    catLabel: 'Ingeniería',
    date: '2026-06-30',
    read: 8
  },
  {
    title: 'El commit perfecto no existe',
    excerpt: 'Sobre convenciones de mensajes, historial legible, y por qué la disciplina importa más que el formato exacto.',
    cat: 'ingenieria',
    catLabel: 'Ingeniería',
    date: '2026-06-11',
    read: 5
  },
  {
    title: 'Lo que nadie te dice del primer año',
    excerpt: 'Notas honestas sobre síndrome del impostor, code reviews duras y aprender a preguntar sin miedo.',
    cat: 'carrera',
    catLabel: 'Carrera',
    date: '2026-05-22',
    read: 7
  },
  {
    title: 'Tokens de diseño en CSS puro',
    excerpt: 'Custom properties, temas claro/oscuro y escalas tipográficas sin dependencias ni build step.',
    cat: 'diseno',
    catLabel: 'Diseño',
    date: '2026-05-03',
    read: 9
  }
];

/* ── Utilidades ─────────────────────────── */
const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const formatDate = (iso) =>
  new Date(iso + 'T00:00:00').toLocaleDateString('es-MX', {
    day: 'numeric', month: 'short', year: 'numeric'
  });

/* ── 1. Tema claro / oscuro ─────────────── */
(function theme() {
  const toggle = $('#theme-toggle');
  const stored = localStorage.getItem('theme');
  const system = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';

  document.documentElement.dataset.theme = stored || system;

  toggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
  });
})();

/* ── 2. Header: sombra + menú móvil ─────── */
(function header() {
  const header  = $('#header');
  const menuBtn = $('#menu-btn');
  const nav     = $('#nav');

  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 20);
  onScroll();

  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });

  // Cerrar el menú al navegar
  $$('.nav-link', nav).forEach((link) =>
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-label', 'Abrir menú');
    })
  );

  window.addEventListener('scroll', onScroll, { passive: true });
})();

/* ── 3. Barra de progreso de lectura ────── */
(function progress() {
  const bar = $('#progress');

  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    bar.style.width = pct + '%';
  };

  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();

/* ── 4. Reveal al hacer scroll ──────────── */
(function reveal() {
  const items = $$('.reveal');

  if (prefersReduced || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('visible'));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        setTimeout(() => entry.target.classList.add('visible'), i * 70);
        io.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -60px' }
  );

  items.forEach((el) => io.observe(el));
})();

/* ── 5. Contadores del hero ─────────────── */
(function counters() {
  const nums = $$('.hero-stats strong');
  if (!nums.length) return;

  const run = (el) => {
    const target = Number(el.dataset.count) || 0;

    if (prefersReduced) { el.textContent = target + '+'; return; }

    const duration = 1400;
    let start = null;

    const step = (ts) => {
      if (start === null) start = ts;
      const p = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);           // easeOutCubic
      el.textContent = Math.round(target * eased) + '+';
      if (p < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  };

  if (!('IntersectionObserver' in window)) { nums.forEach(run); return; }

  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => {
      if (!e.isIntersecting) return;
      run(e.target);
      io.unobserve(e.target);
    }),
    { threshold: 0.6 }
  );

  nums.forEach((el) => io.observe(el));
})();

/* ── 6. Nav activo según sección ────────── */
(function activeNav() {
  const links = $$('.nav-link');
  const map = new Map();

  links.forEach((link) => {
    const section = document.querySelector(link.getAttribute('href'));
    if (section) map.set(section, link);
  });

  if (!map.size || !('IntersectionObserver' in window)) return;

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((l) => l.classList.remove('active'));
        map.get(entry.target)?.classList.add('active');
      });
    },
    { rootMargin: '-45% 0px -50% 0px' }
  );

  map.forEach((_, section) => io.observe(section));
})();

/* ── 7. Blog: render + filtros ──────────── */
(function blog() {
  const grid  = $('#posts');
  const empty = $('#posts-empty');
  const filters = $$('.filter');

  const render = (cat) => {
    const list = cat === 'all' ? POSTS : POSTS.filter((p) => p.cat === cat);

    grid.replaceChildren();
    empty.hidden = list.length > 0;

    list.forEach((post, i) => {
      const card = document.createElement('article');
      card.className = 'post';
      card.style.animationDelay = `${i * 60}ms`;

      const meta = document.createElement('div');
      meta.className = 'post-meta';

      const cat = document.createElement('span');
      cat.className = 'post-cat';
      cat.textContent = post.catLabel;

      const time = document.createElement('time');
      time.dateTime = post.date;
      time.textContent = formatDate(post.date);

      meta.append(cat, time);

      const h3 = document.createElement('h3');
      h3.textContent = post.title;

      const p = document.createElement('p');
      p.textContent = post.excerpt;

      const foot = document.createElement('div');
      foot.className = 'post-foot';

      const read = document.createElement('span');
      read.className = 'post-read';
      read.textContent = 'Leer artículo →';

      const mins = document.createElement('span');
      mins.className = 'post-time';
      mins.textContent = `${post.read} min`;

      foot.append(read, mins);
      card.append(meta, h3, p, foot);
      grid.append(card);
    });
  };

  filters.forEach((btn) => {
    btn.addEventListener('click', () => {
      filters.forEach((b) => {
        b.classList.remove('is-active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-pressed', 'true');
      render(btn.dataset.filter);
    });
  });

  render('all');
})();

/* ── 8. Brillo que sigue al cursor ──────── */
(function spotlight() {
  if (prefersReduced || !window.matchMedia('(hover: hover)').matches) return;

  $$('.project').forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });
})();

/* ── 9. Formulario de suscripción ───────── */
(function subscribe() {
  const form  = $('#subscribe');
  const input = $('#email');
  const msg   = $('#form-msg');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const value = input.value.trim();
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);

    input.classList.toggle('invalid', !valid);
    msg.classList.toggle('error', !valid);

    if (!valid) {
      msg.textContent = 'Escribe un correo válido para continuar.';
      input.focus();
      return;
    }

    // Front-end únicamente: conecta aquí tu servicio de newsletter.
    msg.textContent = '¡Listo! Te avisaré cuando publique algo nuevo.';
    form.reset();
  });

  input.addEventListener('input', () => {
    input.classList.remove('invalid');
    msg.textContent = '';
  });
})();

/* ── 10. Año del footer ─────────────────── */
$('#year').textContent = new Date().getFullYear();
