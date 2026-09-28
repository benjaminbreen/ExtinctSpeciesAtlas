"""Generate the English-language great auk source records.

Transcriptions were checked against the scans linked on each page. The long s
is regularized; wording and historical spellings are otherwise retained.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

READING = {
    "palsson": ("Gísli Pálsson, The Last of Its Kind", "Princeton University Press, 2024.", "https://press.princeton.edu/books/hardcover/9780691230986/the-last-of-its-kind"),
    "thomas": ("Jessica E. Thomas et al., “Demographic reconstruction”", "eLife 8 (2019), e47509.", "https://elifesciences.org/articles/47509"),
    "lucas": ("Frederic A. Lucas, The Expedition to Funk Island", "Report of the National Museum (1888): 493–529.", "https://repository.si.edu/items/c6fcb913-d880-4975-8af9-9f11ce64198f"),
    "birkhead": ("Tim R. Birkhead and Peter T. Gallivan, “Alfred Newton’s contribution to ornithology”", "Ibis 154 (2012): 887–905.", "https://onlinelibrary.wiley.com/doi/full/10.1111/j.1474-919X.2012.01274.x"),
}

SOURCES = {
    "martin": {
        "author": "Martin Martin", "work": "A Late Voyage to St Kilda, chapter II", "period": "1698", "place": "St Kilda", "place_key": "st-kilda",
        "summary": "Martin's description of the Gairfowl records its appearance, egg, inability to fly, and seasonal presence at St Kilda.",
        "facsimile": None, "edition": "A Late Voyage to St. Kilda, the Remotest of All the Hebrides. London: D. Brown and T. Goodwin, 1698, chapter II, p. 27.",
        "primary": ("Full text of chapter II", "https://www.undiscoveredscotland.co.uk/usebooks/martin-stkilda/chapter02.html"),
        "companion": ("1698 edition record", "https://onlinebooks.library.upenn.edu/webbin/book/lookupid?key=olbp96344"),
        "paragraphs": [
            "The sea-fowls are, first, Gairfowl, being the stateliest, as well as the largest of all the fowls here, and above the size of a solan goose, of a black colour, red about the eyes, a large white spot under each eye, a long broad bill; stands stately, its whole body erected, its wings short, it flyeth not at all, lays its egg upon the bare rock, which, if taken away, it lays no more for that year; it is palmypes, or whole-footed, and has the hatching spot upon its breast, i.e., a bare spot from which the feathers have fallen off with the heat in hatching; its egg is twice as big as that of a solan goose, and is variously spotted, black, green, and dark; it comes without regard to any wind, appears the first of May, and goes away about the middle of June.",
        ],
        "note_phrase": "Gairfowl", "note": "Martin visited St Kilda in 1697. Pennant later drew on this description in British Zoology.",
        "reading": ("palsson", "thomas"), "neighbors": (None, "pennant"),
    },
    "pennant": {
        "author": "Thomas Pennant", "work": "British Zoology, vol. II, pp. 507–508", "period": "1776", "place": "St Kilda", "place_key": "st-kilda",
        "summary": "A description of the great auk’s body and breeding season, drawing on Martin Martin’s account of St Kilda.",
        "facsimile": "pennant-507.webp", "facsimile_alt": "Page 507 of Pennant's British Zoology, headed Great Auk", "facsimile_caption": "Pennant, British Zoology, II.507. Scan via Internet Archive / Biodiversity Heritage Library.",
        "edition": "Fourth edition. Warrington: William Eyres for Benjamin White, 1776. Volume II, pages 507–508; plate LXXXI.",
        "primary": ("Scanned volume", "https://archive.org/details/britishzoology21penn"),
        "companion": ("Martin Martin’s St Kilda account", "https://www.undiscoveredscotland.co.uk/usebooks/martin-stkilda/chapter02.html"),
        "paragraphs": [
            "According to Mr. Martin, this bird breeds on the isle of St. Kilda, appearing there the beginning of May, and retiring the middle of June. It lays one egg, which is six inches long, of a white color; some are irregularly marked with purplish lines crossing each other, others blotched with black and ferruginous about the thicker end: if the egg is taken away, it will not lay another that season.",
            "A late writer informs us, that it does not visit that island annually, but sometimes keeps away for several years together; and adds, that it lays its egg close to the sea-mark; being incapable, by reason of the shortness of its wings, to mount higher.",
            "The length of this bird, to the end of its toes, is three feet; the bill, to the corner of the mouth, four inches and a quarter: part of the upper mandible is covered with short, black, velvet-like feathers; it is very strong, compressed and marked with several furrows that tally both above and below: between the eyes and the bill on each side is a large white spot: the rest of the head, the neck, back, tail and wings, are of a glossy black: the tips of the lesser quill-feathers white: the whole under side of the body white: the legs black. The wings of this bird are so small, as to be useless for flight: the length, from the tip of the longest quill-feathers to the first joint, being only four inches and a quarter.",
        ],
        "note_phrase": "According to Mr. Martin", "note": "Pennant cites Martin Martin, A Late Voyage to St Kilda (1698), p. 27, for this breeding account.",
        "reading": ("palsson", "thomas"), "neighbors": ("martin", "cartwright"),
    },
    "cartwright": {
        "author": "George Cartwright", "work": "Journal, vol. III, p. 55", "period": "5 July 1785 · published 1792", "place": "Funk Island", "place_key": "funk-island",
        "summary": "A boat of birds from Funk Island prompts Cartwright’s account of harvesting for food, eggs, and feathers.",
        "facsimile": "cartwright-55.webp", "facsimile_alt": "Page 55 of Cartwright's 1792 journal describing Funk Island and its penguins", "facsimile_caption": "Cartwright, Journal, III.55. Scan via Canadiana.org / Biodiversity Heritage Library.",
        "edition": "A Journal of Transactions and Events during a Residence of Nearly Sixteen Years on the Coast of Labrador. Newark: Allin and Ridge, 1792. Volume III, page 55; entry for 5 July 1785.",
        "primary": ("Scanned volume III", "https://www.biodiversitylibrary.org/item/101679"),
        "companion": ("BHL text of volume III", "https://www.biodiversitylibrary.org/itemtext/101679"),
        "paragraphs": [
            "This morning I had my boat moved nearer to the Lyon, and we spent the day on board that vessel. In the evening the Stag, a brig of Mr. Slade’s, sailed for a market with old fish. A boat came in from Funk Island laden with birds, chiefly penguins.",
            "Funk Island is a small flat island-rock, about twenty leagues east of the island of Fogo, in the latitude of 50° north. Innumerable flocks of sea-fowl breed upon it every summer, which are of great service to the poor inhabitants of Fogo; who make voyages there to load with birds and eggs. When the water is smooth, they make their shallop fast to the shore, lay their gang-boards from the gunwale of the boat to the rocks, and then drive as many penguins on board, as she will hold; for, the wings of those birds being remarkably short, they cannot fly.",
            "But it has been customary of late years, for several crews of men to live all the summer on that island, for the sole purpose of killing birds for the sake of their feathers, the destruction which they have made is incredible. If a stop is not soon put to that practice, the whole breed will be diminished to almost nothing, particularly the penguins: for this is now the only island they have left to breed upon; all others lying so near to the shores of Newfoundland, they are continually robbed. The birds which the people bring from thence, they salt and eat, in lieu of salted pork.",
        ],
        "note_phrase": "penguins", "note": "In this North Atlantic passage, Cartwright’s “penguins” are great auks, Pinguinus impennis.",
        "reading": ("lucas", "thomas"), "neighbors": ("pennant", "newton"),
    },
    "newton": {
        "author": "Alfred Newton", "work": "Ibis 3 (1861): 390–392", "period": "1861 · 1844 testimony", "place": "Eldey", "place_key": "eldey",
        "summary": "Newton reports the 1844 capture on Eldey from interviews conducted with John Wolley in Iceland.",
        "facsimile": "newton-391.webp", "facsimile_alt": "Page 391 of Newton's 1861 article describing the 1844 Eldey capture", "facsimile_caption": "Newton, Ibis 3 (1861), p. 391. Scan via BioStor / Biodiversity Heritage Library.",
        "edition": "“Abstract of Mr. J. Wolley’s Researches in Iceland respecting the Gare-fowl or Great Auk.” Ibis 3, no. 4 (October 1861): 374–399; passage on pages 390–392.",
        "primary": ("Article and page scans", "https://biostor.org/reference/292413"),
        "companion": ("Article DOI", "https://doi.org/10.1111/j.1474-919X.1861.tb08857.x"),
        "paragraphs": [
            "The party consisted of fourteen men: two of these are dead, but with all the remaining twelve we conversed. They were commanded, as I have just said, by Vilhjalmur, and started in an eight-oared boat from Kyrkjuvogr, one evening between the 2nd and 5th of June, 1844. The next morning early they arrived off Eldey.",
            "In form the island is a precipitous stack, perpendicular nearly all round. The most lofty part has been variously estimated to be from fifty to seventy fathoms in height; but on the opposite side a shelf (generally known as the ‘Underland’) slopes up from the sea to a considerable elevation, until it is terminated abruptly by the steep cliff of the higher portion. At the foot of this inclined plane is the only landing-place; and further up, out of the reach of the waves, is the spot where the Gare-fowls had their home.",
            "In this expedition but three men ascended: Jon Brandsson, a son of the former leader, who had several times before visited the rock, with Sigurðr Islefsson and Ketil Ketilsson. A fourth, who was called upon to assist, refused, so dangerous did the landing seem. As the men I have named clambered up, they saw two Gare-fowls sitting among the numberless other rock-birds (Uria troile and Alca torda), and at once gave chase.",
            "The Gare-fowls showed not the slightest disposition to repel the invaders, but immediately ran along under the high cliff, their heads erect, their little wings somewhat extended. They uttered no cry of alarm, and moved, with their short steps, about as quickly as a man could walk. Jon with outstretched arms drove one into a corner, where he soon had it fast. Sigurðr and Ketil pursued the second, and the former seized it close to the edge of the rock, here risen to a precipice some fathoms high, the water being directly below it. Ketil then returned to the sloping shelf whence the birds had started, and saw an egg lying on the lava slab, which he knew to be a Gare-fowl’s. He took it up, but finding it was broken, put it down again. Whether there was not also another egg is uncertain. All this took place in much less time than it takes to tell it. They hurried down again, for the wind was rising.",
        ],
        "note_phrase": "with all the remaining twelve we conversed", "note": "Newton and Wolley conducted these interviews during their 1858 Iceland visit. The passage was published after Wolley’s death.",
        "reading": ("palsson", "birkhead"), "neighbors": ("cartwright", "lucas"),
    },
    "lucas": {
        "author": "Frederic A. Lucas", "work": "The Expedition to Funk Island, pp. 505–507", "period": "1888 report", "place": "Funk Island", "place_key": "funk-island",
        "summary": "Lucas describes the 1887 museum expedition to Funk Island and locates the great auk's former breeding ground through the terrain and surviving bones.",
        "facsimile": None,
        "edition": "“The Expedition to Funk Island, with Observations upon the History and Anatomy of the Great Auk.” Report of the United States National Museum for 1888, pp. 493–529, plates LXXI–LXXIII; field visit in July 1887.",
        "primary": ("Smithsonian report PDF", "https://repository.si.edu/bitstream/handle/10088/29937/1888_Lucas_493-530.pdf"),
        "companion": ("Smithsonian catalog record", "https://repository.si.edu/items/c6fcb913-d880-4975-8af9-9f11ce64198f"),
        "paragraphs": [
            "Leaving St. John's on the morning of July 21, we sailed northward toward Cape Bonavista, a headland that still bears its original appellation, following almost exactly the track pursued by Cartier's vessels more than three centuries ago. Daybreak on the morning of the 22d found us in sight of Funk Island, but the wind was so light that not until noon were we near enough for a boat to be lowered and a start made for the shore.",
            "The best landing is at a spot termed ‘The Bench,’ lying a hundred yards or so to the west of the northeastern or Escape Point, and toward this portion of the island, where from time immemorial man had landed to despoil the feathered inhabitants, we directed our course.",
            "A large portion of the southern and most extensive swell of rock is thickly covered with vegetation, this, the former breeding ground of the Great Auk, being mapped out in vivid green by the plants nourished by the decomposed bodies and slowly decomposing bones of the long extinct bird. It would seem that the Auk inhabited every accessible foot of ground, the inability of the bird to fly restricting it of necessity to such portions of the island as could be reached after a landing had been effected on the northerly or southerly slope.",
        ],
        "note_phrase": "former breeding ground of the Great Auk", "note": "Lucas's observations come from a July 1887 visit. The report includes a map and three plates of island topography and specimens.",
        "reading": ("palsson", "thomas"), "neighbors": ("newton", None),
    },
}


def link(url, label):
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)} ↗</a>'


def render(key, item):
    paras = [escape(p) for p in item["paragraphs"]]
    phrase = escape(item["note_phrase"])
    for i, para in enumerate(paras):
        if phrase in para:
            paras[i] = para.replace(phrase, phrase + '<sup class="footnote-ref" id="fnref-1"><a href="#fn-1" aria-label="Note 1">1</a></sup>', 1)
            break
    else:
        raise ValueError(f"Footnote target missing: {key}")
    original = ''.join(f'<p>{p}</p>' for p in paras)
    reading = ''.join(f'<li><span>{n:02d}</span><div><a href="{escape(READING[slug][2], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(READING[slug][0])} ↗</a><br>{escape(READING[slug][1])}</div></li>' for n, slug in enumerate(item['reading'], 1))
    neighbors = ' · '.join(f'<a href="./source-{slug}.html">{escape(SOURCES[slug]["author"])} ↗</a>' for slug in item['neighbors'] if slug)
    if item['facsimile']:
        facsimile = f'''<figure class="auk-facsimile"><a href="{escape(item['primary'][1], quote=True)}" target="_blank" rel="noopener noreferrer"><img src="./assets/great-auk-facsimiles/{item['facsimile']}" alt="{escape(item['facsimile_alt'], quote=True)}" loading="lazy" /></a><figcaption>{escape(item['facsimile_caption'])}</figcaption></figure>'''
    else:
        facsimile = f'''<div class="facsimile-link"><span class="folio-label">Digitized edition</span><p><a href="{escape(item['primary'][1], quote=True)}" target="_blank" rel="noopener noreferrer">Open the historical text ↗</a></p><p>{escape(item['edition'])}</p></div>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="theme-color" content="#f5f2e9" /><meta name="description" content="{escape(item['summary'], quote=True)}" /><title>{escape(item['author'])} — Great auk — Atlas of Historically Lost Species</title><link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" /><link rel="preload" href="./assets/gfs-didot.ttf" as="font" type="font/ttf" crossorigin /><link rel="stylesheet" href="./styles.css" /><link rel="stylesheet" href="./detail.css" /><link rel="stylesheet" href="./great-auk.css?v=2" /><script type="module" src="./main.js"></script></head>
<body data-page="source" data-species="auk" class="auk-source"><a class="skip-link" href="#main">Skip to content</a><div class="site-seal" aria-hidden="true"><span class="seal-symbol"></span></div><div class="page-shell"><header class="masthead"><a class="wordmark" href="./index.html" aria-label="Atlas of Historically Lost Species, home"><span class="wordmark-short" aria-hidden="true">AHLo<span class="wordmark-accent">S</span></span><span class="wordmark-long" aria-hidden="true">Atlas of Historically Lost Species</span></a><nav aria-label="Main navigation"><a href="./index.html#index">Index</a><a href="./authorities.html">Authorities</a><a href="./about.html">About</a></nav></header><main id="main">
<nav class="source-breadcrumb" aria-label="Breadcrumb"><a href="./great-auk.html#record">Great auk</a> / Primary source / {escape(item['author'])}</nav>
<header class="source-head"><div><span class="folio-label">Primary source · {escape(item['period'])}</span><div class="source-author-title"><a class="source-author-avatar" href="./authorities.html#{key}" aria-label="{escape(item['author'])} in the authorities index"><img src="./assets/authorities/{key}.webp" width="84" height="84" alt="" /></a><h1><a href="./authorities.html#{key}">{escape(item['author'])}</a></h1></div><p class="source-deck"><i>{escape(item['work'])}</i>. {escape(item['summary'])}</p></div><div class="source-head-meta"><dl><div><dt>Passage shown</dt><dd>{escape(item['work'])}</dd></div><div><dt>Original language</dt><dd>English</dd></div><div><dt>Place in record</dt><dd><a href="./index.html?place={item['place_key']}#index">{escape(item['place'])} ↗</a></dd></div></dl></div></header>
<div class="source-grid" aria-label="Historical text and digitized source"><section class="source-column" aria-labelledby="original-title"><div class="source-column-head"><h2 id="original-title">Original text</h2><span>Transcription</span></div><div class="source-text" lang="en">{original}</div></section><section class="source-column" aria-labelledby="facsimile-title"><div class="source-column-head"><h2 id="facsimile-title">Digitized edition</h2><span>{escape(item['period'])}</span></div>{facsimile}<div class="auk-edition"><h3>Edition</h3><p>{escape(item['edition'])}</p></div></section></div>
<div class="source-editions" aria-label="Digitized originals"><span>Open the source</span>{link(item['primary'][1], item['primary'][0])}{link(item['companion'][1], item['companion'][0])}</div>
<section class="further-reading" aria-labelledby="further-title"><h2 id="further-title">Further reading</h2><ol class="further-list">{reading}</ol></section>
<aside class="source-footnotes" aria-labelledby="notes-title"><h2 id="notes-title">Note</h2><ol><li id="fn-1"><span class="footnote-number">01</span><p>{escape(item['note'])} <a class="footnote-back" href="#fnref-1" aria-label="Back to note reference">↩</a></p></li></ol></aside>
</main><footer class="site-footer"><span>Atlas of Historically Lost Species</span><span><a href="./great-auk.html#sources">Great auk source index ↗</a>{' · ' + neighbors if neighbors else ''}</span></footer></div></body></html>
'''


if __name__ == '__main__':
    for slug, item in SOURCES.items():
        (ROOT / f'source-{slug}.html').write_text(render(slug, item), encoding='utf-8')
