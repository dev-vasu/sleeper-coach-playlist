import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

mobile_fix_css = """
/* ==========================================================================
   MOBILE FIXES — Subpage panels, theme explorer, player bar (all 4 themes)
   ========================================================================== */

/* ── Subpage panels (Punjab, Jammu, English) on mobile portrait ── */
@media (max-aspect-ratio: 13/10) {

  /* Subpages don't have a side console panel, only a Spotify player.
     Ensure the compartment visuals fill the screen correctly. */
  .route-punjab .compartment-panels,
  .route-jammu .compartment-panels,
  .route-english .compartment-panels {
    display: none !important; /* Subpages have no side panel — just visuals + player */
  }

  .route-punjab .train-compartment,
  .route-jammu .train-compartment,
  .route-english .train-compartment {
    display: block !important;
    height: 100vh !important;
    overflow: hidden !important;
  }

  .route-punjab .compartment-visuals,
  .route-jammu .compartment-visuals,
  .route-english .compartment-visuals {
    position: relative !important;
    width: 100vw !important;
    height: 100vh !important;
    top: 0 !important;
    left: 0 !important;
  }

  /* Taller player override must revert on mobile to compact size */
  .route-punjab .spotify-glass-player,
  .route-jammu .spotify-glass-player,
  .route-english .spotify-glass-player {
    height: 64px !important;
    bottom: 12px !important;
    padding: 0 16px !important;
    border-radius: 32px !important;
    width: 92% !important;
    max-width: 92vw !important;
  }

  .route-punjab .album-art-container,
  .route-jammu .album-art-container,
  .route-english .album-art-container {
    width: 38px !important;
    height: 38px !important;
    font-size: 18px !important;
  }

  .route-punjab .song-title,
  .route-jammu .song-title,
  .route-english .song-title {
    font-size: 12px !important;
  }

  .route-punjab .song-artist,
  .route-jammu .song-artist,
  .route-english .song-artist {
    font-size: 10px !important;
  }

  .route-punjab .control-btn-icon,
  .route-jammu .control-btn-icon,
  .route-english .control-btn-icon {
    font-size: 15px !important;
  }

  .route-punjab .control-btn-icon.main-play,
  .route-jammu .control-btn-icon.main-play,
  .route-english .control-btn-icon.main-play {
    font-size: 22px !important;
  }

  /* Playlist menu */
  .route-punjab .glass-playlist-menu,
  .route-jammu .glass-playlist-menu,
  .route-english .glass-playlist-menu {
    bottom: 80px !important;
    right: 12px !important;
    max-height: 55vh !important;
    width: min(300px, 90vw) !important;
    overflow-y: auto !important;
  }

  /* Theme Explorer Widget — move to bottom-right on mobile so it doesn't
     overlap with the player bar which sits at bottom-center */
  .theme-explorer-widget {
    bottom: 88px !important;
    left: auto !important;
    right: 14px !important;
  }

  .theme-explorer-panel {
    width: min(260px, 85vw) !important;
    right: 0 !important;
    left: auto !important;
  }

  /* The Change Vibe panel expands upward — ensure it doesn't go off-screen */
  .theme-explorer-widget.open .theme-explorer-panel {
    max-height: 55vh;
    overflow-y: auto;
  }

  /* Sky title on subpages — shrink a bit on portrait mobile */
  .route-punjab .window-sky-title,
  .route-jammu .window-sky-title,
  .route-english .window-sky-title {
    top: 10% !important;
    width: 94% !important;
  }

  .route-punjab .window-sky-title .line1,
  .route-punjab .window-sky-title .line2,
  .route-jammu .window-sky-title .line1,
  .route-jammu .window-sky-title .line2,
  .route-english .window-sky-title .line1,
  .route-english .window-sky-title .line2 {
    font-size: clamp(28px, 8vw, 52px) !important;
    line-height: 1 !important;
  }

  .route-punjab .window-sky-title .line3,
  .route-jammu .window-sky-title .line3,
  .route-english .window-sky-title .line3 {
    font-size: clamp(11px, 3vw, 15px) !important;
    max-width: 85vw !important;
  }

  /* Clock and online counter — keep visible but compact */
  .sky-clock,
  .sky-online-counter {
    font-size: 11px !important;
  }

  /* Splash screen grid on mobile */
  .theme-splash-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px !important;
  }

  .theme-splash-card {
    min-height: 160px !important;
  }

  .theme-splash-card-emoji {
    font-size: 28px !important;
  }

  .theme-splash-card-name {
    font-size: 13px !important;
  }

  .theme-splash-title {
    font-size: clamp(22px, 7vw, 36px) !important;
  }
}

/* Extra small screens */
@media (max-width: 380px) {
  .theme-splash-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
  }
  .theme-splash-card {
    min-height: 130px !important;
  }
  .theme-explorer-trigger {
    padding: 8px 12px 8px 10px !important;
    font-size: 11px !important;
  }
}
"""

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

if "MOBILE FIXES — Subpage panels" not in content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(mobile_fix_css)
    print("Mobile fix CSS appended successfully!")
else:
    print("Mobile fix CSS already present.")
