"""Generate the English-language great auk source records.

Transcriptions were checked against the scans linked on each page. The long s
is regularized; wording and historical spellings are otherwise retained.
"""

from html import escape
from pathlib import Path
from atlas_data import source_contents, bibliography, read
from string import Template

ROOT = Path(__file__).resolve().parents[1]

READING = bibliography('great-auk')

SOURCES = source_contents('great-auk')


def link(url, label):
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} ↗</a>'


def render(key, item, sources=None, reading_records=None):
    sources = SOURCES if sources is None else sources
    reading_records = READING if reading_records is None else reading_records
    paras = [escape(p) for p in item["paragraphs"]]
    phrase = escape(item.get("note_phrase") or "")
    for i, para in enumerate(paras):
        if phrase and phrase in para:
            paras[i] = para.replace(phrase, phrase + '<sup class="footnote-ref" id="fnref-1"><a href="#fn-1" aria-label="Note 1">1</a></sup>', 1)
            break
    else:
        if phrase:
            raise ValueError(f"Footnote target missing: {key}")
    original = ''.join(f'<p>{p}</p>' for p in paras)
    reading = ''.join(f'<li><span>{n:02d}</span><div><a href="{escape(reading_records[slug][2], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(reading_records[slug][0])} ↗</a><br>{escape(reading_records[slug][1])}</div></li>' for n, slug in enumerate(item['reading'], 1))
    if item.get('reader'):
        reader = item['reader']
        species = next(s for s in read('species') if s['id'] == item['species_id'])
        template = Template((ROOT / 'templates/source-reader.html').read_text(encoding='utf-8'))
        fields = {name: value if name.endswith('_html') or name in ('scan_caption', 'dialog_title') else escape(value, quote=True)
                  for name, value in reader.items() if isinstance(value, str)}
        fields['date_rows'] = ''.join(f'<div><span>{i:02d} / {escape(row["label"])}</span><strong>{escape(row["date"])}</strong><small>{row["detail_html"]}</small></div>' for i, row in enumerate(reader['dates'], 1))
        previous = item['neighbors'][0]
        fields['related_link'] = f'<a href="./source-{previous}.html">{escape(reader["related_label"])}</a>' if previous else ''
        fields.update(original=original, reading=reading, note=escape(item['note']), author=escape(item['author']),
                      authority_id=item['authority_id'], facsimile=item['facsimile'],
                      facsimile_path=item.get('facsimile_path', './assets/great-auk-facsimiles/' + item['facsimile']),
                      primary_url=escape(item['primary'][1], quote=True), companion_url=escape(item['companion'][1], quote=True),
                      companion_label=escape(reader.get('companion_label', item['companion'][0])))
        scans = item.get('scans', [])
        fields['scan_choices'] = '<nav class="scan-choices" aria-label="Scanned pages">' + ''.join(
            f'<button type="button" data-scan-src="{escape(scan["src"], quote=True)}" data-scan-caption="{escape(scan["caption"], quote=True)}" data-scan-url="{escape(scan["url"], quote=True)}" aria-pressed="{str(i == 0).lower()}">{escape(scan["label"])}</button>'
            for i, scan in enumerate(scans)) + '</nav>' if len(scans) > 1 else ''
        fields.setdefault('text_label', 'Original text')
        fields['original_language'] = escape(item.get('language', 'en'), quote=True)
        fields['translation'] = ''
        if item.get('translation'):
            fields['translation'] = '<div class="section-label"><h2>English</h2></div><div class="source-text" lang="en">' + ''.join('<p>' + escape(p) + '</p>' for p in item['translation']) + '</div><p class="translation-credit">' + item['translation_credit_html'] + '</p>'
        fields['primary_label'] = escape(item['primary'][0])
        fields['note_nav'] = '<a href="#notes">Note</a>' if phrase else ''
        fields['notes_block'] = f'<aside id="notes" class="source-footnotes" aria-labelledby="notes-title"><h2 id="notes-title">Note</h2><ol><li id="fn-1"><span class="footnote-number">01</span><p>{escape(item.get("note", ""))} <a class="footnote-back" href="#fnref-1" aria-label="Back to note reference">↩</a></p></li></ol></aside>' if phrase else ''
        fields.update(summary=escape(item['summary'], quote=True), species_name=escape(species['name']),
                      species_page=species['page'] or species.get('notes_page'), species_key=species['ui_key'])
        fields['further_reading'] = f'<section class="further-reading" aria-labelledby="further-title"><h2 id="further-title">Further reading</h2><ol class="further-list">{reading}</ol></section>' if reading else ''
        return template.substitute(fields)
    neighbors = ' · '.join(f'<a href="./source-{slug}.html">{escape(sources[slug]["author"])} ↗</a>' for slug in item['neighbors'] if slug)
    if item['facsimile']:
        facsimile = f'''<figure class="auk-facsimile"><a href="{escape(item['primary'][1], quote=True)}" target="_blank" rel="noopener noreferrer"><img src="./assets/great-auk-facsimiles/{item['facsimile']}" alt="{escape(item['facsimile_alt'], quote=True)}" loading="lazy" /></a><figcaption>{escape(item['facsimile_caption'])}</figcaption></figure>'''
    else:
        facsimile = f'''<div class="facsimile-link"><span class="folio-label">Digitized edition</span><p><a href="{escape(item['primary'][1], quote=True)}" target="_blank" rel="noopener noreferrer">Open the historical text ↗</a></p><p>{escape(item['edition'])}</p></div>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="theme-color" content="#f5f2e9" /><meta name="description" content="{escape(item['summary'], quote=True)}" /><title>{escape(item['author'])} — Great auk — Atlas of Historically Lost Species</title><link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" /><link rel="preload" href="./assets/gfs-didot.ttf" as="font" type="font/ttf" crossorigin /><link rel="stylesheet" href="./styles.css?v=footer-3" /><link rel="stylesheet" href="./detail.css" /><link rel="stylesheet" href="./great-auk.css?v=2" /><script type="module" src="./main.js?v=footer-3"></script><link rel="stylesheet" href="./ui.css?v=2" /></head>
<body data-page="source" data-species="auk" class="auk-source"><a class="skip-link" href="#main">Skip to content</a><div class="site-seal" aria-hidden="true"><span class="seal-symbol"></span></div><div class="page-shell"><header class="masthead"><a class="wordmark" href="./index.html" aria-label="Atlas of Historically Lost Species, home"><span class="wordmark-short" aria-hidden="true">AHLo<span class="wordmark-accent">S</span></span><span class="wordmark-long" aria-hidden="true">Atlas of Historically Lost Species</span></a><nav aria-label="Main navigation"><a href="./index.html#index">Index</a><a href="./authorities.html">Authorities</a><a href="./about.html">About</a></nav></header><main id="main">
<nav class="source-breadcrumb" aria-label="Breadcrumb"><a href="./great-auk.html#record">Great auk</a> / Primary source / {escape(item['author'])}</nav>
<header class="source-head"><div><span class="folio-label">Primary source · {escape(item['period'])}</span><div class="source-author-title"><a class="source-author-avatar" href="./authorities.html#{item['authority_id']}" aria-label="{escape(item['author'])} in the authorities index"><img src="./assets/authorities/{item['authority_id']}.webp" width="84" height="84" alt="" /></a><h1><a href="./authorities.html#{item['authority_id']}">{escape(item['author'])}</a></h1></div><p class="source-deck"><i>{escape(item['work'])}</i>. {escape(item['summary'])}</p></div><div class="source-head-meta"><dl><div><dt>Passage shown</dt><dd>{escape(item['work'])}</dd></div><div><dt>Original language</dt><dd>English</dd></div><div><dt>Place in record</dt><dd><a href="./index.html?place={item['place_key']}#index">{escape(item['place'])} ↗</a></dd></div></dl></div></header>
<div class="source-grid" aria-label="Historical text and digitized source"><section class="source-column" aria-labelledby="original-title"><div class="source-column-head"><h2 id="original-title">Original text</h2><span>Transcription</span></div><div class="source-text" lang="en">{original}</div></section><section class="source-column" aria-labelledby="facsimile-title"><div class="source-column-head"><h2 id="facsimile-title">Digitized edition</h2><span>{escape(item['period'])}</span></div>{facsimile}<div class="auk-edition"><h3>Edition</h3><p>{escape(item['edition'])}</p></div></section></div>
<div class="source-editions" aria-label="Digitized originals"><span>Open the source</span>{link(item['primary'][1], item['primary'][0])}{link(item['companion'][1], item['companion'][0])}</div>
<section class="further-reading" aria-labelledby="further-title"><h2 id="further-title">Further reading</h2><ol class="further-list">{reading}</ol></section>
<aside class="source-footnotes" aria-labelledby="notes-title"><h2 id="notes-title">Note</h2><ol><li id="fn-1"><span class="footnote-number">01</span><p>{escape(item['note'])} <a class="footnote-back" href="#fnref-1" aria-label="Back to note reference">↩</a></p></li></ol></aside>
</main><footer class="site-footer"><span>Atlas of Historically Lost Species</span><span><a href="./great-auk.html#sources">Great auk source index ↗</a>{' · ' + neighbors if neighbors else ''}</span></footer></div></body></html>
'''


if __name__ == '__main__':
    for slug, item in SOURCES.items():
        (ROOT / f'source-{slug}.html').write_text(render(slug, item), encoding='utf-8')
