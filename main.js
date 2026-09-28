import { sealMarks } from './assets/species-icons/seal-marks.js';

const species = {
  silphium: '#bd4e36',
  auk: '#536d81',
  seacow: '#68816c',
  dodo: '#856579',
  aurochs: '#8b6743',
  solitaire: '#9a634f',
  saddle: '#58776e',
  domed: '#9a8055',
  bluebuck: '#527d91',
  bluepigeon: '#75638a',
  macaw: '#a35e4b',
  warrah: '#727b56'
};

function setSpecies(name) {
  const item = species[name];
  if (!item) return;
  document.documentElement.style.setProperty('--accent', item);
  const seal = document.querySelector('.seal-symbol');
  if (seal) {
    seal.innerHTML = `<svg viewBox="0 0 100 100" focusable="false" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${sealMarks[name]}</svg>`;
  }
}

setSpecies(document.body.dataset.species || 'silphium');

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
    'st-kilda': 'St Kilda', 'funk-island': 'Funk Island', 'eldey': 'Eldey',
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
