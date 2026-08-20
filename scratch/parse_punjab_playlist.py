import json
import re
import os

raw_path = r"C:\Users\dvasu\window-seat\scratch\punjab_playlist_raw.json"
out_path = r"C:\Users\dvasu\window-seat\punjab_tracks.txt"

with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Found {len(entries)} tracks!")

colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]

with open(out_path, "w", encoding="utf-8") as out:
    for idx, entry in enumerate(entries):
        title = entry.get("title", "Unknown Title")
        ytId = entry.get("id")
        if not ytId:
            continue

        color = colors[idx % len(colors)]

        title_clean = title.replace('"', '\\"').upper()
        title_clean = re.sub(r'\s*\(OFFICIAL\s*(VIDEO|AUDIO|SONG|SOND)?\)', '', title_clean)
        title_clean = re.sub(r'\s*\|.*$', '', title_clean)
        title_clean = re.sub(r'\s*\[OFFICIAL.*$', '', title_clean)
        title_clean = re.sub(r'\s*\(LYRICS\)', '', title_clean)
        title_clean = re.sub(r'\s*FT\.[^|,]*', '', title_clean)
        title_clean = title_clean.strip()

        out.write(f'    "track_{idx + 1}": {{ title: "{title_clean}", ytId: "{ytId}", color: "{color}" }},\n')

print(f"Wrote {len(entries)} tracks to punjab_tracks.txt!")
