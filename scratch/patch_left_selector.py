import os

js_files = ["punjab.js", "jammu.js"]

target_old = "let x = offsetX + (0.86 * renderedWidth);"
target_new = "let x = offsetX + (0.04 * renderedWidth);"

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    print(f"Moving theme selector to left side in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if target_old in content:
        content = content.replace(target_old, target_new)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully moved theme selector to left side in {fn}!")
    else:
        print(f"WARNING: target line not found in {fn}!")

print("Theme selector repositioning completed!")
