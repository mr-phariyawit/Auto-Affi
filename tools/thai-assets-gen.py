#!/usr/bin/env python3
"""Generate candidates for the Thai-cooking-channel asset library.

Reads output/thai-cooking-channel/assets/manifest.json, runs tools/openrouter-imagegen.py for each
requested asset, writes candidates/r<N>.png + r<N>.json, never overwrites, and updates the manifest
(tries, cost_usd, status). Stops launching new jobs once recorded spend + reserve would exceed the cap.

usage: thai-assets-gen.py [--ids id1,id2] [--workers 4] [--dry]
"""
import argparse, glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "output/thai-cooking-channel/assets")
MAN = os.path.join(A, "manifest.json")
EST = 0.13  # reserve per in-flight image, USD


def cost_of(meta):
    """cost from the /generation lookup, else from the response usage block"""
    c = meta.get("cost_usd")
    if not isinstance(c, (int, float)):
        c = (meta.get("usage") or {}).get("cost")
    return c


def spent():
    total = 0.0
    for j in glob.glob(os.path.join(A, "library/*/*/candidates/r*.json")):
        c = cost_of(json.load(open(j)))
        total += c if isinstance(c, (int, float)) else EST
    return total


def key():
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("no OPENROUTER_API_KEY in .env")


def run(asset, man, env):
    d = os.path.join(A, asset["dir"])
    n = len(glob.glob(os.path.join(d, "candidates/r*.png"))) + 1
    out = os.path.join(d, f"candidates/r{n}.png")
    refs = sorted(glob.glob(os.path.join(d, "refs/*")))
    cmd = [sys.executable, os.path.join(ROOT, "tools/openrouter-imagegen.py"), "--model", man["model"],
           "--prompt-file", os.path.join(d, "prompt.txt"), "--out", out, "--aspect", man["aspect"], "--quality", man["quality"]]
    for r in refs:
        cmd += ["--ref", r]
    p = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=600)
    ok = p.returncode == 0 and os.path.exists(out)
    cost = None
    if ok and os.path.exists(out[:-4] + ".json"):
        cost = cost_of(json.load(open(out[:-4] + ".json")))
    if not ok:
        open(os.path.join(d, f"candidates/r{n}.error.txt"), "w").write((p.stdout + "\n" + p.stderr)[-3000:])
    return asset["id"], n, ok, cost


ap = argparse.ArgumentParser()
ap.add_argument("--ids", default="")
ap.add_argument("--workers", type=int, default=4)
ap.add_argument("--dry", action="store_true")
a = ap.parse_args()

man = json.load(open(MAN))
want = set(filter(None, a.ids.split(",")))
todo = [x for x in man["assets"] if (not want or x["id"] in want)]
todo = [x for x in todo if x["tries"] < man["max_tries_per_asset"]]
cap = man["spend_cap_usd"]
budget = cap - spent()
n_ok = int(budget // EST)
skipped = [x["id"] for x in todo[n_ok:]]
todo = todo[:max(n_ok, 0)]
print(f"spent so far ${spent():.3f} of cap ${cap}; launching {len(todo)}; skipped for cap: {skipped}")
if a.dry or not todo:
    sys.exit(0)

env = dict(os.environ, OPENROUTER_API_KEY=key())
with ThreadPoolExecutor(a.workers) as ex:
    results = list(ex.map(lambda x: run(x, man, env), todo))

man = json.load(open(MAN))
by = {x["id"]: x for x in man["assets"]}
for id_, n, ok, cost in results:
    x = by[id_]
    if ok:
        x["tries"] = n
        x["cost_usd"] = round(x["cost_usd"] + (cost if isinstance(cost, (int, float)) else 0.0), 4)
        x["status"] = "generated"
    print(f"{'OK ' if ok else 'ERR'} {id_} r{n} cost={cost}")
man["spent_usd"] = round(spent(), 4)
json.dump(man, open(MAN, "w"), ensure_ascii=False, indent=1)
print(f"total recorded spend ${man['spent_usd']}")
