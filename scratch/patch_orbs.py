import os, re

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

ORB_CSS = """
/* ── Splash ambient orbs (background depth) ── */
.splash-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  animation: orbDrift 12s ease-in-out infinite alternate;
}
.splash-orb-gold {
  width: 480px; height: 480px;
  top: -120px; left: -80px;
  background: radial-gradient(circle, rgba(255,160,40,0.13) 0%, transparent 70%);
  animation-delay: 0s;
}
.splash-orb-purple {
  width: 400px; height: 400px;
  bottom: -100px; right: -60px;
  background: radial-gradient(circle, rgba(130,60,255,0.12) 0%, transparent 70%);
  animation-delay: -4s;
}
.splash-orb-green {
  width: 300px; height: 300px;
  bottom: 20%; left: 30%;
  background: radial-gradient(circle, rgba(30,180,90,0.09) 0%, transparent 70%);
  animation-delay: -8s;
}
@keyframes orbDrift {
  0%   { transform: translate(0px, 0px) scale(1); }
  33%  { transform: translate(30px, -20px) scale(1.05); }
  66%  { transform: translate(-20px, 30px) scale(0.95); }
  100% { transform: translate(10px, -10px) scale(1.02); }
}
"""

if "splash-orb" not in content:
    # Insert right before the COMPREHENSIVE MOBILE section
    mobile_section = "/* ==========================================================================\n   COMPREHENSIVE MOBILE RESPONSIVE"
    idx = content.find(mobile_section)
    if idx != -1:
        content = content[:idx] + ORB_CSS.strip() + "\n\n" + content[idx:]
        with open(style_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Orb CSS added!")
    else:
        content = content.rstrip() + "\n" + ORB_CSS
        with open(style_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Orb CSS appended at end!")
else:
    print("Orb CSS already present")

# Bump CSS version
html_files = [r"C:\Users\dvasu\window-seat\index.html",
              r"C:\Users\dvasu\window-seat\punjab.html",
              r"C:\Users\dvasu\window-seat\jammu.html",
              r"C:\Users\dvasu\window-seat\english.html"]
for p in html_files:
    with open(p, "r", encoding="utf-8") as f:
        h = f.read()
    h2 = re.sub(r'style\.css\?v=[\d\.]+', 'style.css?v=2.1', h)
    with open(p, "w", encoding="utf-8") as f:
        f.write(h2)
    print(f"Bumped CSS v in {os.path.basename(p)}")

print("Done!")
