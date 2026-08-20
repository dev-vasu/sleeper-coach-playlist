import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        print(f"Skipping {fn} (not found)")
        continue
        
    print(f"Patching {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Patch windowShutters to filter out non-existent elements
    old_shutters = """  window.windowShutters = [
    { el: document.getElementById('shutterGlass'), handle: document.querySelector('.glass-handle'), currY: -76 },
    { el: document.getElementById('shutterMetal'), handle: document.querySelector('.metal-handle'), currY: -76 }
  ];"""
  
    new_shutters = """  window.windowShutters = [
    { el: document.getElementById('shutterGlass'), handle: document.querySelector('.glass-handle'), currY: -76 },
    { el: document.getElementById('shutterMetal'), handle: document.querySelector('.metal-handle'), currY: -76 }
  ].filter(shutter => shutter.el && shutter.handle);"""

    content = content.replace(old_shutters, new_shutters)

    # 2. Patch setupInteractiveToggles to check button existence and use btnLight fallback
    old_toggles_start = """function setupInteractiveToggles() {
  const btnLight = document.getElementById('btnCabinLight');
  const btnFan = document.getElementById('btnFan');
  const btnWind = document.getElementById('btnWind');
  const btnRain = document.getElementById('btnRain');
  const btnShutter = document.getElementById('btnShutter');

  if (!btnLight || !btnFan || !btnWind || !btnRain || !btnShutter) {
    console.warn("Cabin toggle buttons not found in DOM.");
    return;
  }"""

    new_toggles_start = """function setupInteractiveToggles() {
  const btnLight = document.getElementById('btnLight') || document.getElementById('btnCabinLight');
  const btnFan = document.getElementById('btnFan');
  const btnWind = document.getElementById('btnWind');
  const btnRain = document.getElementById('btnRain');
  const btnShutter = document.getElementById('btnShutter');"""

    content = content.replace(old_toggles_start, new_toggles_start)

    # Wrap each event listener inside setupInteractiveToggles with existence checks
    content = content.replace("  btnLight.addEventListener('click', () => {", "  if (btnLight) btnLight.addEventListener('click', () => {")
    content = content.replace("  btnFan.addEventListener('click', () => {", "  if (btnFan) btnFan.addEventListener('click', () => {")
    content = content.replace("  btnWind.addEventListener('click', () => {", "  if (btnWind) btnWind.addEventListener('click', () => {")
    content = content.replace("  btnRain.addEventListener('click', () => {", "  if (btnRain) btnRain.addEventListener('click', () => {")
    content = content.replace("  btnShutter.addEventListener('click', () => {", "  if (btnShutter) btnShutter.addEventListener('click', () => {")

    # 3. Patch the soundboard buttons (mute, horn, chai, announce) and ticket zoom
    content = content.replace("  btnHorn.addEventListener('mousedown', startHorn);", "  if (btnHorn) btnHorn.addEventListener('mousedown', startHorn);")
    content = content.replace("  btnHorn.addEventListener('touchstart', startHorn);", "  if (btnHorn) btnHorn.addEventListener('touchstart', startHorn);")
    
    content = content.replace("  document.getElementById('btnAnnounce').addEventListener('click', playIndianRailwayAnnouncements);", 
                              "  const btnAnn = document.getElementById('btnAnnounce'); if (btnAnn) btnAnn.addEventListener('click', playIndianRailwayAnnouncements);")

    content = content.replace("  ticket.addEventListener('click', (e) => {", "  if (ticket) ticket.addEventListener('click', (e) => {")
    
    content = content.replace("  bplTapeDeck.addEventListener('click', (e) => {", "  if (bplTapeDeck) bplTapeDeck.addEventListener('click', (e) => {")

    # 4. Handle other potential null elements
    content = content.replace("  const ticket = document.getElementById('clampedTicket');",
                              "  const ticket = document.getElementById('clampedTicket');")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("All patches completed successfully!")
