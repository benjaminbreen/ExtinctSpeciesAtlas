import { aukLandPaths } from './assets/auk-map-geometry.js';

const mount = document.querySelector('#auk-map');
if (mount) {
  const land = aukLandPaths.map(path => `<path d="${path}"/>`).join('');
  const locations = [
    { id: 'st-kilda', name: 'St Kilda', lon: -8.58, lat: 57.81, dx: -122, dy: -23 },
    { id: 'funk-island', name: 'Funk Island', lon: -53.18, lat: 49.76, dx: 21, dy: -24 },
    { id: 'eldey', name: 'Eldey', lon: -22.96, lat: 63.74, dx: 21, dy: -21 },
  ];
  const point = ({ lon, lat }) => [((lon + 67) / 82) * 1200, ((70 - lat) / 25) * 700];
  const places = locations.map(item => {
    const [x, y] = point(item);
    return `<g class="auk-map-place" data-map-place="${item.id}"><circle class="map-point-ring" cx="${x}" cy="${y}" r="13"/><circle class="map-point" cx="${x}" cy="${y}" r="7"/><text class="map-location-label" x="${x + item.dx}" y="${y + item.dy}">${item.name}</text></g>`;
  }).join('');
  const grid = [-60, -40, -20, 0].map(lon => {
    const x = ((lon + 67) / 82) * 1200;
    return `<line class="map-grid" x1="${x}" y1="0" x2="${x}" y2="700"/><text class="map-grid-label" x="${x + 8}" y="28">${Math.abs(lon)}° ${lon < 0 ? 'W' : 'E'}</text>`;
  }).join('') + [50, 60].map(lat => {
    const y = ((70 - lat) / 25) * 700;
    return `<line class="map-grid" x1="0" y1="${y}" x2="1200" y2="${y}"/><text class="map-grid-label" x="16" y="${y - 8}">${lat}° N</text>`;
  }).join('');

  mount.innerHTML = `<svg id="map-svg" viewBox="0 0 1200 700" role="img" aria-labelledby="auk-map-title auk-map-desc" xmlns="http://www.w3.org/2000/svg">
    <title id="auk-map-title">Great auk places in the North Atlantic</title>
    <desc id="auk-map-desc">Coastlines from Natural Earth with St Kilda, Funk Island, and Eldey marked. Zoom with the controls or scroll, and drag to pan.</desc>
    <defs><pattern id="auk-sea-lines" width="19" height="19" patternUnits="userSpaceOnUse"><path d="M0 18h19" stroke="#9d978b" stroke-width=".6" opacity=".3"/></pattern><pattern id="auk-land-dots" width="11" height="11" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".6" fill="#9b9284" opacity=".3"/></pattern><clipPath id="auk-clip"><rect width="1200" height="700"/></clipPath></defs>
    <g clip-path="url(#auk-clip)"><g id="map-viewport"><rect width="1200" height="700" fill="#e5e5de"/><rect width="1200" height="700" fill="url(#auk-sea-lines)"/><g>${grid}</g><g fill="#e9e2d4" stroke="#c1b7aa" stroke-width="4" stroke-linejoin="round">${land}</g><g fill="url(#auk-land-dots)" stroke="#555149" stroke-width="1.6" stroke-linejoin="round">${land}</g><text class="map-sea-label" x="385" y="458">N O R T H &nbsp; A T L A N T I C</text><text class="map-land-label" x="45" y="370">N E W F O U N D L A N D</text><text class="map-land-label" x="575" y="84">I C E L A N D</text><text class="map-land-label" x="932" y="600">B R I T A I N</text>${places}<g transform="translate(1100 88)" class="map-compass"><path d="M0-25V25M-25 0h50M0-25l5 15-5-5-5 5Z"/><circle r="4" fill="#4a4742" stroke="none"/><text x="-6" y="-36" fill="#4a4742" stroke="none" font="17px Georgia,serif">N</text></g></g></g><rect x=".8" y=".8" width="1198.4" height="698.4" class="map-frame-line" pointer-events="none"/>
  </svg>`;

  const svg = mount.querySelector('#map-svg');
  const viewport = mount.querySelector('#map-viewport');
  const output = document.querySelector('#zoom-level');
  let scale = 1, offsetX = 0, offsetY = 0, drag = null;
  function render() {
    offsetX = Math.min(0, Math.max(1200 * (1 - scale), offsetX));
    offsetY = Math.min(0, Math.max(700 * (1 - scale), offsetY));
    viewport.setAttribute('transform', `translate(${offsetX} ${offsetY}) scale(${scale})`);
    svg.classList.toggle('is-zoomed', scale > 1);
    output.value = `${Math.round(scale * 100)}%`;
    output.textContent = output.value;
  }
  const mapPoint = event => new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
  function zoom(factor, x = 600, y = 350) {
    const next = Math.min(5, Math.max(1, scale * factor));
    const ratio = next / scale;
    offsetX = x - (x - offsetX) * ratio;
    offsetY = y - (y - offsetY) * ratio;
    scale = next;
    render();
  }
  document.querySelector('[data-zoom-in]').addEventListener('click', () => zoom(1.5));
  document.querySelector('[data-zoom-out]').addEventListener('click', () => zoom(1 / 1.5));
  document.querySelector('[data-map-reset]').addEventListener('click', () => { scale = 1; offsetX = 0; offsetY = 0; render(); });
  svg.addEventListener('wheel', event => { if (scale <= 1 && event.deltaY > 0) return; event.preventDefault(); const at = mapPoint(event); zoom(event.deltaY < 0 ? 1.15 : 1 / 1.15, at.x, at.y); }, { passive: false });
  svg.addEventListener('pointerdown', event => { if (scale <= 1 || event.button !== 0) return; drag = { pointerId: event.pointerId, at: mapPoint(event), x: offsetX, y: offsetY }; svg.setPointerCapture(event.pointerId); svg.classList.add('is-dragging'); });
  svg.addEventListener('pointermove', event => { if (!drag || event.pointerId !== drag.pointerId) return; const at = mapPoint(event); offsetX = drag.x + at.x - drag.at.x; offsetY = drag.y + at.y - drag.at.y; render(); });
  const endDrag = event => { if (drag && event.pointerId === drag.pointerId) { drag = null; svg.classList.remove('is-dragging'); } };
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);
  const sourcePlaces = ['st-kilda', 'st-kilda', 'funk-island', 'eldey', 'funk-island'];
  document.addEventListener('atlas:source', event => locations.forEach(item => mount.querySelector(`[data-map-place="${item.id}"]`).classList.toggle('is-active', item.id === sourcePlaces[event.detail.index])));
  mount.querySelector(`[data-map-place="${sourcePlaces[Number(document.body.dataset.defaultSource ?? 0)]}"]`).classList.add('is-active');
  render();
}
