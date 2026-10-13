# Leads: bluebuck (Hippotragus leucophaeus) museum specimens and their provenance gaps

Prepared 7 October 2026. Internal research record. Specimen data below are taken from the open-access text and Supplementary Document S1 of Hempel et al. 2021; nothing here was checked against museum registers. Unverified points are marked.

## Verified references

- **Hempel, E., Bibi, F., Faith, J. T., Brink, J. S., Kalthoff, D. C., Kamminga, P., Paijmans, J. L. A., Westbury, M. V., Hofreiter, M. & Zachos, F. E. 2021.** "Identifying the true number of specimens of the extinct blue antelope (*Hippotragus leucophaeus*)." *Scientific Reports* 11: 2100. DOI 10.1038/s41598-020-80142-2 (PMC7822880, CC BY). Table 1 lists 16 putative specimens; Supplementary Document S1 (file 41598_2020_80142_MOESM7_ESM.pdf) gives provenance notes and Table S1 (lost specimens). Already in `data/bibliography.json` as `hempel`.
- **Hempel, E. et al. 2022.** "Blue turns to gray: paleogenomic insights into the evolutionary history and extinction of the blue antelope." *Molecular Biology and Evolution* 39(12): msac241. DOI 10.1093/molbev/msac241 (PMC9750129). Nuclear genome (3.44×) from NRM 590107 plus Nelson Bay Cave tooth NBC RB4 D3 (9,800–9,300 cal BP). Cites Lichtenstein 1811 and 1814 for extinction "∼1800". No new specimen identifications.
- **Hempel, E. et al. 2024.** "Colonial-driven extinction of the blue antelope despite genomic adaptation to low population size." *Current Biology* 34 (published online 12 April 2024). DOI 10.1016/j.cub.2024.03.051. 40× genome from NRM 590107. A secondary report (Potsdam/SciLifeLab press coverage) refers to "five DNA-validated" specimens, one more than the four in 2021. **Unverified**: the full text was not read and the fifth specimen is not identified here. Check before citing.
- The task brief guessed the 2024 paper was in *MBE*; the *MBE* paper is 2022 and the 2024 paper is *Current Biology*.
- Kerley et al. (2009, range/population model, ~370 individuals) and Faith & Thompson (prehistoric range) are cited by Hempel 2021 for range only; they do not assess specimens. Not read for this record.

## Specimens (Hempel et al. 2021, Table 1 and S1)

Genetically confirmed blue antelope (4):

| Museum, number | Material | Collector / chain stated | Date stated | Locality stated |
|---|---|---|---|---|
| Stockholm NRM 590107 | mounted skin, subadult male; no skull present (Sundevall's c.1840 catalogue said "cr fix") | C. P. Thunberg → A. U. Grill; Grill's heirs donated 1829. Lindroth 1788 *Museum Naturalium Grillium Soderforssiense* cited | before 1788 (implied by Lindroth) | none given |
| Vienna NMW ST 715 | mounted skin, the only female; no skull (X-ray 2017), one phalanx each foreleg | Georg Scholl, during the 1786–88 Cape expedition or his later years there | first recorded in museum 1806 | "Caput bonae spei" only |
| Leiden RMNH.MAM.20681.a ("Leiden 1") | premaxilla and mandible fragments | possibly from the lectotype skin below (Husson & Holthuis 1969) | 1887 catalogue calls it a complete skull | — |
| Uppsala UPSZMC 78488 | pair of horns with fur traces, no frontlet; probably from a skin dismantled after 1846 (1886, 1899 or 1904 suggested) | D. F. Immelmann → Thunberg 1781 (per Rookmaaker) | 1781 | none given |

Not analysed, regarded as probable blue antelope:

| Museum, number | Material | Provenance as stated |
|---|---|---|
| Leiden RMNH.MAM.20681.b | mounted skin, adult male; lectotype | Probably one of Pallas's syntypes seen in the Netherlands (Pallas 1766: skins in The Hague). Swellendam assigned later as locality. History after arrival traced by Husson & Holthuis 1969. Whether a skull is inside is unknown. Note: S1 swaps the a/b labels in one paragraph. |
| Paris MNHN-ZM-MO-1994-1103 | mounted skin, adult male; mannequin, no bone | Catalogue says collected by "Delegorgue" (rejected: travelled after extinction). Two hypotheses: R. J. Gordon specimen sent to J. N. S. Allamand c.1780 → Stadholder William V's cabinet → Paris 1795 (Rookmaaker 1989); or shot by Le Vaillant 1781 and sold to MNHN as "une grande gazelle non décrite" (Glenn 2020, *Zoosystema* 42: 77–84). Unresolved. |
| London NHMUK GERM 636e | frontlet with horns | "provisionally referred" (Lydekker 1914); "long in the Museum" (Sclater & Thomas 1899). Possibly from Pennant's Amsterdam skin (Renshaw 1904; Mohr 1967 calls the match inconclusive), or bought by W. E. Leach at an 1819 London auction. |
| Brussels RBINS 3785 | skull or horns (records disagree); not accessed | Donated 1931 by Louis Giltay with six other horn pairs; "cf. leucophaeus" in catalogue; earlier history unknown. |

Genetically shown to be other species (6): St Andrews BPM 2234, frontlet (roan; no history); Paris MNHN-ZM-AC-1896-100, cranium (roan; catalogue: Senegal, donor "Houdelot(?)"); Berlin ZMB MAM 8859, cranium (roan; no date, locality, sex); Glasgow GLAHM:Z4884, skull (sable; identified as bluebuck by Broom 1949, in museum before 1923); Cape Town SAM ZM 40759, frontlet (sable; ex J. Piek collection, donated 1989; Ozinsky 1989); Leiden ZMA.MAM.18623, skull (sable; ex Zoölogisch Museum Amsterdam; once guessed to be the remains of De Mist's 1805 Haarlem skin).

Not analysed, now labelled otherwise: Berlin ZMB MAM 8855 (cranium, female, "South Africa", relabelled sable after Mohr); ZMB MAM 8860 (skull, male, Sudan, collector Schweinfurth; labelled roan).

Lost (Table S1): Albany Museum horns (Report for 1901; possibly fire; nine genus-only *Hippotragus* specimens now at Amathole Museum unchecked); Royal College of Surgeons cranium no. 1356 (1884 osteology catalogue; before 1861; probably destroyed 1941; Mohr: roan); Haarlem skin with horns (De Mist to Van Marum, 1805); Pennant's Amsterdam skin (before 1781); a possible Berlin skin used by Lichtenstein 1814 (Renshaw: "In 1799 a leucophaeus was shot and sent to Berlin"; no Berlin record now); further NHM London frontlets mentioned by Lydekker 1908.

## What the atlas already has

- `data/passages.json`: `pennant-bluebuck` (Pennant 1771, pp. 24–25, Amsterdam skin) and `barrow-bluebuck` (Barrow 1804, II, p. 47, reported herd "a few months before we evacuated the Cape", i.e. c.1802–03, uncertain).
- `data/bibliography.json`: Husson & Holthuis 1975 (earliest figures), Rookmaaker 1989 (species account 49), Hempel 2021.
- GLOBALISE Cape series and TANAP Council of Policy screens (findings 2026-10-03 and 2026-10-04) found no bluebuck name or description; the Cape-series full case is unrun. These are textual-occurrence screens, not specimen-provenance searches.
- Not yet used: Mohr 1967, Rookmaaker 1992 (*Ann. S. Afr. Mus.* 102: 131–141), Husson & Holthuis 1969 (*Zool. Meded.* 44: 147–157), Glenn 2020, Lichtenstein 1811/1814, Kohl 1886, Lindroth 1788.

## Gaps and documentary leads

1. **Leiden lectotype: which Cape route and sender.** Husson & Holthuis 1969 is the anchor. Leads: Dutch printed sale/cabinet catalogues of the 1760s (Delpher; Pallas's *Miscellanea zoologica* 1766 and *Spicilegia* name the cabinets); Stadholder's cabinet inventories (Vosmaer) in the Koninklijk Huisarchief; VOC return-ship cargo/"rariteiten" lists in GLOBALISE (Cape series VOC 3988–4360, 1760s letters to the Seventeen) for live or dead "blauwe bok" sent to the Netherlands. Tractability: moderate; Husson & Holthuis already did the museum side, so read it first to avoid duplication.
2. **Paris skin: Gordon/William V vs Le Vaillant.** Leads: the 1795 French seizure inventory of the Stadholder's cabinet (Archives nationales / MNHN archives, partly published); Allamand's correspondence with Gordon (Gordon Atlas, Rijksmuseum; Gordon letters in Leiden UB); Le Vaillant's sale to the Muséum (MNHN archives, AM series). Glenn 2020 must be read first; it is the latest argument. Tractability: moderate–good; Gordon material is digitized at the Rijksmuseum.
3. **Stockholm and Uppsala: Thunberg/Immelmann chain.** Leads: Lindroth 1788 Grill catalogue (check BHL/Google Books for the actual entry; **unverified** whether it names Thunberg); Thunberg's *Resa* (1788–93) and *Museum naturalium Academiae Upsaliensis* dissertations (1787–) for the Uppsala horns; Uppsala University Library Thunberg letters (Alvin portal); Immelmann in Cape records (TANAP/Western Cape Archives, MOOC inventories and Council of Policy) to establish when and where he could have obtained an animal. Tractability: good for printed sources; Alvin is searchable.
4. **Vienna: Scholl's date and locality.** Leads: Schönbrunn/Naturalienkabinett acquisition journal (1806 entry), Scholl's letters to Vienna 1786–99 (Haus-, Hof- und Staatsarchiv; NHM Wien archive), Kohl 1886 (BHL). Would fix whether the skin predates or postdates c.1790 and whether "Cape" means Swellendam. Tractability: moderate; manuscript, German, partly undigitized.
5. **London frontlet: Pennant skin or 1819 auction.** Leads: Pennant's own MSS and later editions (*History of Quadrupeds* 1781/1793) for the skin's fate; the 1819 London sale catalogue (probably Bullock's Museum sale; **unverified**) with Leach's purchases, and BM register entries from 1819. Tractability: good; the Bullock sale catalogue is printed and the price annotations are discussed in the literature.
6. **The ~1799/1800 last record.** Hempel 2021/2022 rest on Lichtenstein 1811/1814 and Renshaw's "1799 … sent to Berlin". Barrow (already in atlas) reports a herd c.1802–03 by hearsay, so the terminal date is not secure. Leads: Lichtenstein's *Reisen* (1811) and 1814 *Magazin* article (BHL) for his exact wording and source; Berlin Zoological Museum accession registers 1810–20; Swellendam drostdy records and Cape Gazette 1800–05 (Western Cape Archives; Delpher does not cover Cape Gazette). Tractability: printed part easy; archival confirmation hard.
7. **Haarlem/De Mist 1805 skin.** Leads: Van Marum's diaries and Hollandsche Maatschappij acquisitions (Noord-Hollands Archief; Van Marum diaries published), De Mist's 1802–05 Cape papers; Delpher for an 1805–06 Haarlem notice. Rookmaaker 1992 has details; read first. Tractability: moderate.
8. **Unidentified-genus specimens.** Amathole Museum nine *Hippotragus* sp.; NHM London unlabelled WWII *Hippotragus* sp.; Brussels RBINS 3785. These need museum work or DNA, not documents. Low priority for this project.

## Next actions

Read Rookmaaker 1992, Husson & Holthuis 1969 and Glenn 2020 before any archival search. Then printed sources first: Lichtenstein 1811/1814, Kohl 1886, Lindroth 1788, Bullock 1819 sale catalogue.

## Lichtenstein check (7 Oct 2026)

- **Lichtenstein, *Reisen im südlichen Africa*, vol. 1 (Berlin: Salfeld, 1811), p. 265.** BSB copy, archive.org `10467331bsb`, https://archive.org/details/10467331bsb/page/n296 (checked against page image). Context: 13 Dec. [1803], the day after leaving Zwellendam (p. 264), crossing the Buffelsjagt River toward Duivenhoks River. Text: "aber der schöne Blaubock (*Antilope leucophaea*) ist, wie Barrow richtig behauptet, fast ganz vertilgt. Jm Jahre 1800 war noch einer geschossen, dessen Fell jetzt in Leyden aufbewahrt wird, seitdem aber hat man keine mehr gesehen." Working translation (ours): "but the beautiful bluebuck is, as Barrow rightly maintains, almost entirely exterminated. In the year 1800 one more had been shot, whose skin is now kept in Leiden; since then, however, none have been seen."
  - Establishes: a year (1800), singular ("einer"), skin said to be in **Leiden**, not Berlin. No place of shooting given (only the Swellendam-district context of the remark), no shooter, no informant named; evidently hearsay, cites Barrow for the near-extinction. No Berlin specimen mentioned.
- **Same, vol. 2 (1812), p. 121.** archive.org `10467332bsb`, https://archive.org/details/10467332bsb/page/n132 (image checked). Inland valleys of the mountains between the Gamka/Gouritz area and Zwellendam (1804): "ja selbst der übrigens fast ganz vertilgte Blaauwbok (*Antilope leucophaea*) soll hier noch einzeln vorkommen." Translation (ours): "even the otherwise almost entirely exterminated blaauwbok is said still to occur here singly." Hearsay ("soll"); undermines 1800 as a secure terminal date. Index also lists Blaubock at vol. 1 p. 121 (not checked) and a vocabulary entry (vol. 1, appendix, Xhosa/Tswana name list; not a sighting).
- **Plumptre transl., *Travels in Southern Africa*, vol. 1 (London: Colburn, 1812), pp. 165–166.** archive.org `travelsinsouther01lich`. Renders the sentence "Some were shot so lately as the year 1800, and their skins were brought to Leyden" — plural mistranslation of "einer".
- **Renshaw, *Natural History Essays* (London: Sherratt & Hughes, 1904), "The Blaauwbok."** archive.org `naturalhistoryes00rens`. p. ~46: Lichtenstein "relates that 'some' were shot in 1800" (follows Plumptre). p. ~54, specimen list no. 13: "In 1799 a leucophaeus was shot and sent to Berlin. Dr. Lichtenstein described it in 1814"; nos. 14–16: "Some" shot 1800, skins to Leyden. Renshaw gives no source for 1799 or Berlin in that passage. **Inference:** the 1799/Berlin item is Renshaw's (possibly from the 1814 *Magazin* description or a confusion with the 1800 Leiden skin), duplicated against the Plumptre "some"; not found in *Reisen*.
- **Not checked:** Lichtenstein 1814, *Magazin Ges. naturf. Freunde Berlin* 6 (A. leucophaea entry) — BHL/archive.org search failed to locate a scan this session (archive.org advancedsearch "Magazin naturforschender Freunde Berlin 1814": 0 hits; BHL web search returned nothing parseable). This is the remaining test of whether any 1799 date or Berlin specimen originates with Lichtenstein.
