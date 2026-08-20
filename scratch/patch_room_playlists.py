import os

# 1. Patch jammu.js
jammu_js_path = r"C:\Users\dvasu\window-seat\jammu.js"
jammu_tracks_path = r"C:\Users\dvasu\window-seat\jammu_tracks.txt"

with open(jammu_tracks_path, "r", encoding="utf-8") as f:
    jammu_tracks = f.read()

with open(jammu_js_path, "r", encoding="utf-8") as f:
    jammu_js_content = f.read()

old_jammu_tracks = """const cassetteTracks = {
  "track_1": { title: "JAMMU DIYE RAAHEIN - ACOUSTIC", ytId: "N42UlyZ2BwU", color: "#1abc9c" },
  "track_2": { title: "KUNDA KHOLYA - DOGRI FOLK", ytId: "Gk05tY4U2M4", color: "#e74c3c" },
  "track_3": { title: "CHANN MADA CHADEYA", ytId: "plB0ytzIlqI", color: "#f1c40f" },
  "track_4": { title: "DOGRI ACOUSTIC MIX", ytId: "dDR4oiyjUBA", color: "#2ecc71" },
  "track_5": { title: "JAMMU DI MAAT - DEVOTIONAL", ytId: "9b0iydtDZLU", color: "#9b59b6" },
  "track_6": { title: "KUNDA KHOLYA SHINGHA - ACOUSTIC", ytId: "vzlXfZlH5dk", color: "#e67e22" }
};"""

# Clean trailing comma from last track
jammu_lines = jammu_tracks.rstrip().split("\n")
if jammu_lines:
    last_line = jammu_lines[-1]
    if last_line.endswith(","):
        jammu_lines[-1] = last_line[:-1]
jammu_tracks_formatted = "\n".join(jammu_lines)

new_jammu_tracks = f"""const cassetteTracks = {{
{jammu_tracks_formatted}
}};"""

if old_jammu_tracks in jammu_js_content:
    jammu_js_content = jammu_js_content.replace(old_jammu_tracks, new_jammu_tracks)
    with open(jammu_js_path, "w", encoding="utf-8") as f:
        f.write(jammu_js_content)
    print("Successfully patched jammu.js playlist!")
else:
    # Try normalized lines
    old_jammu_normalized = old_jammu_tracks.replace("\r\n", "\n")
    jammu_normalized = jammu_js_content.replace("\r\n", "\n")
    if old_jammu_normalized in jammu_normalized:
        jammu_normalized = jammu_normalized.replace(old_jammu_normalized, new_jammu_tracks)
        with open(jammu_js_path, "w", encoding="utf-8") as f:
            f.write(jammu_normalized)
        print("Successfully patched jammu.js playlist (normalized line endings)!")
    else:
        print("WARNING: Old jammu tracks not found in jammu.js!")


# 2. Patch english.js
english_js_path = r"C:\Users\dvasu\window-seat\english.js"
english_tracks_path = r"C:\Users\dvasu\window-seat\english_tracks.txt"

with open(english_tracks_path, "r", encoding="utf-8") as f:
    english_tracks = f.read()

with open(english_js_path, "r", encoding="utf-8") as f:
    english_js_content = f.read()

old_english_tracks = """const cassetteTracks = {
  "track_1": { title: "SOUND OF SILENCE - SIMON & GARFUNKEL", ytId: "f7McpVPlhdc", color: "#34495e" },
  "track_2": { title: "HEART OF GOLD - NEIL YOUNG", ytId: "k0tO35VI7MY", color: "#e67e22" },
  "track_3": { title: "WILD WORLD - CAT STEVENS", ytId: "H51B6N1xLFE", color: "#3498db" },
  "track_4": { title: "BLOWIN' IN THE WIND - BOB DYLAN", ytId: "vWwgrjjIMOM", color: "#2ecc71" },
  "track_5": { title: "HOTEL CALIFORNIA (COZY LOFI)", ytId: "m7vF6b7z8xI", color: "#9b59b6" },
  "track_6": { title: "WISH YOU WERE HERE - PINK FLOYD", ytId: "IXdNemPvYQs", color: "#1abc9c" }
};"""

# Clean trailing comma from last track
english_lines = english_tracks.rstrip().split("\n")
if english_lines:
    last_line = english_lines[-1]
    if last_line.endswith(","):
        english_lines[-1] = last_line[:-1]
english_tracks_formatted = "\n".join(english_lines)

new_english_tracks = f"""const cassetteTracks = {{
{english_tracks_formatted}
}};"""

if old_english_tracks in english_js_content:
    english_js_content = english_js_content.replace(old_english_tracks, new_english_tracks)
    with open(english_js_path, "w", encoding="utf-8") as f:
        f.write(english_js_content)
    print("Successfully patched english.js playlist!")
else:
    # Try normalized lines
    old_english_normalized = old_english_tracks.replace("\r\n", "\n")
    english_normalized = english_js_content.replace("\r\n", "\n")
    if old_english_normalized in english_normalized:
        english_normalized = english_normalized.replace(old_english_normalized, new_english_tracks)
        with open(english_js_path, "w", encoding="utf-8") as f:
            f.write(english_normalized)
        print("Successfully patched english.js playlist (normalized line endings)!")
    else:
        print("WARNING: Old english tracks not found in english.js!")
