import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# ─── 1. Fix mobile overlap: on portrait, hide the floating widget on main page ─
# The widget on index.html is inside .compartment-visuals (position:absolute),
# but in portrait mode the visuals area is only 46vh tall — widget bleeds out.
# On mobile portrait, for the main page, we hide the floating widget since
# users can use the console panel below instead.
# For subpages, the widget is inside compartment-panels and is fine as fixed.

MOBILE_OVERLAP_FIX = """
/* ── Mobile: fix Change Vibe widget overlapping console on main train page ── */
@media (max-aspect-ratio: 13/10) {
  /* On main sleeper coach page (route-hindi), the widget lives inside
     compartment-visuals (46vh top zone). Move it to bottom of the panels area
     instead of floating over the console switches. */
  .route-hindi .theme-explorer-widget {
    position: relative !important;
    bottom: auto !important;
    left: auto !important;
    top: auto !important;
    margin: 12px 16px 4px !important;
    width: calc(100% - 32px) !important;
    align-items: stretch !important;
  }

  /* Place it at top of compartmentPanels for easy access */
  .route-hindi .theme-explorer-widget {
    order: -1 !important;
  }

  .route-hindi .theme-explorer-trigger {
    width: 100% !important;
    border-radius: 12px !important;
    justify-content: center !important;
    padding: 12px 16px !important;
    font-size: 13px !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
  }

  .route-hindi .theme-explorer-panel {
    width: 100% !important;
    position: relative !important;
    bottom: auto !important;
    top: auto !important;
    margin-top: 8px !important;
    max-height: none !important;
    overflow: visible !important;
  }

  .route-hindi .theme-card {
    padding: 12px 14px !important;
  }
}
"""

# ─── 2. Dramatically redesign the splash screen CSS ────────────────────────────
# First, find and replace the splash overlay background to make it richer
OLD_SPLASH_BG = "  background: radial-gradient(ellipse at 50% 0%, #1a1008 0%, #0a0a12 60%, #000 100%);"
NEW_SPLASH_BG = """  background:
    radial-gradient(ellipse at 20% 50%, rgba(255, 140, 30, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 30%, rgba(100, 60, 200, 0.07) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 100%, rgba(30, 120, 80, 0.06) 0%, transparent 50%),
    linear-gradient(160deg, #0d0a18 0%, #0a0c10 40%, #080a0d 100%);"""

content = content.replace(OLD_SPLASH_BG, NEW_SPLASH_BG)

# Make cards more dramatic — each gets a proper unique background gradient
OLD_TRAIN_BG = "  background: radial-gradient(ellipse at 50% 100%, rgba(255, 160, 40, 0.18) 0%, transparent 65%);"
NEW_TRAIN_BG = """  background: linear-gradient(135deg, rgba(255,160,40,0.15) 0%, rgba(255,100,20,0.08) 50%, transparent 100%);"""
content = content.replace(OLD_TRAIN_BG, NEW_TRAIN_BG)

OLD_PUNJAB_BG = "  background: radial-gradient(ellipse at 50% 100%, rgba(255, 120, 50, 0.18) 0%, transparent 65%);"
NEW_PUNJAB_BG = """  background: linear-gradient(135deg, rgba(255,100,40,0.18) 0%, rgba(220,60,20,0.08) 50%, transparent 100%);"""
content = content.replace(OLD_PUNJAB_BG, NEW_PUNJAB_BG)

OLD_JAMMU_BG = "  background: radial-gradient(ellipse at 50% 100%, rgba(60, 200, 100, 0.15) 0%, transparent 65%);"
NEW_JAMMU_BG = """  background: linear-gradient(135deg, rgba(40,200,100,0.15) 0%, rgba(20,140,80,0.08) 50%, transparent 100%);"""
content = content.replace(OLD_JAMMU_BG, NEW_JAMMU_BG)

OLD_ENGLISH_BG = "  background: radial-gradient(ellipse at 50% 100%, rgba(130, 80, 255, 0.18) 0%, transparent 65%);"
NEW_ENGLISH_BG = """  background: linear-gradient(135deg, rgba(120,60,255,0.18) 0%, rgba(80,40,180,0.08) 50%, transparent 100%);"""
content = content.replace(OLD_ENGLISH_BG, NEW_ENGLISH_BG)

# Make the card background always slightly visible (not just on hover)
OLD_CARD_BG_VIS = ".theme-splash-card-bg {\n  position: absolute;\n  inset: 0;\n  opacity: 0;\n  transition: opacity 0.35s;\n  border-radius: 20px;\n}\n.theme-splash-card:hover .theme-splash-card-bg { opacity: 1; }"
NEW_CARD_BG_VIS = """.theme-splash-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.4;
  transition: opacity 0.35s;
  border-radius: 20px;
}
.theme-splash-card:hover .theme-splash-card-bg { opacity: 1; }"""
content = content.replace(OLD_CARD_BG_VIS, NEW_CARD_BG_VIS)

# Make card base background richer
OLD_CARD_BASE = "  background: rgba(255,255,255,0.04);"
NEW_CARD_BASE = "  background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);"
content = content.replace(OLD_CARD_BASE, NEW_CARD_BASE, 1)  # only first occurrence (the card one)

# Richer border colors per card — add per-theme borders
# We'll append this at the end along with the mobile fix

SPLASH_ENHANCEMENTS = """
/* ── Splash card per-theme borders & always-on glow ── */
.theme-splash-train  { border-color: rgba(255, 160, 40, 0.25) !important; }
.theme-splash-punjab { border-color: rgba(255, 100, 50, 0.25) !important; }
.theme-splash-jammu  { border-color: rgba(40, 200, 100, 0.22) !important; }
.theme-splash-english{ border-color: rgba(120, 60, 255, 0.25) !important; }

.theme-splash-train:hover  { box-shadow: 0 24px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,160,40,0.15) !important; border-color: rgba(255,160,40,0.5) !important; }
.theme-splash-punjab:hover { box-shadow: 0 24px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,100,50,0.15) !important; border-color: rgba(255,100,50,0.5) !important; }
.theme-splash-jammu:hover  { box-shadow: 0 24px 60px rgba(0,0,0,0.7), 0 0 40px rgba(40,200,100,0.12) !important; border-color: rgba(40,200,100,0.45) !important; }
.theme-splash-english:hover{ box-shadow: 0 24px 60px rgba(0,0,0,0.7), 0 0 40px rgba(120,60,255,0.15) !important; border-color: rgba(120,60,255,0.5) !important; }

/* Tag colors more vivid */
.theme-splash-train .theme-splash-card-tag    { background: rgba(255,160,40,0.2) !important; color: #ffc060 !important; border-color: rgba(255,160,40,0.4) !important; }
.theme-splash-punjab .theme-splash-card-tag   { background: rgba(255,100,50,0.2) !important; color: #ff9070 !important; border-color: rgba(255,100,50,0.4) !important; }
.theme-splash-jammu .theme-splash-card-tag    { background: rgba(40,200,100,0.2) !important; color: #60ee99 !important; border-color: rgba(40,200,100,0.4) !important; }
.theme-splash-english .theme-splash-card-tag  { background: rgba(120,60,255,0.2) !important; color: #b088ff !important; border-color: rgba(120,60,255,0.4) !important; }

/* Richer top divider line */
.theme-splash-overlay::before {
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255,160,40,0.6) 20%,
    rgba(255,255,255,0.4) 50%,
    rgba(120,60,255,0.5) 80%,
    transparent 100%
  ) !important;
  height: 1.5px !important;
  animation: splashTopLine 4s ease-in-out infinite alternate !important;
}

/* Emoji scale on active (pressing) */
.theme-splash-card:active .theme-splash-card-emoji {
  transform: scale(0.9) !important;
}

/* Bigger emoji on desktop for more drama */
@media (min-width: 700px) {
  .theme-splash-card { min-height: 270px !important; }
  .theme-splash-card-emoji { font-size: 52px !important; margin-bottom: 8px !important; }
  .theme-splash-card-name  { font-size: 16px !important; }
  .theme-splash-card-sub   { font-size: 12px !important; }
}
"""

content = content.rstrip() + "\n" + MOBILE_OVERLAP_FIX + SPLASH_ENHANCEMENTS

with open(style_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done! Mobile overlap fix + splash redesign applied.")
