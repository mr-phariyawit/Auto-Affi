#!/usr/bin/env python3
"""Transcribe an audio file verbatim with Gemini. usage: gemini-stt.py file.wav [model]"""
import base64, json, os, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = os.environ.get("GEMINI_API_KEY") or next((l.split("=", 1)[1].strip() for l in open(os.path.join(ROOT, ".env")) if l.startswith("GEMINI_API_KEY=")), None)
f = sys.argv[1]; model = sys.argv[2] if len(sys.argv) > 2 else "gemini-3.5-flash"
body = {"contents": [{"parts": [{"text": "Transcribe this audio verbatim. Output only the words spoken, nothing else."},
                                {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(f, "rb").read()).decode()}}]}],
        "generationConfig": {"temperature": 0}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                             data=json.dumps(body).encode(), headers={"x-goog-api-key": key, "Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req, timeout=120))
print("".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"]).strip())
