import os
import re

html_files = ["index.html", "punjab.html", "jammu.html", "english.html"]
js_files = ["app.js", "punjab.js", "jammu.js", "english.js"]

# 1. Append CSS to style.css
style_path = r"C:\Users\dvasu\window-seat\style.css"
print("Appending dropdown CSS styles to style.css...")
with open(style_path, "r", encoding="utf-8") as f:
    style_content = f.read()

dropdown_css = """
/* Glassmorphic Theme/Route Dropdown */
.route-dropdown-container {
  position: relative;
  width: 100%;
  margin-top: 10px;
}
.route-dropdown-btn {
  width: 100%;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-sizing: border-box;
}
.route-dropdown-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}
.route-dropdown-menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  background: rgba(25, 25, 25, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  display: none;
  flex-direction: column;
  z-index: 100;
  overflow: hidden;
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-sizing: border-box;
}
.route-dropdown-menu.open {
  display: flex;
}
.route-dropdown-item {
  padding: 10px 16px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
}
.route-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.route-dropdown-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  font-weight: 600;
}
"""

if ".route-dropdown-container" not in style_content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(dropdown_css)
    print("CSS successfully appended!")
else:
    print("Dropdown CSS already present.")

# 2. Modify HTML Files
html_dropdowns = {
    "index.html": """        <div class="route-dropdown-container">
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
    "punjab.html": """        <div class="route-dropdown-container">
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
    "jammu.html": """        <div class="route-dropdown-container">
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
    "english.html": """        <div class="route-dropdown-container">
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

for fn, drop_markup in html_dropdowns.items():
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching HTML route dropdown in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Search for route-selector block and replace it
    pattern = r'<div class="route-selector" id="routeSelector">.*?</div>'
    content = re.sub(pattern, drop_markup, content, flags=re.DOTALL)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully patched HTML dropdown in {fn}!")

# 3. Modify JS Files (Replace routeSelector logic with dropdown event listeners)
dropdown_js = """  // Route Dropdown toggle handler
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

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching JS route dropdown in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate and replace the old routeSelector toggle code block
    old_js_pattern = r'const routeSelector = document\.getElementById\(\'routeSelector\'\);\s*if \(routeSelector\) \{.*?\}\s*\}'
    if re.search(old_js_pattern, content, flags=re.DOTALL):
        content = re.sub(old_js_pattern, dropdown_js, content, flags=re.DOTALL)
        print(f"Replaced old routeSelector code in {fn} using pattern 1")
    else:
        # Try alternate pattern
        old_js_pattern2 = r'const routeSelector = document\.getElementById\(\'routeSelector\'\);\s*if \(routeSelector\) \{.*?\}'
        if re.search(old_js_pattern2, content, flags=re.DOTALL):
            content = re.sub(old_js_pattern2, dropdown_js, content, flags=re.DOTALL)
            print(f"Replaced old routeSelector code in {fn} using pattern 2")
        else:
            print(f"WARNING: Could not find routeSelector JS block in {fn}!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Dropdown patches completed successfully!")
