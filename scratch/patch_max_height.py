import os

files_to_patch = ["index.html", "punjab.html", "jammu.html", "english.html"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching max-height in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Change max-height: 280px to max-height: 380px to fit all 6 songs on screen
    old_style = "max-height: 280px;"
    new_style = "max-height: 380px;"
    
    if old_style in content:
        content = content.replace(old_style, new_style)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully patched {fn}!")
    else:
        print(f"WARNING: max-height: 280px; not found in {fn}")
        
print("All HTML max-height patches completed successfully!")
