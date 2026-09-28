# Atlas of Historically Lost Species

I am a historian of science and medicine interested in what the written record can tell us about species that disappeared before 1900. This atlas is a place to gather that evidence: descriptions, names, reported uses, images, and the locations mentioned in historical sources. I want it to be useful both to people researching these histories and to readers encountering them for the first time.

The scope begins with **species reported in writing while they still existed**, or in sources close enough to their disappearance to preserve historical testimony. It does not include animals known only from fossils or archaeological remains, such as Paleolithic megafauna. A historical name does not always correspond neatly to a modern species. Where identification or extinction status is disputed, the dossier should explain the disagreement rather than silently resolve it.

Silphium of Cyrenaica is the first case. Ancient authors describe a plant of economic and medicinal importance, but its botanical identity and the circumstances of its disappearance are uncertain. The dossier begins with three texts presented in depth—Herodotus, Pliny, and Synesius—and a growing index of other passages. Each of the three detailed records has a separate page with its original language, a new working English translation, notes, and relevant further reading. The dossier also has a map, a linked reference panel, and an attributed image gallery. This is a beginning, **not a complete silphium bibliography**. The great auk, Steller’s sea cow, and dodo appear in the index as entries to develop later.

## Research approach

Each finished dossier should make it possible to move from a claim back to its source. The work ahead includes locating further primary material, checking texts in their original languages, comparing translations, recording edition and passage details, and distinguishing historical place names from modern map coordinates. Maps should show what a source actually locates, with uncertainty visible. Images need dates and provenance; an early modern drawing of a proposed silphium is evidence of an interpretation, not a verified portrait of the ancient plant.

The index can be filtered by subject or place from the silphium page and its source records. These links show the current entries associated with that term; a place named as a trade destination is distinguished from a growing region in the source metadata. The source pages are committed static HTML. To revise their texts or bibliography, edit `scripts/build_sources.py`, run `python3 scripts/build_sources.py`, and review the resulting pages. The English translations there are working translations for this atlas, not quotations from the linked historical translations.

The silphium page's **Source index** starts with eleven passages and defaults to chronological list view. It can be sorted by date or author and switched to cards. The three detailed source pages are linked from it; the eight further entries currently link to external editions. The “Later appearances” dates belong to particular reports: Pliny's account of a stalk sent to Nero (during Nero's reign), Synesius's 402 CE letter about a garden plant, and his 405 CE letter about silphium juice. They are **not** three verified sightings of a single identified taxon. The reference panel records Wikidata's claims without treating its classification as a resolved botanical identity. Kew's Plants of the World Online and GBIF both list a living genus called *Silphium* L.; a name search there should not be mistaken for a record of the Cyrenaic plant.

Corrections and leads to overlooked sources are welcome through [GitHub issues](https://github.com/benjaminbreen/ExtinctSpeciesAtlas/issues). Please include a passage reference or link to an edition where possible.

The site has a standalone [About page](about.html) describing its purpose and author. A [proposed first corpus](research/first-corpus.md) records twelve research candidates and starting references; those proposals are not yet completed dossiers.

The **[Authorities index](authorities.html)** connects the eleven silphium passages to nine authorial entries. It can be sorted by chronology, name, or number of indexed passages, with list and card views. The Hippocratic corpus is a composite attribution; its entry does not claim that Hippocrates wrote *Diseases IV*. Author names on the three bilingual source pages link to this index. Short numbered notes linked from the translations replace large interpretive sections. The index also gathers the secondary studies cited in the detailed records.

## Run locally

This is a static HTML, CSS, and JavaScript site. It has no build step, API key, or runtime dependency. From the repository root:

```sh
python3 -m http.server 4173
```

Open [http://localhost:4173/](http://localhost:4173/). JavaScript modules need HTTP rather than a `file:` URL.

## Deploy on Vercel

Import this repository into Vercel. Set the framework preset to **Other**, leave the build command empty, and use `.` as the output directory. The repository root contains `index.html`; no nested root directory is needed. The site uses relative asset and page paths, so the same files can also be served as a standalone subfolder of another static site.

## Sources, images, and map data

`data/authorities.json` holds the edited index of names, approximate dates, brief biographies, image descriptions, and works. Its biographical links point to Wikipedia; the page's descriptions are short paraphrases. The circular images are locally served derivatives of Wikimedia Commons files. They are later busts, statues, engravings, or manuscript depictions, **not contemporary likenesses**. Each entry links to its Commons file page and gives its date or nature, credit, and license. File-level source and license data are in `assets/authorities/manifest.json`. After editing the data, run `python3 scripts/build_authorities.py`; `python3 scripts/fetch_authority_images.py` refreshes the Commons derivatives (requires Pillow). Review provenance and license fields before committing an image refresh.

- Herodotus, *Histories* 4.169, [G. C. Macaulay translation](https://lexundria.com/hdt/4.169/mcly).
- Pliny, *Natural History* 19.15 (numbering varies by edition), [John Bostock and H. T. Riley translation](https://peterburk.github.io/pliny/ChaptersHtml/19.%20Book%20XIX.%20The%20Nature%20And%20Cultivation%20Of%20Flax,%20And%20An%20Account%20Of%20Various%20Garden%20Plants./15.%20Chap.%2015.-Laserpitium,%20Laser,%20And%20Maspetum..html).
- Synesius, *Letter 106*, c. 402 CE, [Augustine Fitzgerald translation](https://www.livius.org/sources/content/synesius/synesius-letter-106/).
- Original-language transcriptions on the source pages are linked there: [Herodotus in Greek](https://penelope.uchicago.edu/Thayer/H/Roman/Texts/Herodotus/4G%2A.html), [Pliny in Latin](https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Pliny_the_Elder/19%2A.html), and [Synesius in Greek](https://eulogikon.org/works/synesius-cyrene-letters-nicander-sys-ah). Source pages also link directly to the secondary works listed in their further-reading sections.
- The historic woodcuts were cropped from page 598 (PDF page 620) of the [1644 Theophrastus edition edited by Johannes Bodaeus van Stapel](https://archive.org/details/BIUSante_00956/page/n619/mode/1up), digitized by the Bibliothèque interuniversitaire de santé / Internet Archive. The scan is public domain. `assets/silphium-woodcut-isolated.webp` is a display derivative of the original crop with the scanned paper background removed; the original crop remains in `assets/silphium-woodcut.webp`. These prints document **early modern interpretations of laserpitium** and do not verify the appearance of ancient Cyrenaic silphium.
- The image gallery includes local WebP thumbnails of all twelve files listed in Wikimedia Commons' [Coins of Cyrene – Silphium](https://commons.wikimedia.org/wiki/Category:Coins_of_Cyrene_-_Silphium) category when checked on 28 September 2026. Each thumbnail links to its Commons file page; nearby captions give its author or holding institution and license. `assets/silphium-gallery/manifest.json` retains the source page, license, and Commons artist field for each file. The local WebP thumbnails are format-converted derivatives and retain their respective Commons licenses. To refresh that category snapshot, run `python3 scripts/fetch_silphium_images.py` with Pillow installed, then review the manifest, license claims, captions, and resulting images before committing changes. The gallery is an inventory of that category and the two 1644 woodcuts, not a claim to contain every depiction elsewhere online.
- The reference panel excerpts [Wikipedia's Silphium entry](https://en.wikipedia.org/wiki/Silphium) (CC BY-SA 4.0, retrieved 28 September 2026) and reads catalog fields from [Wikidata Q1570745](https://www.wikidata.org/wiki/Q1570745). Their claims are attributed to those projects. The linked [Kew](https://powo.science.kew.org/results?q=Silphium) and [GBIF](https://www.gbif.org/taxon/7GWF) pages are name-collision checks for the living genus, not biological records of ancient silphium.
- The map coastline is from [Natural Earth 1:50m land](https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/), public domain. `assets/map-geometry.js` is its clipped, projected form, and `scripts/build_map.py` documents regeneration. The red coastal wash is a schematic reading of Herodotus, not a precise range reconstruction.
- `assets/gfs-didot.ttf` is GFS Didot by the Greek Font Society under the SIL Open Font License; its license is included at `assets/GFS-Didot-OFL.txt`.

## Editorial voice

The site should use direct, historically precise language. Avoid promotional taglines, aphorisms, dramatic claims about loss or memory, and filler text. Say which source makes a claim, what it says, and what remains unknown. The repository's [AGENTS.md](AGENTS.md) records this standard for future contributions.
