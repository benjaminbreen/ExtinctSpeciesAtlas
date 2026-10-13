"""Build or check committed static pages: python3 scripts/build_site.py [--check]."""
import argparse
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from urllib.parse import unquote, urlsplit

from atlas_data import ROOT, read, validate, source_contents, bibliography
import build_sources
import build_auk_sources
import build_authorities
import build_research_notes


def catalog_row(record):
    c = record['catalog']
    href = escape(c['href'], quote=True)
    external = ' target="_blank" rel="noopener noreferrer"' if urlsplit(c['href']).scheme else ''
    aria = f' aria-label="{escape(c["aria_label"], quote=True)}"' if c['aria_label'] else ''
    year = format(c['sort_year'], 'g')
    return f'''<li id="{escape(c['anchor'])}" data-authority="{escape(record['authority_id'])}" data-year="{year}" data-author="{escape(c['sort_author'])}"><span class="catalog-date">{c['date_label']}</span><div class="catalog-main"><h3>{c['heading_html']}</h3><p>{c['summary_html']}</p></div><span class="catalog-kind">{escape(c['kind'])}</span><a href="{href}"{external}{aria}>{escape(c['link_label'])}</a></li>'''


def species_entry(item, passages):
    key = item['ui_key']
    target = item['page'] or item.get('notes_page')
    tag = 'a' if target else 'article'
    label = item['aria_label'] or item['name'] + ', research notes'
    destination = f' href="./{target}" aria-label="{escape(label, quote=True)}"' if target else f' aria-labelledby="{key}-title"'
    title_id = '' if target else f' id="{key}-title"'
    status = item['status_label']
    if target and not item['page']:
        status = 'Research notes'
    if item['status_mode'] == 'source_count':
        records = [r for r in passages if item['id'] in r['species_ids'] and r['page']]
        # Count only the named places attached to detailed records, not region tags.
        places = {r['content']['place_key'] for r in records if r['content'].get('place_key')}
        source_label = 'source' if len(records) == 1 else 'sources'
        place_label = 'place' if len(places) == 1 else 'places'
        status = f'{len(records)} {source_label} · {len(places)} {place_label}'
    arrow = ' <span aria-hidden="true">↗</span>' if target else ''
    return f'''<{tag} class="species-entry observe-species" id="species-{key}" data-species="{key}" data-tags="{' '.join(item['tags'])}" data-places="{' '.join(item['places'])}"{destination}>
            <span class="entry-number">{item['number']}</span>
            <span class="entry-icon {item['icon_class']}" aria-hidden="true"></span>
            <span class="entry-main"><strong{title_id}>{escape(item['name'])}</strong><small>{item['subtitle_html']}</small></span>
            <span class="entry-place">{escape(item['place_label'])}</span>
            <span class="entry-status">{escape(status)}{arrow}</span>
          </{tag}>'''


def outputs():
    validate()
    passages = read('passages')
    result = {}
    for s in read('species'):
        if not s['page']:
            continue
        records = [r for r in passages if s['id'] in r['species_ids']]
        template = Template((ROOT / 'templates' / s['page']).read_text(encoding='utf-8'))
        notes_link = f'<a class="notes-link" href="./{s["notes_page"]}">Research notes ↗</a>' if s.get('notes_page') else ''
        result[s['page']] = template.substitute(source_index='\n          '.join(map(catalog_row, records)), source_count=f'{len(records):02d}', research_notes_link=notes_link)
    template = Template((ROOT / 'templates/index.html').read_text(encoding='utf-8'))
    result['index.html'] = template.substitute(species_index='\n          '.join(species_entry(s, passages) for s in read('species')))
    for record in passages:
        if record['content'] is None:
            continue
        sid = record['species_ids'][0]
        sources = source_contents(sid)
        item = sources[record['id']]
        if record['format'] == 'bilingual':
            if sid != 'silphium':
                raise ValueError('A new bilingual dossier needs its language-specific renderer registered.')
            result[record['page']] = build_sources.page(record['id'], item)
        else:
            if sid != 'great-auk' and not item.get('reader'):
                raise ValueError(f"{record['id']}: new English dossiers must supply reader metadata")
            result[record['page']] = build_auk_sources.render(record['id'], item, sources, bibliography(sid))
    result['authorities.html'] = build_authorities.build(write=False)
    result.update(build_research_notes.outputs())
    check_links(result)
    return result


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids, self.links = set(), []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                raise ValueError(f'Duplicate HTML id: {a["id"]}')
            self.ids.add(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.links.append(a[key])


def check_links(generated):
    # Include authored pages as link targets. External URLs are not fetched.
    pages = {p.name: p.read_text(encoding='utf-8') for p in ROOT.glob('*.html')}
    pages.update(generated)
    parsed = {name: Links(html) for name, html in pages.items()}
    for name in generated:
        for href in parsed[name].links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path).removeprefix('./') or name
            if not (ROOT / path).is_file() and path not in generated:
                raise ValueError(f'{name}: missing local target {href}')
            if url.fragment and path in parsed and unquote(url.fragment) not in parsed[path].ids:
                raise ValueError(f'{name}: missing anchor {href}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate data and fail if committed HTML is stale; write nothing.')
    args = parser.parse_args()
    result = outputs()
    stale = [name for name, html in result.items() if not (ROOT / name).exists() or (ROOT / name).read_text(encoding='utf-8') != html]
    if args.check:
        if stale:
            parser.exit(1, 'Stale pages: ' + ', '.join(stale) + '\nRun python3 scripts/build_site.py\n')
        print(f'{len(result)} pages up to date; records, local links, assets, and anchors valid.')
    else:
        for name in stale:
            (ROOT / name).write_text(result[name], encoding='utf-8')
        print(f'Built {len(result)} pages ({len(stale)} changed).')


if __name__ == '__main__':
    main()
