#!/usr/bin/env python3
"""Image-edit style generation through OpenRouter chat completions (image output).
Usage: python tools/openrouter-imagegen.py --model openai/gpt-5.4-image-2 --prompt-file P --out OUT.png --ref a.jpg --ref b.jpg ...
Refs are attached in the given order as IMAGE 1..N. Writes OUT.png and OUT.json (request/response meta + cost from /generation)."""
import argparse, base64, io, json, os, sys, time, urllib.request
from PIL import Image

def to_data_uri(path, max_side=1536):
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.size

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True); ap.add_argument("--prompt-file", required=True)
ap.add_argument("--out", required=True); ap.add_argument("--ref", action="append", default=[])
ap.add_argument("--aspect", default="3:4"); ap.add_argument("--size", default="2K"); ap.add_argument("--quality", default="high"); ap.add_argument("--reasoning", default="low"); ap.add_argument("--endpoint", default="images", choices=["images","chat"])
a = ap.parse_args()
key = os.environ["OPENROUTER_API_KEY"]
prompt = open(a.prompt_file).read().strip()
if a.endpoint == "images":
    uris = []; sizes = []
    for r in a.ref:
        uri, sz = to_data_uri(r); uris.append(uri); sizes.append((os.path.basename(r), sz))
    body = {"model": a.model, "prompt": prompt, "n": 1, "quality": a.quality, "aspect_ratio": a.aspect}
    if uris: body["input_references"] = [{"type": "image_url", "image_url": {"url": u}} for u in uris]
    url_ep = "https://openrouter.ai/api/v1/images"
else:
    content = []; sizes = []
    for i, r in enumerate(a.ref, 1):
        uri, sz = to_data_uri(r); sizes.append((os.path.basename(r), sz))
        content.append({"type": "text", "text": f"IMAGE {i}: {os.path.basename(r)}"})
        content.append({"type": "image_url", "image_url": {"url": uri, "detail": "high"}})
    content.append({"type": "text", "text": prompt})
    body = {"model": a.model, "messages": [{"role": "user", "content": content}], "modalities": ["image", "text"],
            "image_config": {"aspect_ratio": a.aspect, "image_size": a.size, "quality": a.quality}, "reasoning": {"effort": a.reasoning}}
    url_ep = "https://openrouter.ai/api/v1/chat/completions"
req = urllib.request.Request(url_ep, data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "X-Title": "Auto-Affi musician shoot"})
t0 = time.time()
try:
    resp = json.load(urllib.request.urlopen(req, timeout=540))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:1500]); sys.exit(1)
dt = round(time.time() - t0, 1)
if a.endpoint == "images":
    d0 = (resp.get("data") or [{}])[0]
    u = d0.get("url") or ("data:image/png;base64," + d0["b64_json"] if d0.get("b64_json") else None)
    msg = {"images": [{"image_url": {"url": u}}] if u else [], "content": d0.get("revised_prompt")}
else:
    msg = resp.get("choices", [{}])[0].get("message", {})
imgs = msg.get("images") or [p for p in (msg.get("content") if isinstance(msg.get("content"), list) else []) if p.get("type") == "image_url"]
if not imgs:
    print("NO IMAGE in response:", json.dumps(resp)[:1500]); sys.exit(2)
url = imgs[0]["image_url"]["url"]
raw = base64.b64decode(url.split(",", 1)[1]) if url.startswith("data:") else urllib.request.urlopen(url).read()
open(a.out, "wb").write(raw)
w, h = Image.open(a.out).size
meta = {"model": resp.get("model"), "provider": resp.get("provider"), "id": resp.get("id"), "usage": resp.get("usage"),
        "seconds": dt, "out": a.out, "out_size": [w, h], "n_images": len(imgs), "text": msg.get("content") if isinstance(msg.get("content"), str) else None,
        "refs": sizes, "request": {k: v for k, v in body.items() if k not in ("image", "messages", "input_references")}, "n_refs": len(a.ref), "prompt_sha_len": len(prompt)}
time.sleep(3)
try:
    g = json.load(urllib.request.urlopen(urllib.request.Request(f"https://openrouter.ai/api/v1/generation?id={resp.get('id')}", headers={"Authorization": f"Bearer {key}"}), timeout=30)).get("data", {})
    meta["cost_usd"] = g.get("total_cost"); meta["gen_tokens"] = {k: g.get(k) for k in ("tokens_prompt", "tokens_completion", "native_tokens_prompt", "native_tokens_completion")}
except Exception as e:
    meta["cost_usd"] = None; meta["cost_err"] = str(e)[:200]
json.dump(meta, open(os.path.splitext(a.out)[0] + ".json", "w"), indent=1)
print(json.dumps(meta, indent=1))
