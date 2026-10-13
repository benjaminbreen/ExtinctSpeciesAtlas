#!/usr/bin/env python3
"""Reproducible, standard-library-only acquisition and OCR search for the pilot."""
import argparse
import concurrent.futures
import csv
import datetime as dt
import gzip
import hashlib
import json
import re
import sqlite3
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / 'data/curated'
RAW = ROOT / 'data/raw'
DERIVED = ROOT / 'data/derived'
RESULTS = ROOT / 'results'
CATALOG = 'https://bhl-open-data.s3.amazonaws.com/data/'

def read(path):
    return json.loads(path.read_text())

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def download(url, path, max_bytes=100_000_000):
    """Atomic cached download. Headers/URL/time/checksum stay beside each asset."""
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path = path.with_name(path.name + '.receipt.json')
    if path.exists() and receipt_path.exists():
        receipt = read(receipt_path)
        if receipt['requested_url'] == url and digest(path) == receipt['sha256']:
            return receipt
        raise ValueError(f'Cached file differs from receipt: {path}')
    temp = path.with_name(path.name + '.part')
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'ExtinctSpeciesAtlas-research-pilot/0.1 (public historical research)'})
            with urllib.request.urlopen(request, timeout=90) as response, temp.open('wb') as out:
                size = 0
                for block in iter(lambda: response.read(1024 * 1024), b''):
                    size += len(block)
                    if size > max_bytes:
                        raise ValueError(f'Download exceeds {max_bytes} bytes: {url}')
                    out.write(block)
                receipt = dict(requested_url=url, resolved_url=response.geturl(), retrieved_at=stamp(),
                               content_type=response.headers.get('Content-Type'), etag=response.headers.get('ETag'),
                               last_modified=response.headers.get('Last-Modified'), bytes=size,
                               local_path=str(path.relative_to(ROOT)), sha256=digest(temp))
            temp.replace(path)
            write(receipt_path, receipt)
            return receipt
        except Exception:
            temp.unlink(missing_ok=True)
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def catalog():
    receipts = []
    for name in ['title', 'item']:
        path = RAW / 'bhl' / (name + '.txt.gz')
        # Files bootstrapped by curl are re-downloaded once to establish receipts.
        receipts.append(download(CATALOG + path.name, path))
    write(RESULTS / 'catalog_downloads.json', receipts)
    resolve()

def table(name):
    with gzip.open(RAW / 'bhl' / (name + '.txt.gz'), 'rt', encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f, delimiter='\t')

def resolve():
    titles = {r['TitleID']: r for r in table('title')}
    selected = read(CURATED / 'sources.json')
    wanted = {r['bhl_item_id'] for r in selected if r['bhl_item_id']}
    items = {}
    regional = []
    # Discovery shelf is title-only retrieval, not an exhaustive regional bibliography.
    rx = re.compile(r'cuba|west indies|mauriti|rodrigu|rodriguez|leguat|cap de bonne|cape of good hope|caput bonae|extinct birds', re.I)
    count = 0
    for item in table('item'):
        count += 1
        if item['ItemID'] in wanted:
            items[item['ItemID']] = item
        title = titles.get(item['TitleID'], {})
        if rx.search(title.get('FullTitle', '')):
            regional.append(dict(item=item, title=title, selection_status='title_keyword_match_not_reviewed'))
    resolved = []
    for source in selected:
        s = dict(source)
        if s['bhl_item_id']:
            item = items[s['bhl_item_id']]
            s.update(bhl_item=item, bhl_title=titles.get(item['TitleID'], {}), ia_identifier=item['BarCode'])
        resolved.append(s)
    write(DERIVED / 'sources_resolved.json', resolved)
    write(DERIVED / 'regional_catalog_candidates.json', regional)
    write(RESULTS / 'catalog_summary.json', dict(title_count=len(titles), item_count=count, regional_title_keyword_item_count=len(regional), selected_sources=len(resolved), generated_at=stamp()))
    print(f'Catalog: {len(titles):,} titles, {count:,} items; {len(regional):,} regional candidate items.', flush=True)

def file_by_suffix(files, suffix):
    found = [f for f in files if f['name'].endswith(suffix)]
    if not found:
        raise ValueError(f'Missing {suffix}')
    return sorted(found, key=lambda f: f['name'])[0]

def acquire_one(source):
    sid = source['source_id']
    identifier = source['ia_identifier']
    folder = RAW / 'internet-archive' / sid
    receipts = []
    result = dict(source_id=sid, ia_identifier=identifier, status='failed', receipts=receipts)
    try:
        receipts.append(download('https://archive.org/metadata/' + urllib.parse.quote(identifier, safe=''), folder / 'metadata.json'))
        metadata = read(folder / 'metadata.json')
        if not metadata.get('files'):
            raise ValueError('No public file manifest')
        result['catalog_metadata'] = metadata.get('metadata', {})
        for suffix, local in [('_djvu.xml','ocr.xml'), ('scandata.xml','scandata.xml')]:
            entry = file_by_suffix(metadata['files'], suffix)
            url = 'https://archive.org/download/' + urllib.parse.quote(identifier, safe='') + '/' + urllib.parse.quote(entry['name'], safe='')
            receipt = download(url, folder / local)
            if entry.get('size') and int(entry['size']) != receipt['bytes']:
                raise ValueError(f'File-size mismatch for {entry["name"]}')
            receipts.append(receipt)
        result['status'] = 'downloaded'
    except Exception as exc:
        result['error'] = str(exc)
    print(f'{sid}: {result["status"]}' + (': '+result['error'] if 'error' in result else ''), flush=True)
    return result

def acquire():
    sources = read(DERIVED / 'sources_resolved.json')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(acquire_one, sources))
    write(RESULTS / 'acquisition_manifest.json', records)
    # Review is a local baseline, not redistributed with the public website.
    try:
        receipt = download('https://boc-online.org/bulletins/downloads/BBOC1332-PDFa.pdf', RAW / 'scholarship' / 'BBOC1332-PDFa.pdf')
        write(RESULTS / 'scholarship_downloads.json', [receipt])
    except Exception as exc:
        write(RESULTS / 'scholarship_downloads.json', [dict(status='failed', error=str(exc))])
    print(f'Downloaded {sum(x["status"]=="downloaded" for x in records)}/{len(records)} source volumes.', flush=True)

def normalize(text):
    text = re.sub(r'(?<=\w)[-‐]\s*\n\s*(?=\w)', '', text)
    text = text.replace('ſ', 's')
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold()) if not unicodedata.combining(c))

def extract():
    DERIVED.mkdir(parents=True, exist_ok=True)
    manifest = read(RESULTS / 'acquisition_manifest.json')
    summaries = []
    output = DERIVED / 'pages.jsonl'
    temp = output.with_suffix('.jsonl.part')
    with temp.open('w') as out:
        for record in manifest:
            if record['status'] != 'downloaded':
                continue
            sid, identifier = record['source_id'], record['ia_identifier']
            folder = RAW / 'internet-archive' / sid
            scandata = ET.parse(folder / 'scandata.xml')
            all_scans = scandata.findall('.//pageData/page')
            accessible = [s for s in all_scans if s.findtext('addToAccessFormats', 'true').strip().lower() != 'false']
            # Count before assigning links. Never silently equate OCR sequence with leaf number.
            object_count = sum(1 for _, element in ET.iterparse(folder / 'ocr.xml', events=('end',)) if element.tag == 'OBJECT')
            if len(accessible) == object_count:
                scans, mapping = accessible, 'scandata_accessible_count_match'
            elif len(all_scans) == object_count:
                scans, mapping = all_scans, 'scandata_all_count_match'
            else:
                scans, mapping = [], 'unresolved_no_page_deeplinks'
            count, chars, empty = 0, 0, 0
            for _, element in ET.iterparse(folder / 'ocr.xml', events=('end',)):
                if element.tag != 'OBJECT':
                    continue
                text = '\n'.join(' '.join(''.join(w.itertext()) for w in line.findall('.//WORD')) for line in element.findall('.//LINE'))
                scan = scans[count] if scans else None
                leaf = scan.get('leafNum') if scan is not None else None
                page = dict(page_id=f'{sid}:{count:05d}', source_id=sid, ia_identifier=identifier, ocr_sequence=count,
                            scan_leaf=int(leaf) if leaf is not None else None,
                            printed_page=scan.findtext('pageNumber') if scan is not None else None,
                            scan_url=f'https://archive.org/details/{identifier}/page/n{leaf}/mode/1up' if leaf is not None else f'https://archive.org/details/{identifier}',
                            page_mapping=mapping, text=text, text_status='unreviewed_machine_ocr')
                out.write(json.dumps(page, ensure_ascii=False) + '\n')
                count += 1
                chars += len(text)
                empty += not text.strip()
                element.clear()
            summaries.append(dict(source_id=sid, pages=count, characters=chars, empty_ocr_pages=empty, page_mapping=mapping,
                                  caveat='Page mapping is structural and has not been visually checked page by page.'))
    temp.replace(output)
    write(RESULTS / 'corpus_summary.json', dict(generated_at=stamp(), source_count=len(summaries), page_count=sum(x['pages'] for x in summaries), sources=summaries, pages_sha256=digest(output)))
    print(f'Extracted {sum(x["pages"] for x in summaries):,} pages from {len(summaries)} volumes.', flush=True)

def pages():
    with (DERIVED / 'pages.jsonl').open() as f:
        for line in f:
            yield json.loads(line)

def index():
    destination = DERIVED / 'search.sqlite'
    temp = destination.with_suffix('.sqlite.part')
    temp.unlink(missing_ok=True)
    with sqlite3.connect(temp) as db:
        db.execute('CREATE TABLE pages(page_id TEXT PRIMARY KEY, source_id TEXT, scan_url TEXT, printed_page TEXT, text TEXT)')
        db.execute("CREATE VIRTUAL TABLE fulltext USING fts5(page_id UNINDEXED, source_id UNINDEXED, search_text, tokenize='unicode61 remove_diacritics 2')")
        for p in pages():
            db.execute('INSERT INTO pages VALUES(?,?,?,?,?)',(p['page_id'],p['source_id'],p['scan_url'],p['printed_page'],p['text']))
            db.execute('INSERT INTO fulltext VALUES(?,?,?)',(p['page_id'],p['source_id'],normalize(p['text'])))
    temp.replace(destination)
    print('Built local full-text index.', flush=True)

def search(query, limit):
    db = sqlite3.connect(f'file:{DERIVED / "search.sqlite"}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    # FTS handles case/diacritics itself. Case-folding here would turn OR/AND/NOT
    # into ordinary search tokens and silently change the meaning of a query.
    results = [dict(r) for r in db.execute("SELECT p.page_id,p.source_id,p.scan_url,p.printed_page,snippet(fulltext,2,'[',']',' … ',35) AS normalized_ocr_excerpt FROM fulltext JOIN pages p ON p.page_id=fulltext.page_id WHERE fulltext MATCH ? ORDER BY rank LIMIT ?",(query,limit))]
    db.close()
    print(json.dumps(dict(query=query,status='retrieval_candidates_not_verified_observations',results=results),ensure_ascii=False,indent=2))

def sweep():
    aliases = read(CURATED / 'aliases.json')
    compiled = [(a, re.compile(r'(?<!\w)' + re.escape(normalize(a['term'])).replace(r'\ ',r'\s+') + r'(?!\w)')) for a in aliases]
    counts = {}
    destination = RESULTS / 'mention_candidates.jsonl'
    with destination.open('w') as out:
        for p in pages():
            normalized = normalize(p['text'])
            hits = [a for a,rx in compiled if rx.search(normalized)]
            if not hits:
                continue
            for hit in hits:
                counts[hit['alias_id']] = counts.get(hit['alias_id'],0)+1
            out.write(json.dumps(dict(page_id=p['page_id'],source_id=p['source_id'],scan_url=p['scan_url'],matched_alias_ids=[a['alias_id'] for a in hits],candidate_taxon_ids=sorted({t for a in hits for t in a['taxon_ids']}),review_status='unreviewed',novelty_status='not_assessed',warning='Name matches are not species identifications or independent observations.'),ensure_ascii=False)+'\n')
    write(RESULTS / 'mention_summary.json',dict(candidate_pages=sum(1 for _ in destination.open()),counts_by_alias=counts,method='Unicode normalization, long-s normalization, line-end hyphen repair, whole-term matching. No fuzzy or semantic retrieval yet.',status='retrieval_only'))
    print(f'Wrote {sum(1 for _ in destination.open()):,} candidate pages for review.',flush=True)

def validate():
    taxa = read(CURATED / 'taxa.json')
    ids = {t['taxon_id'] for t in taxa}
    aliases = read(CURATED / 'aliases.json')
    for alias in aliases:
        assert set(alias['taxon_ids']) <= ids
        assert alias['attestation_status'] == 'query_hypothesis' or alias.get('source')
    seen = set()
    for p in pages():
        assert p['page_id'] not in seen
        seen.add(p['page_id'])
        assert p['text_status'] == 'unreviewed_machine_ocr'
        if p['scan_leaf'] is None:
            assert '/page/n' not in p['scan_url']
    summary = read(RESULTS / 'corpus_summary.json')
    assert len(seen) == summary['page_count']
    assert digest(DERIVED/'pages.jsonl') == summary['pages_sha256']
    receipts = []
    for path in RAW.rglob('*.receipt.json'):
        r = read(path)
        assert digest(ROOT/r['local_path']) == r['sha256'], r['local_path']
        receipts.append(r)
    with sqlite3.connect(f'file:{DERIVED / "search.sqlite"}?mode=ro',uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert db.execute('SELECT COUNT(*) FROM pages').fetchone()[0] == len(seen)
        assert db.execute('SELECT COUNT(*) FROM fulltext').fetchone()[0] == len(seen)
    write(RESULTS/'validation.json',dict(status='passed',checked_at=stamp(),pages=len(seen),asset_hashes_verified=len(receipts),checks=['unique page IDs','taxon references','alias provenance labels','page mapping fallback','asset and corpus hashes','SQLite integrity and row counts'],limits='Does not validate historical claims, OCR accuracy, species identity, or novelty.'))
    print(f'Validation passed: {len(seen):,} pages, {len(receipts)} asset hashes.',flush=True)

def snapshot():
    """Keep small provenance manifests in Git while bulky downloaded data stays local."""
    assets = [read(p) for p in sorted(RAW.rglob('*.receipt.json'))]
    write(ROOT/'manifests/assets.json',assets)
    for name in ['catalog_summary','corpus_summary','validation','mention_summary']:
        write(ROOT/'manifests'/f'{name}.json',read(RESULTS/f'{name}.json'))
    acquisitions = {x['source_id']:x for x in read(RESULTS/'acquisition_manifest.json')}
    inventory=[]
    for s in read(DERIVED/'sources_resolved.json'):
        a=acquisitions.get(s['source_id'],{})
        m=a.get('catalog_metadata',{})
        inventory.append(dict(source_id=s['source_id'],bhl_item_id=s['bhl_item_id'],ia_identifier=s['ia_identifier'],
                              title=m.get('title'),creator=m.get('creator'),date=m.get('date'),language=m.get('language'),
                              archive_url='https://archive.org/details/'+s['ia_identifier'],
                              bhl_rights=s.get('bhl_item',{}).get('CopyrightStatus'),ia_rights=m.get('rights'),ia_license=m.get('licenseurl'),
                              cluster=s['cluster'],genre=s['genre'],narrative_family=s['narrative_family'],
                              selection_note=s['selection_note'],status=a.get('status','not_acquired'),error=a.get('error')))
    write(ROOT/'manifests/source_inventory.json',inventory)
    print('Saved compact provenance manifests.',flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['catalog','acquire','extract','index','sweep','validate','snapshot','search','all'])
    parser.add_argument('query',nargs='?')
    parser.add_argument('--limit',type=int,default=10)
    args = parser.parse_args()
    if args.command == 'all':
        for fn in [catalog,acquire,extract,index,sweep,validate,snapshot]:fn()
    elif args.command == 'search':
        if not args.query:parser.error('search requires a quoted query')
        search(args.query,args.limit)
    else:globals()[args.command]()

if __name__ == '__main__':
    main()
