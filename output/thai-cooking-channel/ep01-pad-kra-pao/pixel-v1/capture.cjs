// Capture the pixel demo in render mode, one PNG per frame. usage: node capture.cjs <outDir> [fromFrame] [toFrame]
const puppeteer = require('/Users/phariyawit.jiap/.npm/_npx/23232c69e5d221f3/node_modules/puppeteer');
(async () => {
  const out = process.argv[2], FPS = 30, END = 38.9, a = +(process.argv[3] || 0), b = +(process.argv[4] || Math.round(END * FPS));
  const br = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--hide-scrollbars'] });
  const pg = await br.newPage(); await pg.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  pg.on('pageerror', e => console.log('PAGEERROR', e.message));
  await pg.goto('http://localhost:8931/index.html?render=1', { waitUntil: 'networkidle0' });
  await pg.evaluate(() => document.fonts.ready);
  for (let s = 0; s < 34; s += 4.5) { await pg.evaluate(t => window.__seek(t), s); await new Promise(r => setTimeout(r, 150)); }   // warm every step's images
  for (let f = a; f < b; f++) {
    await pg.evaluate(t => window.__seek(t), f / FPS);
    await pg.screenshot({ path: `${out}/f${String(f).padStart(5, '0')}.png`, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  }
  console.log('frames', a, b); await br.close();
})();
