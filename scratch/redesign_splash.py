import os, re

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# ── Find and replace the entire splash CSS block ─────────────────────────────
start = content.find(".theme-splash-overlay {")
end   = content.find("/* ==========================================================================\n   COMPREHENSIVE MOBILE RESPONSIVE", start)

if start == -1 or end == -1:
    print(f"Block not found: start={start}, end={end}")
    exit()

NEW_SPLASH_CSS = """.theme-splash-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Rich layered background: deep indigo + subtle warm orbs */
  background:
    radial-gradient(ellipse 80% 60% at 15% 50%, rgba(255, 140, 30, 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 85% 20%, rgba(120, 60, 255, 0.1) 0%, transparent 55%),
    radial-gradient(ellipse 50% 70% at 50% 100%, rgba(30, 180, 90, 0.08) 0%, transparent 55%),
    radial-gradient(ellipse 100% 60% at 50% 0%, rgba(255, 180, 60, 0.06) 0%, transparent 50%),
    linear-gradient(160deg, #100c1e 0%, #0c1018 35%, #080f14 70%, #060810 100%);
  transition: opacity 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow-y: auto;
}
.theme-splash-overlay::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 160, 40, 0.0) 10%,
    rgba(255, 160, 40, 0.8) 30%,
    rgba(255, 255, 255, 0.6) 50%,
    rgba(150, 80, 255, 0.7) 70%,
    rgba(150, 80, 255, 0.0) 90%,
    transparent 100%
  );
  animation: splashTopLine 4s ease-in-out infinite alternate;
}
@keyframes splashTopLine {
  0%   { opacity: 0.5; transform: scaleX(0.5); }
  100% { opacity: 1;   transform: scaleX(1); }
}
/* Animated noise texture overlay for richness */
.theme-splash-overlay::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px;
  pointer-events: none;
  z-index: 0;
  opacity: 0.6;
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
  gap: 48px;
  padding: 60px 32px 48px;
  max-width: 1060px;
  width: 100%;
}

/* ── Header ── */
.theme-splash-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
}
.theme-splash-logo {
  font-size: 64px;
  animation: splashLogoFloat 4s ease-in-out infinite;
  filter: drop-shadow(0 0 28px rgba(255, 180, 60, 0.55))
          drop-shadow(0 0 8px rgba(255, 120, 20, 0.4));
  line-height: 1;
}
@keyframes splashLogoFloat {
  0%, 100% { transform: translateY(0px) rotate(-2deg); }
  50%       { transform: translateY(-10px) rotate(2deg); }
}
.theme-splash-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(34px, 6vw, 68px);
  font-weight: 400;
  color: #fff;
  margin: 0;
  letter-spacing: 2px;
  line-height: 1.05;
  text-shadow:
    0 0 60px rgba(255, 180, 60, 0.25),
    0 2px 4px rgba(0,0,0,0.5);
}
.theme-splash-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(12px, 1.8vw, 15px);
  color: rgba(255, 255, 255, 0.38);
  margin: 0;
  letter-spacing: 3px;
  text-transform: uppercase;
}
/* Thin decorative rule under the title */
.theme-splash-header::after {
  content: '';
  display: block;
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,180,60,0.6), transparent);
  margin-top: 4px;
}

/* ── Grid ── */
.theme-splash-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  width: 100%;
}
@media (max-width: 760px) {
  .theme-splash-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 400px) {
  .theme-splash-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
}

/* ── Card base ── */
.theme-splash-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-height: 280px;
  border-radius: 22px;
  overflow: hidden;
  cursor: pointer;
  outline: none;
  text-align: center;
  padding: 0;
  /* Rich glassmorphic base */
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.09);
  backdrop-filter: blur(24px) saturate(140%);
  -webkit-backdrop-filter: blur(24px) saturate(140%);
  transition:
    transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
    border-color 0.3s ease,
    box-shadow 0.3s ease;
  box-shadow:
    0 4px 24px rgba(0,0,0,0.35),
    inset 0 1px 0 rgba(255,255,255,0.07);
}
.theme-splash-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 28px 64px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(255,255,255,0.12);
}
.theme-splash-card:active {
  transform: scale(0.97);
  transition-duration: 0.12s;
}

/* Per-card glow border on hover */
.theme-splash-train  { border-color: rgba(255, 160, 40, 0.18); }
.theme-splash-punjab { border-color: rgba(255, 100, 50, 0.18); }
.theme-splash-jammu  { border-color: rgba(40,  200, 100, 0.16); }
.theme-splash-english{ border-color: rgba(130,  70, 255, 0.18); }

.theme-splash-train:hover  { border-color: rgba(255,160,40,0.55); box-shadow: 0 28px 64px rgba(0,0,0,0.6), 0 0 40px rgba(255,160,40,0.12), inset 0 1px 0 rgba(255,255,255,0.12); }
.theme-splash-punjab:hover { border-color: rgba(255,100,50,0.55); box-shadow: 0 28px 64px rgba(0,0,0,0.6), 0 0 40px rgba(255,100,50,0.12), inset 0 1px 0 rgba(255,255,255,0.12); }
.theme-splash-jammu:hover  { border-color: rgba(40,200,100,0.50); box-shadow: 0 28px 64px rgba(0,0,0,0.6), 0 0 40px rgba(40,200,100,0.10), inset 0 1px 0 rgba(255,255,255,0.12); }
.theme-splash-english:hover{ border-color: rgba(130,70,255,0.55); box-shadow: 0 28px 64px rgba(0,0,0,0.6), 0 0 40px rgba(130,70,255,0.12), inset 0 1px 0 rgba(255,255,255,0.12); }

/* Card inner ambient background — always visible, brighter on hover */
.theme-splash-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.55;
  transition: opacity 0.35s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-bg { opacity: 1; }

.theme-splash-train  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,170,50,0.2) 0%, rgba(200,100,20,0.1) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-punjab .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,100,40,0.22) 0%, rgba(200,50,10,0.1) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-jammu  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(40,210,100,0.18) 0%, rgba(10,140,60,0.09) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-english .theme-splash-card-bg{ background: linear-gradient(145deg, rgba(130,60,255,0.22) 0%, rgba(80,20,180,0.1) 45%, rgba(0,0,0,0) 80%); }

/* Corner stripe accent */
.theme-splash-card-stripe {
  position: absolute;
  top: 0; right: 0;
  width: 90px; height: 90px;
  border-radius: 0 22px 0 100%;
  opacity: 0.2;
  transition: opacity 0.3s, width 0.3s, height 0.3s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-stripe { opacity: 0.45; width: 110px; height: 110px; }
.theme-splash-train  .theme-splash-card-stripe { background: radial-gradient(circle at top right, #ffb830, transparent 70%); }
.theme-splash-punjab .theme-splash-card-stripe { background: radial-gradient(circle at top right, #ff6830, transparent 70%); }
.theme-splash-jammu  .theme-splash-card-stripe { background: radial-gradient(circle at top right, #30e070, transparent 70%); }
.theme-splash-english .theme-splash-card-stripe{ background: radial-gradient(circle at top right, #9050ff, transparent 70%); }

/* Card content: sits at the bottom */
.theme-splash-card-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  padding: 28px 18px 24px;
  width: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.35) 55%, transparent 100%);
}
.theme-splash-card-emoji {
  font-size: 52px;
  margin-bottom: 6px;
  filter: drop-shadow(0 6px 16px rgba(0,0,0,0.55));
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  line-height: 1;
}
.theme-splash-card:hover .theme-splash-card-emoji {
  transform: scale(1.22) translateY(-8px);
}
.theme-splash-card:active .theme-splash-card-emoji {
  transform: scale(0.92);
}
.theme-splash-card-name {
  font-family: 'Outfit', sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: #fff;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 6px rgba(0,0,0,0.6);
}
.theme-splash-card-sub {
  font-family: 'Hind', sans-serif;
  font-size: 11.5px;
  color: rgba(255,255,255,0.48);
  line-height: 1.45;
}
.theme-splash-card-tag {
  font-family: 'Outfit', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 20px;
  margin-top: 6px;
  border: 1px solid;
}
.theme-splash-train  .theme-splash-card-tag { background: rgba(255,160,40,0.18); color: #ffc060; border-color: rgba(255,160,40,0.4); }
.theme-splash-punjab .theme-splash-card-tag { background: rgba(255,100,50,0.18); color: #ff9070; border-color: rgba(255,100,50,0.4); }
.theme-splash-jammu  .theme-splash-card-tag { background: rgba(40,200,100,0.18); color: #60ee99; border-color: rgba(40,200,100,0.4); }
.theme-splash-english .theme-splash-card-tag{ background: rgba(130,70,255,0.18); color: #b088ff; border-color: rgba(130,70,255,0.4); }

/* ── Footnote ── */
.theme-splash-footnote {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.2);
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

print("Splash CSS completely replaced!")
