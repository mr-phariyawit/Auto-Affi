// EP05 render-mode check: mid-frame of every segment + end card.
// Writes check/t<sec>.png, check/subtitle-diff.txt (char-by-char vs approved script), check/subtitle-box.txt (DOM boxes vs safe area).
// usage: node check.cjs   (pixel server on :8931)
const puppeteer = require('/Users/phariyawit.jiap/.npm/_npx/23232c69e5d221f3/node_modules/puppeteer');
const fs = require('fs');
const SEG = [0.0, 14.63, 28.26, 43.57, 53.2, 66.35, 77.26, 90.57, 104.08, 115.95, 128.34, 139.25, 156.14];
// approved script v2 (script/vo-script-v2.md) SUB EN / SUB TH, rows 01–11, 12a, 12b
const SCRIPT = [
  ['Kaeng khiao wan: first seen in a 1926 cookbook.', 'แกงเขียวหวาน พบครั้งแรกในตำราปี 1926'],
  ['Green from fresh chillies. Wan means a pale green.', 'เขียวจากพริกสด หวานคือสีเขียวอ่อน ไม่ใช่รส'],
  ['Spicy plus mild green chillies. Deseed for less heat.', 'พริกเผ็ดผสมพริกเผ็ดน้อย ไม่ทนเผ็ดเอาเมล็ดออก'],
  ['Toast coriander and cumin. Grind with white pepper.', 'คั่วเมล็ดผักชีกับยี่หร่า บดกับพริกไทยขาว'],
  ['Lemongrass, galangal, makrut lime zest, coriander root.', 'ตะไคร้ ข่า ผิวมะกรูด รากผักชี'],
  ['Pound chillies with salt, then herbs, shallots, garlic.', 'โขลกพริกกับเกลือ แล้วสมุนไพร หอมแดง กระเทียม'],
  ['Shrimp paste (gapi). Thai basil for colour.', 'กะปิ และใบโหระพาเพิ่มสีเขียว'],
  ['Store-bought is fine. Add shrimp paste, then taste.', 'พริกแกงสำเร็จก็ได้ เติมกะปิแล้วชิม'],
  ['Fry the paste in coconut milk until the oil separates.', 'ผัดพริกแกงกับกะทิจนน้ำมันแยกตัว'],
  ['Chicken thigh, fish sauce, palm sugar, makrut lime leaves.', 'ไก่สะโพก น้ำปลา น้ำตาลปี๊บ ใบมะกรูด'],
  ['Thai eggplant, or canned bamboo shoots.', 'มะเขือเปราะ หรือหน่อไม้กระป๋อง'],
  ['Thai basil. Spicy and salty, not sweet.', 'ใส่โหระพา รสเผ็ดเค็ม ไม่หวาน'],
  ['In Thailand? Links are in the caption.', 'อยู่ไทย ลิงก์อยู่ในแคปชัน'],
];
const ROW = ['01','02','03','04','05','06','07','08','09','10','11','12a','12b'];
(async () => {
  fs.mkdirSync('check', { recursive: true });
  const br = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--hide-scrollbars'] });
  const pg = await br.newPage();
  await pg.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:' + (process.env.PORT || 8931) + '/index.html?render=1', { waitUntil: 'networkidle0' });
  await pg.evaluate(() => document.fonts.ready);
  const diff = [], box = [];
  const times = SEG.slice(0, 11).map((s, i) => +((s + SEG[i + 1]) / 2).toFixed(2)).concat([+((139.25 + 152.62) / 2).toFixed(2), 152.98, 154.7]);
  for (const t of times) { await pg.evaluate(x => window.__seek(x), t); await new Promise(r => setTimeout(r, 150)); await pg.evaluate(x => window.__seek(x), t); }
  for (let n = 0; n < times.length; n++) {
    const t = times[n];
    await pg.evaluate(x => window.__seek(x), t); await new Promise(r => setTimeout(r, 120));
    await pg.screenshot({ path: `check/t${t}.png` });
    const m = await pg.evaluate(() => {
      const r = id => { const e = document.getElementById(id) || document.querySelector(id); if (!e || getComputedStyle(e).display === 'none') return null; const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; };
      const sub = document.getElementById('subtitle').style.display === 'none' ? null : r('.sub-box');
      return { en: document.getElementById('sub-en').textContent, th: document.getElementById('sub-th').textContent, sub,
        enFs: getComputedStyle(document.getElementById('sub-en')).fontSize, thFs: getComputedStyle(document.getElementById('sub-th')).fontSize,
        title: r('.title'), wm: r('.wm'), ec: r('#endcard'), rail: r('.rail'), meter: r('.meter'), inset: r('#insetimg'),
        overflow: (() => { const b = document.querySelector('.sub-box'); return b.scrollHeight > b.clientHeight + 1 || b.scrollWidth > b.clientWidth + 1; })() };
    });
    if (n < 13) {
      const [en, th] = SCRIPT[n]; const L = ROW[n];
      diff.push(`${L} t=${t} EN ${m.en.replace(/\n/g, ' ') === en ? 'MATCH' : 'DIFF: "' + m.en + '"'} | TH ${m.th.replace(/\n/g, ' ') === th ? 'MATCH' : 'DIFF: "' + m.th + '"'}`);
      const s = m.sub; const ok = s && s[0] >= 120 && s[2] <= 888 && s[1] >= 288 && s[3] <= 840 && !m.overflow;
      const ov = (a, b) => a && b && a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
      const hits = ['title', 'wm', 'rail', 'meter', 'inset'].filter(k => ov(s, m[k]));
      box.push(`${L} t=${t} sub-box ${JSON.stringify(s)} EN ${m.enFs} TH ${m.thFs} safe(x120–888,y288–840) ${ok ? 'OK' : 'OUT'} overflow ${m.overflow} overlaps ${hits.length ? hits.join(',') : 'none'} title ${JSON.stringify(m.title)} wm ${JSON.stringify(m.wm)}`);
    } else box.push(`end t=${t} endcard ${JSON.stringify(m.ec)} subtitle ${m.sub ? 'VISIBLE' : 'hidden'}`);
  }
  for (const t of [153.30, 153.34, 153.36, 156.10]) { await pg.evaluate(x => window.__seek(x), t); const v = await pg.evaluate(() => getComputedStyle(document.getElementById('endcard')).display); box.push(`endcard-probe t=${t} display=${v}`); }
  fs.writeFileSync('check/subtitle-diff.txt', diff.join('\n') + '\n');
  fs.writeFileSync('check/subtitle-box.txt', box.join('\n') + '\n' + (errs.length ? 'PAGEERRORS: ' + errs.join(' | ') : 'no page errors') + '\n');
  console.log(diff.join('\n')); console.log(box.join('\n')); console.log(errs.length ? errs : 'no page errors');
  await br.close();
})();
