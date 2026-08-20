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
  /* Classy, premium Golden Hour & Twilight backdrop */
  background:
    radial-gradient(ellipse 70% 60% at 20% 30%, rgba(255, 180, 100, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse 60% 60% at 80% 80%, rgba(130, 80, 255, 0.12) 0%, transparent 60%),
    radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
    linear-gradient(135deg, #18152c 0%, #0d0f1a 50%, #05060b 100%);
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
    rgba(255, 180, 80, 0.0) 10%,
    rgba(255, 180, 80, 0.8) 35%,
    rgba(255, 255, 255, 0.6) 50%,
    rgba(150, 100, 255, 0.7) 65%,
    rgba(150, 100, 255, 0.0) 90%,
    transparent 100%
  );
  animation: splashTopLine 4s ease-in-out infinite alternate;
}
@keyframes splashTopLine {
  0%   { opacity: 0.5; transform: scaleX(0.5); }
  100% { opacity: 1;   transform: scaleX(1); }
}
/* Film grain texture */
.theme-splash-overlay::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px;
  pointer-events: none;
  z-index: 0;
  opacity: 0.5;
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
  gap: 40px;
  padding: 60px 32px 48px;
  max-width: 1060px;
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
  font-size: 72px;
  animation: splashLogoFloat 4s ease-in-out infinite;
  filter: drop-shadow(0 0 35px rgba(255, 180, 60, 0.7))
          drop-shadow(0 0 10px rgba(255, 120, 20, 0.4));
  line-height: 1;
}
@keyframes splashLogoFloat {
  0%, 100% { transform: translateY(0px) rotate(-1.5deg); }
  50%       { transform: translateY(-8px) rotate(1.5deg); }
}
.theme-splash-title {
  font-family: 'Rozha One', serif;
  font-size: clamp(34px, 5.5vw, 64px) !important;
  font-weight: 400;
  /* Classy white to gold gradient title */
  background: linear-gradient(135deg, #ffffff 40%, #ffdfa9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  letter-spacing: 1.5px;
  line-height: 1.1;
  text-shadow: none !important;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.45));
}
.theme-splash-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(11px, 1.6vw, 14px) !important;
  color: rgba(255, 255, 255, 0.45) !important;
  margin: 0;
  letter-spacing: 4px !important;
  text-transform: uppercase;
}
.theme-splash-header::after {
  content: '';
  display: block;
  width: 50px;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,180,60,0.5), transparent);
  margin-top: 6px;
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
  min-height: 290px;
  border-radius: 22px;
  overflow: hidden;
  cursor: pointer;
  outline: none;
  text-align: center;
  padding: 0;
  /* Classy, high-transparency frosted glass pass */
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(24px) saturate(140%);
  -webkit-backdrop-filter: blur(24px) saturate(140%);
  transition:
    transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
    border-color 0.3s ease,
    box-shadow 0.3s ease;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.12);
}
.theme-splash-card:hover {
  transform: translateY(-10px) scale(1.03);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.35);
  box-shadow:
    0 24px 50px rgba(0,0,0,0.55),
    0 0 30px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255,255,255,0.22);
}
.theme-splash-card:active {
  transform: scale(0.97);
  transition-duration: 0.12s;
}

/* Per-card glow border on hover */
.theme-splash-train  { border-color: rgba(255, 180, 60, 0.22); }
.theme-splash-punjab { border-color: rgba(255, 120, 60, 0.22); }
.theme-splash-jammu  { border-color: rgba(60,  220, 120, 0.18); }
.theme-splash-english{ border-color: rgba(150, 100, 255, 0.22); }

.theme-splash-train:hover  { border-color: rgba(255,180,60,0.7); box-shadow: 0 24px 50px rgba(0,0,0,0.55), 0 0 35px rgba(255,180,60,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-punjab:hover { border-color: rgba(255,120,60,0.7); box-shadow: 0 24px 50px rgba(0,0,0,0.55), 0 0 35px rgba(255,120,60,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-jammu:hover  { border-color: rgba(60,220,120,0.65); box-shadow: 0 24px 50px rgba(0,0,0,0.55), 0 0 35px rgba(60,220,120,0.12), inset 0 1px 0 rgba(255,255,255,0.25); }
.theme-splash-english:hover{ border-color: rgba(150,100,255,0.7); box-shadow: 0 24px 50px rgba(0,0,0,0.55), 0 0 35px rgba(150,100,255,0.15), inset 0 1px 0 rgba(255,255,255,0.25); }

/* Card inner ambient background — always visible, brighter on hover */
.theme-splash-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.65;
  transition: opacity 0.35s;
  pointer-events: none;
}
.theme-splash-card:hover .theme-splash-card-bg { opacity: 0.95; }

.theme-splash-train  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,180,60,0.2) 0%, rgba(200,110,20,0.08) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-punjab .theme-splash-card-bg { background: linear-gradient(145deg, rgba(255,120,60,0.22) 0%, rgba(200,60,10,0.08) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-jammu  .theme-splash-card-bg { background: linear-gradient(145deg, rgba(60,220,120,0.18) 0%, rgba(10,150,70,0.08) 45%, rgba(0,0,0,0) 80%); }
.theme-splash-english .theme-splash-card-bg{ background: linear-gradient(145deg, rgba(150,100,255,0.22) 0%, rgba(90,30,200,0.08) 45%, rgba(0,0,0,0) 80%); }

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
  color: rgba(255,255,255,0.55);
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
.theme-splash-train  .theme-splash-card-tag { background: rgba(255,180,60,0.18); color: #ffc060; border-color: rgba(255,180,60,0.4); }
.theme-splash-punjab .theme-splash-card-tag { background: rgba(255,120,60,0.18); color: #ff9070; border-color: rgba(255,120,60,0.4); }
.theme-splash-jammu  .theme-splash-card-tag { background: rgba(60,220,120,0.18); color: #60ee99; border-color: rgba(60,220,120,0.4); }
.theme-splash-english .theme-splash-card-tag{ background: rgba(150,100,255,0.18); color: #b088ff; border-color: rgba(150,100,255,0.4); }

/* ── Footnote ── */
.theme-splash-footnote {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.22);
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

print("Classy Splash CSS applied successfully!")
