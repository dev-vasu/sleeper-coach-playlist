import os

app_path = r"C:\Users\dvasu\window-seat\app.js"
tracks_path = r"C:\Users\dvasu\window-seat\english_tracks.txt"

with open(tracks_path, "r", encoding="utf-8") as f:
    new_tracks_content = f.read()

with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

# Define the old english block exactly
old_english_block = """  english: {
    "track_1": { title: "SOUND OF SILENCE - SIMON & GARFUNKEL", ytId: "f7McpVPlhdc", color: "#34495e" },
    "track_2": { title: "HEART OF GOLD - NEIL YOUNG", ytId: "k0tO35VI7MY", color: "#e67e22" },
    "track_3": { title: "WILD WORLD - CAT STEVENS", ytId: "H51B6N1xLFE", color: "#3498db" },
    "track_4": { title: "BLOWIN' IN THE WIND - BOB DYLAN", ytId: "vWwgrjjIMOM", color: "#2ecc71" },
    "track_5": { title: "HOTEL CALIFORNIA (COZY LOFI)", ytId: "m7vF6b7z8xI", color: "#9b59b6" },
    "track_6": { title: "WISH YOU WERE HERE - PINK FLOYD", ytId: "IXdNemPvYQs", color: "#1abc9c" }
  }"""

# Remove the trailing comma from the last track in the new tracks content
new_lines = new_tracks_content.rstrip().split("\n")
if new_lines:
    last_line = new_lines[-1]
    if last_line.endswith(","):
        new_lines[-1] = last_line[:-1]
new_tracks_formatted = "\n".join(new_lines)

new_english_block = f"""  english: {{
{new_tracks_formatted}
  }}"""

if old_english_block in app_content:
    app_content = app_content.replace(old_english_block, new_english_block)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)
    print("Successfully patched english playlist in app.js!")
else:
    # Try alternate line ending matching
    old_english_normalized = old_english_block.replace("\r\n", "\n")
    app_normalized = app_content.replace("\r\n", "\n")
    if old_english_normalized in app_normalized:
        app_normalized = app_normalized.replace(old_english_normalized, new_english_block)
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_normalized)
        print("Successfully patched english playlist in app.js (normalized line endings)!")
    else:
        print("WARNING: Old english block not found in app.js!")
