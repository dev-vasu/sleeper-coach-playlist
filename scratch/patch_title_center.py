import os

html_files = ["punjab.html", "jammu.html", "english.html"]

target_old = 'style="z-index: 30; pointer-events: none; left: 18%; top: 15%;"'
target_new = 'style="z-index: 30; pointer-events: none; left: 50%; top: 15%; transform: translate(-50%, 0); text-align: center;"'

for fn in html_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    print(f"Centering title text in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if target_old in content:
        content = content.replace(target_old, target_new)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully centered title in {fn}!")
    else:
        print(f"WARNING: target style not found in {fn}!")

print("Title text centering completed!")
