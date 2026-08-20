import os

files_to_patch = ["punjab.html", "jammu.html", "english.html"]

player_html_block = """    <!-- SPOTIFY-STYLE MUSIC PLAYER BAR -->
    <div class="spotify-glass-player" id="spotifyPlayer">
      <div class="player-left-col">
        <div class="album-art-container">
          <div class="album-art" id="playerAlbumArt"></div>
        </div>
        <div class="song-meta">
          <span class="song-title" id="playerSongTitle">Loading...</span>
          <span class="song-artist" id="playerSongArtist">Sleeper Class FM</span>
        </div>
      </div>
      
      <div class="player-center-col">
        <div class="player-controls">
          <button class="control-btn-icon" id="btnPrev" title="Previous Tape">
            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>
          </button>
          <button class="control-btn-icon main-play" id="btnPlayPause" title="Play">
            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M8 5v14l11-7z"/></svg>
          </button>
          <button class="control-btn-icon" id="btnNext" title="Next Tape">
            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M6 18l8.5-6L6 6zm9-12v12h2V6z"/></svg>
          </button>
        </div>
        <div class="progress-container">
          <span class="time-elapsed" id="timeElapsed">0:00</span>
          <div class="progress-bar-bg" id="progressBarBg">
            <div class="progress-bar-fill" id="progressBarFill"></div>
          </div>
          <span class="time-total" id="timeTotal">--:--</span>
        </div>
      </div>
      
      <div class="player-right-col">
        <button class="playlist-pill-btn" id="btnPlaylistSelect">
          <svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; margin-right: 6px; vertical-align: middle;"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg> SELECT TAPE
        </button>
        
        <div class="volume-slider-container">
          <span class="vol-icon" id="volIcon">
            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.2em; height: 1.2em; vertical-align: middle;"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
          </span>
          <input type="range" id="spotifyVolumeSlider" min="0" max="100" value="80" class="vol-range">
        </div>
      </div>

      <!-- Glassmorphic playlist dropdown menu -->
      <div class="glass-playlist-menu" id="playlistMenu">
        <div class="playlist-menu-header">
          <span>SELECT TAPE / टेप चुनें</span>
          <button class="close-menu" id="closePlaylistMenu">&times;</button>
        </div>
        <div class="playlist-items-scroll" id="playlistItemsScroll">
          <!-- Dynamically populated via JS -->
        </div>
      </div>
    </div>"""

for fn in files_to_patch:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Patching player HTML in {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find where the player block is in the file and replace it.
    # Since we might have deleted it or it might have different tags, we'll locate between <!-- SPOTIFY-STYLE MUSIC PLAYER BAR --> or <div class="spotify-glass-player" id="spotifyPlayer">
    # and the closing script tag.
    
    start_tag = "<!-- SPOTIFY-STYLE"
    if start_tag not in content:
        start_tag = '<div class="spotify-glass-player"'
        
    if start_tag in content:
        parts = content.split(start_tag)
        left = parts[0]
        # Find where it ends: before the script tag at the bottom
        right_parts = parts[1].split('<script src=')
        right = '<script src=' + right_parts[1]
        
        new_content = left + player_html_block + "\n\n  " + right
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Successfully patched {fn}!")
    else:
        # If we replaced it with empty in previous tool call, we find between </div class="compartment-panels"> and script tag
        print(f"WARNING: start_tag not found in {fn}. Writing fallback replace.")
        # Let's see: we split on panels closing tag
        parts = content.split('<!-- Panel Section -->')
        if len(parts) > 1:
            # Let's split on the closing </div> of panels
            inner_parts = parts[1].split('</div>\n    \n\n  </div>\n\n  <script')
            if len(inner_parts) > 1:
                # We put it back
                new_content = parts[0] + '<!-- Panel Section -->' + inner_parts[0] + '</div>\n    \n' + player_html_block + '\n  </div>\n\n  <script' + inner_parts[1]
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Recovered and patched {fn} successfully!")
            else:
                # Try simple split on closing panels div
                print(f"Inner split failed in {fn}. Trying simple end injection.")
                # We find the script tag and inject player block right before </div>\n\n  <script
                parts = content.split('  </div>\n\n  <script')
                new_content = parts[0] + player_html_block + '\n  </div>\n\n  <script' + parts[1]
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Simple end injection worked on {fn}!")
        
print("All HTML patches completed successfully!")
