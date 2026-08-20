import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

widget_css = """
/* ==========================================================================
   FLOATING THEME EXPLORER WIDGET
   ========================================================================== */
.theme-explorer-widget {
  position: absolute;
  bottom: calc(110px * var(--cabin-scale, 1));
  left: calc(28px * var(--cabin-scale, 1));
  z-index: 85;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.theme-explorer-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 50px;
  padding: 10px 18px 10px 14px;
  color: #fff;
  font-family: 'Outfit', sans-serif;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.06);
  white-space: nowrap;
}
.theme-explorer-trigger:hover {
  background: rgba(30, 41, 59, 0.85);
  border-color: rgba(255, 200, 100, 0.35);
  box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 20px rgba(255, 180, 60, 0.15);
  transform: translateY(-2px);
}
.theme-explorer-icon {
  font-size: 16px;
}
.theme-explorer-label {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 11px;
}
.theme-explorer-arrow {
  font-size: 18px;
  opacity: 0.6;
  transition: transform 0.2s, opacity 0.2s;
}
.theme-explorer-widget.open .theme-explorer-arrow {
  transform: rotate(90deg);
  opacity: 1;
}

/* Expand Panel */
.theme-explorer-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  opacity: 0;
  pointer-events: none;
  transform: translateY(10px);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  width: 260px;
}
.theme-explorer-widget.open .theme-explorer-panel {
  opacity: 1;
  pointer-events: all;
  transform: translateY(0);
}

.theme-explorer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255,255,255,0.5);
  font-family: 'Outfit', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 0 4px 4px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 2px;
}
.theme-explorer-close {
  background: none;
  border: none;
  color: rgba(255,255,255,0.4);
  font-size: 18px;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  transition: color 0.2s;
}
.theme-explorer-close:hover { color: #fff; }

/* Theme Cards */
.theme-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(14px) saturate(160%);
  -webkit-backdrop-filter: blur(14px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 12px 14px;
  text-decoration: none;
  color: #fff;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
}
.theme-card:hover {
  transform: translateX(4px);
  border-color: rgba(255,255,255,0.22);
  box-shadow: 0 8px 28px rgba(0,0,0,0.45);
}
.theme-card-glow {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 14px;
}
.theme-card:hover .theme-card-glow { opacity: 1; }

.theme-card-punjab .theme-card-glow { background: radial-gradient(ellipse at left, rgba(255, 160, 60, 0.12), transparent 70%); }
.theme-card-jammu .theme-card-glow { background: radial-gradient(ellipse at left, rgba(80, 200, 120, 0.12), transparent 70%); }
.theme-card-english .theme-card-glow { background: radial-gradient(ellipse at left, rgba(120, 100, 255, 0.12), transparent 70%); }

.theme-card-icon {
  font-size: 24px;
  flex-shrink: 0;
  width: 36px;
  text-align: center;
}
.theme-card-info {
  flex: 1;
}
.theme-card-name {
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #fff;
  text-transform: uppercase;
}
.theme-card-desc {
  font-family: 'Hind', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  margin-top: 2px;
}
.theme-card-arrow {
  font-size: 16px;
  opacity: 0.3;
  transition: opacity 0.2s, transform 0.2s;
}
.theme-card:hover .theme-card-arrow {
  opacity: 0.9;
  transform: translateX(3px);
}

/* Accent left border per theme */
.theme-card-punjab { border-left: 3px solid rgba(255, 165, 60, 0.6); }
.theme-card-jammu  { border-left: 3px solid rgba(80, 210, 120, 0.6); }
.theme-card-english { border-left: 3px solid rgba(130, 100, 255, 0.6); }
"""

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

if "FLOATING THEME EXPLORER WIDGET" not in content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(widget_css)
    print("Theme explorer CSS appended successfully!")
else:
    print("Theme explorer CSS already present.")
