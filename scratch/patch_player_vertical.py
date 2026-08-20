import os

style_path = r"C:\Users\dvasu\window-seat\style.css"
print("Appending music player vertical sizing overrides to style.css...")

with open(style_path, "r", encoding="utf-8") as f:
    style_content = f.read()

player_overrides = """
/* Music Player Taller Vertical Sizing for Room Subpages */
.route-punjab .spotify-glass-player,
.route-jammu .spotify-glass-player,
.route-english .spotify-glass-player {
  height: calc(96px * var(--cabin-scale, 1)) !important;
  border-radius: calc(48px * var(--cabin-scale, 1)) !important;
  padding: 0 calc(32px * var(--cabin-scale, 1)) !important;
  background: rgba(15, 23, 42, 0.6) !important; /* Darker glass for better presence */
  bottom: calc(32px * var(--cabin-scale, 1)) !important;
}

/* Proportional inner elements sizing scaling */
.route-punjab .album-art-container,
.route-jammu .album-art-container,
.route-english .album-art-container {
  width: calc(64px * var(--cabin-scale, 1)) !important;
  height: calc(64px * var(--cabin-scale, 1)) !important;
  font-size: calc(28px * var(--cabin-scale, 1)) !important;
}

.route-punjab .song-title,
.route-jammu .song-title,
.route-english .song-title {
  font-size: calc(15px * var(--cabin-scale, 1)) !important;
}

.route-punjab .song-artist,
.route-jammu .song-artist,
.route-english .song-artist {
  font-size: calc(12px * var(--cabin-scale, 1)) !important;
}

.route-punjab .control-btn-icon,
.route-jammu .control-btn-icon,
.route-english .control-btn-icon {
  font-size: calc(20px * var(--cabin-scale, 1)) !important;
}

.route-punjab .control-btn-icon.main-play,
.route-jammu .control-btn-icon.main-play,
.route-english .control-btn-icon.main-play {
  font-size: calc(32px * var(--cabin-scale, 1)) !important;
}

.route-punjab .progress-container,
.route-jammu .progress-container,
.route-english .progress-container {
  gap: 12px !important;
}

.route-punjab .progress-bar-bg,
.route-jammu .progress-bar-bg,
.route-english .progress-bar-bg {
  height: 6px !important;
  border-radius: 3px !important;
}

.route-punjab .progress-bar-fill,
.route-jammu .progress-bar-fill,
.route-english .progress-bar-fill {
  border-radius: 3px !important;
}

/* Offset playlist dropdown menu above the larger player bar */
.route-punjab .glass-playlist-menu,
.route-jammu .glass-playlist-menu,
.route-english .glass-playlist-menu {
  bottom: calc(140px * var(--cabin-scale, 1)) !important;
}
"""

if "/* Music Player Taller Vertical Sizing for Room Subpages */" not in style_content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(player_overrides)
    print("Player sizing overrides successfully appended!")
else:
    print("Player sizing overrides already present.")
