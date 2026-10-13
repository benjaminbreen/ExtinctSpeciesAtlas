"""Build public research notes from selected, edited atlas passages."""
from html import escape
from string import Template
from atlas_data import ROOT, read


def source_card(record):
    c = record['content']
    pid = record['id']
    scans = c['scans']
    first = scans[0]
    reader = c.get('reader', {})
    title = c.get('work', reader.get('article_title', ''))
    paras = c.get('paragraphs', c.get('original', []))
    original = ''.join(f'<p>{escape(p)}</p>' for p in paras)
    translation = c.get('translation', c.get('english', []))
    translated = ''
    if translation:
        translated = '<h3>English</h3><div class="notes-text" lang="en">' + ''.join(f'<p>{escape(p)}</p>' for p in translation) + '</div><p class="translation-credit">' + c.get('translation_credit_html', 'Translation attribution: see source record.') + '</p>'
    buttons = ''.join(f'<button type="button" data-scan-src="{escape(s["src"], quote=True)}" data-scan-caption="{escape(s["caption"], quote=True)}" data-scan-url="{escape(s["url"], quote=True)}" aria-pressed="{str(i == 0).lower()}">{escape(s["label"])}</button>' for i, s in enumerate(scans))
    scan_choices = f'<nav class="notes-scan-choices" aria-label="Scanned pages">{buttons}</nav>' if len(scans) > 1 else ''
    citation = reader.get('citation_html', escape(c.get('edition', '')))
    return f'''<section class="notes-source" id="{pid}" aria-labelledby="{pid}-title">
      <header class="notes-source-head"><div><a class="notes-author" href="./authorities.html#{record['authority_id']}">{escape(c['author'])}</a><h2 id="{pid}-title"><cite>{escape(title)}</cite></h2><p class="notes-reference">{escape(c['period'])} · {escape(reader.get('passage_label', first['label']))}</p></div><a class="notes-record-link" href="./{record['page']}">Source record ↗</a></header>
      <div class="notes-source-grid"><div class="notes-passage"><h3>Original text</h3><div class="notes-text" lang="{escape(c.get('language', 'en'), quote=True)}">{original}</div>{translated}</div>
      <aside class="notes-scan"><div class="notes-scan-head"><h3>Digitized edition</h3><button type="button" class="notes-enlarge">Enlarge ↗</button></div>{scan_choices}<figure><button type="button" class="notes-image" aria-label="Enlarge scan of {escape(title, quote=True)}"><img src="{first['src']}" alt="{escape(first['caption'], quote=True)}" loading="lazy" /></button><figcaption aria-live="polite">{escape(first['caption'])}</figcaption></figure><a class="notes-edition" href="{escape(first['url'], quote=True)}" target="_blank" rel="noopener noreferrer">Open edition ↗</a></aside></div>
      <div class="notes-citation"><p class="citation-text">{citation}</p><div><a href="#{pid}" aria-label="Permanent link to {escape(c['author'], quote=True)} passage">Link to passage</a><button type="button" class="notes-copy">Copy citation</button><span class="notes-copy-status" role="status"></span></div></div>
    </section>'''


def outputs():
    species = {s['id']: s for s in read('species')}
    passages = {p['id']: p for p in read('passages')}
    groups = read('research-notes')
    template = Template((ROOT / 'templates/research-notes.html').read_text())
    result, rows = {}, []
    for group in groups:
        s = species[group['species_id']]
        articles, nav = [], []
        for n, note in enumerate(group['notes'], 1):
            records = [passages[pid] for pid in note['passage_ids']]
            label = records[0]['content']['author']
            if len(records) > 1:
                label = records[0]['content']['work']
            nav.append(f'<a href="#{note["id"]}"><span>{n:02d}</span>{escape(label)}</a>')
            articles.append(f'<article class="research-note" id="{note["id"]}" aria-label="{escape(label, quote=True)}"><p class="notes-context">{escape(note["context"])}</p>' + ''.join(source_card(r) for r in records) + '</article>')
        back = f'<a href="./{s["page"]}">{escape(s["name"])} ↗</a>' if s['page'] else f'<a href="./index.html#species-{s["ui_key"]}">Species index ↗</a>'
        result[group['page']] = template.substitute(species_name=escape(s['name']),species_key=s['ui_key'],subtitle=s['subtitle_html'],back_link=back,note_nav=''.join(nav),notes=''.join(articles))
        count = sum(len(note['passage_ids']) for note in group['notes'])
        dates = [passages[pid]['content']['period'] for note in group['notes'] for pid in note['passage_ids']]
        rows.append(f'<li><a href="./{group["page"]}"><div><h2>{escape(s["name"])}</h2><p>{s["subtitle_html"]}</p></div><span>{count} sources · {escape(dates[0])}–{escape(dates[-1])}</span><span aria-hidden="true">↗</span></a></li>')
    index = Template((ROOT / 'templates/research-notes-index.html').read_text())
    result['research-notes.html'] = index.substitute(entries=''.join(rows))
    return result
