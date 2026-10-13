// A small illustrated colophon; images retain their linked gallery credits.
const vignettes = [
  { image: './assets/great-auk-gallery/worm-1655-ink.webp', alt: 'Great auk engraving from Ole Worm’s Museum Wormianum', label: 'Ole Worm · 1655', href: './great-auk.html#images' },
  { image: './assets/silphium-woodcut-isolated.webp', alt: 'Laserpitium woodcut from the 1644 van Stapel edition of Theophrastus', label: 'Van Stapel · 1644', href: './silphium.html#images' }
];
const footer = document.querySelector('.site-footer');
if (footer) {
  const oldLinks = document.body.dataset.page === 'source' ? footer.innerHTML : '';
  const vignette = vignettes[Math.floor(Math.random() * vignettes.length)];
  footer.classList.add('atlas-footer');
  document.body.append(footer);
  footer.innerHTML = `<div class="page-shell footer-inner">${oldLinks ? `<div class="footer-context">${oldLinks}</div>` : ''}
    <div class="footer-colophon">
      <a class="footer-vignette" href="${vignette.href}"><img src="${vignette.image}" alt="${vignette.alt}" width="70" height="78" loading="lazy" /><span>${vignette.label}</span></a>
      <div class="footer-signature"><a class="footer-title" href="./index.html">Atlas of Historically Lost Species</a><p class="footer-credit">Made by <a href="https://benjaminpbreen.com/">Benjamin Breen</a><a class="footer-res-obscura" href="https://resobscura.substack.com/" aria-label="Res Obscura on Substack"><img src="./assets/res-obscura.png" alt="" width="27" height="27" loading="lazy" /></a></p></div>
      <nav class="footer-nav" aria-label="Footer"><a href="./index.html#index">Index</a><a href="./research-notes.html">Research notes</a><a href="./authorities.html">Authorities</a><a href="./about.html">About</a><a href="https://github.com/benjaminbreen/ExtinctSpeciesAtlas/issues">Corrections</a><a class="footer-top" href="#main">Back to top ↑</a></nav>
    </div></div>`;
}
for (const entry of document.querySelectorAll('.species-entry[data-species]')) {
  if (!entry.id) entry.id = `species-${entry.dataset.species}`;
}
