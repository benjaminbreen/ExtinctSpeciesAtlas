const dialog = document.querySelector('#notes-dialog');
const dialogImage = document.querySelector('#notes-dialog-image');
const dialogTitle = document.querySelector('#notes-dialog-title');
let opener;
for (const source of document.querySelectorAll('.notes-source')) {
  const image = source.querySelector('.notes-image img');
  const caption = source.querySelector('figcaption');
  const edition = source.querySelector('.notes-edition');
  for (const button of source.querySelectorAll('[data-scan-src]')) {
    button.addEventListener('click', () => {
      image.src = button.dataset.scanSrc;
      image.alt = button.dataset.scanCaption;
      caption.textContent = button.dataset.scanCaption;
      edition.href = button.dataset.scanUrl;
      for (const sibling of source.querySelectorAll('[data-scan-src]')) sibling.setAttribute('aria-pressed', String(sibling === button));
    });
  }
  for (const button of source.querySelectorAll('.notes-enlarge, .notes-image')) {
    button.addEventListener('click', () => {
      opener = button;
      dialogImage.src = image.src;
      dialogImage.alt = image.alt;
      dialogTitle.textContent = caption.textContent;
      dialog.showModal();
      dialog.scrollTop = 0;
    });
  }
  source.querySelector('.notes-copy').addEventListener('click', async () => {
    const status = source.querySelector('.notes-copy-status');
    try {
      await navigator.clipboard.writeText(source.querySelector('.citation-text').textContent.trim());
      status.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(source.querySelector('.citation-text'));
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Citation selected; copy with your keyboard.';
    }
  });
}
document.querySelector('#notes-close')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('close', () => opener?.focus());
