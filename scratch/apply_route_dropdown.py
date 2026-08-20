import os
import re

html_files = ["index.html", "punjab.html", "jammu.html", "english.html"]
js_files = ["app.js", "punjab.js", "jammu.js", "english.js"]

# 1. HTML dropdown blocks (normalized with \n)
html_dropdowns = {
    "index.html": """        <label class="control-label">JOURNEY ROUTE / यात्रा मार्ग</label>
        <div class="route-dropdown-container">
          <button class="route-dropdown-btn" id="btnRouteDropdown">
            🚂 CLASSIC TRAIN <span style="font-size: 10px; opacity: 0.6;">▼</span>
          </button>
          <div class="route-dropdown-menu" id="routeDropdownMenu">
            <a href="/" class="route-dropdown-item active">🚂 CLASSIC TRAIN</a>
            <a href="/punjab" class="route-dropdown-item">🌾 SAD PUNJABI</a>
            <a href="/jammu" class="route-dropdown-item">🏔️ JAMMU (DOGRI)</a>
            <a href="/english" class="route-dropdown-item">🌲 ENGLISH CLASSICS</a>
          </div>
        </div>""",
    "punjab.html": """        <label class="control-label">SWITCH THEME / थीम बदलें</label>
        <div class="route-dropdown-container">
          <button class="route-dropdown-btn" id="btnRouteDropdown">
            🌾 SAD PUNJABI <span style="font-size: 10px; opacity: 0.6;">▼</span>
          </button>
          <div class="route-dropdown-menu" id="routeDropdownMenu">
            <a href="/" class="route-dropdown-item">🚂 CLASSIC TRAIN</a>
            <a href="/punjab" class="route-dropdown-item active">🌾 SAD PUNJABI</a>
            <a href="/jammu" class="route-dropdown-item">🏔️ JAMMU (DOGRI)</a>
            <a href="/english" class="route-dropdown-item">🌲 ENGLISH CLASSICS</a>
          </div>
        </div>""",
    "jammu.html": """        <label class="control-label">SWITCH THEME / थीम बदलें</label>
        <div class="route-dropdown-container">
          <button class="route-dropdown-btn" id="btnRouteDropdown">
            🏔️ JAMMU (DOGRI) <span style="font-size: 10px; opacity: 0.6;">▼</span>
          </button>
          <div class="route-dropdown-menu" id="routeDropdownMenu">
            <a href="/" class="route-dropdown-item">🚂 CLASSIC TRAIN</a>
            <a href="/punjab" class="route-dropdown-item">🌾 SAD PUNJABI</a>
            <a href="/jammu" class="route-dropdown-item active">🏔️ JAMMU (DOGRI)</a>
            <a href="/english" class="route-dropdown-item">🌲 ENGLISH CLASSICS</a>
          </div>
        </div>""",
    "english.html": """        <label class="control-label">SWITCH THEME / थीम बदलें</label>
        <div class="route-dropdown-container">
          <button class="route-dropdown-btn" id="btnRouteDropdown">
            🌲 ENGLISH CLASSICS <span style="font-size: 10px; opacity: 0.6;">▼</span>
          </button>
          <div class="route-dropdown-menu" id="routeDropdownMenu">
            <a href="/" class="route-dropdown-item">🚂 CLASSIC TRAIN</a>
            <a href="/punjab" class="route-dropdown-item">🌾 SAD PUNJABI</a>
            <a href="/jammu" class="route-dropdown-item">🏔️ JAMMU (DOGRI)</a>
            <a href="/english" class="route-dropdown-item active">🌲 ENGLISH CLASSICS</a>
          </div>
        </div>"""
}

# 2. Match patterns for route selector in HTML (allowing optional blank lines/spaces)
html_patterns = {
    "index.html": r'<label class="control-label">JOURNEY ROUTE / यात्रा मार्ग</label>\s*<div class="route-selector" id="routeSelector">.*?</div>',
    "punjab.html": r'<label class="control-label">SWITCH THEME / थीम बदलें</label>\s*<div class="route-selector" id="routeSelector">.*?</div>',
    "jammu.html": r'<label class="control-label">SWITCH THEME / थीम बदलें</label>\s*<div class="route-selector" id="routeSelector">.*?</div>',
    "english.html": r'<label class="control-label">SWITCH THEME / थीम बदलें</label>\s*<div class="route-selector" id="routeSelector">.*?</div>'
}

print("=== Patches Processing ===")

# Process HTML
for fn in html_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    pattern = html_patterns[fn]
    new_block = html_dropdowns[fn]
    
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, new_block, content, flags=re.DOTALL)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully patched HTML dropdown in {fn}!")
    else:
        print(f"WARNING: HTML pattern not found in {fn}!")

# 3. Process JS Files
# In app.js (main script)
app_js_path = r"C:\Users\dvasu\window-seat\app.js"
if os.path.exists(app_js_path):
    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    old_js_block = """  const routeSelector = document.getElementById('routeSelector');
  if (routeSelector) {
    const routeBtns = routeSelector.querySelectorAll('.route-btn');
    routeBtns.forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-route') === initialRoute);
    });
  }"""
  
    new_js_block = """  // Route Dropdown toggle handler
  const btnRouteDropdown = document.getElementById('btnRouteDropdown');
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

    if old_js_block in content:
        content = content.replace(old_js_block, new_js_block)
        with open(app_js_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully patched JS route dropdown in app.js!")
    else:
        print("WARNING: Old JS block not found in app.js!")

# In room scripts (punjab.js, jammu.js, english.js)
room_js_pattern = r'// Journey Route Selector\s*const routeSelector = document\.getElementById\(\'routeSelector\'\);\s*if \(routeSelector\) \{.*?\}\s*\}'

for fn in ["punjab.js", "jammu.js", "english.js"]:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")
        
    new_room_js = """// Journey Route Selector
  const btnRouteDropdown = document.getElementById('btnRouteDropdown');
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

    if re.search(room_js_pattern, content, flags=re.DOTALL):
        content = re.sub(room_js_pattern, new_room_js, content, flags=re.DOTALL)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully patched JS route dropdown in room script: {fn}!")
    else:
        print(f"WARNING: room JS pattern not found in {fn}!")

print("=== Patches Finished ===")
