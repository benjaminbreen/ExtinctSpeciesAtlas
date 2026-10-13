# Harness repairs and local Cape searches, 3 October 2026

Internal research record. The runs below used local retrieval. API stages were tested with mocked responses, not paid requests. No accepted occurrence or public atlas passage was added.

## Completed repairs

- Validate model quotations against the precise input window and retain original offsets; audit rejected flags. Malformed/incomplete responses remain retryable rather than becoming negative results.
- Bind local outputs and paid checkpoints to their inputs/settings. Recover interrupted vector/journal writes and reject stale outputs. Normalize vectors once and retain full page text through windowing.
- Distinguish an exact passage match from a known page, neighbouring context or related source. Keep planted pilot finds in the pending queue. Preserve review decisions outside generated results and mark them stale after transcription changes.
- Reconcile the dodo baseline's interpreted identifications against Cheke and Parish 2020, Table A1, pp. 8–11. Described red hens using dodo names remain red hens; undescribed late birds retain uncertainty. Hugo's retrospective report is distinct from a current sighting. Leguat's table/text date discrepancy remains explicit. This is a secondary-chronology reconciliation, not a fresh review of primary transcriptions.
- Add the TANAP Council of Policy adapter, source hashes and a pinned snapshot receipt. Separate editorial footnotes from retrieval text, retain Hague-copy references and distinct sections sharing a locator, and avoid invented scan links. Zero-day date tags retain month precision, with the source tag preserved.

## Dodo regression

The vocabulary sweep recovered 9/9 development-control pages among 1,943 candidate pages. The geographical pool contains 52,824 pages and includes 7/9 controls; the two Japan records are outside that pool. The pool/sweep union contains 54,696 pages and includes all nine controls. Every page in that union was checked for preservation of full source text. This is input coverage and a development regression, not measured model screening recall or blinded discovery recall.

The four 1615/1638 pilot pages now have persistent ledger entries carrying their existing qualifications and outstanding source/literature checks. None is automatically classified as a published discovery.

## Cape GLOBALISE

The original catalogue filter selected 329 volumes and omitted both game controls: settlement fields are blank for VOC 3995 and 4089. Adding the documented Cape papers range, VOC 3988–4360, expands the selection to 617 volumes and 53,479 anchored/context pages. These are selected volumes, not uniformly Cape-only documents. Finding aid: [eGGSA, papers received from the Cape](https://eggsa.org/sarecords/index.php/indexes-to-online-records/nationaal-archief-den-haag/indexes-to-papers-received-from-the-cape).

Both proxy controls are now included:

- VOC 3995, scan 1265: a game list near Riebeecks Casteel, naming lions, rhinoceroses, ostriches and hartebeests in the HTR text.
- VOC 4089, scan 0080: the expedition towards the stranded Schonenberg; the HTR reports four elands seen by the party.

These are machine-text game controls, not bluebuck occurrences, and their manuscript scans were not reviewed in this run. VOC 4026, scan 0038, is a negative control: Buffels Jagt is a place in a travel account, not a buffalo sighting.

The corpus-wide bluebuck spelling/pattern sweep returned 30 pages. The matched contexts concern personal names (especially Blaauwpot), textiles, materials or administrative references. These lexical assessments are saved in the ledger. Whole-page semantic reading and scans remain pending; these annotations do not close the candidate pages. No bluebuck occurrence was established.

## Cape TANAP

The adapter indexed 5,032 edition sections from the existing repository snapshot `1b65251f111cc0bee5084af73eb048a2a83bec4c`. The scoped pool contains 1,377 sections. Both hunting-regulation controls are included:

- Council of Policy, 20 January 1688, C. 19, pp. 99–100: permission to hunt large and small game, subject to existing placards. [Edition](https://docs.globalise.huygens.knaw.nl/tanap/cape-transcriptions/Council-of-Policy/TKF3_C011-C020/C019_v1.20/).
- Council of Policy, 30 July 1698, C. 23, pp. 22–24: regulation of licensed hunting and excessive taking of game. [Edition](https://docs.globalise.huygens.knaw.nl/tanap/cape-transcriptions/Council-of-Policy/TKF3_C021-C030/C023_v1.20/).

The ship Oliphant in C. 1, pp. 12–14 (11 May 1652) provides a negative control. The configured bluebuck sweep returned no matches. This is a result for those terms/patterns in the indexed primary text; it does not establish historical absence. The hunting controls do not evaluate bluebuck identification or discovery recall. No confirmed bluebuck positive has yet been mapped to either corpus.

## Validation and remaining research

Thirty-five harness tests (28 reliability tests, four baseline tests and three original unit/integration tests), four pilot tests and 15 site tests passed. The site build check passed. Model-stage tests use mocked responses; their live provider behavior and actual costs remain untested in this repair run.

Paid reading of the expanded scopes remains a separate research run. Input-only estimates exceed the earlier Cape estimate: the GLOBALISE pool contains about 99.7 million characters. Screening cost estimates must include overlap, prompts and bounded model output; the CLI's estimate check is not a provider-enforced spending cap. The bluebuck baseline still needs the unread specialist works, including Skead and Mohr. Verified species-specific positives and independent document-family holdouts are needed before estimating discovery recall.
