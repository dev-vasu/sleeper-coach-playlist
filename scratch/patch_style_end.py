with open(r"C:\Users\dvasu\window-seat\style.css", "r", encoding="utf-8") as f:
    content = f.read()

# Split on body.route-english #trainTypeSection
parts = content.split('body.route-english #trainTypeSection,')
if len(parts) > 1:
    end_styles = """body.route-english #trainTypeSection,
body.route-english #btnHorn,
body.route-english #btnAnnounce {
  display: none !important;
  pointer-events: none !important;
}

/* Interactive Diary Hotspot */
.prop-diary-hotspot {
  position: absolute;
  bottom: 25px;
  left: 41%;
  width: 250px;
  height: 120px;
  cursor: pointer;
  z-index: 25;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.01);
  transition: box-shadow 0.3s;
}
.prop-diary-hotspot:hover {
  box-shadow: 0 0 18px rgba(226, 184, 101, 0.5);
}

/* Diary Zoom Modal Card */
.diary-zoom-card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  width: 440px;
  max-width: 90%;
  background: #fdfaf0; /* vintage paper texture coloring */
  border-radius: 8px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.85), inset 0 0 50px rgba(139,121,94,0.25);
  border: 1px solid #e5d8be;
  padding: 35px 30px;
  z-index: 1000;
  display: none;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  color: #4a3b32;
  box-sizing: border-box;
}
.diary-zoom-card.open {
  display: block;
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}
.diary-close {
  position: absolute;
  top: 15px;
  right: 18px;
  background: none;
  border: none;
  font-size: 28px;
  color: #8b795e;
  cursor: pointer;
  transition: color 0.2s;
}
.diary-close:hover {
  color: #5c4033;
}
.diary-poetry {
  font-style: italic;
  font-size: 15px;
  line-height: 1.7;
  margin-top: 20px;
  border-left: 3px solid #8b795e;
  padding-left: 14px;
  color: #5c4033;
  font-family: 'Hind', sans-serif;
  letter-spacing: 0.2px;
}

/* Warm Golden Parallax Dust/Leaves for Punjab */
.route-punjab .dust-dot {
  background: rgba(230, 126, 34, 0.45); /* warm golden orange leaves/spores */
  box-shadow: 0 0 8px rgba(230, 126, 34, 0.25);
  animation: floatLeaves 18s linear infinite;
}

@keyframes floatLeaves {
  0% {
    transform: translateY(110vh) translateX(-20px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-10vh) translateX(120px) rotate(360deg);
    opacity: 0;
  }
}
"""
    new_content = parts[0] + end_styles
    with open(r"C:\Users\dvasu\window-seat\style.css", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully patched style.css end!")
else:
    print("Could not find trainTypeSection in style.css")
