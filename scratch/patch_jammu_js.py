with open(r"C:\Users\dvasu\window-seat\jammu.js", "r", encoding="utf-8") as f:
    content = f.read()

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
    with open(r"C:\Users\dvasu\window-seat\jammu.js", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched jammu.js with the diary listeners!")
else:
    print("WARNING: target block not found in jammu.js!")
