import re
import html

path = r"C:\Users\dvasu\.gemini\antigravity-cli\brain\c0dc278a-945b-452c-a2e3-ccf5fd593546\.system_generated\steps\5263\content.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for links like /watch?v=VIDEO_ID or youtube.com/watch?v=VIDEO_ID
# We can search for markdown links: [Title](...watch?v=VIDEO_ID...)
pattern = r'\[([^\]]+)\]\([^)]*watch\?v=([a-zA-Z0-9_-]{11})[^)]*\)'

matches = re.findall(pattern, content)
seen = set()
tracks = []
colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]

for title, vid in matches:
    if vid not in seen:
        seen.add(vid)
        # Clean title
        title_clean = html.unescape(title).strip()
        # Skip titles that are just durations or play icons
        if re.match(r'^\d+:\d+$', title_clean) or title_clean.lower() in ["play", "play all", "shuffle", ""]:
            continue
        title_clean = title_clean.replace('"', '\\"').upper()
        tracks.append((title_clean, vid))

print(f"Parsed {len(tracks)} tracks:")
for t, v in tracks[:15]:
    print(f"- {t} (ID: {v})")

with open("jammu_tracks.txt", "w", encoding="utf-8") as out:
    for idx, (title, ytId) in enumerate(tracks):
        color = colors[idx % len(colors)]
        out.write(f'    "track_{idx + 1}": {{ title: "{title}", ytId: "{ytId}", color: "{color}" }},\n')

print(f"Wrote {len(tracks)} tracks to jammu_tracks.txt")
