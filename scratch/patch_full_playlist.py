with open(r"C:\Users\dvasu\.gemini\antigravity-cli\brain\c0dc278a-945b-452c-a2e3-ccf5fd593546\scratch\js_tracks_v2.txt", "r", encoding="utf-8") as f:
    js_lines = f.readlines()

# Extract tracks lines from line 2 to 64 (index 1 to 63)
tracks_lines = [line.strip() for line in js_lines[1:64]]
custom_stream_line = js_lines[64].strip()

# Construct the hindi route playlist string
hindi_tracks_content = ",\n    ".join(tracks_lines)

# Construct the default cassette tracks string
cassette_tracks_content = ",\n  ".join(tracks_lines) + ",\n  " + custom_stream_line

# Load app.js
with open(r"C:\Users\dvasu\window-seat\app.js", "r", encoding="utf-8") as f:
    app_content = f.read()

# Replace hindi route playlist block
# Let's locate:
#   hindi: {
#     "track_1": { title: "PEHLA NASHA", ytId: "iSUK1QoK9-E", color: "#e74c3c" },
#     ...
#     "track_6": { title: "KUCH KUCH HOTA HAI", ytId: "bKZTnnFU9HA", color: "#1abc9c" }
#   },
old_hindi_block = """  hindi: {
    "track_1": { title: "PEHLA NASHA", ytId: "iSUK1QoK9-E", color: "#e74c3c" },
    "track_2": { title: "PEHLA PEHLA PYAR HAI (HD)", ytId: "w2iozAbNXAo", color: "#3498db" },
    "track_3": { title: "AAYE HO MERI ZINDAGI", ytId: "Vzt2wFAg4og", color: "#f1c40f" },
    "track_4": { title: "DIL NE YE KAHA HAI DIL SE", ytId: "MvcNeQlqtes", color: "#2ecc71" },
    "track_5": { title: "MERA DIL BHI KITNA PAGAL", ytId: "x_elT6zkqN0", color: "#9b59b6" },
    "track_6": { title: "KUCH KUCH HOTA HAI", ytId: "bKZTnnFU9HA", color: "#1abc9c" }
  },"""

new_hindi_block = "  hindi: {\n    " + hindi_tracks_content + "\n  },"

# Replace cassetteTracks block
# Let's locate:
# const cassetteTracks = {
#   "track_1": { title: "PEHLA NASHA", ytId: "iSUK1QoK9-E", color: "#e74c3c" },
#   ...
#   "track_6": { title: "KUCH KUCH HOTA HAI", ytId: "bKZTnnFU9HA", color: "#1abc9c" }
# };
old_cassette_block = """const cassetteTracks = {
  "track_1": { title: "PEHLA NASHA", ytId: "iSUK1QoK9-E", color: "#e74c3c" },
  "track_2": { title: "PEHLA PEHLA PYAR HAI (HD)", ytId: "w2iozAbNXAo", color: "#3498db" },
  "track_3": { title: "AAYE HO MERI ZINDAGI MEIN TUM BAHAR BANKE FEMALE", ytId: "Vzt2wFAg4og", color: "#f1c40f" },
  "track_4": { title: "DIL NE YE KAHA HAI DIL SE", ytId: "MvcNeQlqtes", color: "#2ecc71" },
  "track_5": { title: "MERA DIL BHI KITNA PAGAL HAI", ytId: "x_elT6zkqN0", color: "#9b59b6" },
  "track_6": { title: "KUCH KUCH HOTA HAI", ytId: "bKZTnnFU9HA", color: "#1abc9c" }
};"""

new_cassette_block = "const cassetteTracks = {\n  " + cassette_tracks_content + "\n};"

if old_hindi_block in app_content:
    app_content = app_content.replace(old_hindi_block, new_hindi_block)
    print("Replaced routePlaylists.hindi successfully!")
else:
    print("WARNING: old_hindi_block not found in app.js!")

# We also check with different trailing semi-colons or characters for cassetteTracks
if old_cassette_block in app_content:
    app_content = app_content.replace(old_cassette_block, new_cassette_block)
    print("Replaced cassetteTracks successfully!")
else:
    # Try alternate formatting
    alt_cassette = old_cassette_block + ";"
    if alt_cassette in app_content:
        app_content = app_content.replace(alt_cassette, new_cassette_block)
        print("Replaced cassetteTracks (alt) successfully!")
    else:
        print("WARNING: old_cassette_block not found in app.js!")

with open(r"C:\Users\dvasu\window-seat\app.js", "w", encoding="utf-8") as f:
    f.write(app_content)
    
print("app.js patching complete!")
