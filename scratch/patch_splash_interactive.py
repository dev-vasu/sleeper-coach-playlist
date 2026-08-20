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
  /* Make the background the actual live retro train cabin! */
  /* Semi-transparent dark overlay + soft glass blur allows the moving cabin & scenery to show through */
  background: rgba(8, 10, 15, 0.55);
  backdrop-filter: blur(14px) saturate(120%);
  -webkit-backdrop-filter: blur(14px) saturate(120%);
  transition: opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow-y: auto;
}
.theme-splash-overlay::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 180, 80, 0.0) 10%,
    rgba(255, 180, 80, 0.8) 35%,
    rgba(255, 255, 255, 0.65) 50%,
    rgba(150, 100, 255, 0.8) 65%,
    rgba(150, 100, 255, 0.0) 90%,
    transparent 100%
  );
  animation: splashTopLine 4s ease-in-out infinite alternate;
  z-index: 2;
}
@keyframes splashTopLine {
  0%   { opacity: 0.5; transform: scaleX(0.5); }
  100% { opacity: 1;   transform: scaleX(1); }
}
/* Subtle film grain on top of the blurred cabin scenery */
.theme-splash-overlay::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.95' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px;
  pointer-events: none;
  z-index: 1;
  opacity: 0.6;
}
.theme-splash-overlay.dismissing {
  opacity: 0;
  pointer-events: none;
}
.theme-splash-overlay.hidden {
  display: none;
}

/* ── Ambient floating orbs (gives a warm colored glow over the blurred cabin) ── */
.splash-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(100px);
  pointer-events: none;
  z-index: 1;
  animation: orbDrift 16s ease-in-out infinite alternate;
}
.splash-orb-gold {
  width: 500px; height: 500px;
  top: -100px; left: -100px;
  background: radial-gradient(circle, rgba(255,160,40,0.14) 0%, transparent 70%);
  animation-delay: 0s;
}
.splash-orb-purple {
  width: 450px; height: 450px;
  bottom: -80px; right: -80px;
  background: radial-gradient(circle, rgba(140,70,255,0.12) 0%, transparent 70%);
  animation-delay: -4s;
}
.splash-orb-green {
  width: 400px; height: 400px;
  bottom: 25%; left: 30%;
  background: radial-gradient(circle, rgba(40,210,120,0.1) 0%, transparent 70%);
  animation-delay: -8s;
}
@keyframes orbDrift {
  0%   { transform: translate(0px, 0px) scale(1); }
  50%  { transform: translate(30px, -20px) scale(1.05); }
  100% { transform: translate(-20px, 20px) scale(0.95); }
}

/* ── Inner layout ── */
.theme-splash-inner {
  position: relative;
  z-index: 2;
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
  font-size: 76px;
  animation: splashLogoFloat 4s ease-in-out infinite;
  filter: drop-shadow(0 0 30px rgba(255, 180, 60, 0.65))
          drop-shadow(0 0 8px rgba(255, 120, 20, 0.4));
  line-height: 1;
}
@keyframes splashLogoFloat {
  0%, 100% { transform: translateY(0px) rotate(-1deg); }
  50%       { transform: translateY(-6px) rotate(1deg); }
}
.theme-splash-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(36px, 5.8vw, 68px) !important;
  font-weight: 400;
  /* Classy white-to-gold gradient text */
  background: linear-gradient(135deg, #ffffff 30%, #ffdfaa 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  margin: 0;
  letter-spacing: 2px;
  line-height: 1.05;
  text-shadow: none !important;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.6)) !important;
}
.theme-splash-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(11.5px, 1.7vw, 14.5px) !important;
  color: rgba(255, 255, 255, 0.5) !important;
  margin: 0;
  letter-spacing: 4px !important;
  text-transform: uppercase;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
.theme-splash-header::after {
  content: '';
  display: block;
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,180,60,0.6), transparent);
  margin-top: 8px;
}

/* ── Grid ── */
.theme-splash-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
}
@media (max-width: 760px) {
  .theme-splash-grid { grid-template-columns: repeat(2, 1fr); gap: 14px; }
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
  min-height: 295px;
  border-radius: 22px;
  overflow: hidden;
  cursor: pointer;
  outline: none;
  text-align: center;
  padding: 0;
  /* Frost glassmorphism over the active cabin background */
  background: rgba(15, 18, 25, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(12px) saturate(120%);
  -webkit-backdrop-filter: blur(12px) saturate(120%);
  transition:
    transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
    border-color 0.3s ease,
    box-shadow 0.3s ease;
  box-shadow:
    0 12px 35px rgba(0,0,0,0.5),
    inset 0 1px 0 rgba(255,255,255,0.08);
}
.theme-splash-card:hover {
  transform: translateY(-10px) scale(1.03);
  background: rgba(25, 30, 42, 0.68);
  border-color: rgba(255, 255, 255, 0.38);
  box-shadow:
    0 28px 60px rgba(0,0,0,0.65),
    0 0 35px rgba(255, 255, 255, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.2);
}
.theme-splash-card:active {
  transform: scale(0.97);
  transition-duration: 0.12s;
}

/* Per-card border glow states */
.theme-splash-train  { border-color: rgba(255, 180, 60, 0.25); }
.theme-splash-punjab { border-color: rgba(255, 120, 60, 0.25); }
.theme-splash-jammu  { border-color: rgba(60,  220, 120, 0.22); }
.theme-splash-english{ border-color: rgba(150, 100, 255, 0.25); }

.theme-splash-train:hover  { border-color: rgba(255,180,60,0.7); box-shadow: 0 28px 60px rgba(0,0,0,0.65), 0 0 35px rgba(255,180,60,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-punjab:hover { border-color: rgba(255,120,60,0.7); box-shadow: 0 28px 60px rgba(0,0,0,0.65), 0 0 35px rgba(255,120,60,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-jammu:hover  { border-color: rgba(60,220,120,0.65); box-shadow: 0 28px 60px rgba(0,0,0,0.65), 0 0 35px rgba(60,220,120,0.12), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-english:hover{ border-color: rgba(150,100,255,0.7); box-shadow: 0 28px 60px rgba(0,0,0,0.65), 0 0 35px rgba(150,100,255,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }

/* Card inner ambient background — always visible, brighter on hover */
.theme-splash-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.65;
  transition: opacity 0.35s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-bg { opacity: 0.95; }

.theme-splash-train  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,180,60,0.18) 0%, rgba(200,110,20,0.06) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-punjab .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,120,60,0.2) 0%, rgba(200,60,10,0.06) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-jammu  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(60,220,120,0.16) 0%, rgba(10,150,70,0.06) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-english .theme-splash-card-bg{ background: linear-gradient(145deg, rgba(150,100,255,0.2) 0%, rgba(90,30,200,0.06) 45%, rgba(0,0,0,0) 80%); }

/* Corner stripe accent */
.theme-splash-card-stripe {
  position: absolute;
  top: 0; right: 0;
  width: 90px; height: 90px;
  border-radius: 0 22px 0 100%;
  opacity: 0.25;
  transition: opacity 0.3s, width 0.3s, height 0.3s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-stripe { opacity: 0.55; width: 110px; height: 110px; }
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
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 55%, transparent 100%);
}

/* Glass Badge round container for Emojis */
.theme-splash-card-emoji {
  width: 76px;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1.5px solid rgba(255, 255, 255, 0.18);
  border-radius: 50%;
  font-size: 36px;
  margin-bottom: 10px;
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.25),
    inset 0 2px 5px rgba(255, 255, 255, 0.12);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  line-height: 1;
}
.theme-splash-card:hover .theme-splash-card-emoji {
  transform: scale(1.18) rotate(6deg);
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 
    0 12px 25px rgba(0, 0, 0, 0.35),
    inset 0 2px 8px rgba(255, 255, 255, 0.25);
}
.theme-splash-card:active .theme-splash-card-emoji {
  transform: scale(0.92);
}

.theme-splash-train .theme-splash-card-emoji { border-color: rgba(255, 180, 60, 0.38); }
.theme-splash-punjab .theme-splash-card-emoji { border-color: rgba(255, 120, 60, 0.38); }
.theme-splash-jammu .theme-splash-card-emoji { border-color: rgba(60, 220, 120, 0.34); }
.theme-splash-english .theme-splash-card-emoji { border-color: rgba(150, 100, 255, 0.38); }

.theme-splash-train:hover .theme-splash-card-emoji { border-color: rgba(255, 180, 60, 0.85); box-shadow: 0 0 15px rgba(255, 180, 60, 0.3), inset 0 2px 8px rgba(255, 255, 255, 0.25); }
.theme-splash-punjab:hover .theme-splash-card-emoji { border-color: rgba(255, 120, 60, 0.85); box-shadow: 0 0 15px rgba(255, 120, 60, 0.3), inset 0 2px 8px rgba(255, 255, 255, 0.25); }
.theme-splash-jammu:hover .theme-splash-card-emoji { border-color: rgba(60, 220, 120, 0.85); box-shadow: 0 0 15px rgba(60, 220, 120, 0.3), inset 0 2px 8px rgba(255, 255, 255, 0.25); }
.theme-splash-english:hover .theme-splash-card-emoji { border-color: rgba(150, 100, 255, 0.85); box-shadow: 0 0 15px rgba(150, 100, 255, 0.3), inset 0 2px 8px rgba(255, 255, 255, 0.25); }

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
  font-size: 12px;
  color: rgba(255,255,255,0.65);
  line-height: 1.45;
  text-shadow: 0 1px 3px rgba(0,0,0,0.5);
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
.theme-splash-train  .theme-splash-card-tag { background: rgba(255,180,60,0.22); color: #ffc060; border-color: rgba(255,180,60,0.4); }
.theme-splash-punjab .theme-splash-card-tag { background: rgba(255,120,60,0.22); color: #ff9070; border-color: rgba(255,120,60,0.4); }
.theme-splash-jammu  .theme-splash-card-tag { background: rgba(60,220,120,0.22); color: #60ee99; border-color: rgba(60,220,120,0.4); }
.theme-splash-english .theme-splash-card-tag{ background: rgba(150,100,255,0.22); color: #b088ff; border-color: rgba(150,100,255,0.4); }

/* ── Footnote ── */
.theme-splash-footnote {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.25);
  letter-spacing: 1.5px;
  text-align: center;
  margin: 0;
  animation: splashFootnotePulse 4s ease-in-out infinite;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
@keyframes splashFootnotePulse {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
}
"""

content = content[:start] + NEW_SPLASH_CSS + content[end:]

with open(style_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Cozy interactive glass splash CSS applied!")
