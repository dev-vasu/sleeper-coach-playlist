import json, re

raw_path = r"C:\Users\dvasu\window-seat\scratch\jammu_playlist_raw.json"
out_path = r"C:\Users\dvasu\window-seat\jammu_tracks.txt"

with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Found {len(entries)} tracks!")

colors = ["#e74c3c","#3498db","#f1c40f","#2ecc71","#9b59b6","#1abc9c","#e67e22","#34495e"]

with open(out_path, "w", encoding="utf-8") as out:
    for idx, entry in enumerate(entries):
        title = entry.get("title", "Unknown Title")
        ytId  = entry.get("id")
        if not ytId:
            continue
        color = colors[idx % len(colors)]
        t = title.replace('"', '\\"').upper()
        t = re.sub(r'\s*\(OFFICIAL\s*(VIDEO|AUDIO|SONG)?\)', '', t)
        t = re.sub(r'\s*\|.*$', '', t)
        t = re.sub(r'\s*\[OFFICIAL.*$', '', t)
        t = re.sub(r'\s*\(LYRICS\)', '', t)
        t = re.sub(r'\s*FT\.[^|,]*', '', t)
        t = t.strip()
        out.write(f'    "track_{idx+1}": {{ title: "{t}", ytId: "{ytId}", color: "{color}" }},\n')
        print(f"  {idx+1}. {t}")

print(f"\nWrote {len(entries)} tracks to jammu_tracks.txt")
