import os

js_files = ["punjab.js", "jammu.js", "english.js"]

target_broken = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }

function updateAmbientDarkness() {"""

correct_block = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }
}

function updateAmbientDarkness() {"""

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    print(f"Adding closing brace to setupInteractiveToggles in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    if target_broken in content:
        content = content.replace(target_broken, correct_block)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully added closing brace to {fn}!")
    else:
        print(f"WARNING: target_broken block not found in {fn}!")
        
print("Room JS patches completed!")
