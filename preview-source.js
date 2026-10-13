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
