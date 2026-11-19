// EP04 render-mode check: mid-frame of every segment + end card.
// Writes check/t<sec>.png, check/subtitle-diff.txt (char-by-char vs approved script), check/subtitle-box.txt (DOM boxes vs safe area).
// usage: node check.cjs   (pixel server on :8931)
const puppeteer = require('/Users/phariyawit.jiap/.npm/_npx/23232c69e5d221f3/node_modules/puppeteer');
const fs = require('fs');
const SEG = [0.0, 5.67, 10.14, 15.49, 19.84, 24.71, 29.67, 36.42, 44.81];
// approved script v1 (script/vo-script-v1.md), curly apostrophe as rendered
const SCRIPT = [
  ['Khao pad, Thai fried rice, served at nearly every street stall.', 'ข้าวผัด มีขายแทบทุกร้านริมทาง'],
  ['Cook jasmine rice drier: one cup rice, one cup water.', 'หุงข้าวหอมมะลิให้แห้งขึ้น ข้าวหนึ่งถ้วย น้ำหนึ่งถ้วย'],
  ['Fry garlic on medium heat until the smallest bits turn golden.', 'เจียวกระเทียมไฟกลาง จนชิ้นเล็กเริ่มเหลือง'],
  ['Turn the heat up. Eggs go in, only half set.', 'เร่งไฟแรง ใส่ไข่ ให้สุกแค่ครึ่งเดียว'],
  ['Season with Thai soy sauce, fish sauce, and white pepper.', 'ปรุงด้วยซีอิ๊วขาวแบบไทย น้ำปลา และพริกไทยขาว'],
  ['A little sugar balances the salt. It should not taste sweet.', 'น้ำตาลนิดเดียวช่วยตัดเค็ม ข้าวต้องไม่หวาน'],
  ['Crab is arguably Thailand’s favourite. No crab? Use shrimp, pork, or chicken.', 'ข้าวผัดปูน่าจะนิยมที่สุดในไทย ไม่มีปู ใช้กุ้ง หมู หรือไก่'],
  ['Always serve lime. Add cucumber and prik nam pla. In Thailand, affiliate links are in the caption.', 'เสิร์ฟกับมะนาวเสมอ เพิ่มแตงกวาและพริกน้ำปลา อยู่ไทย ลิงก์แอฟฟิลิเอตอยู่ในแคปชัน'],
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
  const times = SEG.slice(0, 8).map((s, i) => +((s + SEG[i + 1]) / 2).toFixed(2)).concat([43.8]);
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
