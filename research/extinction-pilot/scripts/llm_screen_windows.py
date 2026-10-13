"""Screen every gift/cargo passage window with a small LLM for dodos, red hens and other
Mascarene or unidentified rare birds. Embeddings missed one-word list entries such as
"1 dodeers"; this reads every window instead.

    python3 research/extinction-pilot/scripts/llm_screen_windows.py test
    python3 research/extinction-pilot/scripts/llm_screen_windows.py run
"""
import json, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from embed_mauritius import key  # noqa: E402
from embed_gifts import OUT  # noqa: E402

MODEL = "gpt-5.4-mini"
PER_CALL = 25
SYSTEM = """You screen machine transcriptions (noisy HTR) of 17th-century Dutch VOC records for evidence of LIVE OR DEAD BIRDS FROM MAURITIUS / THE MASCARENES, especially the DODO, and unusual birds moved as gifts, cargo or rarities.
Dodo names vary: dodaers, dodaersen, dodeers, dodeersen, dodersen, dottaersen, doderse, dod-aers, walghvogel, walchvogel, dronte, kermisgans, "Indische swaen", or descriptions (large fat flightless bird, tiny wings, hooked beak). Red hen: velthoenders, roode hennen, patrysen on Mauritius. Also flag: any bird said to come from Mauritius/Cerne/Mascarenhas/Rodrigues; any 'casuaris'/cassowary or other strange bird sent as a gift/present/rarity to a ruler; any unnamed 'vreemde vogel'/'rariteyt' bird.
Do NOT flag: ship names (Swaen, Vogelstruys, Mauritius, Hert, etc.), ordinary poultry/hens as provisions, personal names (Dodo as a name), 'Doctoren', place names.
Return JSON: {"flags":[{"id":<int>,"category":"dodo|red_hen|mascarene_bird|cassowary|rare_bird_gift|other","quote":"<exact words from the text, <=25 words>","why":"<short>"}]}. Return {"flags":[]} if nothing qualifies. Be precise; quote only text that is present."""


def call(batch, k):
    user = "\n\n".join(f"[{i}] {w['text']}" for i, w in batch)
    body = {"model": MODEL, "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
            return json.loads(r["choices"][0]["message"]["content"]).get("flags", []), r["usage"]
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if attempt == 5: print("failed batch", e); return [], {}
            time.sleep(5 * 2 ** attempt)


def run(windows, label):
    k = key()
    items = list(enumerate(windows))
    batches = [items[i:i + PER_CALL] for i in range(0, len(items), PER_CALL)]
    flags, usage = [], {"prompt_tokens": 0, "completion_tokens": 0}
    with ThreadPoolExecutor(8) as pool:
        for fl, us in pool.map(lambda b: call(b, k), batches):
            for f in fl:
                i = f.get("id")
                if isinstance(i, int) and 0 <= i < len(windows):
                    f.update(scan_id=windows[i]["scan_id"], volume_years=windows[i]["volume_years"],
                             window=windows[i]["text"])
                    flags.append(f)
            for x in usage: usage[x] += us.get(x, 0)
    json.dump(flags, open(OUT / f"llm_flags_{label}.json", "w"), ensure_ascii=False, indent=1)
    print(label, len(windows), "windows;", len(flags), "flags; usage", usage)
    return flags


if __name__ == "__main__":
    ws = json.load(open(OUT / "windows.json"))
    if sys.argv[1] == "test":
        pos = [w for w in ws if w["scan_id"].endswith("1164_0738") and "dodeers" in w["text"]]
        neg = [w for w in ws if not w["scan_id"].startswith("NL-HaNA_1.04.02_11")][:40]
        fl = run(pos + neg, "test")
        for f in fl: print(f["scan_id"], f["category"], "|", f["quote"])
    else:
        run(ws, "all")
