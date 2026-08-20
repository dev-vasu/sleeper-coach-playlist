import os

# ─── 1. Wire JS for desktop widget in app.js ─────────────────────────────────
app_path = r"C:\Users\dvasu\window-seat\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    app = f.read()

DESKTOP_WIDGET_JS = """
// ─── Desktop Change Vibe Widget ───────────────────────────────────────────────
(function() {
  const w = document.getElementById('themeExplorerDesktop');
  const t = document.getElementById('themeExplorerTriggerDesktop');
  const c = document.getElementById('themeExplorerCloseDesktop');
  if (!w || !t) return;
  t.addEventListener('click', (e) => { e.stopPropagation(); w.classList.toggle('open'); });
  if (c) c.addEventListener('click', (e) => { e.stopPropagation(); w.classList.remove('open'); });
  document.addEventListener('click', (e) => { if (!e.target.closest('#themeExplorerDesktop')) w.classList.remove('open'); });
})();
"""

if "Desktop Change Vibe Widget" not in app:
    with open(app_path, "a", encoding="utf-8") as f:
        f.write(DESKTOP_WIDGET_JS)
    print("Added desktop widget JS to app.js")
else:
    print("Desktop widget JS already present")

# ─── 2. Completely overhaul splash screen HTML in index.html ─────────────────
idx_path = r"C:\Users\dvasu\window-seat\index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    idx = f.read().replace("\r\n", "\n")

NEW_SPLASH = """  <!-- ✦ Theme Selector Splash (shown on first visit via sessionStorage) -->
  <div class="theme-splash-overlay" id="themeSplashOverlay">
    <div class="theme-splash-inner">

      <div class="theme-splash-header">
        <div class="theme-splash-logo">🚂</div>
        <h1 class="theme-splash-title">स्लीपर कोच प्लेलिस्ट</h1>
        <p class="theme-splash-subtitle">Choose your vibe for tonight's journey</p>
      </div>

      <div class="theme-splash-grid">

        <!-- Classic Train -->
        <button class="theme-splash-card theme-splash-train" id="splashPickTrain" data-href="/">
          <div class="theme-splash-card-bg"></div>
          <div class="theme-splash-card-stripe"></div>
          <div class="theme-splash-card-content">
            <div class="theme-splash-card-emoji">🚂</div>
            <div class="theme-splash-card-name">Classic Train</div>
            <div class="theme-splash-card-sub">Hindi classics · Retro sleeper coach</div>
            <div class="theme-splash-card-tag">HINDI</div>
          </div>
        </button>

        <!-- Sad Punjabi -->
        <button class="theme-splash-card theme-splash-punjab" id="splashPickPunjab" data-href="/punjab">
          <div class="theme-splash-card-bg"></div>
          <div class="theme-splash-card-stripe"></div>
          <div class="theme-splash-card-content">
            <div class="theme-splash-card-emoji">🌾</div>
            <div class="theme-splash-card-name">Sad Punjabi</div>
            <div class="theme-splash-card-sub">सदा-ए-हिज्र · Sufi folk</div>
            <div class="theme-splash-card-tag">PUNJABI</div>
          </div>
        </button>

        <!-- Jammu Dogri -->
        <button class="theme-splash-card theme-splash-jammu" id="splashPickJammu" data-href="/jammu">
          <div class="theme-splash-card-bg"></div>
          <div class="theme-splash-card-stripe"></div>
          <div class="theme-splash-card-content">
            <div class="theme-splash-card-emoji">🏔️</div>
            <div class="theme-splash-card-name">Jammu (Dogri)</div>
            <div class="theme-splash-card-sub">Valley folk · Mountain vibes</div>
            <div class="theme-splash-card-tag">DOGRI</div>
          </div>
        </button>

        <!-- 80's English R&B -->
        <button class="theme-splash-card theme-splash-english" id="splashPickEnglish" data-href="/english">
          <div class="theme-splash-card-bg"></div>
          <div class="theme-splash-card-stripe"></div>
          <div class="theme-splash-card-content">
            <div class="theme-splash-card-emoji">🎵</div>
            <div class="theme-splash-card-name">80's English R&B</div>
            <div class="theme-splash-card-sub">Timeless music · Rainy city night</div>
            <div class="theme-splash-card-tag">ENGLISH</div>
          </div>
        </button>

      </div>

      <p class="theme-splash-footnote">✦ You can always switch themes from inside the experience</p>
    </div>
  </div>"""

# Find and replace the entire splash block
start = idx.find("  <!-- ✦ Theme Selector Splash")
end   = idx.find("  </div>\n\n  <!-- Mobile Portrait", start)
if start != -1 and end != -1:
    end = end + len("  </div>")
    idx = idx[:start] + NEW_SPLASH + idx[end:]
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(idx)
    print("Splash HTML updated in index.html")
else:
    print(f"Could not find splash block: start={start}, end={end}")

print("Done!")
