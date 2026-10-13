"""Read Hudson's Bay Company post-journal microfilm PDFs with a vision model and extract
bison, provision and scarcity entries.

    python3 research/extinction-pilot/scripts/hbca_screen.py test MODEL PDF PAGE [PAGE...]
    python3 research/extinction-pilot/scripts/hbca_screen.py run MODEL --cap 3.0

Inputs: research/extinction-pilot/data/raw/hbca/B39/*.pdf (Fort Chipewyan, HBCA B.39/a).
Outputs (Git-ignored): research/extinction-pilot/results/hbca/<post>/pages.jsonl (one line per image).
Model output is a machine reading of handwriting; every quotation must be checked against the scan.
"""
import base64, json, os, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fitz  # PyMuPDF

PILOT = Path(__file__).resolve().parents[1]
ROOT = PILOT.parent.parent
RAW = PILOT / "data/raw/hbca/B39"
OUT = PILOT / "results/hbca/B39"

PROMPT = """Microfilm scan of a Hudson's Bay Company post journal, Fort Chipewyan (Lake Athabasca), 1802-1871; usually two handwritten pages.

Extract ONLY entries that mention: buffalo/bison/"cattle"; moose, deer, reindeer or other large game killed; meat, dry meat, pounded meat, pemmican, grease, tongues or "provisions" (NOT fish); hunters' returns; scarcity, abundance or starvation of animals or provisions.

Copy each such sentence EXACTLY as written ([?] for illegible). Ignore fish, weather, building work, furs, men's names-only entries.

Return compact JSON only:
{"dates":"months/years on the page","e":[{"d":"date as written","q":"exact sentence(s)","bison":integer or null,"meat_lb":integer or null,"place":string or null,"scarce":true/false}]}"""


def key():
    for line in open(ROOT / ".env.local"):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("OPENROUTER_API_KEY missing")


def page_jpeg(pdf, i, width=2000):
    page = fitz.open(pdf)[i]
    zoom = width / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), colorspace=fitz.csGRAY)
    return pix.tobytes("jpeg", jpg_quality=80)


def call(model, img, k):
    body = {"model": model, "response_format": {"type": "json_object"}, "temperature": 0,
            "usage": {"include": True},
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(img).decode()}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=180))
            txt = r["choices"][0]["message"]["content"]
            txt = re.sub(r"^```(?:json)?|```$", "", txt.strip()).strip()
            return json.loads(txt), r.get("usage", {})
        except urllib.error.HTTPError as e:
            if e.code in (402, 403):
                raise SystemExit(f"provider refused ({e.code}): out of credit or key limit")
            time.sleep(3 * 2 ** attempt)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
            time.sleep(3 * 2 ** attempt)
    return {"error": "failed"}, {}


def test(model, pdf, *pages):
    k = key()
    for p in pages:
        res, usage = call(model, page_jpeg(RAW / pdf, int(p)), k)
        print(f"=== {model} {pdf} image {p} cost={usage.get('cost')} tokens={usage.get('prompt_tokens')}/{usage.get('completion_tokens')}")
        print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])


def run(model, cap):
    k = key()
    OUT.mkdir(parents=True, exist_ok=True)
    done_path = OUT / "pages.jsonl"
    done = set()
    spent = 0.0
    if done_path.exists():
        for line in open(done_path):
            r = json.loads(line)
            if "error" not in r["result"]:
                done.add((r["pdf"], r["image"]))
            spent += r.get("cost") or 0
    jobs = [(f.name, i) for f in sorted(RAW.glob("*.pdf"), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.name)])
            for i in range(fitz.open(f).page_count) if (f.name, i) not in done]
    print(f"{len(jobs)} images to read; spent so far ${spent:.3f}; cap ${cap:.2f}")

    def one(job):
        pdf, i = job
        res, usage = call(model, page_jpeg(RAW / pdf, i), k)
        return {"pdf": pdf, "image": i, "model": model, "result": res, "cost": usage.get("cost"),
                "tokens": [usage.get("prompt_tokens"), usage.get("completion_tokens")]}

    with ThreadPoolExecutor(20) as ex, open(done_path, "a") as f:
        for g in range(0, len(jobs), 40):
            if spent > cap - 0.05:
                print(f"spend cap reached: ${spent:.3f}"); break
            for r in ex.map(one, jobs[g:g + 40]):
                f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()
                spent += r["cost"] or 0
            print(f"  {min(g + 40, len(jobs))}/{len(jobs)} images, ${spent:.3f}", flush=True)
    print(f"done; spent ${spent:.3f}")


if __name__ == "__main__":
    if sys.argv[1] == "test":
        test(sys.argv[2], sys.argv[3], *sys.argv[4:])
    elif sys.argv[1] == "run":
        run(sys.argv[2], float(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 3.0)
