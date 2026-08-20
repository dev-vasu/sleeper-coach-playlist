import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate the theme selector splash block
start = content.find(".theme-splash-overlay {")
end   = content.find("/* ==========================================================================\n   COMPREHENSIVE MOBILE RESPONSIVE", start)

if start == -1 or end == -1:
    print(f"FAILED: start={start}, end={end}")
    exit(1)

NEW_SPLASH_CSS = """.theme-splash-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Luxury, ultra-clean matte obsidian black background */
  background: radial-gradient(circle at 50% 50%, #111216 0%, #08090b 100%);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  overflow-y: auto;
}
.theme-splash-overlay::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
}
/* Extremely subtle dust/grain filter to give a high-end physical texture */
.theme-splash-overlay::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.95' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.015'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px;
  pointer-events: none;
  z-index: 0;
}
.theme-splash-overlay.dismissing {
  opacity: 0;
  pointer-events: none;
}
.theme-splash-overlay.hidden {
  display: none;
}

/* ── Inner layout ── */
.theme-splash-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 44px;
  padding: 64px 24px;
  max-width: 1000px;
  width: 100%;
}

/* ── Header ── */
.theme-splash-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}
.theme-splash-logo {
  font-size: 54px;
  margin-bottom: 4px;
  animation: splashLogoFloat 5s ease-in-out infinite;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
  opacity: 0.9;
}
@keyframes splashLogoFloat {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-6px); }
}
.theme-splash-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(32px, 5vw, 56px) !important;
  font-weight: 400;
  color: #ffffff;
  margin: 0;
  letter-spacing: 1px;
  line-height: 1.1;
  text-shadow: 0 4px 20px rgba(0,0,0,0.5);
  background: none !important;
  -webkit-background-clip: initial !important;
  -webkit-text-fill-color: initial !important;
  filter: none !important;
}
.theme-splash-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(10.5px, 1.4vw, 13px) !important;
  color: rgba(255, 255, 255, 0.4) !important;
  margin: 0;
  letter-spacing: 4px !important;
  text-transform: uppercase;
  font-weight: 500;
}
.theme-splash-header::after {
  content: '';
  display: block;
  width: 40px;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin-top: 12px;
}

/* ── Grid ── */
.theme-splash-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}
@media (max-width: 760px) {
  .theme-splash-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 400px) {
  .theme-splash-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
}

/* ── Card base ── */
.theme-splash-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-height: 270px;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  outline: none;
  text-align: center;
  padding: 0;
  /* Clean, minimalist dark glass pass */
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition:
    transform 0.4s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.3s ease,
    background-color 0.3s ease,
    box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
}
.theme-splash-card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
.theme-splash-card:active {
  transform: translateY(-2px);
  transition-duration: 0.1s;
}

/* Hide ambient color gradient backgrounds (for clean matte look) */
.theme-splash-card-bg {
  display: none !important;
}
/* Hide stripes */
.theme-splash-card-stripe {
  display: none !important;
}

/* Card content */
.theme-splash-card-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 16px 24px;
  width: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 60%, transparent 100%);
}

/* Clean, floating emoji (no border rings, just clean layout) */
.theme-splash-card-emoji {
  width: auto;
  height: auto;
  background: none !important;
  border: none !important;
  box-shadow: none !important;
  font-size: 44px !important;
  margin-bottom: 8px !important;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.theme-splash-card:hover .theme-splash-card-emoji {
  transform: scale(1.12) translateY(-4px) !important;
}

.theme-splash-card-name {
  font-family: 'Outfit', sans-serif;
  font-size: 15.5px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 0.5px;
}
.theme-splash-card-sub {
  font-family: 'Hind', sans-serif;
  font-size: 11.5px;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.45;
  font-weight: 500;
}

/* Accent Tags */
.theme-splash-card-tag {
  font-family: 'Outfit', sans-serif;
  font-size: 8.5px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 12px;
  margin-top: 6px;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;
}
.theme-splash-card:hover .theme-splash-card-tag {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.08);
}

/* ── Footnote ── */
.theme-splash-footnote {
  font-family: 'Outfit', sans-serif;
  font-size: 10.5px;
  color: rgba(255, 255, 255, 0.18);
  letter-spacing: 1.5px;
  text-align: center;
  margin: 0;
  animation: splashFootnotePulse 4s ease-in-out infinite;
}
@keyframes splashFootnotePulse {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
}
"""

content = content[:start] + NEW_SPLASH_CSS + content[end:]

with open(style_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Minimal Classy Splash CSS applied!")
