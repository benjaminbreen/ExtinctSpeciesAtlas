"""Build the three committed, standalone bilingual source records.

Run after editing the source data below. The published site needs no build step.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECONDARY = {
    "amigues": (
        "Suzanne Amigues, “Le silphium — État de la question,” Journal des Savants (2004), 191–226.",
        "A close study of ancient evidence for the plant's range, identification, and later testimony.",
        "https://www.persee.fr/doc/jds_0021-8103_2004_num_2_1_1685",
    ),
    "briggs": (
        "Lisa Briggs and Jens Jakobsson, “Searching for Silphium: An Updated Review,” Heritage 5 (2022), 936–955.",
        "Surveys the sources, material evidence, trade, and proposed botanical identifications.",
        "https://doi.org/10.3390/heritage5020051",
    ),
    "parejko": (
        "Ken Parejko, “Pliny the Elder’s Silphium: First Recorded Species Extinction,” Conservation Biology 17 (2003), 925–927.",
        "Reads Pliny's scarcity report as a possible account of human-driven extinction.",
        "https://doi.org/10.1046/j.1523-1739.2003.02067.x",
    ),
    "roques": (
        "Denis Roques, “Synésios de Cyrène et le Silphion de Cyrénaïque,” Revue des Études Grecques 97 (1984), 218–231.",
        "A study focused on Synesius's letters and the problem of late silphium testimony.",
        "https://doi.org/10.3406/reg.1984.1380",
    ),
}
SOURCES = {
    "herodotus": {
        "author": "Herodotus",
        "work": "Histories 4.169",
        "period": "Fifth century BCE",
        "language": "Ancient Greek",
        "scope": "Complete section 4.169",
        "summary": "A geographic statement within Herodotus's account of Libyan peoples. The plant is placed between named coastal landmarks; no botanical description is given.",
        "place": "Cyrenaica",
        "place_note": "Reported coastal span; endpoints uncertain",
        "original_source": "https://penelope.uchicago.edu/Thayer/H/Roman/Texts/Herodotus/4G%2A.html",
        "original_label": "Greek text at LacusCurtius",
        "other_source": "https://lexundria.com/hdt/4.169/mcly",
        "other_label": "Macaulay's historical translation",
        "original": [
            "Τούτων δὲ ἔχονται Γιλιγάμαι, νεμόμενοι τὸ πρὸς ἑσπέρην χώρην μέχρι Ἀφροδισιάδος νήσου. ἐν δὲ τῷ μεταξὺ τούτου χώρῳ ἥ τε Πλατέα νῆσος ἐπικέεται, τὴν ἔκτισαν οἱ Κυρηναῖοι, καὶ ἐν τῇ ἠπείρῳ Μενέλαος λιμήν ἐστι καὶ Ἄζιρις, τὴν οἱ Κυρηναῖοι οἴκεον, καὶ τὸ σίλφιον ἄρχεται ἀπὸ τούτου·",
            "παρήκει δὲ ἀπὸ Πλατέην νήσου μέχρι τοῦ στόματος τῆς Σύρτιος τὸ σίλφιον, νόμοισι δὲ χρέωνται οὗτοι παραπλησίοισι τοῖσι ἑτέροισι.",
        ],
        "english": [
            "Next to these are the Gilligamae, who occupy the country westward as far as the island of Aphrodisias. In the intervening country lies the island of Platea, which the Cyreneans settled. On the mainland are Menelaus's harbor and Aziris, where the Cyreneans lived; silphium begins there.",
            "Silphium extends from the island of Platea as far as the mouth of the Syrtis. The customs of these people resemble those of the others.",
        ],
        "notes": [
            "The passage's frame is an account of the Gilligamae, not a botanical description. Its named endpoints should not be treated as precise coordinates or as proof that every part of the intervening land supported the plant.",
            "Cyrenaica is the regional association used by the atlas. Platea, Aziris, Menelaus's harbor, and the Syrtis appear in the text; their modern identifications need separate source work before point mapping.",
        ],
        "reading": ["amigues", "briggs"],
        "neighbors": (None, "pliny"),
    },
    "pliny": {
        "author": "Pliny the Elder",
        "work": "Natural History 19.38–40",
        "period": "First century CE",
        "language": "Latin",
        "scope": "Continuous passage, sections 38–40",
        "summary": "Pliny describes the Cyrenaic plant, its valued resin, its reported scarcity, and substitute resin still reaching Rome from other regions.",
        "place": "Cyrenaica",
        "place_note": "Growing region; Rome is a destination in the account",
        "original_source": "https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Pliny_the_Elder/19%2A.html",
        "original_label": "Latin text at LacusCurtius",
        "other_source": "https://peterburk.github.io/pliny/ChaptersHtml/19.%20Book%20XIX.%20The%20Nature%20And%20Cultivation%20Of%20Flax,%20And%20An%20Account%20Of%20Various%20Garden%20Plants./15.%20Chap.%2015.-Laserpitium,%20Laser,%20And%20Maspetum..html",
        "other_label": "Bostock and Riley translation",
        "original": [
            "Ab his proximum dicetur auctoritate clarissimum laserpicium, quod Graeci silphion vocant, in Cyrenaica provincia repertum, cuius sucus laser vocatur, magnificum in usu medicamentisque et ad pondus argentei denarii repensum.",
            "Multis iam annis in ea terra non invenitur, quoniam publicani, qui pascua conducunt, maius ita lucrum sentientes depopulantur pecorum pabulo. unus omnino caulis nostra memoria repertus Neroni principi missus est. si quando incidit pecus in spem nascentis, hoc deprehenditur signo: ove, cum comederit, dormiente protinus, capra sternuente crebrius.",
            "Diuque iam non aliud ad nos invenitur laser, quam quod in Perside aut Media et Armenia nascitur large, sed multo infra Cyrenaicum, id quoque adulteratum cummi aut sacopenio aut faba fracta; quo minus omittendum videtur C. Valerio M. Herennio cos. Cyrenis advecta Romam publice laserpicii pondo XXX, Caesarem vero dictatorem initio belli civilis inter aurum argentumque protulisse ex aerario laserpicii pondo MD.",
        ],
        "english": [
            "Next in importance comes the much celebrated laserpicium, which the Greeks call silphion. It was found in the province of Cyrenaica. Its juice is called laser; it was highly prized for ordinary and medicinal uses and weighed against silver denarii.",
            "For many years now it has not been found in that land, because the contractors who rent the pastures, finding greater profit in it, devastate the plant as fodder for their flocks. In our own time only one stalk was found, and it was sent to the emperor Nero. If an animal comes upon a growing shoot, one can tell: after eating it, a sheep immediately sleeps, while a goat sneezes repeatedly.",
            "For a long time the only laser reaching us has been what grows abundantly in Persia, Media, and Armenia. It is much inferior to the Cyrenaic product, and even it is adulterated with gum, sagapenum, or ground beans. It should therefore be remembered that, in the consulship of Gaius Valerius and Marcus Herennius, thirty pounds of laserpicium were officially brought from Cyrene to Rome; and that Caesar, at the beginning of the civil war, brought out fifteen hundred pounds from the treasury along with gold and silver.",
        ],
        "notes": [
            "Pliny's 'not found in that land' refers to Cyrenaica. In the next section he explicitly distinguishes the Cyrenaic product from resin imported from Persia, Media, and Armenia. His narrative is evidence for scarcity and changing supply, not a securely dated last surviving plant.",
            "The passage attributes destruction to pasture contractors. That is Pliny's explanation, not independently verified evidence for the cause of disappearance. Section numbering follows the continuous Latin text; some English editions call the chapter 19.15.",
        ],
        "reading": ["parejko", "amigues", "briggs"],
        "neighbors": ("herodotus", "synesius"),
    },
    "synesius": {
        "author": "Synesius of Cyrene",
        "work": "Letter 106",
        "period": "Early fifth century CE",
        "language": "Ancient Greek",
        "scope": "Complete letter",
        "summary": "A letter to his brother about silphium brought from a garden. The text uses the ancient name but does not identify the plant botanically or name the garden's town.",
        "place": "Cyrenaica",
        "place_note": "Regional context; town not stated in the letter",
        "original_source": "https://eulogikon.org/works/synesius-cyrene-letters-nicander-sys-ah",
        "original_label": "Greek text of Letter 106",
        "other_source": "https://www.livius.org/sources/content/synesius/synesius-letter-106/",
        "other_label": "Fitzgerald translation and context",
        "original": [
            "Ἠρόμην τὸ μειράκιον ὑπὲρ τοῦ σιλφίου πότερον ἀπὸ γεωργίας σοι γέγονεν, ἢ δῶρον λαβὼν ἔθου μερίδα κἀμοί. καὶ δῆτα μαθὼν ὡς τὸ σπουδαζόμενον ὑπὸ σοῦ κηπίον πρὸς ἅπασι καὶ τοῦτον ἐκόμισε τὸν καρπόν, ἥσθην διπλῇ, τῷ τε κάλλει τοῦ λαχάνου καὶ τῇ φήμῃ τοῦ τόπου.",
            "ὄναιο τοῦ παμφόρου χωρίου, καὶ μήτε σὺ κάμοις ἐπαντλῶν ταῖς φιλτάταις πρασιαῖς, μήτ’ ἐκεῖναί ποτε πρὸς τὰς ὠδῖνας ἀπαγορεύσειαν, ἵν’ ἔχοις αὐτός τε χρῆσθαι καὶ ἡμῖν διαπέμπειν ὅσα φέρουσιν ὧραι.",
        ],
        "english": [
            "I asked the young man about the silphium: had it come to you from cultivation, or had you received it as a gift and set aside a portion for me? When I learned that the garden you care for had produced this yield too, along with everything else, I was pleased twice over: by the beauty of the plant and by the reputation of the place.",
            "May you enjoy that fertile plot. May you not tire of watering your beloved beds, nor may they ever cease to produce, so that you have enough for yourself and can send us whatever the seasons bring.",
        ],
        "notes": [
            "The letter is addressed to Synesius's brother Euoptius. The garden's town is not named in these lines. Associating it with Ptolemais comes from the broader correspondence and modern editorial context, not from Letter 106 itself.",
            "The Greek word καρπός can mean fruit, produce, or yield; the translation here uses 'yield.' The letter shows that a plant called silphium was cultivated and exchanged, but its identity with earlier Cyrenaic silphium cannot be proven from the name alone.",
        ],
        "reading": ["roques", "amigues"],
        "neighbors": ("pliny", None),
    },
}


def external_link(url, label):
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} ↗</a>'


def page(key, item):
    title = f'{item["author"]} — {item["work"]}'
    original_lang = 'la' if key == 'pliny' else 'grc'
    original = ''.join(f'<p>{escape(text)}</p>' for text in item['original'])
    english = ''.join(f'<p>{escape(text)}</p>' for text in item['english'])
    notes = ''.join(f'<p>{escape(text)}</p>' for text in item['notes'])
    bibliography = ''.join(
        f'<li><span>{n:02d}</span><div><a href="{escape(SECONDARY[ref][2], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(SECONDARY[ref][0])} ↗</a><br>{escape(SECONDARY[ref][1])}</div></li>'
        for n, ref in enumerate(item['reading'], 1)
    )
    previous, next_ = item['neighbors']
    next_links = ' · '.join(f'<a href="./source-{neighbor}.html">{escape(SOURCES[neighbor]["author"])} ↗</a>' for neighbor in (previous, next_) if neighbor)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#f5f2e9" />
  <meta name="description" content="{escape(item['summary'], quote=True)}" />
  <title>{escape(title)} — Atlas of Historically Lost Species</title>
  <link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" />
  <link rel="preload" href="./assets/gfs-didot.ttf" as="font" type="font/ttf" crossorigin />
  <link rel="stylesheet" href="./styles.css" />
  <link rel="stylesheet" href="./detail.css" />
  <script type="module" src="./main.js"></script>
</head>
<body data-page="source">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-seal" aria-hidden="true"><span class="seal-symbol"></span></div>
  <div class="page-shell">
    <header class="masthead"><a class="wordmark" href="./index.html" aria-label="Atlas home">Atlas<span class="wordmark-period">.</span></a><nav aria-label="Main navigation"><a href="./index.html#index">Index</a><a href="./index.html#about">About</a></nav></header>
    <main id="main">
      <nav class="source-breadcrumb" aria-label="Breadcrumb"><a href="./silphium.html#record">Silphium</a> / Primary source / {escape(item['author'])}</nav>
      <header class="source-head"><div><span class="folio-label">Primary source · {escape(item['period'])}</span><h1>{escape(item['author'])}</h1><p class="source-deck"><i>{escape(item['work'])}</i>. {escape(item['summary'])}</p></div>
      <div class="source-head-meta"><dl><div><dt>Passage shown</dt><dd>{escape(item['scope'])}</dd></div><div><dt>Original language</dt><dd>{escape(item['language'])}</dd></div><div><dt>Place in record</dt><dd><a href="./index.html?place=cyrenaica#index">{escape(item['place'])} ↗</a><br>{escape(item['place_note'])}</dd></div></dl></div></header>
      <div class="source-grid" aria-label="Original text and English translation">
        <section class="source-column" aria-labelledby="original-title"><div class="source-column-head"><h2 id="original-title">Original text</h2><span>{escape(item['language'])}</span></div><div class="source-text" lang="{original_lang}">{original}</div></section>
        <section class="source-column" aria-labelledby="translation-title"><div class="source-column-head"><h2 id="translation-title">English</h2><span>New working translation for this atlas</span></div><div class="source-text">{english}</div></section>
      </div>
      <section class="source-notes" aria-label="Notes and text provenance"><div><h2>Reading the passage</h2>{notes}</div><div><h2>Text and translation</h2><p>The English beside the original is a working translation prepared for this atlas. Consult the linked editions for textual variants, notes, and alternative translations.</p><div class="edition-links">{external_link(item['original_source'], item['original_label'])}{external_link(item['other_source'], item['other_label'])}</div></div></section>
      <section class="further-reading" aria-labelledby="further-title"><h2 id="further-title">Further reading</h2><p class="source-reading">Scholarship that discusses silphium and helps interpret this source. Linked works may differ in their conclusions.</p><ol class="further-list">{bibliography}</ol></section>
    </main>
    <footer class="site-footer"><span>Atlas of Historically Lost Species</span><span><a href="./silphium.html#record">Back to the silphium record ↗</a>{' · ' + next_links if next_links else ''}</span></footer>
  </div>
</body>
</html>
'''


for key, item in SOURCES.items():
    (ROOT / f'source-{key}.html').write_text(page(key, item), encoding='utf-8')
