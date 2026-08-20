import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching {fn} for playlist trigger...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Wrap btnPlaylistSelect addEventListener in an existence check
    content = content.replace("  btnPlaylistSelect.addEventListener('click', (e) => {", 
                              "  if (btnPlaylistSelect) btnPlaylistSelect.addEventListener('click', (e) => {")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("V2 patches completed successfully!")
