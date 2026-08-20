import os

js_files = ["punjab.js", "jammu.js", "english.js"]

target_broken = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }
});"""

correct_block = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }"""

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Fixing closing brace at line 1775 in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    if target_broken in content:
        content = content.replace(target_broken, correct_block)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully removed extra brace from {fn}!")
    else:
        print(f"WARNING: target block not found in {fn}!")
        
print("Braces fix complete!")
