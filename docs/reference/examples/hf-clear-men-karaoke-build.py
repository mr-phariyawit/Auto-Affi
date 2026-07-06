"""Worked example — CLEAR Men Scalp Pro couple ad (runs/2026-07-04-clear-men-couple-v9).

Builds the HyperFrames composition index.html + renders master_karaoke.mp4:
  - real WORD-LEVEL Thai KARAOKE captions (from 07-vo/words.json, pythainlp-tokenized + STT timings)
  - cinematic-zoom per-clip transitions
  - vignette (real hf component) — ellipse edge-darken over all shots, under captions
  - shimmer-sweep (real hf component) — light glint sweeps the whole orange price card at the endcard
  - animated Shopee CTA endcard + persistent #โฆษณา + producer audio auto-mix (Thai VO + ducked BGM)
  - OFFLINE-100%: vendored GSAP (hf/vendor/gsap.min.js), zero external URLs

NOTE: the run dir (clips/audio/master_karaoke.mp4) is gitignored (large generated media);
this script IS the source — the master is regenerable from it + the run assets.
Reference: docs/reference/hyperframes-{components,compose-cookbook,packages-guides}.md"""
import pathlib, subprocess, html, json
RUN=pathlib.Path("/Users/phariyawit.jiap/Documents/Auto-Affi/runs/2026-07-04-clear-men-couple-v9")
HF=RUN/"hf"; N=6.0
words=json.load(open(RUN/"07-vo/words.json",encoding="utf-8"))
# group words by shot (start // 6)
shots={}
for w in words: shots.setdefault(int(w["start"]//N),[]).append(w)

clips="\n".join(
 f'<video class="clip" src="clip{i+1}.mp4" muted playsinline data-start="{i*N}" data-duration="{N}" '
 f'data-track-index="0" id="clip{i+1}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video>'
 for i in range(5))
# karaoke caption group per shot (skip shot 4 = endcard shot, keep caption too)
capblocks=[]
for si in range(5):
    ws=shots.get(si,[])
    if not ws: continue
    spans="".join(f'<span class="kw" id="{w["id"]}">{html.escape(w["text"])}</span>' for w in ws)
    capblocks.append(f'<div class="clip cap" id="cap{si}" data-start="{si*N}" data-duration="{N}" data-track-index="1">'
                     f'<div class="capinner thai">{spans}</div></div>')
captions="\n".join(capblocks)
audio="\n".join(f'<audio src="vo{i+1}.wav" data-start="{i*N+0.3}" data-track-index="2" data-volume="1.0"></audio>' for i in range(5))
audio+=f'\n<audio src="bgm.mp3" data-start="0" data-duration="30" data-track-index="3" data-volume="0.15"></audio>'

# GSAP: cinematic-zoom per clip + word karaoke (active word: accent + scale pop) + caption group fade + endcard
zoom="".join(f"tl.fromTo('#clip{i+1}',{{scale:1.24,transformOrigin:'50% 44%'}},{{scale:1.04,duration:.55,ease:'power3.out'}},{i*N});"
             f"tl.to('#clip{i+1}',{{scale:1.10,duration:5.45,ease:'none'}},{i*N+0.55});" for i in range(5))
grpfade="".join(f"tl.from('#cap{si}',{{opacity:0,y:50,duration:.35}},{si*N+0.3});" for si in shots)
kara=""
for w in words:
    kara+=(f"tl.to('#{w['id']}',{{color:'#ffd24a',scale:1.16,fontWeight:900,duration:.14,transformOrigin:'center bottom'}},{w['start']});"
           f"tl.to('#{w['id']}',{{color:'#ffffff',scale:1.0,duration:.2}},{w['end']});")

doc=f"""<!doctype html>
<html lang="th" data-resolution="portrait"><head><meta charset="UTF-8">
<script src="vendor/gsap.min.js"></script>  <!-- OFFLINE: vendored gsap 3.14.2, no CDN -->
<style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
 .thai{{font-family:'Noto Sans Thai','Thonburi',sans-serif}}
 .cap{{position:absolute;bottom:560px;left:44px;right:44px;text-align:center;z-index:50}}
 .capinner{{display:inline-block;background:rgba(10,12,18,.60);border-radius:22px;padding:16px 30px;
   font-size:56px;font-weight:800;line-height:1.32;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.5)}}
 .kw{{display:inline-block;margin:0 .12em;color:#fff}}
 #disc{{position:absolute;top:44px;right:34px;font-size:30px;color:#fff;background:rgba(0,0,0,.5);padding:8px 18px;border-radius:10px;z-index:70}}
 #endcard{{position:absolute;left:60px;right:60px;bottom:300px;background:#ee4d2d;border-radius:26px;padding:34px 30px;text-align:center;opacity:0;z-index:60;overflow:hidden}}
 #endcard .p{{color:#fff;font-size:50px;font-weight:900}} #endcard .b{{display:inline-block;margin-top:14px;background:#fff;color:#ee4d2d;font-size:40px;font-weight:900;padding:14px 34px;border-radius:16px}}
 /* vignette (real hf component) — ellipse, alpha .5, over video, under captions */
 #hf-vignette{{background:radial-gradient(var(--vignette-shape,ellipse) at center,transparent var(--vignette-size,45%),var(--vignette-color,rgba(0,0,0,.5)) var(--vignette-edge,100%))}}
 /* shimmer-sweep (real hf component) — glint sweeps the whole orange price card */
 #endcard .shimmer-mask{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;background:linear-gradient(var(--shimmer-angle,115deg),transparent 0%,transparent calc(var(--shimmer-pos,-20%) - var(--shimmer-width,22%)/2),var(--shimmer-color,rgba(255,255,255,.92)) var(--shimmer-pos,-20%),transparent calc(var(--shimmer-pos,-20%) + var(--shimmer-width,22%)/2),transparent 100%);mix-blend-mode:overlay}}
</style></head><body>
 <div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1080" data-height="1920">
   {clips}
   <div id="hf-vignette" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:40"></div>
   {captions}
   <div id="endcard" class="thai" data-start="24" data-duration="6" data-track-index="1"><div class="shimmer-mask"></div><div class="p">CLEAR Men Scalp Pro · ฿199</div><div class="b">กดลิงก์ใต้คลิป 🛒</div></div>
   <div id="disc" class="thai" data-start="0" data-duration="30" data-track-index="4">#โฆษณา</div>
   {audio}
 </div>
 <script>
  window.__timelines=window.__timelines||{{}};
  const tl=gsap.timeline({{paused:true}});
  {zoom}
  {grpfade}
  {kara}
  tl.fromTo('#endcard',{{opacity:0,y:80,scale:.9}},{{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.6)'}},24.3);
  tl.to('#endcard .b',{{scale:1.12,duration:.3,yoyo:true,repeat:3,transformOrigin:'center'}},25.2);
  // shimmer glint sweeps the whole orange price card when the endcard lands (twice)
  tl.fromTo('#endcard',{{'--shimmer-pos':'-20%'}},{{'--shimmer-pos':'120%',duration:1.1,ease:'power2.inOut'}},25.0);
  tl.fromTo('#endcard',{{'--shimmer-pos':'-20%'}},{{'--shimmer-pos':'120%',duration:1.1,ease:'power2.inOut'}},27.4);
  tl.set({{}},{{}},30);
  window.__timelines['main']=tl;
 </script>
</body></html>"""
(HF/"index.html").write_text(doc,encoding="utf-8")
print("karaoke index.html written (",len(words),"words )")
