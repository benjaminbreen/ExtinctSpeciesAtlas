import { landPaths } from './assets/map-geometry.js';

const mount = document.querySelector('#atlas-map');
if (mount) {
  const land = landPaths.map(path => `<path d="${path}"/>`).join('');
  const grid = [16, 20, 24, 28].map(lon => {
    const x = (lon - 13) * 1200 / 18;
    return `<line class="map-grid" x1="${x}" y1="0" x2="${x}" y2="700"/><text class="map-grid-label" x="${x + 8}" y="28">${lon}° E</text>`;
  }).join('') + [30, 33, 36].map(lat => {
    const y = (39 - lat) * 700 / 12;
    return `<line class="map-grid" x1="0" y1="${y}" x2="1200" y2="${y}"/><text class="map-grid-label" x="16" y="${y - 8}">${lat}° N</text>`;
  }).join('');

  mount.innerHTML = `<svg id="map-svg" viewBox="0 0 1200 700" role="img" aria-labelledby="map-svg-title map-svg-desc" xmlns="http://www.w3.org/2000/svg">
    <title id="map-svg-title">Cyrenaica and the coast of North Africa</title>
    <desc id="map-svg-desc">An engraved-style map with modern coastline. A translucent wash marks the approximate coastal reach reported by Herodotus, with points for Cyrene and Ptolemais. Use the buttons to zoom and drag to pan.</desc>
    <defs>
      <pattern id="sea-lines" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M0 17h18" stroke="#9d978b" stroke-width=".55" opacity=".32"/></pattern>
      <pattern id="land-dots" width="11" height="11" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".6" fill="#9b9284" opacity=".3"/></pattern>
      <clipPath id="map-clip"><rect width="1200" height="700"/></clipPath>
    </defs>
    <g clip-path="url(#map-clip)"><g id="map-viewport">
      <rect width="1200" height="700" fill="#e6e5de"/><rect width="1200" height="700" fill="url(#sea-lines)"/>
      <g>${grid}</g>
      <g fill="#e7e0d1" stroke="#c3b8a7" stroke-width="5" stroke-linejoin="round">${land}</g>
      <g fill="url(#land-dots)" stroke="#555149" stroke-width="1.5" stroke-linejoin="round">${land}</g>
      <path d="M309 477 C360 435 414 407 483 391 S640 338 724 346 S790 365 832 373" fill="none" stroke="#bd4e36" stroke-width="75" stroke-linecap="round" opacity=".17"/>
      <path d="M309 477 C360 435 414 407 483 391 S640 338 724 346 S790 365 832 373" fill="none" stroke="#a6422d" stroke-width="2" stroke-dasharray="7 10" opacity=".8"/>
      <text class="map-sea-label" x="395" y="155">MEDITERRANEAN SEA</text>
      <text class="map-small-label" x="250" y="340">Gulf of Sidra</text>
      <text class="map-land-label" x="550" y="548">C Y R E N A I C A</text>
      <text class="map-land-label" x="837" y="627" style="font-size:15px;letter-spacing:5px">NORTH AFRICA</text>
      <path class="map-hair" d="M593 363l32-40"/><circle class="map-point-ring" cx="593" cy="363" r="9"/><circle class="map-point" cx="593" cy="363" r="5"/><text class="map-location-label" x="630" y="322">Cyrene</text>
      <path class="map-hair" d="M530 368l-60 43"/><circle class="map-point-ring" cx="530" cy="368" r="8"/><circle class="map-point" cx="530" cy="368" r="5"/><text class="map-small-label" x="373" y="432">Ptolemais</text>
      <g transform="translate(1058 115)" class="map-compass"><path d="M0-30V30M-30 0h60M0-30l5 17-5-5-5 5Z"/><circle r="4" fill="#4a4742" stroke="none"/><text x="-6" y="-41" fill="#4a4742" stroke="none" font="17px Georgia,serif">N</text></g>
    </g></g>
    <rect x=".8" y=".8" width="1198.4" height="698.4" class="map-frame-line" pointer-events="none"/>
  </svg>`;

  const svg = mount.querySelector('#map-svg');
  const viewport = mount.querySelector('#map-viewport');
  const output = document.querySelector('#zoom-level');
  let scale = 1;
  let offsetX = 0;
  let offsetY = 0;
  let drag = null;

  function render() {
    offsetX = Math.min(0, Math.max(1200 * (1 - scale), offsetX));
    offsetY = Math.min(0, Math.max(700 * (1 - scale), offsetY));
    viewport.setAttribute('transform', `translate(${offsetX} ${offsetY}) scale(${scale})`);
    svg.classList.toggle('is-zoomed', scale > 1);
    output.value = `${Math.round(scale * 100)}%`;
    output.textContent = output.value;
  }

  function point(event) {
    const position = new DOMPoint(event.clientX, event.clientY);
    return position.matrixTransform(svg.getScreenCTM().inverse());
  }

  function zoom(factor, centerX = 600, centerY = 350) {
    const next = Math.min(4.5, Math.max(1, scale * factor));
    const ratio = next / scale;
    offsetX = centerX - (centerX - offsetX) * ratio;
    offsetY = centerY - (centerY - offsetY) * ratio;
    scale = next;
    render();
  }

  document.querySelector('[data-zoom-in]').addEventListener('click', () => zoom(1.5));
  document.querySelector('[data-zoom-out]').addEventListener('click', () => zoom(1 / 1.5));
  document.querySelector('[data-map-reset]').addEventListener('click', () => {
    scale = 1; offsetX = 0; offsetY = 0; render();
  });
  svg.addEventListener('wheel', event => {
    if (scale <= 1 && event.deltaY > 0) return;
    event.preventDefault();
    const at = point(event);
    zoom(event.deltaY < 0 ? 1.15 : 1 / 1.15, at.x, at.y);
  }, { passive: false });
  svg.addEventListener('pointerdown', event => {
    if (scale <= 1 || event.button !== 0) return;
    drag = { pointerId: event.pointerId, at: point(event), x: offsetX, y: offsetY };
    svg.setPointerCapture(event.pointerId);
    svg.classList.add('is-dragging');
  });
  svg.addEventListener('pointermove', event => {
    if (!drag || event.pointerId !== drag.pointerId) return;
    const at = point(event);
    offsetX = drag.x + at.x - drag.at.x;
    offsetY = drag.y + at.y - drag.at.y;
    render();
  });
  const endDrag = event => {
    if (drag && event.pointerId === drag.pointerId) {
      drag = null;
      svg.classList.remove('is-dragging');
    }
  };
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);
  render();
}
