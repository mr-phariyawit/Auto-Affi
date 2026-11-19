// EP03 render-mode check: mid-frame of every segment + end card.
// Writes check/t<sec>.png, check/subtitle-diff.txt (char-by-char vs approved script), check/subtitle-box.txt (DOM boxes vs safe area).
// usage: node check.cjs   (pixel server on :8931)
const puppeteer = require('/Users/phariyawit.jiap/.npm/_npx/23232c69e5d221f3/node_modules/puppeteer');
const fs = require('fs');
const SEG = [0.0, 5.83, 11.34, 18.57, 23.4, 27.99, 33.22, 38.05, 45.89];
// approved script v1 (script/vo-script-v1.md), curly apostrophe as rendered
const SCRIPT = [
  ['Tom yum kung, listed as UNESCO heritage in 2024.', 'ต้มยำกุ้ง ยูเนสโกขึ้นทะเบียนเป็นมรดกเมื่อปี 2567'],
  ['It began in riverside communities of Thailand’s Central Plains.', 'เริ่มจากชุมชนริมน้ำในที่ราบภาคกลาง'],
  ['Three herbs: lemongrass, galangal, makrut lime leaf. Never ginger.', 'สมุนไพรสามอย่าง ตะไคร้ ข่า ใบมะกรูด ห้ามใช้ขิงแทน'],
  ['Smash the lemongrass. Twist and tear the lime leaves.', 'ทุบตะไคร้ บิดแล้วฉีกใบมะกรูด'],
  ['Keep the prawn heads. Their orange fat adds richness.', 'เก็บหัวกุ้งไว้ มันกุ้งสีส้มให้ความมัน'],
  ['Add straw mushrooms. Never boil the prawns until tough.', 'ใส่เห็ดฟาง อย่าต้มกุ้งจนแข็ง'],
  ['Fish sauce seasons it. Lime goes in last, off the heat.', 'ปรุงด้วยน้ำปลา ใส่มะนาวท้ายสุด นอกเตา'],
  ['Abroad? Frozen lemongrass and galangal work. In Thailand, affiliate links are in the caption.', 'อยู่ต่างประเทศ ใช้ตะไคร้กับข่าแช่แข็งได้ อยู่ไทย ลิงก์แอฟฟิลิเอตอยู่ในแคปชัน'],
];
(async () => {
  fs.mkdirSync('check', { recursive: true });
  const br = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--hide-scrollbars'] });
  const pg = await br.newPage();
  await pg.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8931/index.html?render=1', { waitUntil: 'networkidle0' });
  await pg.evaluate(() => document.fonts.ready);
  const diff = [], box = [];
  const times = SEG.slice(0, 8).map((s, i) => +((s + SEG[i + 1]) / 2).toFixed(2)).concat([44.5]);
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
        title: r('.title'), wm: r('.wm'), ec: r('endcard') };
    });
    if (n < 8) {
      const [en, th] = SCRIPT[n];
      diff.push(`${n + 1} t=${t} EN ${m.en.replace(/\n/g, ' ') === en ? 'MATCH' : 'DIFF: "' + m.en + '"'} | TH ${m.th.replace(/\n/g, ' ') === th ? 'MATCH' : 'DIFF: "' + m.th + '"'}`);
      const s = m.sub; const ok = s && s[0] >= 120 && s[2] <= 888 && s[1] >= 288 && s[3] <= 840;
      box.push(`${n + 1} t=${t} sub-box ${JSON.stringify(s)} EN ${m.enFs} TH ${m.thFs} safe(x120–888,y288–840) ${ok ? 'OK' : 'OUT'} title ${JSON.stringify(m.title)} wm ${JSON.stringify(m.wm)}`);
    } else box.push(`end t=${t} endcard ${JSON.stringify(m.ec)} subtitle ${m.sub ? 'VISIBLE' : 'hidden'}`);
  }
  fs.writeFileSync('check/subtitle-diff.txt', diff.join('\n') + '\n');
  fs.writeFileSync('check/subtitle-box.txt', box.join('\n') + '\n' + (errs.length ? 'PAGEERRORS: ' + errs.join(' | ') : 'no page errors') + '\n');
  console.log(diff.join('\n')); console.log(box.join('\n')); console.log(errs.length ? errs : 'no page errors');
  await br.close();
})();
