const dialog = document.querySelector('#scan-dialog');
for (const button of document.querySelectorAll('#enlarge, .scan-open')) {
  button.addEventListener('click', () => dialog.showModal());
}
document.querySelector('#close-scan').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
document.querySelector('#copy-citation').addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try { await navigator.clipboard.writeText(document.querySelector('#citation-text').textContent); status.textContent = 'Citation copied.'; }
  catch { status.textContent = 'Select the citation above to copy it.'; }
});

for (const button of document.querySelectorAll('[data-scan-src]')) {
  button.addEventListener('click', () => {
    for (const choice of document.querySelectorAll('[data-scan-src]')) choice.setAttribute('aria-pressed', String(choice === button));
    const { scanSrc, scanCaption, scanUrl } = button.dataset;
    for (const image of document.querySelectorAll('.scan-open img, #scan-dialog img')) {
      image.src = scanSrc;
      image.alt = scanCaption;
    }
    document.querySelector('.scan-panel figcaption').textContent = scanCaption;
    document.querySelector('.scan-panel .external-link').href = scanUrl;
    document.querySelector('.scan-open').setAttribute('aria-label', `Enlarge ${scanCaption}`);
    document.querySelector('#dialog-title').textContent = scanCaption;
  });
}
