import os
import re

html_files = ["punjab.html", "jammu.html", "english.html"]
js_files = ["punjab.js", "jammu.js", "english.js"]

# 1. Update HTML Files
for fn in html_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Removing train leftovers from HTML: {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Rename JOURNEY ROUTE to SWITCH THEME
    content = content.replace(
        '<label class="control-label">JOURNEY ROUTE / यात्रा मार्ग</label>',
        '<label class="control-label">SWITCH THEME / थीम बदलें</label>'
    )
    
    # Rename CLASSIC HINDI link
    content = content.replace(
        '<a href="/" class="route-btn">🇮🇳 CLASSIC HINDI</a>',
        '<a href="/" class="route-btn">🚂 CLASSIC TRAIN</a>'
    )

    # Use regex to strip out the Sound Board section
    # This matches: <hr class="card-section-divider"> ... SOUND BOARD / ध्वनि पट्टिका ... </button> \n </div>
    pattern = r'<hr class="card-section-divider">\s*<label class="control-label">SOUND BOARD / ध्वनि पट्टिका</label>\s*<div class="sound-board-triggers">.*?</div>'
    content = re.sub(pattern, "", content, flags=re.DOTALL)
    print(f"Stripped soundboard from {fn} using regex!")

    # Update Player Artist Name to match theme
    if "punjab" in fn:
        content = content.replace(
            '<span class="song-artist" id="playerSongArtist">Sleeper Class FM</span>',
            '<span class="song-artist" id="playerSongArtist">Sada-e-Hijr FM</span>'
        )
    elif "jammu" in fn:
        content = content.replace(
            '<span class="song-artist" id="playerSongArtist">Sleeper Class FM</span>',
            '<span class="song-artist" id="playerSongArtist">Dogri Folk FM</span>'
        )
    elif "english" in fn:
        content = content.replace(
            '<span class="song-artist" id="playerSongArtist">Sleeper Class FM</span>',
            '<span class="song-artist" id="playerSongArtist">English Classics FM</span>'
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 2. Update JS Files (Safety wrap event listeners)
for fn in js_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Adding safety wraps to JS: {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Wrap btnMuteAmbience listener
    # Search for document.getElementById('btnMuteAmbience').addEventListener
    old_mute = "document.getElementById('btnMuteAmbience').addEventListener"
    new_mute = "const btnMute = document.getElementById('btnMuteAmbience');\n  if (btnMute) btnMute.addEventListener"
    content = content.replace(old_mute, new_mute)

    # Wrap btnChai listener
    old_chai = "document.getElementById('btnChai').addEventListener('click', callChaiWallahVoice);"
    new_chai = "const btnChai = document.getElementById('btnChai');\n  if (btnChai) btnChai.addEventListener('click', callChaiWallahVoice);"
    content = content.replace(old_chai, new_chai)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("All train leftovers removed and scripts wrapped safely!")
