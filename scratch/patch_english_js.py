import os

path = r"C:\Users\dvasu\window-seat\english.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

# 1. Update mapElement
old_map = "mapElement('diaryHotspot', 0.38, 0.78, 0.30, 0.20); // Diary hotspot over the notebook"
new_map = "mapElement('diaryHotspot', 0.33, 0.84, 0.20, 0.16); // Diary hotspot over the notebook in the new R&B illustration"

if old_map in content:
    content = content.replace(old_map, new_map)
    print("Successfully patched mapElement in english.js!")
else:
    print("WARNING: old_map not found in english.js!")

# 2. Inject click handlers
target = """  // Tea cup clinking & gulping sounds
  document.getElementById('chaiGlass').addEventListener('click', () => {"""

diary_code = """  // Diary/Notebook interaction
  const diaryHotspot = document.getElementById('diaryHotspot');
  const diaryZoomCard = document.getElementById('diaryZoomCard');
  const closeDiary = document.getElementById('closeDiary');

  if (diaryHotspot && diaryZoomCard) {
    diaryHotspot.addEventListener('click', (e) => {
      e.stopPropagation();
      diaryZoomCard.classList.add('open');
      if (!audio.initialized) audio.init();
      audio.resume();
      audio.playSwitchClick();
    });
  }

  if (closeDiary && diaryZoomCard) {
    closeDiary.addEventListener('click', (e) => {
      e.stopPropagation();
      diaryZoomCard.classList.remove('open');
      audio.playSwitchClick();
    });
  }

  document.addEventListener('click', (e) => {
    if (diaryZoomCard && diaryZoomCard.classList.contains('open')) {
      if (!e.target.closest('#diaryZoomCard') && e.target !== diaryHotspot) {
        diaryZoomCard.classList.remove('open');
      }
    }
  });

  // Tea cup clinking & gulping sounds
  document.getElementById('chaiGlass').addEventListener('click', () => {"""

if target in content:
    content = content.replace(target, diary_code)
    print("Successfully injected diary listeners in english.js!")
else:
    print("WARNING: target not found in english.js!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
