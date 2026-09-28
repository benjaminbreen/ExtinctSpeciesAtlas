const species = {
  silphium: {
    color: '#bd4e36',
    symbol: '<path d="M0 13C-11 4-8-6 0-3c8-3 11 7 0 16Z"/><path d="M0-3V-16M0-11c-5-4-9-3-12 0M0-11c5-4 9-3 12 0"/>'
  },
  auk: {
    color: '#536d81',
    symbol: '<path d="M-8 12C-9-2-4-14 3-15c6 6 8 15 5 27Z"/><path d="M-7-1C-2 1 2 0 7-3M3-15l9 4-7 2"/>'
  },
  seacow: {
    color: '#68816c',
    symbol: '<path d="M-14 2c7-7 17-7 25-1M-14 2c7 6 17 6 25-1M11 1l5-6M11 1l5 6M-4-2c1 3 1 5 0 8"/>'
  },
  dodo: {
    color: '#856579',
    symbol: '<path d="M-10 11c-1-8 2-18 11-19 9-1 13 7 11 17-6 3-15 4-22 2Z"/><path d="M2-7c3-6 9-7 12-4l-6 4M-10 4l-5-2M-3 12v5M5 12v5"/>'
  }
};

function setSpecies(name) {
  const item = species[name];
  if (!item) return;
  document.documentElement.style.setProperty('--accent', item.color);
  const seal = document.querySelector('.seal-symbol');
  if (seal) {
    seal.innerHTML = `<svg viewBox="-22 -22 44 44" focusable="false" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round">${item.symbol}</svg>`;
  }
}

setSpecies('silphium');

if (document.body.dataset.page === 'home') {
  const entries = [...document.querySelectorAll('.species-entry')];
  const params = new URLSearchParams(location.search);
  const tag = params.get('tag');
  const place = params.get('place');
  const filters = {
    'classical-era': 'Classical era', mediterranean: 'Mediterranean', medicinal: 'Medicinal',
    'early-modern': 'Early modern', 'north-atlantic': 'North Atlantic',
    'north-pacific': 'North Pacific', 'indian-ocean': 'Indian Ocean',
    cyrenaica: 'Cyrenaica', rome: 'Rome', 'bering-sea': 'Bering Sea', mauritius: 'Mauritius'
  };
  const selected = tag && filters[tag] ? { type: 'tags', key: tag, label: filters[tag] }
    : place && filters[place] ? { type: 'places', key: place, label: filters[place] } : null;
  if (selected) {
    const visible = entries.filter(entry => {
      const matches = (entry.dataset[selected.type] || '').split(' ').includes(selected.key);
      entry.hidden = !matches;
      return matches;
    });
    const status = document.querySelector('#filter-status');
    status.hidden = false;
    document.querySelector('#filter-description').textContent = `${selected.type === 'tags' ? 'Subject' : 'Place'}: ${selected.label} · ${visible.length} ${visible.length === 1 ? 'entry' : 'entries'}`;
    document.querySelector('.section-heading span').textContent = `${visible.length} / ${entries.length}`;
  }
  const items = [...document.querySelectorAll('.observe-species')].filter(item => !item.hidden);
  const update = () => {
    const referenceY = window.innerHeight * 0.44;
    const current = items.reduce((best, element) => {
      const rect = element.getBoundingClientRect();
      const distance = rect.top <= referenceY && rect.bottom >= referenceY
        ? 0
        : Math.min(Math.abs(rect.top - referenceY), Math.abs(rect.bottom - referenceY));
      return distance < best.distance ? { element, distance } : best;
    }, { element: items[0], distance: Infinity }).element;
    setSpecies(current.dataset.species);
    document.body.classList.toggle('has-scrolled', window.scrollY > 150);
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
}

if (['detail', 'source'].includes(document.body.dataset.page)) {
  const updateSeal = () => document.body.classList.toggle('has-scrolled', window.scrollY > 150);
  window.addEventListener('scroll', updateSeal, { passive: true });
  updateSeal();
}

if (document.body.dataset.page === 'detail') {
  const buttons = [...document.querySelectorAll('[data-source-tab]')];
  const panels = [...document.querySelectorAll('[data-source-panel]')];
  function selectSource(index, focus = false) {
    buttons.forEach((button, i) => {
      const selected = i === index;
      button.setAttribute('aria-selected', String(selected));
      button.tabIndex = selected ? 0 : -1;
    });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    if (focus) buttons[index].focus();
    document.dispatchEvent(new CustomEvent('atlas:source', { detail: { index } }));
  }
  buttons.forEach((button, index) => {
    button.addEventListener('click', () => selectSource(index));
    button.addEventListener('keydown', event => {
      if (!['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
        : (index + (['ArrowDown', 'ArrowRight'].includes(event.key) ? 1 : -1) + buttons.length) % buttons.length;
      selectSource(next, true);
    });
  });
  selectSource(1);
}
