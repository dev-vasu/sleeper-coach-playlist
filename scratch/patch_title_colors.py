import os

style_path = r"C:\Users\dvasu\window-seat\style.css"
print("Appending legible title color overrides to style.css...")

with open(style_path, "r", encoding="utf-8") as f:
    style_content = f.read()

color_overrides = """
/* Thematic & Symmetrically Legible Sky Title Overrides */
.route-punjab .window-sky-title .line1,
.route-punjab .window-sky-title .line2 {
  color: #ffe0b3 !important; /* Warm peach-gold */
  text-shadow: 2px 4px 12px rgba(0, 0, 0, 0.95), 0 0 20px rgba(139, 69, 19, 0.5) !important;
}
.route-punjab .window-sky-title .line3 {
  color: #ffd9a6 !important;
  text-shadow: 1px 2px 6px rgba(0, 0, 0, 0.9) !important;
}

.route-jammu .window-sky-title .line1,
.route-jammu .window-sky-title .line2 {
  color: #fff9f0 !important; /* Clean ivory */
  text-shadow: 2px 4px 12px rgba(0, 0, 0, 0.95), 0 0 15px rgba(0, 0, 0, 0.6) !important;
}
.route-jammu .window-sky-title .line3 {
  color: #ffebd6 !important;
  text-shadow: 1px 2px 6px rgba(0, 0, 0, 0.9) !important;
}

.route-english .window-sky-title .line1,
.route-english .window-sky-title .line2 {
  color: #ffd899 !important; /* Ambient candle gold */
  text-shadow: 2px 4px 15px rgba(0, 0, 0, 0.98), 0 0 25px rgba(243, 104, 33, 0.35) !important;
}
.route-english .window-sky-title .line3 {
  color: #ffc475 !important;
  text-shadow: 1px 2px 8px rgba(0, 0, 0, 0.95) !important;
}
"""

if "/* Thematic & Symmetrically Legible Sky Title Overrides" not in style_content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(color_overrides)
    print("Legibility CSS successfully appended!")
else:
    print("Legibility CSS already present.")
