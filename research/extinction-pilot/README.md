# Extinction research pilot

This pilot belongs to **ExtinctSpeciesAtlas**. It assembles multilingual historical texts for recovering evidence about extinct species, with Cuban macaw, Mascarene fauna, and bluebuck as the first investigations. Great auk provides existing source records for testing retrieval and dependence between accounts. All twelve atlas cases have seed search terms; silphium remains a separate, unresolved identification problem.

The standalone checkout is `~/Code/ExtinctSpeciesAtlas`. The older checkout inside Historical Mysteries has been left intact. Work in this checkout to avoid diverging copies. Creating this folder does not change the Codex chat's project association; add/open this directory as a project in the app when desired.

## What is here

- **12 atlas cases**, 53 seed terms, 7 place-query groups, and 10 inherited detailed atlas source records.
- **20 downloaded volumes / 7,841 OCR pages**, covering Spanish, French, Dutch, German, Latin, and English.
- **191,690 BHL title records and 324,356 item records**, plus a shelf of 728 regional title matches.
- **318 candidate pages** from the first name sweep; all remain unreviewed.
- Five scholarly baseline entries and a local copy of the 2013 BOC issue containing Wiley and Kirwan's macaw review.

These are source volumes and machine OCR pages, not independent observations. The complete BHL OCR corpus has **not** been downloaded or searched. The BHL title/item catalogs describe holdings; they do not supply the full text of every holding. Source files come from the selected BHL-linked Internet Archive scans plus additional public IA editions.

## Start here

- [Source inventory](manifests/source_inventory.json): exact editions, archive identifiers, language metadata, narrative families, and acquisition state.
- [Species](data/curated/taxa.json), [search vocabulary](data/curated/aliases.json), and [place queries](data/curated/places.json).
- [Known passages to review first](data/curated/retrieval_examples.json): recovered OCR pages from Perpiña, Gundlach, Cory, and Barbour. These are known sources, not discoveries.
- [Scholarly baselines](data/curated/scholarly_baselines.json) and [remaining acquisition leads](data/curated/acquisition_queue.json).
- [Benchmark cases](data/curated/benchmarks.json), [inherited atlas records](data/curated/atlas_source_records.json), and [evidence record template](data/curated/evidence_template.json).
- Local generated data: `data/derived/pages.jsonl`, `data/derived/search.sqlite`, and `results/mention_candidates.jsonl`.
- [Download provenance](manifests/assets.json), [corpus counts](manifests/corpus_summary.json), and [validation](manifests/validation.json).

## Shared harness

The [historical-record harness](harness/README.md) adds structured dodo and bluebuck baselines, GLOBALISE and TANAP adapters, resumable retrieval stages, quotation validation, development controls and persistent review decisions. Its candidates remain internal research material. See its README for current run results and limitations.

## Search locally

Python 3.9+ with SQLite FTS5 is sufficient; there are no pip dependencies or API keys. From the repository root:

```sh
python3 research/extinction-pilot/scripts/pilot.py search '"Ara tricolor" OR guacamayo OR lorirojo'
python3 research/extinction-pilot/scripts/pilot.py search 'tortues AND Rodrigues'
python3 research/extinction-pilot/scripts/pilot.py search '"blue antelope" OR blaauwbok'
```

Queries use SQLite FTS5 syntax; quote phrases, and write boolean operators in uppercase. Search results include scan links and printed page labels where structurally matched. Excerpts are normalized machine OCR, not checked transcriptions. `data/derived/pages.jsonl` retains the unnormalized OCR text. Open the linked scan before quoting.

To reproduce downloads, extraction, index, seed sweep, validation, and compact manifests:

```sh
python3 research/extinction-pilot/scripts/pilot.py all
python3 -m unittest discover -s research/extinction-pilot/tests -v
```

Downloads are cached with SHA-256 receipts and requested/resolved URLs. Network access is needed to rebuild on another machine. Current downloads are approximately 287 MiB; allow additional working space. `all` preserves cached snapshots when their hashes match; it does not silently refresh existing source files. To refresh a particular asset intentionally, move that file and its `.receipt.json` aside before rerunning. Derived index and candidate outputs are regenerated.

## Dataset conventions

Curated JSON is the editable research input. Local file references inside its provenance fields are relative to the repository root. Sources have stable pilot IDs and retain external IA/BHL IDs. Raw catalog metadata is preserved rather than silently corrected. Publication dates and language labels inherited from catalogs still need checks against scans; OCR-derived volume identifications are labeled accordingly.

Aliases distinguish atlas-attested names, names found in modern reviews/catalogs, and unverified query hypotheses. Place forms are search suggestions with no asserted coordinates. A generic reference to Rodrigues tortoises remains a group-level candidate; it does not establish either species. No page automatically becomes an occurrence record.

The initial sweep uses normalized whole-term matching: case/diacritic folding, long-s normalization, and repair of words hyphenated across lines. It has no semantic retrieval, general OCR-error correction, fuzzy matching, or historical name discovery yet. The absence of a hit is not evidence of historical absence. Candidate pages may be indexes, plates, bibliographies, copied accounts, or discussions of other animals.

OCR sequence is mapped to IA scan leaves using scandata and page-count agreement. If the counts do not agree, the code deliberately returns the book link and no precise leaf. Count agreement is structural validation, not a visual check of every page. Empty OCR pages are retained and counted; many are plates or blank leaves.

The current benchmark cases are development cases. They are not a blinded evaluation set. Before evaluating a multilingual discovery method, reserve entire narrative families, not individual translations or pages, to prevent source leakage.

## Immediate research work

1. Check Perpiña's recovered `lorirojo` passage on printed p.247 against the scan and the Wiley–Kirwan review. Inspect the hunting accounts around pp.32–33 and 242–243; citation locators may point to the beginning of a passage rather than the exact sentence. Establish the journey's dates from context.
2. Compare Leguat's French, Dutch, German, and English texts, separating narrative from later editors' notes. Treat them as related witnesses. Extract ecological claims with passage-level dependence, not one dependence label for an entire book.
3. Verify bluebuck search vocabulary against Kolb and other Cape texts before expanding retrieval. Generic color words cannot establish identification.
4. Acquire Gundlach's separate 1893 *Ornitología cubana*, Sonnerat's relevant text volumes, and precisely selected German journal contributions. The acquired Gundlach volume is **1876**. Pallas's acquired *Spicilegia* is **not** his 1766 *Miscellanea*.
5. Review the initial candidate queue and build family-separated evaluation cases. Then expand into the 728 title-selected regional items and, if warranted, BHL's bulk OCR. These title matches are a discovery shelf, not an exhaustive regional bibliography.

For each accepted claim, retain original passage, scan, translation credit, observation/publication dates separately, locality, wild/captive/traded status, identification rationale, source relationships, and novelty assessment against scholarship. The JSON evidence template is intentionally unpopulated.

## Storage and publication

Raw downloads, derived full text/index, and local review outputs are Git-ignored. Small curated inputs, scripts, tests, and provenance manifests can be versioned. `.vercelignore` excludes this entire pilot from the static website deployment. No website pages were regenerated, and nothing was committed, pushed, or deployed during setup.

BHL catalog metadata is CC0; do not generalize that license to all texts or images. Individual source rights and licenses remain in the saved catalog metadata. The downloaded modern BOC issue is a local scholarly baseline, not site content. Original historical texts, modern annotations, and digitization conditions may differ.

Technical references: [BHL data tools](https://about.biodiversitylibrary.org/tools-and-services/developer-and-data-tools/), [BHL open data](https://github.com/gbhl/bhl-open-data), and [bulk OCR export](https://doi.org/10.25573/data.21422193.v4).
