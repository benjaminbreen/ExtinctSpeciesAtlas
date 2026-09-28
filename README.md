# Atlas of Historically Lost Species

I am a historian of science and medicine interested in what the written record can tell us about species that disappeared before 1900. This atlas is a place to gather that evidence: descriptions, names, reported uses, images, and the locations mentioned in historical sources. I want it to be useful both to people researching these histories and to readers encountering them for the first time.

The scope begins with **species reported in writing while they still existed**, or in sources close enough to their disappearance to preserve historical testimony. It does not include animals known only from fossils or archaeological remains, such as Paleolithic megafauna. A historical name does not always correspond neatly to a modern species. Where identification or extinction status is disputed, the dossier should explain the disagreement rather than silently resolve it.

Silphium of Cyrenaica is the first case. Ancient authors describe a plant of economic and medicinal importance, but its botanical identity and the circumstances of its disappearance are uncertain. Its dossier presents five texts in depth: Herodotus, Theophrastus, two passages from Pliny, and Synesius. A larger index points to other passages. Each detailed record has a separate page with its original language, a new working English translation, notes, and relevant further reading.

The [great auk](great-auk.html) is the second dossier. Five transcribed English sources have separate records: Martin Martin’s *A Late Voyage to St Kilda* (1698), Thomas Pennant’s *British Zoology* (1776), George Cartwright’s journal entry of 5 July 1785, Alfred Newton’s 1861 account of interviews about the 1844 Eldey capture, and Frederic A. Lucas’s report on his 1887 Funk Island expedition. The records link to digitized editions; three include local page scans. The dossier maps St Kilda, Funk Island, and Eldey, and gathers catalog metadata and credited historical images. Both source indexes are starting sets to expand through further research. The other ten species in the homepage index remain research stubs.

## Research approach

The atlas connects claims to the passages and objects on which they rest. The research involves locating further primary material, checking texts in their original languages, comparing translations, recording edition and passage details, and distinguishing historical place names from modern map coordinates. Maps are tied to the places named in the sources, and images carry dates and provenance.

The index can be filtered by subject or place from the dossiers and their source records. These links show the current entries associated with that term. The English translations of the Greek and Latin silphium passages are working translations for this atlas.

The silphium page's **Source index** starts with eleven passages and defaults to chronological list view. It can be sorted by date or author and switched to cards. Five detailed source pages are linked from it; the six further entries currently link to external editions. The “Later appearances” dates belong to particular reports: Pliny's account of a stalk sent to Nero (during Nero's reign), Synesius's 402 CE letter about a garden plant, and his 405 CE letter about silphium juice. They are **not** three verified sightings of a single identified taxon. The reference panel records Wikidata's claims without treating its classification as a resolved botanical identity. Kew's Plants of the World Online and GBIF both list a living genus called *Silphium* L.; a name search there should not be mistaken for a record of the Cyrenaic plant.

Corrections and leads to overlooked sources are welcome through [GitHub issues](https://github.com/benjaminbreen/ExtinctSpeciesAtlas/issues). Please include a passage reference or link to an edition where possible.

The site has a standalone [About page](about.html) describing its purpose and author. A [proposed first corpus](research/first-corpus.md) records the twelve cases and starting references. A separate [assessment](research/corpus-assessment.md) compares the evidence for human involvement and the likely research yield of each case.

The **[Authorities index](authorities.html)** connects the eleven silphium passages and five great auk records to fourteen authorial entries. It can be sorted by chronology, name, or number of indexed passages, with list and card views. Author names on the detailed source pages link to this index. Short numbered notes linked from the texts replace large interpretive sections. The index also gathers the studies cited in the detailed records.

## Run locally

This is a static HTML, CSS, and JavaScript site. It has no build step, API key, or runtime dependency. From the repository root:

```sh
python3 -m http.server 4173
```

Open [http://localhost:4173/](http://localhost:4173/). JavaScript modules need HTTP rather than a `file:` URL.

## Deploy on Vercel

Import this repository into Vercel. The included `vercel.json` sets the framework preset to **Other**, skips the build command, and serves the repository root (`.`), where `index.html` lives. No environment variables are needed. The site uses relative asset and page paths, so the same files can also be served as a standalone subfolder of another static site.

## Sources, images, and map data

The homepage index uses three transparent, AI-generated contact sheets as small interface illustrations. Their quadrant mapping, prompts, and historical visual points of departure are recorded in [assets/species-icons/README.md](assets/species-icons/README.md). The dossier galleries use attributed historical images.

`data/authorities.json` holds the edited index of names, approximate dates, brief biographies, image descriptions, and works. Its biographical links point to Wikipedia; the page's descriptions are short paraphrases. Most circular images are locally served derivatives of Wikimedia Commons files: later busts, statues, engravings, or manuscript depictions. Martin Martin and Frederic A. Lucas currently have typographic initials in place of portraits. Each entry links to its image source and gives its nature, credit, and license. File-level data are in `assets/authorities/manifest.json`.

- Herodotus, *Histories* 4.169, [G. C. Macaulay translation](https://lexundria.com/hdt/4.169/mcly).
- Pliny, *Natural History* 19.15 (numbering varies by edition), [John Bostock and H. T. Riley translation](https://peterburk.github.io/pliny/ChaptersHtml/19.%20Book%20XIX.%20The%20Nature%20And%20Cultivation%20Of%20Flax,%20And%20An%20Account%20Of%20Various%20Garden%20Plants./15.%20Chap.%2015.-Laserpitium,%20Laser,%20And%20Maspetum..html).
- Synesius, *Letter 106*, c. 402 CE, [Augustine Fitzgerald translation](https://www.livius.org/sources/content/synesius/synesius-letter-106/).
- Original-language transcriptions on the source pages are linked there: [Herodotus in Greek](https://penelope.uchicago.edu/Thayer/H/Roman/Texts/Herodotus/4G%2A.html), [Pliny in Latin](https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Pliny_the_Elder/19%2A.html), and [Synesius in Greek](https://eulogikon.org/works/synesius-cyrene-letters-nicander-sys-ah). Source pages also link directly to the secondary works listed in their further-reading sections.
- The historic woodcuts were cropped from page 598 (PDF page 620) of the [1644 Theophrastus edition edited by Johannes Bodaeus van Stapel](https://archive.org/details/BIUSante_00956/page/n619/mode/1up), digitized by the Bibliothèque interuniversitaire de santé / Internet Archive. The scan is public domain. `assets/silphium-woodcut-isolated.webp` is a display derivative of the original crop with the scanned paper background removed; the original crop remains in `assets/silphium-woodcut.webp`. These prints document **early modern interpretations of laserpitium** and do not verify the appearance of ancient Cyrenaic silphium.
- The image gallery includes local WebP thumbnails of all twelve files listed in Wikimedia Commons' [Coins of Cyrene – Silphium](https://commons.wikimedia.org/wiki/Category:Coins_of_Cyrene_-_Silphium) category when checked on 28 September 2026. Each thumbnail links to its Commons file page; nearby captions give its author or holding institution and license. `assets/silphium-gallery/manifest.json` retains the source page, license, and Commons artist field for each file. The gallery also includes the two 1644 woodcuts.
- The reference panel excerpts [Wikipedia's Silphium entry](https://en.wikipedia.org/wiki/Silphium) (CC BY-SA 4.0, retrieved 28 September 2026) and reads catalog fields from [Wikidata Q1570745](https://www.wikidata.org/wiki/Q1570745). Their claims are attributed to those projects. The linked [Kew](https://powo.science.kew.org/results?q=Silphium) and [GBIF](https://www.gbif.org/taxon/7GWF) pages are name-collision checks for the living genus, not biological records of ancient silphium.
- The map coastline is from [Natural Earth 1:50m land](https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/), public domain. The red coastal wash illustrates the span described by Herodotus.
- The great auk pages link to scans of [Pennant’s *British Zoology*](https://archive.org/details/britishzoology21penn), [Cartwright’s *Journal*](https://www.biodiversitylibrary.org/item/101679), and [Newton’s article in *Ibis*](https://biostor.org/reference/292413). Their displayed page facsimiles are local WebP derivatives of those scans. The North Atlantic map uses the same public-domain Natural Earth land data. Four great auk image files, links, credits, and licenses appear in `assets/great-auk-gallery/manifest.json`. The transparent 1655 engraving in the hero is a display derivative of the credited gallery image.
- `assets/gfs-didot.ttf` is GFS Didot by the Greek Font Society under the SIL Open Font License; its license is included at `assets/GFS-Didot-OFL.txt`.

Note that this README was written primarily by GPT-6 Sol, based on guidance and writing from Benjamin Breen. I promise I will replace it with a fully human-authored overview when the site is closer to a finished form :)
