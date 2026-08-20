import os

style_path = r"C:\Users\dvasu\window-seat\style.css"
print("Improving sky quote legibility in style.css...")

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

# Locate the marker
marker = "/* Thematic & Symmetrically Legible Sky Title Overrides */"
parts = content.split(marker)

if len(parts) > 1:
    new_overrides = """/* Thematic & Symmetrically Legible Sky Title Overrides */
.route-punjab .window-sky-title .line1,
.route-punjab .window-sky-title .line2 {
  color: #ffe0b3 !important; /* Warm peach-gold */
  text-shadow: 2px 4px 12px rgba(0, 0, 0, 0.95), 0 0 20px rgba(139, 69, 19, 0.5) !important;
}
.route-punjab .window-sky-title .line3 {
  color: #ffd9a6 !important;
  font-size: calc(16px * var(--cabin-scale, 1)) !important;
  opacity: 1.0 !important;
  max-width: 520px !important;
  text-shadow: 2px 3px 8px rgba(0, 0, 0, 0.95), 0 0 10px rgba(0, 0, 0, 0.6) !important;
  font-style: italic !important;
  font-family: 'Playfair Display', 'Georgia', serif !important;
}

.route-jammu .window-sky-title .line1,
.route-jammu .window-sky-title .line2 {
  color: #fff9f0 !important; /* Clean ivory */
  text-shadow: 2px 4px 12px rgba(0, 0, 0, 0.95), 0 0 15px rgba(0, 0, 0, 0.6) !important;
}
.route-jammu .window-sky-title .line3 {
  color: #ffebd6 !important;
  font-size: calc(16px * var(--cabin-scale, 1)) !important;
  opacity: 1.0 !important;
  max-width: 520px !important;
  text-shadow: 2px 3px 8px rgba(0, 0, 0, 0.95), 0 0 10px rgba(0, 0, 0, 0.6) !important;
  font-style: italic !important;
  font-family: 'Playfair Display', 'Georgia', serif !important;
}

.route-english .window-sky-title .line1,
.route-english .window-sky-title .line2 {
  color: #ffd899 !important; /* Ambient candle gold */
  text-shadow: 2px 4px 15px rgba(0, 0, 0, 0.98), 0 0 25px rgba(243, 104, 33, 0.35) !important;
}
.route-english .window-sky-title .line3 {
  color: #ffb85c !important; /* Brighter gold */
  font-size: calc(17px * var(--cabin-scale, 1)) !important;
  opacity: 1.0 !important;
  max-width: 520px !important;
  text-shadow: 2px 3px 10px rgba(0, 0, 0, 0.98), 0 0 15px rgba(243, 104, 33, 0.4) !important;
  font-style: italic !important;
  font-family: 'Playfair Display', 'Georgia', serif !important;
}"""
    
    new_content = parts[0] + new_overrides
    with open(style_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Quote styles successfully upgraded!")
else:
    print("WARNING: Marker not found in style.css!")
