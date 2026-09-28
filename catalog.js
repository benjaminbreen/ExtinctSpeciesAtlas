const catalog = document.querySelector('#source-catalog');
const sortControl = document.querySelector('#catalog-sort');
const viewButtons = [...document.querySelectorAll('[data-catalog-view]')];

if (catalog && sortControl) {
  const records = [...catalog.children];
  sortControl.addEventListener('change', () => {
    const mode = sortControl.value;
    const sorted = [...records].sort((a, b) => {
      if (mode === 'author') {
        return a.dataset.author.localeCompare(b.dataset.author) || Number(a.dataset.year) - Number(b.dataset.year);
      }
      return (Number(a.dataset.year) - Number(b.dataset.year)) * (mode === 'newest' ? -1 : 1);
    });
    catalog.replaceChildren(...sorted);
  });

  viewButtons.forEach(button => button.addEventListener('click', () => {
    catalog.dataset.view = button.dataset.catalogView;
    viewButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
}
