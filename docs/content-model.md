# Atlas content and publishing

The site remains static HTML, CSS, and JavaScript. The build uses Python's standard library and requires no service, database, API key, or frontend framework. Deploy the generated files as before.

## Where to edit

| File | Responsibility |
| --- | --- |
| `data/species.json` | Twelve stable species IDs, names, page paths, tags, place associations, and homepage display fields. |
| `data/passages.json` | Sixteen indexed passages, including the ten detailed source records. Each record owns its species and authority references, catalog entry, text, notes, and source links. |
| `data/bibliography.json` | Further-reading citations grouped by dossier. |
| `data/authorities.json` | Author names, dates, biographies, and portrait metadata. Work lists come from passage records. |
| `templates/index.html` | Homepage surrounding the generated species entries. |
| `templates/silphium.html`, `templates/great-auk.html` | Dossier layouts and authored featured excerpts; source indexes and their numerical counts are generated. |
| `templates/source-reader.html` | The expanded English source-reader layout currently used by Newton. |
| `scripts/build_sources.py`, `scripts/build_auk_sources.py` | Source renderers. Their old in-script text dictionaries now load from the shared data. |
| `scripts/build_authorities.py` | Authority-page renderer. |
| `scripts/build_site.py` | Build entry point and local-link validation. |

Fields ending in `_html` contain edited presentation markup. They are trusted repository content, not an input for raw OCR or externally supplied HTML. Original passages and translations remain plain strings escaped by the renderer. The migration preserves the existing text and source URLs; it does not certify a new historical verification.

## Passage records

`id` is a stable passage ID, not necessarily an author ID. Multiple passages by one author have separate IDs and share `authority_id`. Existing page URLs are preserved. `species_ids` permits a passage to concern more than one species without duplicating the text.

`catalog` supplies the source index's date label, sorting value, title, summary, genre/language label, anchor, and destination. `sort_year` is an ordering aid; it must not be treated as an observation date. Existing date wording remains unchanged, including approximate dates and event/publication pairs.

`authority_work` supplies the concise work label and link used on the Authorities page. It belongs to the passage, not to a separately maintained author work list.

A detailed record has a `page`, a renderer `format` (`bilingual`, `english`, or `reader`), and `content`. An indexed external reference has all three set to `null`; it remains a citation rather than gaining an empty source page. `content` retains the existing source-specific fields for text, edition links, translations, notes, reading, and neighboring records. English records can opt into the expanded reader with `content.reader`; its date rows distinguish event, interview, and publication dates without inferring dates for other records.

`research` is internal metadata. Reviewer and date fields are initially null: the migration does not invent a review history. `relationships` accepts explicit passage links with `translation_of`, `quotes`, `copies`, or `discusses`. Empty relationships mean not yet recorded, not proven independence. No review badges or procedural commentary are generated from these fields.

## Add a passage to an existing dossier

1. Add a unique record to `data/passages.json`, referencing an existing species and authority. Add an authority biography and its credited image record when needed, following the existing authority-image requirements.
2. Supply its catalog and authority-work fields. For an external-only citation, leave `page`, `format`, and `content` null. For a detailed record, use `source-<id>.html` and supply the applicable text, edition, notes, and reading fields.
3. Check new or changed transcriptions and translations against their sources before publication. Keep work reports in the conversation/internal research records. Public labels remain compact.
4. Update source neighbors if needed. Add or revise a featured excerpt in the dossier template only when wanted; featured excerpts are editorial selections and are not automatically clipped from the full text.
5. Run the build, checks, and tests below. Inspect the changed page in the browser.

The source index, its numerical count, authority work lists, and generated source pages update together. The great auk and dodo homepage counts is calculated from detailed records and their distinct place keys. The silphium status remains “Identity unresolved.”

## Add a dossier

Set the species `page` in `data/species.json`, supply a matching dossier template with `${source_index}` and `${source_count}` placeholders, and add its passages and bibliography. Choose the appropriate renderer for detailed records. New language layouts or material objects may need a renderer extension; do not force them into an English transcription layout. New English dossiers use `content.reader` and the shared source-reader template automatically. Use `format: "reader"` for the shared scan reader, including Latin or French extracts with historical English translations. Supply `language`, optional `translation`, and `translation_credit_html`; no translation is generated by the build. For a scan outside the great auk asset folder, provide `content.facsimile_path`.

The hand-edited dossier sections, image galleries, maps, and featured excerpts are deliberately retained. Their prose, map coordinates, and source dependence still require editorial work. This is a publishing foundation, not an automatic research-to-website pipeline.

## Build and checks

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 -m unittest discover -s tests -v
```

`--check` writes nothing. It rejects invalid references, duplicate IDs, broken note targets, stale generated pages, and missing local links, assets, or fragments. It does not check remote availability, factual truth, copyright, or translation quality. The build is deterministic and only rewrites changed outputs.

The research pilot has a separate lifecycle. Downloaded books, OCR, candidate hits, and its evidence template are not build inputs. Move an edited passage into the publication records deliberately; matching a species name in OCR does not publish it.

## Page scans

Shared-reader records can supply `scans`, an ordered list of `{src, label, caption, url}`. The first entry must match `facsimile_path`. The reader shows page buttons, updates the archive link and caption, and enlarges the selected scan. Store local image files with an image manifest recording the edition, printed page, archive download URL, holding institution, and rights. Check the printed page itself: Internet Archive image numbers can differ from scandata leaf numbers and can skip plates.

The dodo records use original editions for Clusius (1605), Herbert (1634), and Cauche (1651). L’Estrange uses the printed transcription in Strickland and Melville (1848), p. 22; it is not a manuscript image. Latin and French extracts use the English text printed in that volume’s appendix. The source record, edition date, and caption distinguish these editions.

## Public research notes

`data/research-notes.json` selects edited passage IDs by species and supplies a brief historical context for each group. It contains no second copy of the transcription. `scripts/build_research_notes.py` renders `research-notes.html` and a stable `research-notes-<species-id>.html` page using the shared passage records, scans, citations and authority links. Each passage has an anchor for citation; its full source record remains available separately.

Set `notes_page` on the corresponding species entry. A species with a dossier links to its notes from that dossier; an entry without a dossier can link directly to its notes from the homepage. Create pages only when there is substantive material, rather than empty placeholders. The build rejects notes referencing another species, repeated passages, missing scans, or passages without a recorded transcription review. Review metadata stays internal; a recorded date is a publishing guard, not proof of factual accuracy.

To preserve a research foray, move selected, checked passages into `data/passages.json`, preserve facsimile provenance and rights in the relevant asset manifest, and select them in `data/research-notes.json`. Keep search logs, OCR, failed searches and unfinished archival leads under `research/extinction-pilot/`; the public build does not read them. Public context should describe the historical testimony and its particular uncertainties, without reporting the agent's progress or claiming a discovery. Retain stable passage IDs and page URLs when correcting text.

The initial warrah records reproduce Tyssen's statement and rescue report from the parliamentary paper (1843), and the July inquiry and October letters in the Falkland Islands Magazine (1894). The Tyssen extract excludes the preceding covering letter and final signature; the magazine letters include Smith's coin postscript and the editor's reply. Line-end hyphenation is joined; paragraphing, typographical quotation marks and spacing are normalized. The scans show the complete printed pages. The magazine edition links use the Internet Archive's archived copy of the Jane Cameron National Archives PDF.
