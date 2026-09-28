const list = document.querySelector('#authority-list');
const sort = document.querySelector('#authority-sort');
const buttons = [...document.querySelectorAll('[data-authority-view]')];

if (list && sort) {
  const entries = [...list.children];
  sort.addEventListener('change', () => {
    const mode = sort.value;
    const ordered = [...entries].sort((a, b) => {
      if (mode === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      if (mode === 'sources') return Number(b.dataset.count) - Number(a.dataset.count) || Number(a.dataset.year) - Number(b.dataset.year);
      return Number(a.dataset.year) - Number(b.dataset.year);
    });
    list.replaceChildren(...ordered);
  });
  buttons.forEach(button => button.addEventListener('click', () => {
    list.dataset.view = button.dataset.authorityView;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
}
