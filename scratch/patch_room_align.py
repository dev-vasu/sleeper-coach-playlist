import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

new_align_function = """function alignCompartmentElements() {
  const visualsEl = document.getElementById('compartmentVisuals') || document.body;
  const dispWidth = visualsEl.clientWidth;
  const dispHeight = visualsEl.clientHeight;
  const canvas = document.getElementById('cabinCanvas');
  if (!canvas) return;
  
  canvas.width = 1920; 
  canvas.height = 1080;
  
  const ctx = canvas.getContext('2d');
  
  if (!window.cabinImg || !window.cabinImg.complete) return;
  
  const img = window.cabinImg;
  
  ctx.clearRect(0, 0, 1920, 1080);
  ctx.drawImage(img, 0, 0, 1920, 1080);

  // Fit cover scaling calculations
  const scale = Math.max(dispWidth / 1920, dispHeight / 1080);
  document.documentElement.style.setProperty('--cabin-scale', scale);
  
  const renderedWidth = 1920 * scale;
  const renderedHeight = 1080 * scale;
  const offsetX = (dispWidth - renderedWidth) / 2;
  let offsetY = (dispHeight - renderedHeight) / 2;
  if (offsetY < 0) {
    offsetY = offsetY * 0.15;
  }

  canvas.style.position = 'absolute';
  canvas.style.left = `${offsetX}px`;
  canvas.style.top = `${offsetY}px`;
  canvas.style.width = `${renderedWidth}px`;
  canvas.style.height = `${renderedHeight}px`;
  canvas.style.objectFit = 'fill';

  const mapElement = (elId, xPct, yPct, wPct, hPct, isSquare = false, clampToScreen = false) => {
    const el = document.getElementById(elId);
    if (!el) return;
    
    let w = wPct * renderedWidth;
    let h = hPct * renderedHeight;
    if (isSquare) h = w;
    
    let x = offsetX + (xPct * renderedWidth);
    let y = offsetY + (yPct * renderedHeight);
    
    if (clampToScreen) {
      x = Math.max(12, Math.min(dispWidth - w - 12, x));
      y = Math.max(12, Math.min(dispHeight - h - 12, y));
    }
    
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    el.style.width = `${w}px`;
    el.style.height = `${h}px`;
    el.style.position = 'absolute';
  };

  // Align UI elements
  mapElement('skyClock', 0.04, 0.035, 0.09, 0.04, false, true);
  mapElement('skyOnlineCounter', 0.86, 0.035, 0.10, 0.04, false, true);
  mapElement('chaiGlass', 0.682, 0.61, 0.07, 0.20); 
  mapElement('diaryHotspot', 0.38, 0.78, 0.30, 0.20); // Diary hotspot over the notebook

  const timeCard = document.getElementById('timeOfDayCard');
  if (timeCard) {
    const w = 0.11 * renderedWidth;
    const h = timeCard.offsetHeight || 300;
    let x = offsetX + (0.86 * renderedWidth);
    let y = offsetY + (0.32 * renderedHeight);
    
    x = Math.max(12, Math.min(dispWidth - w - 12, x));
    y = Math.max(12, Math.min(dispHeight - h - 12, y));
    
    timeCard.style.left = `${x}px`;
    timeCard.style.top = `${y}px`;
    timeCard.style.width = `${w}px`;
    timeCard.style.height = 'auto';
    timeCard.style.position = 'absolute';
  }
}"""

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Replacing alignCompartmentElements in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the start of function alignCompartmentElements() and end (before processCabinChromaKey)
    start_str = "function alignCompartmentElements() {"
    end_str = "function processCabinChromaKey() {"
    
    if start_str in content and end_str in content:
        parts = content.split(start_str)
        left = parts[0]
        right_parts = parts[1].split(end_str)
        right = end_str + right_parts[1]
        
        new_content = left + new_align_function + "\n\n" + right
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Successfully patched alignment in {fn}!")
    else:
        print(f"Failed to find match markers in {fn}")
        
print("All alignments patched successfully!")
