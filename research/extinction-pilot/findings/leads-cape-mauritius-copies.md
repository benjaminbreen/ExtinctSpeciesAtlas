# Leads: Cape copies of Dutch Mauritius records (1638–1710), dodo and red hen

Prepared 1 October 2026. Scope: digitized or digitally searchable copies of Dutch Mauritius records kept at the Cape, plus published editions, checked for dodo and red-hen terms. GLOBALISE (NA 1.04.02) was already covered and is used here only for cross-checks.

Search terms used in every full-text check, as case-insensitive regular expressions: `dod[aeo]{1,2}r…` (covers dodaers, dodaersen, dodaarsen, dodeersen, doddaerssen, dodaars), `dodo`, `dronte`, `walg/walch-vogel`, `velt/veld-hoen(der)`, `dottaer`, `toddar`, `gelinotte`, `poule rouge`, `red hen`, plus `Lamotius` and `Mauritius` for context. Downloads and working files are in the session scratchpad (`…/scratchpad/cape/`).

Reference list of known records: Cheke & Parish 2020, *Quaternary* 3(1): 4, Table A1 (PDF: https://pdfs.semanticscholar.org/a21f/aedeaf61b802fd6101c096cf98e906537ed5.pdf). The only Cape-archive entry in Table A1 is "1685–1688 Isaac J. Lamotius, *dodaarsen*", refs [6, 22, 25, 29]. Its supporting notes add three points. Sleigh (2000) reported about 50 "dodos" in the same period. The Lamotius reports of 1683 and 1690, and his journal entries for June–September 1678 and April 1682, mention no native birds. An entry for two dodos on 25 November 1688 in Parish (2013) was an error.

## Summary

- **No new dodo or red-hen occurrences turned up in any digitized Cape-derived source I could reach.** Every hit is either already in Table A1 or a known secondary retelling.
- **The 1685–1688 Mauritius journals have still not been digitized.** These are Cape Archives C 2238–2240, the source of the *dodaersen*. The secondary counts do not agree with each other:
  - Hume et al. (2004) give 12 occasions, the last on 25 Nov 1688.
  - Den Hengst (2009) gives about 20 birds.
  - Sleigh gives about 50.
  - Cheke & Parish treat the 25 Nov 1688 entry as an error.
- **The strongest unexamined leads are Cape dossiers that Table A1 does not cite:**
  - Court of Justice **CJ 643**, *Papers relative to the careless administration of Isaac Johannes Lamotius* (1691).
  - **CJ 642**, *Mauritius Papers: Case Swaanswyk, Molyn and Geel* (1686).
  - Council of Policy **Letters Received** for the years outside the journal run: about C 310–C 334 (1677–1684) and C 345–C 356 (1689–1694).

## (a) What is digitized and how to reach it

### 1. TANAP Cape transcriptions (moved)

- `databases.tanap.net` no longer resolves (NXDOMAIN), and `tanap.net` is now an empty WordPress placeholder.
- The TANAP Cape material is republished by GLOBALISE at **https://docs.globalise.huygens.knaw.nl/tanap/cape-transcriptions/** under a CC0 licence. Its Markdown source is at **https://github.com/globalise-huygens/tanap.docs.globalise.huygens.knaw.nl**, which can be cloned and grepped.
- Contents:
  - **Resolutions of the Council of Policy**, C 1–C 231 (1651–1795). The volumes for 1651–1743 are the edited *Suid-Afrikaanse Argiefstukke* text with Böeseken and De Wet's footnotes.
  - **Orphan Chamber inventories** (MOOC 8).
  - A glossary and a bilingual word list.
- **What the Resolutions do not contain.** They hold Council decisions only, not inward letters or Mauritius journals. By volume: C 1–C 27 cover 1651–1710, C 17–C 20 cover the Lamotius years 1685–1690, and C 21–C 27 cover 1691–1710.
- The site also hosts PDF inventories of the Cape Town Archives Repository (`/tanap/archival-inventories/`). I used them to identify the series below.

### 2. eGGSA "VOC Archive 1651–1795" dashboard

- URL: **https://eggsa.org/WebApps/VOCArchive/**. Its data is plain JavaScript under `data-diaries/` and `data-tanap/`, which I downloaded and parsed.
- It combines:
  - the TANAP Resolutions;
  - the **Cape Journals (Daghregister)** for 1647, 1651–1674, 1676, 1687, 1692 and 1699–1712;
  - Leibbrandt's *Requesten*.
- Text by period:
  - 1651–1662: the Bosman & Thom Dutch text.
  - About 1662–1676: mostly Leibbrandt's English (the `dutch` field holds English for those years).
  - 1687 and 1692: full Dutch transcriptions, apparently the Tracing History Trust transcriptions of the Hague copies.
- **Coverage gaps:** there is no Cape journal for 1677–1686, 1688–1691, 1693–1698 or 1675.

### 3. Tracing History Trust CDs (purchase only)

- Ordering: https://tracinghistorytrust.co.za/products.htm
- The CDs hold:
  - the full TANAP Resolutions;
  - "VOC-Daghregisters" for 1687, 1692, 1695, 1699, 1700, 1704, 1706, 1709, 1713, 1714 and 1789, photographed at the Nationaal Archief and transcribed;
  - "VC-Daghregisters" parts 1–2 (contents not stated online).
- Not consulted. The 1687 and 1692 years appear to be what eGGSA serves.

### 4. Cape Town Archives Repository holdings (not online)

Source: Inventory 1/1, *Archives of the Secretary, Council of Policy* (De Wet, 2003), PDF at `docs.globalise.huygens.knaw.nl/tanap/archival-inventories/pdf/CapeTown_1.1.pdf`; and Inventory 1/2, Court of Justice, `…/CapeTown_1.2.pdf`.

| Reference | Content | Relevance |
|---|---|---|
| **C 2238–2240** "Journals: Mauritius" | 1 Jan 1685–27 May 1686; 28 May 1686–31 Dec 1687; 1 Jan–31 Dec 1688 | Source of the Lamotius *dodaersen*. Known in aggregate; no published day-by-day list. |
| C 274–C 359… Letters Received | C 310–C 334 cover Sep 1677–Dec 1684; C 335–C 344 cover 1685–1688; C 345–C 356 cover Dec 1688–Oct 1695. C 315 holds three Mauritius free-burgher petitions (1678) and a letter of the captain of the *Bode* to the Mauritius chief (21 Sep 1678). | Mauritius letters and annexures, which may include journal extracts, for the years with no surviving Mauritius journal. |
| C 1317–C 1828 Letters Despatched | C 1353–C 1390 cover 1677–1692. C 1386 has a register of letters to "the governor, Mauritius", 24 Jun 1690. The SAA footnotes cite "C.503 Uitg. Brieven 1691–1692" (old number). | Cape replies to Mauritius. Low chance of fauna content. |
| C 1870–C 2071 Journals (Cape) | Gaps: 15 Dec 1679–31 Dec 1683; 28 Dec 1687–31 Dec 1688; 1690–1693; 1695. Verbatim copies VC 1–34 (1651–1687, 1689–1690, 1691–1789) and microfilm ZA 2/6/1–20. | Summaries of Mauritius ship arrivals. |
| **CJ 642** | *Mauritius Papers: Case Swaanswyk, Molyn and Geel*, 1686 | Mutiny or conspiracy case from Mauritius, examined at the Cape May–Oct 1687 (the 1687 Cape journal confirms). Interrogations of men who lived and hunted on the island in 1685–86. |
| **CJ 643** | *Papers relative to the careless administration of Isaac Johannes Lamotius, Chief on the Isle of Mauritius*, 1691 | Witness statements on Lamotius's administration. Pitot paraphrases Deodati's later complaints that hunters' dogs killed game wholesale and that wild geese were "exterminated", which suggests the dossier discusses hunting. Not cited in Table A1. |

**Online status of the Cape Town holdings**

- The Western Cape Archives say they have no digitised records online.
- NAAIRS (the national finding aid) is in maintenance mode: `nationalarchives.gov.za` shows a maintenance page, and the old NAAIRS record links (`/node/8462025`, "Journal of IJ Lamotius") return 404.
- FamilySearch holds digitized Cape Archives microfilm, including inventories and Council of Policy incoming letters. Viewing requires a FamilySearch login, so I did not check it.

### 5. Leibbrandt, *Précis of the Archives of the Cape of Good Hope*, on Internet Archive

The volumes that bear on Mauritius are:

- *Letters and documents received* 1649–1662 (2 vols.);
- *Letters despatched* 1652–1662 (3 vols.);
- *Journal* 1662–1670; *Journal* 1671–1674 & 1676; *Journal* 1699–1732;
- *Letters received* 1695–1708; *Letters despatched* 1696–1708.

**Leibbrandt calendared no letters received for 1663–1694 and no journal for 1677–1698.** That is the whole Lamotius period (1677–1692), so a null result in Leibbrandt says nothing about those years.

### 6. Published editions: full text checked

| Edition | Where | Result |
|---|---|---|
| Pitot, *T'Eylandt Mauritius* (1905) | IA `teylandtmauriti00pitogoog` | Retells Harry 1681 and Simon/Hugo 1674 (both in Table A1). Pitot says Dutch official documents after Hugo do not mention the dodo. He paraphrases Deodati on the destruction of game under Lamotius, which points to CJ 643 and Letters Received for 1692–93. No *dodaersen*. |
| Bonaparte, *Le premier établissement des Néerlandais à Maurice* (1890) | IA `lepremiertablis00bonagoog`, `lepremiertabli01bona` | First settlement only; nothing new. |
| Grandidier et al., *Collection des ouvrages anciens concernant Madagascar*, vols. 1–5 (1903–) | IA `collectiondesou00–04grangoog`, `collectiondesouv02/03/05gran` | Nieuhof's 1662 *dronte* description (a compilation, not an observation). Harry 1681. Hoffmann's *Toddarsche* (in Table A1). Leguat's *gelinottes* "devenues rares" (in Table A1 under 1691). Nothing new. |
| Valentyn, *Oud en Nieuw Oost-Indiën* vol. 1; Leguat (Dutch ed., 1708) | IA | Nothing new. |
| *Dagh-register gehouden int Casteel Batavia* | IA: 1636, 1640–48, 1656–59, 1664, 1670, 1676–1681 (33 items) | No dodo, red-hen or *dodaers* hits. Several volumes have poor OCR, and 1665–69, 1671–75 and 1682+ were not available. |
| Delpher (KB SRU API, `jsru.kb.nl`) | Books, periodicals, newspapers | 2–27 hits per term. All are 19th–20th-century secondary texts, for example Oudemans 1918 on the 1598–1602 journals and *De Nederlandsche jager* 1913. None is a new primary record. |

**Not reachable as text**

- **Moree, *A Concise History of Dutch Mauritius* (1998)** and ***The Dutch Odyssey*** **(2002, which contains Hugo's 1673 missive)** are on Internet Archive only as controlled-lending scans (`concisehistoryof0000pjmo`, `isbn_9990339368`). Search-inside is closed to unauthenticated requests.
- Not found online in any form:
  - Barnwell, *Visits and Despatches* (1948);
  - Barnwell, "Extracts from ships' logs", *Revue rétrospective de l'Île Maurice* (1950);
  - Sleigh, *Die buiteposte* (1993);
  - Sleigh (2000), "The economy of Mauritius…";
  - Staub & Herbereau de Lachaise (eds.), *Papiers Doyen* (2013).
- I found no work titled "Diary of the Dutch in Mauritius". The title may be confused with *Visits and Despatches* or the *Revue rétrospective* extracts.
- **HathiTrust full-text search** is behind a JavaScript bot check, so I did not use it. It is the best way to find page hits in Barnwell, Sleigh, *Revue rétrospective* and *Proc. R. Soc. Arts Sci. Mauritius*, and should be run by hand in a browser.

### 7. National Archives of Mauritius

- I found no online catalogue of Dutch-period holdings.
- In 2020 the Nationaal Archief gave Mauritius digital copies of more than 700 VOC documents, selected and translated by Joël Edouard ("Slavery in Dutch Mauritius: a selection of Primary Sources (1638–1710)"). They are not publicly online. They come from the Hague VOC series, so they overlap with GLOBALISE.
- I found nothing to show that the NAM holds original Dutch-period manuscripts beyond copies.

## (b) Search results and occurrences

| Source | Hits for dodo/red-hen terms | In Table A1? |
|---|---|---|
| TANAP Resolutions C 1–C 231 (all volumes; 1651–1710 read closely) | **0**. *Velthoen* hits are all the ship names *'t Velthoen* (1662–63) and *'t Veldhoen* (1760s–70s). Mauritius is mentioned 2–28 times per volume (Lamotius in C 11, 13, 14, 17, 20, 22, 25, 26). | n/a |
| eGGSA Cape Journals 1647–1712 | **0** | n/a |
| Pitot 1905 | Harry 1681 dodo; Simon (maroon) via Hugo 1674 | Known (1681 Harry; 1662+ Simon) |
| Grandidier, *COACM* | Nieuhof 1662 (derivative); Harry 1681; Hoffmann *Toddarsche*; Leguat *gelinottes* | Harry, Hoffmann and Leguat are known. Nieuhof is not in Table A1 but is a compilation, not new evidence. |
| Batavia *Dagh-register* (available volumes) | **0** | n/a |
| Delpher | Secondary literature only | n/a |

**No possibly-new occurrences were found.**

### Negative evidence worth recording (not dodo records)

1. **Jacob Granaet, report on Mauritius, November 1666.**
   - Where: Cape Journal 11 Nov 1666, in Leibbrandt's English via eGGSA. The Dutch original is in GLOBALISE at VOC 4001, scans `NL-HaNA_1.04.02_4001_0821–0822`.
   - The report lists forest birds (parrots, parakeets, doves, ravens, falcons, bats, and "other birds" the writer could not name). It also lists waterfowl: geese, teals, *[water]hoenders* and flamingos.
   - It names no dodo and no *velthoender*.
   - It complements the 1664–1676 run in Table A2, where red hens are described under dodo names.
   - Check the exact Dutch word on scan 0821 before citing it: the HTR line reads only "…hoenders en flaminges".
2. **VOC 4024 (in GLOBALISE): Mauritius account books, July 1684–June 1686.**
   - They record issues of salt, powder and match to the hunters (*jaagers*), the hunters' boat (*Jagers champan*), and goats "caught in the forest by the Company's hunters".
   - They record no birds. Game is booked as livestock.
   - The account books are not the hunting tallies. Those are in C 2238–2240.
3. **VOC 1467 and 7532 (in GLOBALISE): Batavia copies of the 1691 case against Lamotius.**
   - These are declarations against Lamotius and the advocate fiscal's report of 2 March 1691.
   - They contain no dodo or bird terms in the HTR text.
   - The Cape dossier CJ 643 is a separate set of papers and may differ.

## (c) Next steps, ranked

1. **Get images or a transcription of C 2238–2240 (Western Cape Archives, Roeland Street, Cape Town).**
   - Every *dodaersen* entry needs a date, context and number, for three reasons:
     - to settle the disagreement between the published counts (12 occasions, about 20 birds, about 50 birds);
     - to settle the disputed 25 Nov 1688 entry;
     - to show whether any entry describes the bird.
   - Paths, in rough order of speed:
     - Email the archive about reproduction. The reading room allows personal cameras under its rules.
     - Ask Julian Hume, Jolyon Parish or Anthony Cheke, or the estate or colleagues of Dan Sleigh (d. 2023), whether working transcriptions exist.
     - Check FamilySearch while logged in, in case the C series was filmed.
2. **CJ 643 (1691) and CJ 642 (1686).**
   - These are witness interrogations about Mauritius in exactly 1685–1691. They could name what the hunters caught, and in particular whether *dodaersen* were described or distinguished from *velthoenders*.
   - Table A1 does not cite either dossier, and I found no published study that uses them.
   - Order them together with item 1.
3. **Letters Received C 310–C 334 (1677–1684) and C 345–C 356 (1689–1695).**
   - These are the Mauritius chief's letters and annexures for the years outside the journal run.
   - A *dodaersen* mention in these years would extend or test the 1685–88 series.
   - Table A1 notes no native birds in the 1678 and 1682 extracts or the 1683 and 1690 reports, but the run of letters for these years has not been read.
4. **HathiTrust full-text search in a browser**, for *dodaersen / dodaarsen / dodaers / velthoenders / Lamotius*. Targets: Barnwell 1948; *Revue rétrospective de l'Île Maurice* (1950–); Sleigh 1993; Moree 1998; *Proc. R. Soc. Arts Sci. Mauritius*. This turns secondary claims into page references cheaply.
5. **Cape Journals for 1677–1686 and 1688–1698.**
   - The Cape originals are partly lost (see the gaps above).
   - The Hague copies of the Cape daghregister for those years are in NA 1.04.02, which means GLOBALISE.
   - Confirm that the GLOBALISE search included the Cape journal copies for 1688 and 1690–93, since no Cape original survives for those years.
   - The Tracing History Trust "VC-Daghregisters" CDs may hold transcriptions for further years; ask them which years.
6. **eGGSA index to the Hague "Papers received from the Cape"** (VOC 3988–4360; https://eggsa.org/sarecords/index.php/indexes-to-online-records/nationaal-archief-den-haag/indexes-to-papers-received-from-the-cape). Use it as a finding aid to locate Mauritius items inside the GLOBALISE volumes and check that none were missed for poor HTR.
7. **National Archives of Mauritius and University of Mauritius:** ask for the list of the 2020 Edouard set and for any Dutch-period originals. Low priority, because the set derives from Hague copies.

## Notes

1. The Western Cape Archives' statement that no records are digitised online comes from a web-search summary of a page I did not open (the earlier family-history PDF). I did open the 2025 access guide, but it is a generic guide.
2. The C-volume date ranges above are copied from the 2003 inventory. Old numbers in footnotes (for example "C.503 Uitg. Brieven") follow the earlier numbering; see the concordance in Inventory 1/1.
3. All IA, TANAP and eGGSA texts were searched as downloaded. OCR and HTR errors could hide variant spellings, especially in the poorer Batavia *Dagh-register* scans.
