import os, re

base = r"C:\Users\dvasu\window-seat"

# ─── Load existing Jammu tracks (25) + extra Dogri tracks (28) ───────────────
existing_path = os.path.join(base, "jammu_tracks.txt")
extra_path    = os.path.join(base, "dogri_extra_tracks.txt")

with open(existing_path, "r", encoding="utf-8") as f:
    existing = f.read().strip()
with open(extra_path, "r", encoding="utf-8") as f:
    extra = f.read().strip()

# Re-number extra tracks starting from 26
colors = ["#e74c3c","#3498db","#f1c40f","#2ecc71","#9b59b6","#1abc9c","#e67e22","#34495e"]
renumbered = []
for line in extra.split("\n"):
    m = re.match(r'\s*"track_(\d+)":(.*)', line)
    if m:
        old_num = int(m.group(1))
        rest = m.group(2)
        new_num = old_num + 25
        renumbered.append(f'    "track_{new_num}":{rest}')

extra_renumbered = "\n".join(renumbered)

# Remove trailing comma from last line of each block
def strip_last_comma(block):
    lines = block.rstrip().split("\n")
    if lines and lines[-1].rstrip().endswith(","):
        lines[-1] = lines[-1].rstrip()[:-1]
    return "\n".join(lines)

all_tracks_for_js = existing.rstrip() + "\n" + extra_renumbered
all_tracks_for_js = strip_last_comma(all_tracks_for_js)

new_cassette_block = f'const cassetteTracks = {{\n{all_tracks_for_js}\n}};'

# ─── Patch jammu.js ────────────────────────────────────────────────────────────
jammu_js_path = os.path.join(base, "jammu.js")
with open(jammu_js_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

start = content.find("const cassetteTracks = {")
end   = content.find("\n};", start)
if start != -1 and end != -1:
    old_block = content[start:end + 3]
    content = content.replace(old_block, new_cassette_block)
    with open(jammu_js_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Patched jammu.js — now has {all_tracks_for_js.count('track_')} tracks")
else:
    print(f"FAILED: start={start}, end={end}")

# ─── Patch app.js (the jammu: block in routePlaylists) ───────────────────────
app_js_path = os.path.join(base, "app.js")
with open(app_js_path, "r", encoding="utf-8") as f:
    app = f.read().replace("\r\n", "\n")

# Find the jammu: { ... } block inside routePlaylists
jam_start = app.find("  jammu: {")
jam_end   = app.find("\n  },", jam_start)
if jam_start != -1 and jam_end != -1:
    # Format tracks with 4-space indent for app.js
    app_tracks = "\n".join(["  " + l for l in all_tracks_for_js.split("\n")])
    new_jammu_block = f"  jammu: {{\n{app_tracks}\n  }}"
    old_jammu_block = app[jam_start:jam_end + 4]
    app = app.replace(old_jammu_block, new_jammu_block)
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(app)
    print("Patched app.js jammu block")
else:
    print(f"app.js jammu block not found: start={jam_start}, end={jam_end}")

print("All done!")
