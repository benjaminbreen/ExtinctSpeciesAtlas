"""Shared edited atlas records. No research-pilot data is published implicitly."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def read(name, root=ROOT):
    return json.loads((root / 'data' / f'{name}.json').read_text(encoding='utf-8'))

def source_contents(species_id):
    return {r['id']: dict(r['content'], authority_id=r['authority_id'], species_id=r['species_ids'][0])
            for r in read('passages') if species_id in r['species_ids'] and r['content'] is not None}

def bibliography(species_id):
    return read('bibliography')[species_id]

def authorities():
    passages = read('passages')
    return [dict(a, works=[r['authority_work'] for r in passages if r['authority_id'] == a['slug']])
            for a in read('authorities')]

def validate(species=None, passages=None, authors=None, books=None, notes=None):
    species = read('species') if species is None else species
    passages = read('passages') if passages is None else passages
    authors = read('authorities') if authors is None else authors
    books = read('bibliography') if books is None else books
    notes = read('research-notes') if notes is None else notes
    def unique(rows, key, label):
        values = [r[key] for r in rows]
        if len(values) != len(set(values)):
            raise ValueError(f'Duplicate {label}')
        return set(values)
    species_ids = unique(species, 'id', 'species ID')
    unique(species, 'ui_key', 'species UI key')
    passage_ids = unique(passages, 'id', 'passage ID')
    authority_ids = unique(authors, 'slug', 'authority ID')
    pages, anchors = set(), set()
    for r in passages:
        label = r['id']
        if not r['species_ids'] or not set(r['species_ids']) <= species_ids:
            raise ValueError(f'{label}: unknown or missing species')
        if r['authority_id'] not in authority_ids:
            raise ValueError(f'{label}: unknown authority')
        c = r['catalog']
        if not isinstance(c['sort_year'], (int, float)):
            raise ValueError(f'{label}: sort_year must be numeric')
        for sid in r['species_ids']:
            anchor = (sid, c['anchor'])
            if anchor in anchors:
                raise ValueError(f'{label}: duplicate catalog anchor')
            anchors.add(anchor)
        if urlsplit(c['href']).scheme not in ('', 'http', 'https'):
            raise ValueError(f'{label}: invalid catalog URL')
        for relation in r['research']['relationships']:
            if relation['passage_id'] not in passage_ids or relation['passage_id'] == label:
                raise ValueError(f'{label}: invalid related passage')
            if relation['type'] not in ('translation_of', 'quotes', 'copies', 'discusses'):
                raise ValueError(f'{label}: unknown relationship type')
        content = r['content']
        if content is None:
            if r['page'] is not None or r['format'] is not None:
                raise ValueError(f'{label}: indexed-only record cannot have a source page')
            continue
        if r['format'] not in ('bilingual', 'english', 'reader'):
            raise ValueError(f'{label}: unknown source format')
        if r['page'] != f'source-{label}.html' or r['page'] in pages:
            raise ValueError(f'{label}: invalid or duplicate source page')
        pages.add(r['page'])
        if c['href'] != './' + r['page'] or r['authority_work']['href'] != c['href']:
            raise ValueError(f'{label}: catalog/authority links disagree with source page')
        for sid in r['species_ids']:
            if any(ref not in books.get(sid, {}) for ref in content['reading']):
                raise ValueError(f'{label}: unknown bibliography reference')
        for neighbor in content['neighbors']:
            if neighbor is not None:
                other = next((p for p in passages if p['id'] == neighbor), None)
                if other is None or other['content'] is None or not set(other['species_ids']) & set(r['species_ids']):
                    raise ValueError(f'{label}: invalid source neighbor')
        if r['format'] == 'reader' and not content.get('reader'):
            raise ValueError(f'{label}: reader metadata required')
        if content.get('translation') and not content.get('translation_credit_html'):
            raise ValueError(f'{label}: translation credit required')
        scans = content.get('scans', [])
        for scan in scans:
            if not scan.get('label') or not scan.get('caption') or not scan.get('url'):
                raise ValueError(f'{label}: incomplete scan metadata')
            if not (ROOT / scan['src'].removeprefix('./')).is_file():
                raise ValueError(f'{label}: missing scan image')
        if scans and content.get('facsimile_path') != scans[0]['src']:
            raise ValueError(f'{label}: initial scan does not match scan list')
        if r['format'] == 'bilingual':
            if not content['original'] or not content['english']:
                raise ValueError(f'{label}: missing original or translation')
            if len(content['notes']) != len(content['note_targets']):
                raise ValueError(f'{label}: note/anchor count mismatch')
            for index, phrase in content['note_targets']:
                if index < 0 or index >= len(content['english']) or phrase not in content['english'][index]:
                    raise ValueError(f'{label}: note target missing')
        elif content.get('note_phrase') and not any(content['note_phrase'] in p for p in content['paragraphs']):
            raise ValueError(f'{label}: note target missing')
    unique(notes, 'species_id', 'research-notes species')
    note_pages = unique(notes, 'page', 'research-notes page')
    records = {r['id']: r for r in passages}
    for group in notes:
        sid = group['species_id']
        entry = next((s for s in species if s['id'] == sid), None)
        if entry is None or entry.get('notes_page') != group['page']:
            raise ValueError(f'{sid}: research-notes destination disagrees with species')
        if group['page'] != f'research-notes-{sid}.html' or group['page'] in pages:
            raise ValueError(f'{sid}: invalid research-notes page')
        unique(group['notes'], 'id', 'research-note anchor')
        if not group['notes']:
            raise ValueError(f'{sid}: empty research-notes page')
        used = set()
        for note in group['notes']:
            if not note.get('context') or not note.get('passage_ids'):
                raise ValueError(f'{sid}: incomplete research note')
            for pid in note['passage_ids']:
                record = records.get(pid)
                if record is None or sid not in record['species_ids']:
                    raise ValueError(f'{sid}: unknown or cross-species note passage')
                if pid in used:
                    raise ValueError(f'{sid}: repeated note passage')
                used.add(pid)
                if not record['content'] or not record['content'].get('scans') or not record['research'].get('reviewed_on'):
                    raise ValueError(f'{pid}: research notes require a reviewed passage and scans')
    for entry in species:
        if entry.get('notes_page') and entry['notes_page'] not in note_pages:
            raise ValueError(f'{entry["id"]}: missing research-notes page')
    return True
