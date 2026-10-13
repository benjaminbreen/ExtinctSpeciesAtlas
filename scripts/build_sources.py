"""Build the committed, standalone bilingual silphium source records.

Run after editing data/passages.json and data/bibliography.json. The published site needs no build step.
"""
from html import escape
from pathlib import Path
from atlas_data import source_contents, bibliography

ROOT = Path(__file__).resolve().parents[1]
SECONDARY = bibliography('silphium')
SOURCES = source_contents('silphium')


def external_link(url, label):
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} ↗</a>'


def annotated_english(item):
    paragraphs = [escape(text) for text in item['english']]
    for n, (paragraph_index, phrase) in enumerate(item['note_targets'], 1):
        target = escape(phrase)
        if target not in paragraphs[paragraph_index]:
            raise ValueError(f'Footnote anchor not found: {item["author"]}, {phrase}')
        marker = f'<sup class="footnote-ref" id="fnref-{n}"><a href="#fn-{n}" aria-label="Note {n}">{n}</a></sup>'
        paragraphs[paragraph_index] = paragraphs[paragraph_index].replace(target, target + marker, 1)
    return ''.join(f'<p>{paragraph}</p>' for paragraph in paragraphs)


def page(key, item):
    title = f'{item["author"]} — {item["work"]}'
    original_lang = 'la' if item['language'] == 'Latin' else 'grc'
    authority = item['authority_id']
    original = ''.join(f'<p>{escape(text)}</p>' for text in item['original'])
    english = annotated_english(item)
    notes = ''.join(
        f'<li id="fn-{n}"><span class="footnote-number">{n:02d}</span><p>{escape(text)} <a class="footnote-back" href="#fnref-{n}" aria-label="Back to note {n} reference">↩</a></p></li>'
        for n, text in enumerate(item['notes'], 1)
    )
    bibliography = ''.join(
        f'<li><span>{n:02d}</span><div><a href="{escape(SECONDARY[ref][2], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(SECONDARY[ref][0])} ↗</a><br>{escape(SECONDARY[ref][1])}</div></li>'
        for n, ref in enumerate(item['reading'], 1)
    )
    previous, next_ = item['neighbors']
    next_links = ' · '.join(f'<a href="./source-{neighbor}.html">{escape(SOURCES[neighbor]["author"])} ↗</a>' for neighbor in (previous, next_) if neighbor)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#f5f2e9" />
  <meta name="description" content="{escape(item['summary'], quote=True)}" />
  <title>{escape(title)} — Atlas of Historically Lost Species</title>
  <link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" />
  <link rel="preload" href="./assets/gfs-didot.ttf" as="font" type="font/ttf" crossorigin />
  <link rel="stylesheet" href="./styles.css?v=footer-3" />
  <link rel="stylesheet" href="./detail.css" />
  <script type="module" src="./main.js?v=footer-3"></script>
<link rel="stylesheet" href="./ui.css?v=2" /></head>
<body data-page="source">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-seal" aria-hidden="true"><span class="seal-symbol"></span></div>
  <div class="page-shell">
    <header class="masthead"><a class="wordmark" href="./index.html" aria-label="Atlas of Historically Lost Species, home"><span class="wordmark-short" aria-hidden="true">AHLo<span class="wordmark-accent">S</span></span><span class="wordmark-long" aria-hidden="true">Atlas of Historically Lost Species</span></a><nav aria-label="Main navigation"><a href="./index.html#index">Index</a><a href="./authorities.html">Authorities</a><a href="./about.html">About</a></nav></header>
    <main id="main">
      <nav class="source-breadcrumb" aria-label="Breadcrumb"><a href="./silphium.html#record">Silphium</a> / Primary source / {escape(item['author'])}</nav>
      <header class="source-head"><div><span class="folio-label">Primary source · {escape(item['period'])}</span><div class="source-author-title"><a class="source-author-avatar" href="./authorities.html#{authority}" aria-label="{escape(item['author'], quote=True)} in the authorities index"><img src="./assets/authorities/{authority}.webp" width="84" height="84" alt="" /></a><h1><a href="./authorities.html#{authority}">{escape(item['author'])}</a></h1></div><p class="source-deck"><i>{escape(item['work'])}</i>. {escape(item['summary'])}</p></div>
      <div class="source-head-meta"><dl><div><dt>Passage shown</dt><dd>{escape(item['scope'])}</dd></div><div><dt>Original language</dt><dd>{escape(item['language'])}</dd></div><div><dt>Place in record</dt><dd><a href="./index.html?place=cyrenaica#index">{escape(item['place'])} ↗</a><br>{escape(item['place_note'])}</dd></div></dl></div></header>
      <div class="source-grid" aria-label="Original text and English translation">
        <section class="source-column" aria-labelledby="original-title"><div class="source-column-head"><h2 id="original-title">Original text</h2><span>{escape(item['language'])}</span></div><div class="source-text" lang="{original_lang}">{original}</div></section>
        <section class="source-column" aria-labelledby="translation-title"><div class="source-column-head"><h2 id="translation-title">English</h2><span>New working translation for this atlas</span></div><div class="source-text">{english}</div></section>
      </div>
      <div class="source-editions" aria-label="Texts used"><span>Texts used</span>{external_link(item['original_source'], item['original_label'])}{external_link(item['other_source'], item['other_label'])}</div>
      <section class="further-reading" aria-labelledby="further-title"><h2 id="further-title">Further reading</h2><ol class="further-list">{bibliography}</ol></section>
      <aside class="source-footnotes" aria-labelledby="notes-title"><h2 id="notes-title">Notes</h2><ol>{notes}</ol></aside>
    </main>
    <footer class="site-footer"><span>Atlas of Historically Lost Species</span><span><a href="./silphium.html#record">Back to the silphium record ↗</a>{' · ' + next_links if next_links else ''}</span></footer>
  </div>
</body>
</html>
'''


if __name__ == '__main__':
    for key, item in SOURCES.items():
        (ROOT / f'source-{key}.html').write_text(page(key, item), encoding='utf-8')
