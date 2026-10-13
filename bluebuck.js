// Keep the facsimile beside the selected account.
const scans = [...document.querySelectorAll('[data-source-scan]')];
function selectScan(index) {
  for (const scan of scans) scan.hidden = Number(scan.dataset.sourceScan) !== index;
}
document.addEventListener('atlas:source', event => selectScan(event.detail.index));
selectScan(Number(document.body.dataset.defaultSource ?? 0));
