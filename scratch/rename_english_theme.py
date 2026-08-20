import os

html_files = ["index.html", "punjab.html", "jammu.html", "english.html"]

old_term_1 = "🌲 ENGLISH CLASSICS"
new_term_1 = "🎵 80s ENGLISH R&B"

for fn in html_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    print(f"Renaming English Classics to 80s English R&B in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if old_term_1 in content:
        content = content.replace(old_term_1, new_term_1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated theme name in {fn}!")
    else:
        print(f"WARNING: '{old_term_1}' not found in {fn}!")

print("Theme renaming completed!")
