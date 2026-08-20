import os

base = r"C:\Users\dvasu\window-seat"

EXPLORER_JS = """
// ─── Theme Explorer Widget ────────────────────────────────────────────────────
(function() {
  const themeExplorer = document.getElementById('themeExplorer');
  const trigger = document.getElementById('themeExplorerTrigger');
  const closeBtn = document.getElementById('themeExplorerClose');
  if (!themeExplorer || !trigger) return;
  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    themeExplorer.classList.toggle('open');
  });
  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      themeExplorer.classList.remove('open');
    });
  }
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#themeExplorer')) {
      themeExplorer.classList.remove('open');
    }
  });
})();
"""

for fn in ["punjab.js", "jammu.js", "english.js"]:
    path = os.path.join(base, fn)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "Theme Explorer Widget" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(EXPLORER_JS)
        print(f"Added theme explorer JS to {fn}")
    else:
        print(f"Theme explorer JS already in {fn}")

print("Done!")
