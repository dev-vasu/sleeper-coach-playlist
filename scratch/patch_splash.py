import os

# 1. Add CSS to style.css
style_path = r"C:\Users\dvasu\window-seat\style.css"
with open(style_path, "r", encoding="utf-8") as f:
    style_content = f.read()

splash_css = """
/* ==========================================================================
   THEME SELECTOR SPLASH OVERLAY (First-visit welcome screen)
   ========================================================================== */
.theme-splash-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at 50% 0%, #1a1008 0%, #0a0a12 60%, #000 100%);
  transition: opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow-y: auto;
}
.theme-splash-overlay.dismissing {
  opacity: 0;
  pointer-events: none;
}
.theme-splash-overlay.hidden {
  display: none;
}
.theme-splash-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 48px 24px 36px;
  max-width: 960px;
  width: 100%;
}

/* Header */
.theme-splash-logo {
  font-size: 52px;
  animation: splashLogoFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 0 20px rgba(255, 180, 60, 0.5));
}
@keyframes splashLogoFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}
.theme-splash-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
}
.theme-splash-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(28px, 5vw, 52px);
  font-weight: 400;
  color: #fff;
  margin: 0;
  letter-spacing: 1px;
  text-shadow: 0 2px 30px rgba(255, 180, 60, 0.3);
}
.theme-splash-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(13px, 2vw, 16px);
  color: rgba(255, 255, 255, 0.45);
  margin: 0;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

/* Grid */
.theme-splash-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}
@media (max-width: 700px) {
  .theme-splash-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 420px) {
  .theme-splash-grid {
    grid-template-columns: 1fr;
  }
}

/* Card */
.theme-splash-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-height: 240px;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  background: rgba(255,255,255,0.04);
  transition: transform 0.28s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              border-color 0.28s,
              box-shadow 0.28s;
  outline: none;
  text-align: center;
  padding: 0;
}
.theme-splash-card:hover {
  transform: translateY(-6px) scale(1.02);
  border-color: rgba(255, 255, 255, 0.22);
  box-shadow: 0 24px 60px rgba(0,0,0,0.7);
}
.theme-splash-card:active {
  transform: scale(0.97);
}

.theme-splash-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.35s;
  border-radius: 20px;
}
.theme-splash-card:hover .theme-splash-card-bg { opacity: 1; }

.theme-splash-train .theme-splash-card-bg {
  background: radial-gradient(ellipse at 50% 100%, rgba(255, 160, 40, 0.18) 0%, transparent 65%);
}
.theme-splash-punjab .theme-splash-card-bg {
  background: radial-gradient(ellipse at 50% 100%, rgba(255, 120, 50, 0.18) 0%, transparent 65%);
}
.theme-splash-jammu .theme-splash-card-bg {
  background: radial-gradient(ellipse at 50% 100%, rgba(60, 200, 100, 0.15) 0%, transparent 65%);
}
.theme-splash-english .theme-splash-card-bg {
  background: radial-gradient(ellipse at 50% 100%, rgba(130, 80, 255, 0.18) 0%, transparent 65%);
}

.theme-splash-card-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 16px;
  width: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%);
}
.theme-splash-card-emoji {
  font-size: 40px;
  margin-bottom: 4px;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));
  transition: transform 0.25s;
}
.theme-splash-card:hover .theme-splash-card-emoji {
  transform: scale(1.15) translateY(-4px);
}
.theme-splash-card-name {
  font-family: 'Outfit', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}
.theme-splash-card-sub {
  font-family: 'Hind', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  line-height: 1.4;
}
.theme-splash-card-tag {
  font-family: 'Outfit', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 20px;
  margin-top: 4px;
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.6);
  border: 1px solid rgba(255,255,255,0.12);
}
.theme-splash-train .theme-splash-card-tag    { background: rgba(255,160,40,0.15); color: #ffb84d; border-color: rgba(255,160,40,0.25); }
.theme-splash-punjab .theme-splash-card-tag   { background: rgba(255,120,50,0.15); color: #ff9966; border-color: rgba(255,120,50,0.25); }
.theme-splash-jammu .theme-splash-card-tag    { background: rgba(60,200,100,0.15); color: #66dd88; border-color: rgba(60,200,100,0.25); }
.theme-splash-english .theme-splash-card-tag  { background: rgba(130,80,255,0.15); color: #aa88ff; border-color: rgba(130,80,255,0.25); }

/* Footnote */
.theme-splash-footnote {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.25);
  letter-spacing: 1px;
  text-align: center;
  margin: 0;
}

/* Ambient particle lines (decorative top strip) */
.theme-splash-overlay::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255,180,60,0.5), rgba(255,255,255,0.3), rgba(255,180,60,0.5), transparent);
  animation: splashTopLine 3s ease-in-out infinite alternate;
}
@keyframes splashTopLine {
  0%  { opacity: 0.4; transform: scaleX(0.6); }
  100% { opacity: 1; transform: scaleX(1); }
}
"""

if "THEME SELECTOR SPLASH OVERLAY" not in style_content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(splash_css)
    print("Splash CSS appended successfully!")
else:
    print("Splash CSS already present.")

# 2. Add JS to app.js
app_path = r"C:\Users\dvasu\window-seat\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

splash_js = """
// ─── Theme Selector Splash Overlay ────────────────────────────────────────────
(function() {
  const overlay = document.getElementById('themeSplashOverlay');
  if (!overlay) return;

  // Show only if not seen this session (sessionStorage)
  const seen = sessionStorage.getItem('splash_seen');
  if (seen) {
    overlay.classList.add('hidden');
    return;
  }

  // Wire up card clicks
  overlay.querySelectorAll('.theme-splash-card').forEach(card => {
    card.addEventListener('click', () => {
      const href = card.getAttribute('data-href');
      sessionStorage.setItem('splash_seen', '1');
      overlay.classList.add('dismissing');
      setTimeout(() => {
        overlay.classList.add('hidden');
        if (href && href !== '/') {
          window.location.href = href;
        }
      }, 600);
    });
  });
})();
"""

target = "// ─── Theme Selector Splash Overlay ────────────────────────────────────────────"
if target not in app_content:
    with open(app_path, "a", encoding="utf-8") as f:
        f.write(splash_js)
    print("Splash JS appended to app.js successfully!")
else:
    print("Splash JS already present in app.js.")
