#!/usr/bin/env python3
"""Gemini TTS -> WAV. usage: gemini-tts.py --voice Kore --text "..." --out x.wav [--model gemini-3.8-flash-tts] [--style "..."]
Reads GEMINI_API_KEY from the environment or the project .env. Writes OUT and OUT.json (model, voice, text, usage, seconds)."""
import argparse, base64, json, os, re, sys, urllib.request, urllib.error, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--model", default="gemini-3.8-flash-tts")
ap.add_argument("--voice", required=True)
ap.add_argument("--text", required=True)
ap.add_argument("--style", default="")
ap.add_argument("--system", default="", help="style direction sent as systemInstruction (not spoken)")
ap.add_argument("--out", required=True)
a = ap.parse_args()

key = os.environ.get("GEMINI_API_KEY")
if not key:
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("GEMINI_API_KEY="):
            key = line.split("=", 1)[1].strip()
if not key:
    sys.exit("no GEMINI_API_KEY")

prompt = (a.style.strip() + "\n\n" if a.style else "") + a.text
body = {"contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": a.voice}}}}}
if a.system:
    body["systemInstruction"] = {"parts": [{"text": a.system}]}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent",
                             data=json.dumps(body).encode(), headers={"x-goog-api-key": key, "Content-Type": "application/json"})
try:
    resp = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:800]); sys.exit(2)
try:
    part = resp["candidates"][0]["content"]["parts"][0]["inlineData"]
except Exception:
    print("NO AUDIO:", json.dumps(resp)[:800]); sys.exit(3)
pcm = base64.b64decode(part["data"])
mime = part.get("mimeType", "")
if pcm[:4] == b"RIFF" or "wav" in mime:          # newer models return a WAV container
    open(a.out, "wb").write(pcm)
else:                                           # older models return raw 16-bit PCM
    rate = int((re.search(r"rate=(\d+)", mime) or [0, 24000])[1])
    with wave.open(a.out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
with wave.open(a.out, "rb") as w:
    secs = w.getnframes() / w.getframerate(); rate = w.getframerate()
meta = {"model": a.model, "voice": a.voice, "text": a.text, "style": a.style, "system": a.system, "mime": part.get("mimeType"),
        "seconds": round(secs, 3), "rate": rate, "usage": resp.get("usageMetadata")}
json.dump(meta, open(os.path.splitext(a.out)[0] + ".json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: meta[k] for k in ("model", "voice", "seconds", "mime")}))
