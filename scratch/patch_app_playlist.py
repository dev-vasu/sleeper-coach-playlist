import os

app_path = r"C:\Users\dvasu\window-seat\app.js"
tracks_path = r"C:\Users\dvasu\window-seat\jammu_tracks.txt"

with open(tracks_path, "r", encoding="utf-8") as f:
    new_tracks_content = f.read()

with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

# Define the old jammu block exactly
old_jammu_block = """  jammu: {
    "track_1": { title: "JAMMU DIYE RAAHEIN - ACOUSTIC", ytId: "N42UlyZ2BwU", color: "#1abc9c" },
    "track_2": { title: "KUNDA KHOLYA - DOGRI FOLK", ytId: "Gk05tY4U2M4", color: "#e74c3c" },
    "track_3": { title: "CHANN MADA CHADEYA", ytId: "plB0ytzIlqI", color: "#f1c40f" },
    "track_4": { title: "DOGRI ACOUSTIC MIX", ytId: "dDR4oiyjUBA", color: "#2ecc71" },
    "track_5": { title: "JAMMU DI MAAT - DEVOTIONAL", ytId: "9b0iydtDZLU", color: "#9b59b6" },
    "track_6": { title: "KUNDA KHOLYA SHINGHA - ACOUSTIC", ytId: "vzlXfZlH5dk", color: "#e67e22" }
  },"""

# Remove the trailing comma from the last track in the new tracks content
# new_tracks_content has lines like: ... "track_25": { ... },\n
# We want to replace the last comma with a blank space or remove it so it's clean JSON/JS syntax
new_lines = new_tracks_content.rstrip().split("\n")
if new_lines:
    last_line = new_lines[-1]
    if last_line.endswith(","):
        new_lines[-1] = last_line[:-1]
new_tracks_formatted = "\n".join(new_lines)

new_jammu_block = f"""  jammu: {{
{new_tracks_formatted}
  }},"""

if old_jammu_block in app_content:
    app_content = app_content.replace(old_jammu_block, new_jammu_block)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)
    print("Successfully patched jammu playlist in app.js!")
else:
    # Try alternate line ending matching
    old_jammu_normalized = old_jammu_block.replace("\r\n", "\n")
    app_normalized = app_content.replace("\r\n", "\n")
    if old_jammu_normalized in app_normalized:
        app_normalized = app_normalized.replace(old_jammu_normalized, new_jammu_block)
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_normalized)
        print("Successfully patched jammu playlist in app.js (normalized line endings)!")
    else:
        print("WARNING: Old jammu block not found in app.js!")
