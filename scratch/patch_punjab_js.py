import os

punjab_js_path = r"C:\Users\dvasu\window-seat\punjab.js"
tracks_path = r"C:\Users\dvasu\window-seat\punjab_tracks.txt"

with open(tracks_path, "r", encoding="utf-8") as f:
    new_tracks = f.read()

with open(punjab_js_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

old_block = '''const cassetteTracks = {
  "track_1": { title: "CHALLA - GURDAS MAAN", ytId: "G4H-W1e5_8o", color: "#e67e22" },
  "track_2": { title: "RANJHA (LOFI) - SAD PUNJABI", ytId: "R-v_1n8o_9A", color: "#3498db" },
  "track_3": { title: "MAI NI MERIYE - COZY SAD", ytId: "T75q4Q6W3vQ", color: "#e74c3c" },
  "track_4": { title: "RABBA RABBA MEINH BARSA", ytId: "hZuwe72Rtcc", color: "#2ecc71" },
  "track_5": { title: "YAAR ANMULLLE (SAD ACOUSTIC)", ytId: "eYF04jA5W1I", color: "#9b59b6" },
  "track_6": { title: "SUHE VE CHEERE WALEYA - SAD", ytId: "Gz6D4Y5H6vA", color: "#1abc9c" }
};'''

# Format new tracks - remove trailing comma from last track
lines = new_tracks.rstrip().split("\n")
if lines and lines[-1].endswith(","):
    lines[-1] = lines[-1][:-1]
tracks_formatted = "\n".join(lines)

new_block = f'''const cassetteTracks = {{
{tracks_formatted}
}};'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(punjab_js_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched punjab.js cassetteTracks!")
else:
    print("WARNING: Old block not found in punjab.js!")
