// Capture EP03 pixel demo in render mode, one PNG per frame.
// usage: node capture.cjs <outDir> [fromFrame] [toFrame]
const puppeteer = require('/Users/phariyawit.jiap/.npm/_npx/23232c69e5d221f3/node_modules/puppeteer');
(async () => {
  const out = process.argv[2], FPS = 30, END = 45.89;
  const a = +(process.argv[3] || 0), b = +(process.argv[4] || Math.round(END * FPS));
  const br = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--hide-scrollbars']
  });
  const pg = await br.newPage();
  await pg.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  pg.on('pageerror', e => console.log('PAGEERROR', e.message));
  await pg.goto('http://localhost:8931/index.html?render=1', { waitUntil: 'networkidle0' });
  await pg.evaluate(() => document.fonts.ready);
  // warm all steps so images are decoded
  const SEG = [0.0, 5.83, 11.34, 18.57, 23.4, 27.99, 33.22, 38.05, 45.89];
  for (let i = 0; i < SEG.length; i++) {
    await pg.evaluate(t => window.__seek(t), SEG[i] + 0.1);
    await new Promise(r => setTimeout(r, 200));
  }
  for (let fr = a; fr < b; fr++) {
    await pg.evaluate(t => window.__seek(t), fr / FPS);
    await pg.screenshot({ path: `${out}/f${String(fr).padStart(5, '0')}.png`, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    if (fr % 150 === 0) process.stdout.write(`frame ${fr}/${b}\n`);
  }
  console.log('done frames', a, '–', b - 1);
  await br.close();
})();
