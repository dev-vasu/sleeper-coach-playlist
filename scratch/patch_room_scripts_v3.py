import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching {fn} for windowControls filter...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Filter out controls that don't exist
    old_controls = """  window.windowControls = [
    { knob: document.getElementById('volumeKnob'), indicator: document.getElementById('volumeIndicator'), type: 'volume' },
    { knob: document.getElementById('tuningKnob'), indicator: document.getElementById('tuningIndicator'), type: 'tuning' }
  ];"""

    new_controls = """  window.windowControls = [
    { knob: document.getElementById('volumeKnob'), indicator: document.getElementById('volumeIndicator'), type: 'volume' },
    { knob: document.getElementById('tuningKnob'), indicator: document.getElementById('tuningIndicator'), type: 'tuning' }
  ].filter(ctrl => ctrl.knob && ctrl.indicator);"""

    content = content.replace(old_controls, new_controls)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("V3 patches completed successfully!")
