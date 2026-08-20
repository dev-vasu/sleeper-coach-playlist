import os

app_js_path = r"C:\Users\dvasu\window-seat\app.js"
tracks_path = r"C:\Users\dvasu\window-seat\punjab_tracks.txt"

with open(tracks_path, "r", encoding="utf-8") as f:
    new_tracks = f.read()

with open(app_js_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

old_block = '''  punjab: {
    "track_1": { title: "CHALLA - GURDAS MAAN", ytId: "G4H-W1e5_8o", color: "#e67e22" },
    "track_2": { title: "RANJHA (LOFI) - SAD PUNJABI", ytId: "R-v_1n8o_9A", color: "#3498db" },
    "track_3": { title: "MAI NI MERIYE - COZY SAD", ytId: "T75q4Q6W3vQ", color: "#e74c3c" },
    "track_4": { title: "RABBA RABBA MEINH BARSA", ytId: "hZuwe72Rtcc", color: "#2ecc71" },
    "track_5": { title: "YAAR ANMULLLE (SAD ACOUSTIC)", ytId: "eYF04jA5W1I", color: "#9b59b6" },
    "track_6": { title: "SUHE VE CHEERE WALEYA - SAD", ytId: "Gz6D4Y5H6vA", color: "#1abc9c" }
  },'''

# Format new tracks - keep trailing comma on last track (since there's a next block)
lines = new_tracks.rstrip().split("\n")
tracks_formatted = "\n".join(lines)

new_block = f'''  punjab: {{
{tracks_formatted}
  }},'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched app.js punjab block!")
else:
    print("WARNING: Old punjab block not found in app.js!")
