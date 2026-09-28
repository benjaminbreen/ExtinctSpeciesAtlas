"""Build the static primary-authority index from the edited local data."""
import json
from html import escape
from pathlib import Path

from build_sources import SECONDARY

ROOT = Path(__file__).resolve().parents[1]


def text(value):
    return escape(str(value))


def link(url):
    return escape(url, quote=True)


def build():
    records = json.loads((ROOT / 'data/authorities.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'assets/authorities/manifest.json').read_text(encoding='utf-8'))
    image_sources = {image['authority']: image['source'] for image in manifest}
    slugs = [record['slug'] for record in records]
    assert len(slugs) == len(set(slugs)) == 9
    assert set(slugs) == set(image_sources)
    assert sum(len(record['works']) for record in records) == 11
    catalog = (ROOT / 'silphium.html').read_text(encoding='utf-8')
    for slug in slugs:
        assert catalog.count(f'data-authority="{slug}"') == next(len(r['works']) for r in records if r['slug'] == slug)
        assert (ROOT / f'assets/authorities/{slug}.webp').is_file()

    entries = []
    for index, record in enumerate(sorted(records, key=lambda r: r['sort_year']), 1):
        slug = record['slug']
        works = ''.join(f'<li><a href="{link(work["href"])}">{text(work["label"])} ↗</a></li>' for work in record['works'])
        entries.append(f'''<li class="authority-entry" id="{slug}" data-name="{link(record['name'])}" data-year="{record['sort_year']}" data-count="{len(record['works'])}">
          <span class="authority-index-number">{index:02d}</span>
          <a class="authority-portrait" href="{link(image_sources[slug])}" target="_blank" rel="noopener noreferrer" aria-label="Wikimedia Commons image for {link(record['name'])}"><img src="./assets/authorities/{slug}.webp" width="144" height="144" loading="lazy" alt="{link(record['image_description'])}" /></a>
          <div class="authority-identity"><h2><a href="{link(record['wikipedia'])}" target="_blank" rel="noopener noreferrer">{text(record['name'])}</a></h2><p class="authority-dates">{text(record['dates'])}</p><p class="authority-field">{text(record['field'])}</p></div>
          <div class="authority-description"><p>{text(record['description'])}</p><p class="authority-depiction"><a href="{link(image_sources[slug])}" target="_blank" rel="noopener noreferrer">Image ↗</a> {text(record['image_description'])}. {text(record['image_credit'])}.</p></div>
          <div class="authority-works"><span>{len(record['works']):02d} {"passages" if len(record['works']) > 1 else "passage"}</span><ul>{works}</ul></div>
        </li>''')

    studies = ''.join(
        f'<li><span>{index:02d}</span><a href="{link(work[2])}" target="_blank" rel="noopener noreferrer">{text(work[0])} ↗</a></li>'
        for index, work in enumerate(SECONDARY.values(), 1)
    )
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#f5f2e9" />
  <meta name="description" content="Authors and authorial attributions of the primary silphium passages in the atlas, with dates, works, and attributed images." />
  <title>Authorities — Atlas of Historically Lost Species</title>
  <link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" />
  <link rel="preload" href="./assets/gfs-didot.ttf" as="font" type="font/ttf" crossorigin />
  <link rel="stylesheet" href="./styles.css" />
  <link rel="stylesheet" href="./authorities.css" />
  <script type="module" src="./main.js"></script>
  <script type="module" src="./authorities.js"></script>
</head>
<body data-page="authorities">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-seal" aria-hidden="true"><span class="seal-symbol"></span></div>
  <div class="page-shell">
    <header class="masthead"><a class="wordmark" href="./index.html" aria-label="Atlas home">Atlas<span class="wordmark-period">.</span></a><nav aria-label="Main navigation"><a href="./index.html#index">Index</a><a href="./authorities.html" aria-current="page">Authorities</a><a href="./index.html#about">About</a></nav></header>
    <main id="main">
      <header class="authority-head"><div><span class="folio-label">Silphium / primary texts</span><h1>Authorities</h1></div><div class="authority-head-side"><span>09 authorial entries</span><span>11 passages indexed</span></div></header>
      <div class="authority-intro"><p>Authors and authorial attributions of the primary passages currently indexed for silphium. Select a work to return to its record.</p><p>Dates are approximate. The images are later representations, identified and credited with each entry.</p></div>
      <div class="authority-toolbar"><label for="authority-sort">Sort <select id="authority-sort"><option value="chronological">Chronological</option><option value="name">Name A–Z</option><option value="sources">Most passages</option></select></label><div class="authority-view" role="group" aria-label="Display authorities"><button type="button" data-authority-view="list" aria-pressed="true">List</button><button type="button" data-authority-view="cards" aria-pressed="false">Cards</button></div></div>
      <ol class="authority-list" id="authority-list" data-view="list">{''.join(entries)}</ol>
      <section class="studies-cited" aria-labelledby="studies-title"><div><span class="folio-label">Bibliography</span><h2 id="studies-title">Studies cited</h2></div><ol>{studies}</ol></section>
    </main>
    <footer class="site-footer"><span>Atlas of Historically Lost Species</span><span><a href="./silphium.html#source-catalog">Silphium source index ↗</a></span></footer>
  </div>
</body>
</html>
'''
    (ROOT / 'authorities.html').write_text(html, encoding='utf-8')


if __name__ == '__main__':
    build()
