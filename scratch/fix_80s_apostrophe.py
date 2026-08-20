import os, re

base = r"C:\Users\dvasu\window-seat"
files = ["index.html", "punjab.html", "jammu.html", "english.html",
         "app.js", "style.css"]

# Fix: 80s -> 80's and 80S -> 80's in display text
# Only in contexts that are human-readable labels, not numbers
pattern = re.compile(r'\b80[sS]\b')

for fn in files:
    path = os.path.join(base, fn)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = pattern.sub("80's", content)
    
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        count = len(pattern.findall(content))
        print(f"Fixed {count} occurrence(s) of '80s/80S' in {fn}")
    else:
        print(f"No changes needed in {fn}")

print("80s -> 80's fix complete!")
