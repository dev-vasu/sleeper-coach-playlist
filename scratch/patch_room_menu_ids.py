import os

files_to_patch = ["punjab.html", "jammu.html", "english.html"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching playlist ID in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace <div class="playlist-items-scroll" id="playlistItemsScroll">
    # with the correct dynamicMenuItems wrapper
    old_tag = '<div class="playlist-items-scroll" id="playlistItemsScroll">'
    new_tag = '<div id="dynamicMenuItems" style="display: flex; flex-direction: column; max-height: 380px; overflow-y: auto; scrollbar-width: thin;">'
    
    if old_tag in content:
        content = content.replace(old_tag, new_tag)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully patched {fn}!")
    else:
        print(f"WARNING: old_tag not found in {fn}")
        
print("Playlist menu ID patches completed successfully!")
