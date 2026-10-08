// Read the live credit price + visible job settings from the Higgsfield create page WITHOUT clicking.
// Run with the Claude-in-Chrome javascript tool on https://higgsfield.ai/ai/video?model=... .
// Verified 2026-10-08: button text "Generate\n48\n36" = list 48 (struck), current 36 credits
// for Seedance 2.0 · 8s · Auto · 720p. The current price is the LAST number in the button.
(() => {
  const btn = [...document.querySelectorAll('button')]
    .find((b) => /^\s*generate/i.test(b.innerText) && b.getBoundingClientRect().width > 0);
  if (!btn) return { error: 'no visible Generate button — wrong page or not logged in' };
  const numbers = (btn.innerText.match(/\d[\d,]*(?:\.\d+)?/g) || []).map((n) => parseFloat(n.replace(/,/g, '')));
  const panel = btn.closest('form') || btn.parentElement?.parentElement?.parentElement || document.body;
  const chips = [...panel.querySelectorAll('button')]
    .filter((b) => b.getBoundingClientRect().left < btn.getBoundingClientRect().right)
    .map((b) => b.innerText.trim())
    .filter((t) => /^(\d+(?:\.\d+)?s|Auto|\d+:\d+|\d+p|[14]k)$/i.test(t));
  return {
    credits: numbers.length ? numbers[numbers.length - 1] : null,
    list_price: numbers.length > 1 ? numbers[0] : null,
    raw_button: btn.innerText.replace(/\s+/g, ' ').trim(),
    model: (document.body.innerText.match(/(Seedance|Kling|Veo|Genjutsu|Sora)[ \w.]*?\d(?:\.\d)?/) || [])[0] || null,
    settings_chips: [...new Set(chips)].slice(0, 6),
    disabled: btn.disabled,
    url: location.pathname + location.search,
    read_at: new Date().toISOString(),
  };
})();
