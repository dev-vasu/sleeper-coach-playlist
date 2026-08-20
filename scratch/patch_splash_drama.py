import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# ── Patch: make splash always show (for testing: remove sessionStorage gate temporarily)
# Actually leave sessionStorage but reset it. Just patch in DRAMATIC new CSS.

STRIPE_AND_DRAMA_CSS = """
/* ==========================================================================
   SPLASH SCREEN — Dramatic card stripes + rich visual treatment
   ========================================================================== */

/* Coloured diagonal stripe on each card (top-right corner accent) */
.theme-splash-card-stripe {
  position: absolute;
  top: 0; right: 0;
  width: 80px; height: 80px;
  border-radius: 0 20px 0 100%;
  opacity: 0.25;
  transition: opacity 0.3s, width 0.3s, height 0.3s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-stripe {
  opacity: 0.5;
  width: 100px; height: 100px;
}
.theme-splash-train  .theme-splash-card-stripe { background: radial-gradient(circle at top right, #ffb840, transparent); }
.theme-splash-punjab .theme-splash-card-stripe { background: radial-gradient(circle at top right, #ff7040, transparent); }
.theme-splash-jammu  .theme-splash-card-stripe { background: radial-gradient(circle at top right, #30d870, transparent); }
.theme-splash-english .theme-splash-card-stripe{ background: radial-gradient(circle at top right, #9060ff, transparent); }

/* Bottom gradient lift per card */
.theme-splash-card-content {
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 60%, transparent 100%) !important;
}

/* Bigger, richer cards on desktop */
@media (min-width: 700px) {
  .theme-splash-card {
    min-height: 280px !important;
    border-radius: 22px !important;
  }
  .theme-splash-card-emoji {
    font-size: 56px !important;
    margin-bottom: 10px !important;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  }
  .theme-splash-card:hover .theme-splash-card-emoji {
    transform: scale(1.2) translateY(-6px) !important;
  }
  .theme-splash-card-name { font-size: 17px !important; font-weight: 800 !important; }
  .theme-splash-card-sub  { font-size: 12px !important; }
  .theme-splash-card-tag  { font-size: 10px !important; letter-spacing: 2.5px !important; margin-top: 8px !important; padding: 4px 12px !important; }
}

/* Glowing pulsing enter prompt */
.theme-splash-footnote {
  animation: splashFootnotePulse 3s ease-in-out infinite !important;
}
@keyframes splashFootnotePulse {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 0.5; }
}

/* Splash inner max width */
.theme-splash-inner {
  max-width: 1000px !important;
}

/* Bigger, bolder title */
.theme-splash-title {
  font-size: clamp(32px, 6vw, 64px) !important;
  letter-spacing: 2px !important;
  line-height: 1.1 !important;
}
.theme-splash-logo {
  font-size: 64px !important;
  margin-bottom: -8px !important;
}
"""

if "card-stripe" not in content:
    content = content.rstrip() + "\n" + STRIPE_AND_DRAMA_CSS
    with open(style_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Dramatic splash CSS written!")
else:
    print("Already present")

# ── Also patch app.js splash JS to always show (remove sessionStorage gate) ──
app_path = r"C:\Users\dvasu\window-seat\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    app = f.read()

# Remove the sessionStorage check so it always shows
OLD_SPLASH_JS = """  const seen = sessionStorage.getItem('splash_seen');
  if (seen) {
    overlay.classList.add('hidden');
    return;
  }"""

NEW_SPLASH_JS = """  // Always show splash — user picks their vibe every session
  // (Remove the line below to only show once per session)
  sessionStorage.removeItem('splash_seen');"""

if OLD_SPLASH_JS in app:
    app = app.replace(OLD_SPLASH_JS, NEW_SPLASH_JS)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app)
    print("Splash JS updated to always show!")
else:
    print("Splash JS pattern not found — may already be updated")
