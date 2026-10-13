# Cape screening runs and BHL name sweep, 4 October 2026

Internal research record. Machine transcriptions and model flags below have not been checked against scans unless stated. No public atlas data was changed.

**Update, 10 October:** [Manuscript and printed-edition checks](2026-10-10-cape-equid-verification.md) date the Wagenaer letter containing scan 0639 to **19 April 1665**, replacing the provisional 1666 attribution below. The 1689 equid passage is Schrijver's entry for **28 January**, printed in Godée Molsbergen (1922), III, pp. 103–104; its predominant course is **east-northeast**, not north-northeast. Neither animal is yet identified securely as a quagga.

## Screening validator repair

The first live screening run (TANAP Council of Policy, bluebuck case) returned 120 accepted flags and 1,012 rejected ones, and missed both hunting-regulation controls. The rejected quotations were not invented:

- 676 quoted text that occurs in the pool; most gave the wrong bracketed window number within the batch.
- Most of the remaining 336 joined real fragments with ellipses.

`validate_flags` now accepts a quotation found in a different window of the same batch only when all matching windows belong to one page, and accepts elided quotations only when every fragment of two or more words occurs in order in one window. Both repairs are recorded per flag (`repairs`). The prompt now asks for one contiguous quotation and the correct window number. Screening results are re-validated from the saved response journal, so the repair needed no new API calls. All 35 harness tests pass.

After re-validation: 802 accepted flags (673 with a corrected window number, 9 elided), 330 rejected, and 2/2 TANAP hunting controls recovered.

## TANAP Council of Policy (bluebuck case)

- Pool: 1,377 edition sections; 18,780 windows; 752 batches. Actual cost US$6.37 (gpt-5.4-mini).
- No bluebuck reference. The single "bluebuck" flag is a false positive: "kirmansse bocken" imported on 't Huijs te Assenburg (C. 71, 23 January 1725), i.e. Kerman goats for breeding.
- Model precision is low in the shipment category (enslaved people, salt meat and gunpowder were flagged as "shipments"). A second, stricter reading pass is needed before review.

## Lead: live "striped asses" for the king of Kandy, 1737–c. 1776

Not an atlas species as it stands; the animals could be zebras (most likely Cape mountain zebra) or quaggas. Recorded because the quagga cannot yet be excluded and because the episode is a well-documented live-animal transfer.

1. **Request and bounty.** Council of Policy, 17 June 1738, C. 107, pp. 53–65 (TANAP edition): Ceylon asked for "twee a drie leevendige gestreepte ezels, soodanig als deselve ter deeser plaatse in het wilde loopende worden gevonden" as a present for the Kandyan king; the Council posted notices offering 100 rixdollars per live animal delivered to the Castle. [Edition](https://docs.globalise.huygens.knaw.nl/tanap/cape-transcriptions/Council-of-Policy/TKF3_C101-C110/C107_v1.20/)
2. **Ceylon's acknowledgement.** GLOBALISE inv. 2429, scan 0782 (Ceylon to Cape, copy, 1738): pleased that the Cape had offered the 100-rixdollar premium; repeats the request.
3. **Failure.** Inv. 2457, scan 0759 (1738–39): despite efforts the Cape had not yet obtained "de geEyschte Leevendige gestreepte Ezels tot geschenck voor den [Candiasen vorst]".
4. **Delivery.** Inv. 3484, scans 0304–0305 (Cape to Ceylon, volume 1775–78): the Cape happened to have "twee Jange en fraaije gestreepte wand Ezels, die niet algemeen zeldzaam te bekomen zijn"; they were taken overland to False Bay and shipped on Willem de Vijfde for Ceylon. Exact date of the letter not yet established.

Related but separate: inv. 1313, scan 1434 (1674–75) translates an Abyssinian royal letter sending four horses and "twee gestreepte wout ezels" (Ethiopian embassy to Batavia; presumably Grevy's zebra), and inv. 1330, scan 0703 (1675–78) reports failure to obtain striped wild asses on the Red Sea coast.

To do: check zebra/quagga and Kandyan court literature for the 1738 request and the c. 1776 shipment; date the 3484 letter; look for Ceylon/Kandy records of the animals' arrival; see whether "wand Ezels" (wild asses) is ever distinguished from "quacha" in contemporary Cape usage.

## BHL bulk OCR name sweep

`scripts/bhl_stream_sweep.py` streams the full BHL OCR export (May 2026; 45 GB compressed) once without extracting it, matching the distinctive names in `data/curated/bhl_sweep_vocab.json` (20 taxon groups: the atlas species plus other pre-1900 extinctions with distinctive names). Common words and living plant genera are excluded by design. Outputs (Git-ignored): `results/bhl_sweep/hits.jsonl`, then `annotate` joins BHL item/title metadata (year, language, title) and writes `early_hits.jsonl` for items dated 1860 or earlier. Documented noise rules mark (not delete) pre-1598 Mascarene hits, bare 'dodo(s)' in Latin books (OCR of 'doctos', split 'Dodonaeus') and 'tzeiran' (usually the Persian gazelle).

Status at stop (4 Oct, 20:30): 63,488,644 pages searched, 75,891 hit pages, 15,006 signal hits in items dated 1860 or earlier. The sweep was stopped before the end of the archive (one crash on an unexpected member name, now handled). `sweep` resumes from `results/bhl_sweep/checkpoint.json`, but must re-decompress the first 63.5M pages (about 50 minutes) before searching new ones. The early-hit list has not yet been reviewed; pre-1800 dodo hits still contain OCR noise.

## GLOBALISE Cape (bluebuck case)

**Broad scope abandoned.** The `bluebuck-cape-globalise` screen completed 506 of 3,763 batches (US$3.83) before the OpenAI credit balance ran out (also interrupted by the machine hibernating 14:40–18:39). The completed batches covered general correspondence volumes (VOC 1188–1379, 10427) that the catalogue filter had selected because they contain some Cape document; their pages mostly concern Ceylon, Bengal and Bantam. All seven "bluebuck" flags there were false positives (blue cloth, goat skins). Of the broad pool, 23,695 pages (48.7M characters) lie in the Cape series VOC 3988–4360; 8,898 pages are general volumes.

**Budget run (Benjamin: at most US$5).** Case `bluebuck-cape-priority-globalise`: VOC 3988–4360 only; a free lexical triage scores each window by distinct game/hunting/travel cues (`screen.window_priority`), keeps up to 11,000 windows with at least one cue, and screens them highest-score first; `screen.max_spend_usd` = 4.00 stops dispatch on actual reported usage. Result: 384 of 440 batches screened, US$3.77 at harness price constants; 56 lowest-priority batches unscreened. Both expedition game controls recovered. 1,586 accepted flags.

- **No bluebuck.** All 11 "bluebuck" flags are false positives: blue stones, the Blaauwberg, Kerman goats, goats on islands. Neither the corpus-wide spelling sweep nor this reading found any bluebuck name or description in the Cape series, within the limits of HTR, triage and an incomplete run.
- **Lead: Wagenaer 1666 on striped "wild horses".** VOC 4000, scan 0639 (Commander Zacharias Wagenaer and council to the Seventeen, volume 1664–66; letter of 16 May 1666 in the same volume, exact letter not yet confirmed). Reports "wilde paerden", "ongemeene groote bocken" near waterholes 14–15 miles from the fort that come to drink at night, and the commander's plan to catch them alive after the rains. Some horses are "met bruijne streepen alleen, andere met blauwe geele rootachtige stralen / vergelijckende die bij een regenbooch / over 't geheele lichaem". A distinction between brown-striped-only and fully striped animals reads like an early quagga/zebra contrast; the "uncommonly large bucks" are unidentified (eland is the obvious candidate). Machine reading only; check the scan, the Wagenaer dagregister, Leibbrandt's précis, Skead and the quagga literature. A first web search (4 Oct) found no citation; a SAHistory quagga essay describes the early Cape record of quagga versus mountain zebra as unclear and gives Van Riebeeck's 1657 'horse' spoor near Paarl as the first equid mention (https://sahistory.org.za/sites/default/files/archive_files/The%20Quagga%20%28Equus%20quagga%20quagga%29.pdf).
- **Lead: 1689 expedition shoots a striped wild ass.** VOC 4027, scan 0226 (journal copied with Van der Stel's letters of 1690), duplicate in VOC 4029, scan 0375: in a mountain pass, "een rare soort van wilde Esels ... van dewelke wij er een schooten, hebbende de groote van een paard, en bruijn en grauw gestreept". Course mostly north-northeast; the party named a valley "de Goede Hoop". Identify the expedition (possibly Isaq Schrijver's expedition, which left on 4 January 1689) and check whether its journal is published and cited for quagga or Cape mountain zebra.
- 1752 expedition journal (VOC 4187, scan 0202): a buck killed by a leopard, near the size of a female hartebeest, thick-necked, brown-yellow, white below. Not a bluebuck description.

Unscreened: the 56 lowest-priority batches of the budget run; the rest of the Cape series (windows with no cue); TANAP sections were fully screened. The Cape-series full case (`bluebuck-cape-series-globalise`, about US$14) is configured for a later run.
