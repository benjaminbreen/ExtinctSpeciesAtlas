# Mauritius embedding run, 30 September 2026

## Method

- Corpus: GLOBALISE v2 (VOC OBP series), local index at `~/Code/Historical Mysteries/globalise-drugs/data/voc.sqlite`.
- Selection: 111 volumes whose catalogue entries mention Mauritius (1638–1712). Within them, every page naming Mauritius/Rodrigues/Bourbon or a Mauritian landmark, plus one page before and six after. 17,513 pages.
- Embedding: `text-embedding-3-large`, 12.67M tokens (about US$1.65). Script: `scripts/embed_mauritius.py`.
- Ranking: 16 descriptive queries written for the run (none quotes a source). Union of top 25 per query and top 150 overall: 219 pages.
- Reading: four model readers transcribed and translated relevant lines, checked neighbouring scans and catalogue entries for date and authorship, and assessed whether each passage was likely already known. Machine output only: no transcription or translation below has been checked against the scan.

Raw outputs (Git-ignored): `results/embed_mauritius/candidates.json`, `read_all.json`.

## Retrieval check

Pretorius's 1669 report (inv. 4005, scans 0600–0606; published by Hume and Winters) was never used as a query. It ranked first among 17,513 pages for 13 of 16 queries.

Of the 213 other candidate pages: 24 high, 13 medium, 72 low (mostly introduced animals, Cape or Madagascar material), 104 irrelevant.

## Known passages the run recovered

These are the kinds of passage published extinction chronologies rest on. Recovering them is validation, not discovery.

| Scan | Date | Content | Status |
|---|---|---|---|
| 4039_0031–0032 | letter of 1698 (copy), Opperhoofd Roelof Diodati | Land tortoises almost gone and none found by a search party. The "wilde gansen" (OCR reads "mansen"), once catchable by hand, are no longer seen. Blames Lamotius for allowing ebony-mill workers to take 70–80 tortoises a trip for fat alone. | Known: Cheke (1987) cites Diodati 1698 as the last record of the Mauritius sheldgoose. |
| 4011_0411 | Jan 1674, Hubert Hugo | A runaway slave who lived 11 years in the forest saw "dodeersen" twice, "as big as a cassowary". | Probably known (Hugo's dodo report). |
| 4001_0821–0822 | 1666, Jacob Granaet | Fauna list: parrots, doves, large "ravens", bats, tortoises, geese, teal and coots so tame they could be clubbed; flamingos; sea cows. | Known: used by Hume and colleagues. |

## Candidates needing a literature check

Possibly new, or new in detail. Check against Cheke and Hume (2008), Cheke and Bour on Cylindraspis, Barnwell's translations, and the 2015 Hume and Winters paper.

1. **4019_0155–0157, letter of 26 Aug 1683, Jacob Urbanus to Lamotius.** English ships took two sea cows and many land and sea turtles. One captain took about 20 live land tortoises, intending to land them on St Helena to breed. A deliberate translocation attempt of Mascarene tortoises; no published mention found in a quick search.
   - Ships, as the copy names them: "Jan bowers Cap=n vantschip de persiaense Coopman" (admiral), "Tonatan riede Cap=t op t' schip den president", and "Reijnolad: Capn op t schip de Surathe merch=t". The St Helena passage falls in the President's section, which runs from 0156 to the Surat Merchant entry on 0158. The ships were to leave on 27 Aug 1683.
   - Identification: English East India Company homeward voyage from Surat/Calicut 1683. Persia Merchant, Capt. John Bowers; President, Capt. **Jonathan Hide** ("Tonatan riede" is a garbled form); Surat Merchant, returning from Batavia. The ships waited about three months at Mauritius for the winds. Only the Persia Merchant reached England. The President was wrecked at Loe Bar, Mount's Bay, Cornwall, on 9 or 11 Feb 1684, leaving two survivors. The Surat Merchant was presumed lost near the Azores. Source: David Gibbins, "The bell of the East Indiaman the President" (2021), citing IOR/E/3/43, IOR/E/3/90 and IOR/B/38.
   - Open questions: did the President call at St Helena and land the tortoises? Check the St Helena Consultations (Janisch, *Extracts from the St Helena Records*, 1885; BL IOR/G/32), any surviving Persia Merchant journal (IOR/L/MAR/A), and the Loe Bar wreck finds for tortoise bone.
2. **4003_1614–1623, Jan van Laar's day register, Oct 1667–Jan 1668.** Daily counts of tortoises taken for fat at the Vuile Bocht rendering station (e.g. 19, 26, 18 and 25 on four days in Dec 1667). Also a dated capture of a sea cow over 7 feet long (5 Jan 1668) after a harpoon was made for the purpose. Quantitative exploitation data.
3. **4011_0415, Hugo's register, 13–19 May 1674.** On an islet (identification uncertain), tortoises so crowded they ate each other and bit people's legs; 320 brought back alive. A snake about an ell long was seen (possibly a boa; uncertain).
4. **4011_0409–0410 and 4010_0893–0895, 4011_0403, Hugo, 1673–74.** Pigs digging up turtle nests. Smeersouckers ("fat-seekers") killed 400–500 tortoises to fill half an aam. Tortoises on the "ambergris islands" killed off in the belief they ate ambergris. Geese, ducks, doves and small birds so tame they were killed by the dozen with sticks.
5. **4008_0845 and 4010_0931–0933, 1672–73.** Tortoises abundant on five islets but unable to breed on the mainland because pigs eat the eggs. Proposal to move islet tortoises to the mainland.
6. **1330_0756–0757, Hugo, 23 May 1677.** Cats do not control rats because they eat small birds and lizards, "by thousands in the woods". Not yet read in full.
7. **4006_1054, Wreede's register, Feb 1670.** Thousands of tortoises on an islet, with signs of recent slaughter attributed to French or English crews; rats and snakes present.
8. **4018_0112–0114, 0141, 1681–82, Lamotius.** Placard fining needless killing of sea turtles for fat; freemen "cruising for sea cows"; English crews leaving tortoises on their backs in groups of 10–20.
9. **1203_1192, 1654, probably Maximiliaan de Jongh.** "The tortoises on the whole land are already destroyed." An early (probably exaggerated) depletion claim from the first occupation.

Sea-cow records concern the dugong, locally extirpated rather than extinct; they are outside the atlas's scope but relevant to Mascarene historical ecology.

## Dodo spelling sweep (whole GLOBALISE vocabulary)

A scan of the full-text index vocabulary for dodo names (dodaers/dodeersen/dodersen and variants) found few genuine hits; "dodo" itself occurs only as personal names (Timor, Ternate, Surat). Two pages from inv. 1059 are new to this pilot:

- **1059_0276–0277, prose journal at Mauritius, 15–23 April 1615.** The ship anchors at the "moluckse Ree". It learns of the wrecks of the Banda and Provintia and Pieter Both's drowning, and meets the Walcheren and Engel. Entries: 17 April, hunters bring "sommighe schiltpadden & dodersen" aboard; 21 April, "veel schilt padden dodeersen ende sommighe gansen & papegayen geuangen". The ship is probably 't Wapen van Amsterdam, whose journal (11 May 1614–3 Dec 1615) is catalogued in this inventory; that attribution needs confirming against the folio numbers.
- **1059_0050–0052, rhymed journal of the same voyage, May–June 1615.** Stanzas numbered c. 182–222; one reads "Mauritius is lustich ... dodersen en patrysen / gansen weert om te prijsen / en schiltpadden daer syn", followed by birds, doves, bats, pigs and goats, fish and parrots, then an attempt to reach "Diogo rodrigos" in June 1615. This is the rhymed journal of Johan Both Volkertsz. van Utrecht, **published** as *De reis naar Oost-Indië van het VOC-schip 't Wapen van Amsterdam in de jaren 1614 en 1615*, ed. L.M. Akveld and J.P. Houterman (MNVZ, 1971).
- **Attribution confirmed (1 Oct 2026).** Scans 1059_0271–0281 carry folio numbers 138–143, inside the catalogue's range for "Journael van 't Wapen van Amsterdam 't sedert 11 Meij 1614 tot 3 December 1615" (fol. 121–152). Scan 0300 carries the endorsement "Journael van 't Wapen van Amsterdam". The dodo entries are therefore on about fol. 141 of the ship's official journal. According to *Batavia berijmd* (UvA dissertation, p. 260, citing Akveld and Houterman 1971, p. 14 n. 21), the journal was kept by Isbrant Cornelisz van Petten. Both Volkertsz used it as the basis of his rhymed *Cort verhaell*. Scan viewer: https://www.nationaalarchief.nl/onderzoeken/archief/1.04.02/invnr/1059/file/NL-HaNA_1.04.02_1059_0277
- **Literature check (1 Oct 2026):**
  - Hume (2006, *Historical Biology*) lists the Dutch dodo accounts and says that after 1611 "the next mention occurred in 1631". No 1615 record.
  - Cheke and Hume, *Lost Land of the Dodo* (Google Books search-inside): 0 hits for "Wapen", "Akveld", "Volkertsz" or "Banda Provintia". It has 4 hits for "1615" whose snippets are hidden; most likely the Pieter Both wreck. The control search "Lamotius" returns 5.
  - Parish, *The Dodo and the Solitaire* (2013), which aims to include all known contemporary accounts. "Wapen" has one hit, p. 28: Pieter Both's 1610 letter from the Wapen van Amsterdam, a different voyage. "Volkertsz", "Akveld" and "dodersen" return 0. "dodeersen" returns 2 (pp. 173 and 401, the name discussion and the index). "Walcheren" has 1 hit (p. 164, secondary sources) and "Petten" 2 (p. 99, illustrations chapter, and the index); none of these could be read. None falls in the written-accounts chapter (pp. 3–54) at a 1615 position.
  - The rhymed version mentioning "dodersen" has been in print since 1971 (MNVZ) and discussed by literary historians since 1850 (Lauts, De Haan, Du Perron, Stapel). The prose journal's dodo entries appear not to have been cited in the dodo literature.
- **Status:** probably overlooked by dodo specialists, though not "unknown to anyone". Still to do: read Parish pp. 99 and 164 and the four Cheke and Hume 1615 pages in a physical copy; check Akveld and Houterman (1971) for whether they quote the prose journal's Mauritius entries; check Hume (2017, *Extinct Birds*, 2nd ed.) and the 2017 *Archives of Natural History* paper on the 1631 manuscript; verify the transcription against the scan.

## 1615 dodo record: verification (1 Oct 2026)

**Scan check.** Read on the Nationaal Archief viewer (inv. 1059, scan 277 of 700, folio number "141" visible at top right). Both machine readings match the hand:
- 17 April: "…souden meede Jagers vuyt die sommighe schiltpadden & dodersen aen boort brochten" (…and sent hunters out, who brought some tortoises and dodos aboard).
- 21 April: "Den 21 dito wederom water gehaelt ende veel schilt padd[en] / dodeersen ende sommighe gansen & papegayen geuangen" (On the 21st again fetched water and caught many tortoises, dodos and some geese and parrots). There is no "ende" between "schilt padden" and "dodeersen", so it is grammatically open whether "veel" (many) governs the dodos as well as the tortoises.
- **A third entry, scan 278** (summary on leaving, 30 April 1615): "Wy hebben al hier opde Moluckse Ree leggende goede ververssinge gecregen, soe van dodeersen, landt ende water schiltpadden met meenichte, veel verckens doch mager, veel bocken die in grote abondantie syn, meede veel schone visch". It also records a deliberate release of livestock: "wy hebben hier oock een schaep ende een Ram met dicke steerten opgeseth die wij van Santa [Lucia] gebracht hadden" (a sheep and a fat-tailed ram brought from Madagascar). Machine reading of scan 278; not yet checked against the image.

**Literature, confirmed directly.**
- Cheke and Parish 2020, *Quaternary* 3(4), Table A1 (PDF read). The chronology runs 1606 Matelief, 1607 Van der Hagen, 1611 Verken, **1616 Almeida, 1617 Van den Broecke**, 1628 Altham, 1629 Herbert, 1629 Le Febvre, 1632? Wallesius, … No 1615 entry.
- Cheke and Hume 2008 (user's screenshots): Appendix 9 lists "1610–15 [Verhuff]" and "1615–20 [van den Broecke, Almeida]". The text says that after Verhoeff (1611) "the Dutch were curiously silent about Dodos until … 1662; there is just one mention in the interval, in 1631". 1615 appears only for the wrecks and the stranded sailors.
- Hume 2006: "the next mention occurred in 1631".
- Parish 2013: no Wapen van Amsterdam 1615, Akveld or Volkertsz hits (Google Books).
- Rhymed version: Both Volkertsz's *Cort verhaell*, edited by Akveld and Houterman (1971); the Mauritius stanza names "dodersen en patrysen".
- Unverified claim from another model: that Winters, Hume and Leenstra (2017) cite Akveld and Houterman (1971) only for livestock. The 2017 paper is listed as ref. 73 in Cheke and Parish; not yet read.

**Status.** Apparently absent from every specialist dodo chronology. Three dated entries (17, 21 and 30 April 1615) fall before the earliest currently recognised post-1611 account (Almeida, 1616). The verse's pairing of dodos with "patrysen" (partridges) is relevant to the red-hen naming question that Cheke and Parish discuss: their table reads Verken's 1611 "rebhüner" (partridges) as probably the red hen.

## Whole-corpus dodo sweep (1 Oct 2026)

- **GLOBALISE vocabulary.** Exact and fuzzy (edit distance ≤ 2) matching against dodo and red-hen names, then a read of every candidate. Genuine dodo pages:
  - 1059_0277–0278 (1615, new);
  - 1059_0051 (1615 verse; published 1971);
  - 1095_0922 (Le Febvre, Nassau, Jan 1629: "bocken, schildpadden, velthoenders, dodeersen, verckens, palmiet, cocosnoten"; **known**, Cheke and Parish 2020);
  - 1164_0738 and 1165_0143 (Japan dodo, 1647: cargo "1 dodeers"; on 2 Sept 1647 "het hert ende den dodeers" viewed at the governor's request and by the lord of Hakata; **known**, Winters and Hume, "The dodo, the deer and a 1647 voyage to Japan");
  - 4005_0603 (Pretorius 1669, known);
  - 4011_0411 (Hugo 1674, known).

  Everything else matched by the patterns was noise: personal names, "Doctoren", Trondheim, cloth names.
- **Delpher newspapers 1618–1799** (`scripts/delpher_dodo_grep.py`; 1,627 articles matched dodo or Mauritius terms). No dodo-the-bird references; the matches are OCR forms of "Doctor", surnames and Trondheim.
- **Embedding pass over pre-1640 Mauritius pages** (`EMBED_RUN=embed_mauritius_early EMBED_YEARS=1595-1640`; 7,895 pages, US$0.83). The 1615 journal pages ranked 163 and 171 and the verse 58 among 273 candidates. The 1629 Nassau page was **not** retrieved: its dodo line sits in a page mostly about crew changes. Recall limitation: one-line mentions in administrative pages need lexical search alongside embeddings.

## Early-period reading results (1 Oct 2026)

Three readers covered all 270 candidates from the pre-1640 pass. No dodo or red-hen name appears beyond the pages already listed. Additional items:

- **Gooyer, 20 Dec 1638 (inv. 1128, fol. 251–252, scans 0359–0361; original letter from the fort at the South-East Harbour).** On 3 November 1638 Gooyer sailed round Mauritius in the newly built yacht and found it "over al vol vees soo van bocken varkers koebeesten gansz velthoenderen eenden duijnen als ander vees en over al vis rijck" (everywhere full of game, goats, pigs, cattle, geese, field-hens, ducks, doves, and rich in fish). It is the first Dutch commander's own report, made in the settlement's first months.
  - **Published in French.** Bonaparte, *Le premier établissement des Néerlandais à Maurice* (1890), pp. 39–40, renders the list as "chèvres, cochons, vaches, oies, **perdrix**, canards, pigeons".
  - **Why it matters.** Cheke and Parish (2020, citing Bonaparte as ref. 8) state that faunal accounts for the first settlement (1638–58) are lacking and that "the limited Dutch accounts only refer to introduced ungulates", calling it a lacuna. Their own Table A1 reads the Dutch "velthoenders" of 1629 (Le Febvre) and c. 1632 (Wallesius) as the red hen.
  - **Status.** Gooyer's "velthoenderen" is therefore a probable red-hen record (with the endemic goose and duck plausible) from Nov 1638, inside the period they describe as empty. The translation as "perdrix" probably hid it. Published, but apparently not counted. No dodo is mentioned.
- **Inv. 1104, scans 0765–0766, copy letter of 1631–32 (fol. 419–420).** Pigs released on Mauritius "Anno 1605" have multiplied. They are caught in covered pits baited with dead "schilpadden" (tortoises or turtles) or fish, and the writer took six or seven in a night in 1615. The writer is unidentified; possibly someone on the 1615 Wapen van Amsterdam visit (J.D. Lam was later in Banda; this needs checking). Relevant to the chronology of introduced predators.
- **Inv. 1131, scan 1748, Gooyer, July 1638.** A greyhound bought at the Cape Verde islands to hunt Mauritius's feral pigs and goats.

## Out-of-distribution probes (1 Oct 2026)

- **Printed English and Cape calendars** (Internet Archive full text, 211 volumes): Foster, *English Factories in India*; Danvers and Foster, *Letters Received by the EIC*; Sainsbury, *Calendar of State Papers, East Indies*; *Court Minutes of the EIC*; Leibbrandt, *Précis of the Archives of the Cape*. No dodo references. The "Dodo" hits are the Japanese honorific "Dono" misread by OCR, plus cassowaries. Texts cached in the session scratchpad only.
- **Lead: the "cassowary" sent to Jahangir, 1625.**
  - VOC Surat letters by Pieter van den Broecke (inv. 1084 scan 0134; copy in inv. 1085 scan 0390; April 1625) record sending senior merchant Hendrick Arentsz. Vapour to Agra "met den Casuwaris vogel" for the emperor: "twijffele niet ofte den casuwaris vogel sal aengenaem wesen, daer het heele lant alree vol van is".
  - Inv. 1090 scan 0626 reports that "Den Coninck Is de Casuaris boven maten aengenaem geweest" and that Vapour was honoured.
  - Inv. 1100 scan 0784 (Agra accounts) pays "de Man vande Caffel die de casuwaar ons thuijs brachte".
  - Origin of the bird not stated. Real cassowaries were at Dutch posts in Banda and Amboina (e.g. inv. 1074 scan 0170, 1621).
  - **Why it matters.** Ustad Mansur's Mughal dodo painting is dated c. 1625 and its route to Jahangir's court is unknown (Parish 2013, p. 74). Van den Broecke drew dodos on Mauritius in 1617, and Dutch writers compared dodos to cassowaries. It is possible, though unproven and probably less likely than a true cassowary, that the 1625 "casuwaris" was a dodo. To test it: the ship and route that brought the bird to Surat (1623–24 arrivals), whether a cassowary painting survives from Jahangir's atelier, and the Jahangirnama.
- **Cassowary trace (1 Oct 2026).**
  - Van den Broecke's printed journal (*Wonderlijcke historische ende journaelsche aenteyckeningh*, 1648; IA `wonderlijckehist00broe`) records only the dispatch: "Den 30 dito [March 1625] sondt ick den Opperkoopman Hendrick Arentsz Vapour, met een Casuwaris, met een Caffila na Agra, om den Coninck den Casuwaris te presenteren". No arrival or origin is given.
  - Ships reaching Surat beforehand came mainly from Batavia (Oct 1624: Nieuw Bantam, Zuydt-Hollandt, Weesp), plus the Dordrecht from the Netherlands. Batavia–Surat ships did not call at Mauritius.
  - The gift-list screen (below) shows cassowaries were a routine VOC diplomatic present across Asia: "Casawaris vogels om aanden Coninck te seijnde" (1635), "1 Casuaris Vogel ongetaxeert" (1644), a cassowary taken to Osaka (1656), and many more.
  - Conclusion: the 1625 bird was almost certainly a real cassowary. The dodo hypothesis is weak; keep it as a footnote only.
- **Gift and cargo screen (1 Oct 2026).** Scripts `embed_gifts.py`, `embed_gift_windows.py`, `llm_screen_windows.py`.
  - Pool: 7,453 pre-1700 GLOBALISE pages matching gift or rarity words and animal words.
  - Whole-page embedding (US$0.83) and 500-character passage embedding (US$0.21) both **failed** the recall check. The known Japan cargo line "1 dodeers" ranked 2,293rd of 7,415: the embedding model does not know the word.
  - gpt-5.4-mini then read all 8,287 windows (1.61M input tokens). It flagged 914 items; 460 had quotes actually present in the text.
  - The model **invented** a "1 dodeers" quote for inv. 1053 scan 0430, so quotes must be checked against the source automatically.
  - Verified results: no new dodo or red hen in gift or cargo lists. Real hits are cassowaries, birds of paradise, lories, cockatoos and ostriches as diplomatic gifts, and metaphorical bird language ("een vogel welkers vleugelen te kort zijn", Ternate 1685).
  - Method lesson: for one-word mentions in lists, use lexical search plus an LLM reader with quote verification; embeddings do not help.
- **Exotic-animal pipeline.** Inv. 3992 scan 0916 (1657): ostriches sent from the Cape to Batavia, the survivors forwarded "voor een rariteijt nae Jappan". The same channel as the 1647 dodo.

## Next steps

- Check each candidate against the scan (GLOBALISE viewer) and against Cheke and Hume (2008) before treating it as new.
- Read neighbouring pages for items 1, 2 and 6 in full.
- Extend the same method to the Cape volumes (bluebuck, quagga), where published coverage of the unpublished VOC papers is thinner.
