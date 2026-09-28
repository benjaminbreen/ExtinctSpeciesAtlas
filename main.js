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
  },
  aurochs: {
    color: '#8b6743',
    symbol: '<path d="M-13-4c-6-3-7-11-6-14 4 7 8 8 12 8M13-4c6-3 7-11 6-14-4 7-8 8-12 8M-12-5C-11 5-6 15 0 16 6 15 11 5 12-5 6-11-6-11-12-5Z"/><path d="M-7 1h1M7 1h1M-4 9c3 2 5 2 8 0"/>'
  },
  solitaire: {
    color: '#9a634f',
    symbol: '<path d="M-11 12c1-9 6-12 10-10l3-15c1-5 6-5 7 0l6 1-5 4-3 11c5 4 6 8 5 12Z"/><path d="M-4 14l-2 5M5 14l2 5M-2 5c3 0 5 2 5 4"/>'
  },
  saddle: {
    color: '#58776e',
    symbol: '<path d="M-15 9c1-8 5-14 11-14l4-10 5 10c5 0 9 6 10 14Z"/><path d="M-12 9v6M10 9v6M-7 0l6 6 7-6M0-6v11"/>'
  },
  domed: {
    color: '#9a8055',
    symbol: '<path d="M-16 9c1-11 7-18 16-18S15-2 16 9Z"/><path d="M-12 9v6M12 9v6M-7-5l7 6 7-6M0 1v8M-16 9h32"/>'
  },
  bluebuck: {
    color: '#527d91',
    symbol: '<path d="M-8-3c-5-7-5-13-1-17 1 7 4 10 8 13M8-3c5-7 5-13 1-17-1 7-4 10-8 13M-10-3c-3 9-1 16 10 19C11 13 13 6 10-3 4-7-4-7-10-3Z"/><path d="M-5 2h1M5 2h1M-2 11h4"/>'
  },
  bluepigeon: {
    color: '#75638a',
    symbol: '<path d="M-12 10c0-9 5-14 11-14l2-10 8 3-5 5c7 4 10 9 10 16Z"/><path d="M-7-3l8 10M-5 1l8 10M-10 11l-5 4M4 11v6"/>'
  },
  macaw: {
    color: '#a35e4b',
    symbol: '<path d="M-8 12C-13 2-8-12 1-13c7 1 9 6 7 11l8-3c-1 6-5 9-12 7 0 8-3 13-8 17"/><path d="M-2-7c2 1 3 1 4 0M-7 8l-7 11"/>'
  },
  warrah: {
    color: '#727b56',
    symbol: '<path d="M-13-4l2-13 8 8h6l8-8 2 13c5 7 3 16-13 21-16-5-18-14-13-21Z"/><path d="M-6 1h1M6 1h1M-3 9l3 2 3-2"/>'
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
    'south-atlantic': 'South Atlantic', 'southern-africa': 'Southern Africa',
    europe: 'Europe', caribbean: 'Caribbean', mammal: 'Mammals', bird: 'Birds', reptile: 'Reptiles',
    cyrenaica: 'Cyrenaica', rome: 'Rome', 'bering-sea': 'Bering Sea', mauritius: 'Mauritius',
    rodrigues: 'Rodrigues', cape: 'Cape, South Africa', cuba: 'Cuba', 'falkland-islands': 'Falkland Islands'
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

if (['detail', 'source', 'authorities', 'about'].includes(document.body.dataset.page)) {
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
