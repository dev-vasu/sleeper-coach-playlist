import os

js_files = ["app.js", "punjab.js", "jammu.js", "english.js"]

target_broken = """  const btnRouteDropdown = document.getElementById('btnRouteDropdown');
  const routeDropdownMenu = document.getElementById('routeDropdownMenu');
  if (btnRouteDropdown && routeDropdownMenu) {
    btnRouteDropdown.addEventListener('click', (e) => {
      e.stopPropagation();
      routeDropdownMenu.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  });
    });
  }
}"""

correct_block = """  const btnRouteDropdown = document.getElementById('btnRouteDropdown');
  const routeDropdownMenu = document.getElementById('routeDropdownMenu');
  if (btnRouteDropdown && routeDropdownMenu) {
    btnRouteDropdown.addEventListener('click', (e) => {
      e.stopPropagation();
      routeDropdownMenu.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }"""

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Fixing syntax in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if target_broken in content:
        content = content.replace(target_broken, correct_block)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully fixed syntax in {fn}!")
    else:
        # Try finding a more loose version in case indentation differs
        # Let's replace the block with single lines using find and replace
        # We can just look for the trailing extra lines
        bad_tail = """    });
  });
    });
  }
}"""
        good_tail = """    });
  }"""
        if bad_tail in content:
            content = content.replace(bad_tail, good_tail)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully fixed tail syntax in {fn}!")
        else:
            print(f"WARNING: target_broken and bad_tail not found in {fn}!")
            
print("Syntax correction completed!")
