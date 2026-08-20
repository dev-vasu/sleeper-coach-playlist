import os

files_to_patch = ["punjab.js", "jammu.js", "english.js"]

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching {fn} with polyfills and wrapper checks...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Wrap spotifyVolumeSlider listener
    old_vol_listener = """  document.getElementById('spotifyVolumeSlider').addEventListener('input', (e) => {
    const val = parseInt(e.target.value);
    state.volume = val;
    if (ytPlayer && ytApiReady && typeof ytPlayer.setVolume === 'function') {
      ytPlayer.setVolume(val);
    }
    const volIcon = document.getElementById('volIcon');
    if (volIcon) {
      if (val === 0) volIcon.textContent = "🔇";
      else if (val < 30) volIcon.textContent = "🔈";
      else if (val < 70) volIcon.textContent = "🔉";
      else volIcon.textContent = "🔊";
    }
  });"""

    new_vol_listener = """  const volSlider = document.getElementById('spotifyVolumeSlider');
  if (volSlider) {
    volSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value);
      state.volume = val;
      if (ytPlayer && ytApiReady && typeof ytPlayer.setVolume === 'function') {
        ytPlayer.setVolume(val);
      }
      const volIcon = document.getElementById('volIcon');
      if (volIcon) {
        if (val === 0) volIcon.textContent = "🔇";
        else if (val < 30) volIcon.textContent = "🔈";
        else if (val < 70) volIcon.textContent = "🔉";
        else volIcon.textContent = "🔊";
      }
    });
  }"""

    content = content.replace(old_vol_listener, new_vol_listener)

    # 2. Wrap btnLoadCustomTape listener
    old_load_listener = """  document.getElementById('btnLoadCustomTape').addEventListener('click', (e) => {
    e.preventDefault();
    const inputVal = document.getElementById('ytUrlInput').value.trim();
    const ytId = extractYoutubeId(inputVal);
    if (ytId) {
      state.customYtId = ytId;
      loadCassette('custom_stream', ytId);
      document.getElementById('customTapeForm').style.display = 'none';
    } else {
      alert("Invalid YouTube URL/ID. Please try again.");
    }
  });"""

    new_load_listener = """  const btnLoad = document.getElementById('btnLoadCustomTape');
  if (btnLoad) {
    btnLoad.addEventListener('click', (e) => {
      e.preventDefault();
      const inputVal = document.getElementById('ytUrlInput').value.trim();
      const ytId = extractYoutubeId(inputVal);
      if (ytId) {
        state.customYtId = ytId;
        loadCassette('custom_stream', ytId);
        const tapeForm = document.getElementById('customTapeForm');
        if (tapeForm) tapeForm.style.display = 'none';
      } else {
        alert("Invalid YouTube URL/ID. Please try again.");
      }
    });
  }"""

    content = content.replace(old_load_listener, new_load_listener)

    # 3. Inject ID mapper polyfills at DOMContentLoaded start
    target_dom_start = """// Init Setup
document.addEventListener("DOMContentLoaded", () => {
  // Set initial route styling on load
  const initialRoute = state.activeRoute;
  document.body.classList.remove('route-hindi', 'route-punjab', 'route-jammu', 'route-english');
  document.body.classList.add(`route-${initialRoute}`);"""

    replacement_dom_start = """// Init Setup
document.addEventListener("DOMContentLoaded", () => {
  // Polyfill ID mismatches between Train page and Room pages
  const mapId = (targetId, fallbackId) => {
    const el = document.getElementById(fallbackId);
    if (el && !document.getElementById(targetId)) {
      el.id = targetId;
    }
  };
  mapId('progressBarBg', 'progressBg');
  mapId('progressBarFill', 'progressFill');
  mapId('timeElapsed', 'timeCurrent');
  mapId('btnPlaylistSelect', 'playlistTrigger');

  // Set initial route styling on load
  const initialRoute = state.activeRoute;
  document.body.classList.remove('route-hindi', 'route-punjab', 'route-jammu', 'route-english');
  document.body.classList.add(`route-${initialRoute}`);"""

    content = content.replace(target_dom_start, replacement_dom_start)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("V6 patches completed successfully!")
