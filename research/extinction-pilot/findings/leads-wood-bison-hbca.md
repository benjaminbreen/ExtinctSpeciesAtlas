# Leads: wood bison in Hudson's Bay Company post journals (tractability check)

Checked 7 October 2026. Readings below are mine from the microfilm PDF and have not been verified by a second reader.

## Why

Oppenheimer et al. (Green, Shapiro; *Science* 2026, doi:10.1126/science.aee4205; preprint doi:10.64898/2025.12.24.696034) find that the wood bison decline at Wood Buffalo began nearly 200 years before the plains decline, "possibly coinciding with the expansion of the Canadian fur trade". Dated, located kill counts and scarcity reports from Athabasca and Peace River posts would test this.

## Access

- HBCA digitized 1,052 microfilm reels (pre-1870 post records) in 2018–19 as image-only multi-page PDFs. No OCR or HTR.
- Keystone listings search works in a normal browser (the built-in pane and the old pam.minisisinc.com/pam links fail): `https://pam.minisisinc.com/scripts/mwimain.dll/144/PAM_LISTINGS?DIRECTSEARCH`, keyword plus "Digital Copies".
- "Chipewyan" returns 314 listings, including Fort Chipewyan post journals almost every year 1802–1871, correspondence books 1818–1868 and Athabasca District accounts from 1817.
- PDFs are at a predictable path and download with curl: `https://PAM.MINISISINC.COM/DIGITALOBJECTS/Access/HBCA%20Microfilm/{reel}/{code}.pdf`, e.g. reel 1M23, B.39/a/21b (Fort Chipewyan 1822–23) → `1M23/B39-A-21B.pdf` (41 page images, 19 MB).

## Test volume: Fort Chipewyan post journal 1822–23 (B.39/a/21b)

The hand is clear and readable at 150–260 dpi.
- 10 Sept 1822: men sent out with "170 lb Pemmican & 171 lb Dry meat as Provisions".
- 31 Dec 1822: André Paquette arrives "from the Hunters. Says they have killed 4 Buffaloes above [?] Point in Peace River at no great distance from the River".
- 13 Mar 1823: A. Pillon "from the Hunters, tells us they have killed 19 Animals — 16 Buffaloes & 3 Moose". Same entry: news from Peace River "does not give us great hopes of getting any quantity of Provisions"; the Indians' produce in provisions "is much reduced, ascribed to scarcity of Animals".
- Daily weights of meat and fish brought in (e.g. 7–11 March 1823: 1,425 lb, 372 lb, 927 lb, 624 lb "meat of 3 large animals").

## Assessment

Tractable. The journals give species, counts, places and explicit scarcity statements. Scale for Athabasca–Peace River posts, 1802–1870, is probably several thousand pages. Reading requires handwriting recognition (a vision model or Transkribus), then a lexical and model screen like the GLOBALISE harness.

## Before claiming novelty

Check Soper 1941 (*Ecol. Monogr.* 11, northern bison history), Stephenson et al. 2001 (wood bison historical records), Colpitts, *Pemmican Empire* (2015), and the sources cited by Oppenheimer et al.

## Pilot run, 7 October 2026: all digitized Fort Chipewyan post journals

**Corpus and method.**
- 48 PDFs, HBCA B.39/a/1–47 (1801–1871; A-37 and A-39 are weather journals and were not included). 2,790 page images, 1.2 GB, in `data/raw/hbca/B39/` (Git-ignored).
- Each image was read by `google/gemini-3.1-flash-lite` through OpenRouter, using `scripts/hbca_screen.py`. The model extracted entries on bison, large game, meat and provisions, and scarcity. Cost US$2.21; 18 images failed.
- Summarised by `scripts/hbca_analyze.py`. Years are anchored to the Keystone volume ranges. Entries duplicated in overlapping copy volumes are dropped.
- B.39/a/2 scans 0–32 are excluded: they are Fidler's Chesterfield House (South Saskatchewan) journal, 1800–02, and concern plains bison.
- After about 1852 "cattle" means the post's domestic stock. It is counted as bison only before 1850, where it is the usual northern usage ("14 Cattle", "Wild cattle").
- Outputs (Git-ignored) in `results/hbca/B39/`: `pages.jsonl`, `entries.jsonl` (8,054 entries), `by_year.csv`, `game_share_5yr.csv`.

**Accuracy.** Entry detection is reliable; numbers are not. Spot checks against the scans:
- 1823 "16 Buffaloes" was read as 18.
- 1826 "54 Deer & Buffaloe wt 18587" was read as "54 Dead Buffalo".
- 1846 "6 Buffaloe" was read as 8.
- 1835 "winter hunt is 24 Moose deer, 12 Buffaloe, & 16 Rein deer… 12,375 lbs" (B.39/a/31 scan 37 = B.39/a/30 scan 36) was read correctly.

Every figure must be checked against the scan before use.

**Provisional result: bison share of large-game mentions (bison / [bison + moose + caribou]), 5-year bins**

| Period | Entries | Bison | Moose | Caribou | Bison share |
|---|---|---|---|---|---|
| 1800–04 | 577 | 22 | 39 | 62 | 0.18 |
| 1805–09 | 219 | 14 | 18 | 24 | 0.25 |
| 1815–19 | 570 | 40 | 24 | 21 | 0.47 |
| 1820–24 | 954 | 64 | 105 | 49 | 0.29 |
| 1825–29 | 382 | 11 | 29 | 20 | 0.18 |
| 1830–34 | 583 | 26 | 72 | 51 | 0.17 |
| 1835–39 | 1358 | 76 | 207 | 112 | 0.19 |
| 1840–44 | 896 | 40 | 169 | 71 | 0.14 |
| 1845–49 | 570 | 25 | 112 | 27 | 0.15 |
| 1850–54 | 403 | 1 | 40 | 15 | 0.02 |
| 1855–59 | 465 | 2 | 37 | 21 | 0.03 |
| 1860–64 | 267 | 0 | 39 | 7 | 0.00 |
| 1865–69 | 670 | 4 | 118 | 33 | 0.03 |
| 1870–74 | 140 | 1 | 16 | 5 | 0.05 |

**Reading (provisional).**
- In the journals of this post, bison are a steady part of the large-game record from 1800 to 1849, at about one sixth to one quarter of mentions. They fall sharply around 1849–50.
- The break occurs inside one volume (B.39/a/42, 1846–52). That reduces, but does not remove, the chance that it reflects a change of keeper or style.
- Bison are still occasionally brought in during the 1860s, e.g. 1869: "3 Buffalo, 1 Buck Moose & 6 deer in cache".
- Scarcity statements cluster early: Dec 1804 (men "starving, finding no Buffalo"); 1821 ("the prospects of the Buffaloes is miserable"); Mar 1823 (Indian provision hunts "much reduced, ascribed to scarcity of Animals").

**Relation to prior work.**
- Ferguson (1993; pre-1840 records, qualitative) argued the decline was well under way before 1840, probably beginning 1800–20. Raup (1933; travellers) put it after 1840, rapid after 1860–70.
- At Fort Chipewyan the share series is flat through the 1840s and breaks about 1850. This is closer to Raup's timing, while the early scarcity complaints match Ferguson's.
- Oppenheimer et al. date the start of the Wood Buffalo decline in effective population size to 52 generations ago. At 7–10 years per generation, counting back from about 2025, that is roughly 1505–1661. Their only citation for the fur-trade link is Geist 1998.

**Framing (Benjamin, 7 Oct 2026): complementary, not competing.**
- The genomic estimate tracks effective population size: a slow, smoothed signal that can register range contraction, fragmentation or gradual pressure, and depends on generation-time assumptions.
- The journals track local harvest year by year from 1800 and capture abrupt change.
- Both can hold: a long early-modern erosion (genomic), then a sharp mid-19th-century inflection at Fort Chipewyan (documentary), then the 1890s low (COSEWIC).
- Candidate early drivers to examine:
  - indirect trade effects via Cree middlemen and guns after 1670;
  - horses and changing Indigenous economies on the southern margin;
  - epidemics, e.g. 1781–82 smallpox, altering hunting pressure;
  - Little Ice Age winters (deep-snow die-offs recorded 1820s–30s; Raup's snow hypothesis).
- Bovine brucellosis and tuberculosis entered Wood Buffalo bison with the 1925–28 plains bison transfers. They belong to the 20th-century story, not the early decline.
- Evidence for the earlier phase: Hearne (1770–72), Pond (1778), Mackenzie (1789); York Factory and Churchill journals 1680s–1770s; Indigenous oral histories; radiocarbon-dated faunal remains.

**Limits.** These are mentions, not counts, and they are machine-read. Mentions depend on hunting grounds, which hunters were employed, the fish/meat balance at a "fish post", competition years (1815–21) and journal style. One post only. The model's numbers are unreliable.

**Next steps.**
1. Verify by eye every bison entry 1840–1855 and a sample from each decade, and correct the counts.
2. Run the same pipeline on the Peace River posts (Fort Vermilion B.224/a, Dunvegan B.56/a) and Fort Resolution (B.181/a). These are closer to the core range and to Wood Buffalo National Park. Cost about $1 per 1,000 images.
3. Extract the annual hunters' accounts and provision totals where they exist, for species composition by weight.
4. Read the Athabasca District reports (B.39/e) for explicit statements on bison status.
