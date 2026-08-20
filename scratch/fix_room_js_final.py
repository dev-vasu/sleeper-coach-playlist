import os

js_files = ["punjab.js", "jammu.js", "english.js"]

target_bad = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  });
    });
  }
}"""

correct_good = """    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }
});"""

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    print(f"Fixing closing braces in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    if target_bad in content:
        content = content.replace(target_bad, correct_good)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully fixed braces in {fn}!")
    else:
        print(f"WARNING: target_bad block not found in {fn}!")

print("All room js files fixed!")
