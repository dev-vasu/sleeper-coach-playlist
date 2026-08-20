import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching {fn} for playlistTrigger fallback...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Change btnPlaylistSelect retrieve line to fallback to playlistTrigger
    old_line = "  const btnPlaylistSelect = document.getElementById('btnPlaylistSelect');"
    new_line = "  const btnPlaylistSelect = document.getElementById('btnPlaylistSelect') || document.getElementById('playlistTrigger');"

    content = content.replace(old_line, new_line)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("V5 patches completed successfully!")
