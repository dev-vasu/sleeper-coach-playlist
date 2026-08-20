import os

js_files = ["app.js", "punjab.js", "jammu.js", "english.js"]

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Appending closing brace to {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Append }); to the end of the file
    content = content.rstrip() + "\n});\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Braces appended successfully!")
