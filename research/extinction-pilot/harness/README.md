# Historical-record search harness

This is an internal research tool. Its reports contain retrieval candidates, not accepted occurrences or publishable transcriptions. No stage writes to the public atlas data.

Current local results and remaining research are recorded in [the 3 October 2026 findings](../findings/2026-10-03-harness-repair-cape-local.md).

Subsequent English, Portuguese, and German source reading is kept in [the bluebuck source log](../data/curated/bluebuck_source_checks.json). It corrects this project's Barrow herd citation to the 1804 second volume, p. 47 (repeated in 1806), with an inferred report date of late 1802 or early 1803. The passage is secondhand and does not independently establish the animals' identity or a later extinction date.

## Local runs

From the repository root:

```sh
python3 research/extinction-pilot/harness/run.py dodo-globalise local
python3 research/extinction-pilot/harness/run.py bluebuck-cape-globalise local
python3 research/extinction-pilot/harness/run.py bluebuck-cape-tanap local
python3 -m unittest discover -s research/extinction-pilot/harness/tests -v
```

`local` runs scope, vocabulary sweep and report without API calls. Results are in `research/extinction-pilot/results/harness/<case>/`, which is Git-ignored. The local integration test runs the real dodo vocabulary sweep when GLOBALISE is available; the other tests use temporary fixtures and mocked API responses.

GLOBALISE uses the existing read-only SQLite index. Set `GLOBALISE_DB` or `corpus.path` to override its default location. Scope selection accepts catalogue settlement names, description substrings, explicit inventories and inclusive inventory ranges. Catalogue date intervals are selected by overlap. Whole-volume selection can include documents about other regions; volume date bounds are not observation dates. The Cape case includes VOC 3988–4360 because settlement fields are blank in the game-control volumes.

TANAP uses the Council of Policy Markdown files from [GLOBALISE's repository](https://github.com/globalise-huygens/tanap.docs.globalise.huygens.knaw.nl). Copy the repository's `docs/cape-transcriptions/Council-of-Policy/` directory to `research/extinction-pilot/data/raw/tanap/Council-of-Policy/`, or set `TANAP_ROOT` to that directory. The indexed snapshot and source-file hashes are recorded in `manifests/tanap.json`. The cached SQLite index is keyed by source content and parser version. An intentional refresh should update the provenance manifest as well.

TANAP units are edition sections with printed page/folio locators, including separately identified Hague-copy sections. They have transcription links and no invented manuscript scan links. Editorial footnotes are retained separately and excluded from retrieval. Missing dates remain missing and their sections stay eligible for scope selection. Zero-day tags such as `{16880400}` become month-level dates (`1688-04`), with explicit precision and the original tag retained. Curly-brace dates are edition metadata; they are not automatically observation dates. Distinct sections sharing a locator are retained; exact duplicate text is collapsed. The source is published under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Retrieval and paid stages

- `scope`: retain complete transcription text for catalogue-selected pages and context windows.
- `sweep`: lexical seeds, fuzzy spelling candidates and configured text patterns over the corpus. The fuzzy candidate prefilter uses matching first letters or final two letters; it is a heuristic, not a guarantee of finding every word within the edit-distance threshold. Frequent terms can be explicitly dropped by case settings. A negative sweep does not demonstrate absence.
- `embed`: split complete pages into overlapping windows; rank pages by their best window score. Normalize each vector once. The default window is 6,000 characters with 200-character overlap.
- `screen`: read the configured pool/sweep union in windows. The dodo and Cape cases use both inputs. Retain exact window and quote offsets. Accept quotations only when their characters match the input, allowing whitespace differences. Invalid flags go to `screen_rejected.jsonl`. Malformed, incomplete or failed responses remain retryable and the command reports incomplete screening.
- `report`: combine validated current outputs and create `candidates.jsonl`, `evidence_records.jsonl` and `report.md`. Machine-text quotation matching is kept distinct from scan verification and taxonomic identification. Evidence drafts leave interpreted taxa, translation, dates of observation, source dependence and novelty unset until reviewed.

For an explicitly intended paid run:

```sh
python3 research/extinction-pilot/harness/run.py dodo-globalise embed --budget 5
python3 research/extinction-pilot/harness/run.py dodo-globalise screen --budget 50
python3 research/extinction-pilot/harness/run.py dodo-globalise report
```

API credentials come from the environment or `.env.local` and are never included in reports. `--budget` rejects a stage whose estimated cumulative cost exceeds the supplied amount; `--yes` overrides that estimate check. It is not a provider-enforced spending cap. Screening estimates reserve maximum configured output per remaining batch, include prompt/overlap costs and account for previous attempts. Character-based input estimates and the constants in `engine.py` remain estimates. Scope output shows input-only estimates. `max_completion_tokens` bounds each screening response. Review the model/pricing configuration before a paid run.

## Resuming and provenance

Scope and sweep outputs have input and content fingerprints. Paid checkpoints bind the actual ordered texts/windows, queries, model and relevant settings. Changed inputs, legacy outputs without fingerprints and inconsistent checkpoints are refused rather than silently reused. An embedding file tail written before a crash but beyond its committed checkpoint is truncated and recomputed. An unterminated final screening journal write is discarded; corruption of a committed line raises an error. Generated JSON/JSONL outputs are replaced atomically.

To start a materially different run, archive the existing results directory and run `local` again. Reports also refuse stale paid outputs. Development-control results identify their control configuration; results from a different configuration are not reused in the report.

## Baselines and review decisions

Baselines are literature inventories with incomplete coverage. Dodo `names_used` records the chronology's name columns separately from `identification`, which identifies the proposing authority, locator and certainty. `taxa` does not turn a historical word into a species identification. The Leguat table/text date discrepancy and retrospective/derived testimony remain explicit. Primary editions and scans require their own review. The bluebuck baseline still identifies unread works, including Skead and Mohr.

Matching statuses are `exact_passage`, `known_page`, `possible_context`, `possible_source` and `possible_observer_date`. An exact passage requires an explicit adapter/scan/quotation key. Source or observer/date comparisons use actual supplied passage metadata, never volume date bounds. A matching page, neighbouring page or planted control does not close a candidate or establish its novelty. Candidates remain pending until a documented review decision closes them.

Review decisions live in versionable `reviews/<case>.json`, outside generated results. To record a page-level decision:

```sh
python3 research/extinction-pilot/harness/review.py CASE PAGE_ID \
  --status needs_literature_check --novelty possible_new \
  --reviewer 'Reviewer name' --note 'Sources checked, identification and outstanding questions.'
```

A page-level decision covers the whole candidate page: inspect all its flags before using `known` or `rejected`. Other statuses are `unreviewed`, `needs_scan_check` and `reviewed`; other novelty values are `not_assessed`, `known` and `rejected`. Edits retain decision history. Reports never overwrite the ledger. If the transcription hash changes, the prior decision is shown as stale and the page returns to pending review. Dodo pilot leads have been transferred with their existing qualifications and unfinished checks.

## Evaluation limits

The dodo's nine planted pages are development controls selected during the pilot. They do not form a blinded discovery evaluation. Cape controls are game lists and hunting regulations, with ship/place-name negatives; they test retrieval of that material, not identification or recall of bluebuck. No confirmed bluebuck passage has yet been mapped to either corpus. Stage-specific controls prevent proxy passages from being counted as failures in a species-name sweep. A case/stage with no relevant controls is explicitly `not_evaluated`. Screening controls require the expected category, and negatives distinguish flagged, clear and outside the input pool.

Before estimating discovery recall, reserve independent document families and identify verified species-specific positives. Read the missing specialist literature before treating an unmatched candidate as new.
