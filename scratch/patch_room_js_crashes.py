import os

js_files = ["punjab.js", "jammu.js", "english.js"]

for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Wrapping unsafe lookups in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")

    # 1. Wrap chainPull inside setupEmergencyChain
    old_chain = """function setupEmergencyChain() {
  const chainPull = document.getElementById('chainPull');
  let startY = 0;"""
  
    new_chain = """function setupEmergencyChain() {
  const chainPull = document.getElementById('chainPull');
  if (!chainPull) return;
  let startY = 0;"""

    content = content.replace(old_chain, new_chain)

    # 2. Wrap btnLoadCustomTape inside DOMContentLoaded
    old_custom_tape = """  // Custom tape loader button
  document.getElementById('btnLoadCustomTape').addEventListener('click', (e) => {
    e.stopPropagation();
    const inputVal = document.getElementById('ytUrlInput').value.trim();
    const ytId = extractYoutubeId(inputVal) || inputVal;

    if (ytId) {
      playlistMenu.classList.remove('open');
      document.getElementById('customTapeForm').style.display = 'none';
      loadCassette('custom_stream', ytId);
    } else {
      alert("Invalid Youtube link or ID!");
    }
  });"""

    new_custom_tape = """  // Custom tape loader button
  const btnLoadCustomTape = document.getElementById('btnLoadCustomTape');
  if (btnLoadCustomTape) {
    btnLoadCustomTape.addEventListener('click', (e) => {
      e.stopPropagation();
      const inputVal = document.getElementById('ytUrlInput').value.trim();
      const ytId = extractYoutubeId(inputVal) || inputVal;

      if (ytId) {
        playlistMenu.classList.remove('open');
        const customTapeForm = document.getElementById('customTapeForm');
        if (customTapeForm) customTapeForm.style.display = 'none';
        loadCassette('custom_stream', ytId);
      } else {
        alert("Invalid Youtube link or ID!");
      }
    });
  }"""

    content = content.replace(old_custom_tape, new_custom_tape)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("JS safety wraps applied successfully!")
