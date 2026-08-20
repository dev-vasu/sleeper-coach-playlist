import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching {fn} for DOMContentLoaded block...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate and clean DOMContentLoaded block
    target_block = """// Init Setup
document.addEventListener("DOMContentLoaded", () => {
  // Set initial route styling on load
  const initialRoute = state.activeRoute;
  document.body.classList.remove('route-hindi', 'route-punjab', 'route-jammu', 'route-english');
  document.body.classList.add(`route-${initialRoute}`);

  // Swap to the selected playlist tracks for startup
  if (initialRoute !== 'hindi') {
    const newTracks = routePlaylists[initialRoute];
    if (newTracks) {
      Object.keys(cassetteTracks).forEach(k => delete cassetteTracks[k]);
      Object.keys(newTracks).forEach(k => {
        cassetteTracks[k] = newTracks[k];
      });
      state.activeCassette = 'track_1';
    }
  }

  const routeSelector = document.getElementById('routeSelector');
  if (routeSelector) {
    const routeBtns = routeSelector.querySelectorAll('.route-btn');
    routeBtns.forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-route') === initialRoute);
    });
  }

  processCabinChromaKey();"""

    replacement_block = """// Init Setup
document.addEventListener("DOMContentLoaded", () => {
  // Set initial route styling on load
  const initialRoute = state.activeRoute;
  document.body.classList.remove('route-hindi', 'route-punjab', 'route-jammu', 'route-english');
  document.body.classList.add(`route-${initialRoute}`);

  processCabinChromaKey();"""

    if target_block in content:
        content = content.replace(target_block, replacement_block)
        print(f"Successfully replaced in {fn}")
    else:
        # Fallback if whitespace differs
        print(f"WARNING: Direct block match failed in {fn}, trying line replacements.")
        # We can do individual line deletions
        lines = content.split("\n")
        new_lines = []
        skip = False
        skip_count = 0
        for line in lines:
            if "// Swap to the selected playlist tracks for startup" in line:
                skip = True
                skip_count = 11 # skip the 11 lines of the swap block
            if "const routeSelector = document.getElementById('routeSelector');" in line:
                skip = True
                skip_count = 7 # skip the 7 lines of route selector
            
            if skip:
                skip_count -= 1
                if skip_count <= 0:
                    skip = False
                continue
            new_lines.append(line)
        content = "\n".join(new_lines)
        print(f"Applied fallback line replacement in {fn}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("V4 patches completed successfully!")
