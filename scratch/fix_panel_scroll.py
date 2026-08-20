import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

SCROLL_FIX = """
/* ==========================================================================
   MOBILE PANEL SCROLL FIX — ensures content never clips off-screen
   ========================================================================== */
@media (max-aspect-ratio: 13/10) {

  /* Critical: train-compartment must be a proper grid, not overflow:hidden globally */
  .train-compartment {
    display: grid !important;
    grid-template-rows: 46vh 1fr !important;
    height: 100dvh !important;       /* dvh = dynamic viewport height (handles browser chrome) */
    width: 100vw !important;
    overflow: hidden !important;
  }

  /* The panels grid cell must shrink to fill remaining space, NOT overflow */
  .compartment-panels {
    grid-row: 2 !important;
    position: relative !important;
    left: auto !important;
    top: auto !important;
    width: 100% !important;
    height: 100% !important;         /* fill the grid row */
    min-height: 0 !important;        /* ← CRITICAL: allows flex/grid child to scroll */
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    padding: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    -webkit-overflow-scrolling: touch !important;
    background: #0b0f14 !important;
    border-top: 1.5px solid rgba(255,255,255,0.08) !important;
    box-sizing: border-box !important;
    /* Enough bottom padding to clear the fixed player bar (62px) + gap (14px) + safety (14px) */
    padding-bottom: 90px !important;
    scroll-behavior: smooth !important;
  }

  /* Sticky tabs must not grow (locks position at top during scroll) */
  .mobile-tabs-nav {
    flex-shrink: 0 !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 50 !important;
    background: #0b0f14 !important;
    border-bottom: 1.5px solid rgba(255,255,255,0.08) !important;
  }

  /* All panel cards: position:relative, height:auto, no fixed heights */
  .glass-control-panel,
  .time-of-day-card,
  .clamped-ticket-hotspot,
  .vintage-frame,
  #switchboardPanel {
    position: relative !important;
    left: auto !important;
    top: auto !important;
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    flex-shrink: 0 !important;         /* don't let flex compress content */
    transform: none !important;
    box-sizing: border-box !important;
    overflow: visible !important;
  }

  /* Console switches grid: 2-col, no fixed height */
  .console-switches,
  .glass-control-panel {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
    padding: 14px !important;
    flex-shrink: 0 !important;
    height: auto !important;
  }

  /* Switch items: compact but never clipped */
  .glass-switch-item {
    padding: 10px 12px !important;
    border-radius: 10px !important;
    box-sizing: border-box !important;
    min-height: 44px !important;       /* touch target minimum */
  }

  /* Hide long descriptions to save space */
  .switch-desc { display: none !important; }
  .switch-title { font-size: 11px !important; white-space: nowrap !important; overflow: hidden !important; text-overflow: ellipsis !important; }

  /* Toggle sizing */
  .glass-toggle {
    width: 32px !important;
    height: 17px !important;
    flex-shrink: 0 !important;
  }
  .toggle-nob { width: 13px !important; height: 13px !important; }

  /* Panel header spans full width */
  .panel-header {
    grid-column: span 2 !important;
    font-size: 10px !important;
    padding: 8px 0 6px !important;
    flex-shrink: 0 !important;
  }

  /* Change Vibe widget inline in panel: no absolute positioning */
  .theme-explorer-widget-mobile {
    flex-shrink: 0 !important;
    margin: 8px 14px !important;
    width: calc(100% - 28px) !important;
  }
  .theme-explorer-widget-mobile .theme-explorer-trigger {
    width: 100% !important;
    border-radius: 12px !important;
    justify-content: center !important;
    padding: 13px 16px !important;
    font-size: 12px !important;
  }
  .theme-explorer-widget-mobile .theme-explorer-panel {
    width: 100% !important;
    position: relative !important;
    bottom: auto !important;
    top: auto !important;
    margin-top: 8px !important;
    max-height: none !important;
    overflow: visible !important;
    opacity: 1 !important;
    pointer-events: none;
    transform: translateY(8px);
    transition: all 0.25s ease;
  }
  .theme-explorer-widget-mobile.open .theme-explorer-panel {
    pointer-events: auto !important;
    transform: translateY(0) !important;
  }
  .theme-explorer-widget-mobile .theme-card {
    margin-bottom: 6px !important;
    border-radius: 12px !important;
  }

  /* Ticket card: full width inline, no absolute overlay */
  .clamped-ticket-hotspot {
    background: transparent !important;
    border: none !important;
    padding: 14px !important;
  }
  .clamped-ticket-hotspot .ticket-zoom-card {
    display: block !important;
    position: relative !important;
    width: 100% !important;
    left: auto !important;
    top: auto !important;
    transform: none !important;
    opacity: 1 !important;
    margin: 0 !important;
  }

  /* Vintage poster frame */
  .vintage-frame {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    background: rgba(15,23,42,0.5) !important;
    padding: 16px !important;
  }
  .vintage-frame .frame-glass { width: 130px !important; }

  /* Sound board triggers: wrap neatly */
  .sound-board-triggers {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    padding: 0 14px 14px !important;
  }
  .trigger-btn {
    flex: 1 1 calc(50% - 8px) !important;
    min-width: 0 !important;
    font-size: 11px !important;
    padding: 10px 8px !important;
    white-space: nowrap !important;
  }

  /* Train map / schedule if present */
  .control-label {
    font-size: 10px !important;
    padding: 10px 14px 4px !important;
    display: block !important;
  }

  /* Fixed music player at bottom — always visible */
  .spotify-glass-player {
    position: fixed !important;
    bottom: 10px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 94vw !important;
    max-width: 520px !important;
    height: 62px !important;
    z-index: 200 !important;
    padding: 0 14px !important;
    border-radius: 30px !important;
    box-sizing: border-box !important;
  }

  /* Album art compact */
  .album-art-container {
    width: 36px !important;
    height: 36px !important;
    font-size: 18px !important;
  }
  .song-title  { font-size: 12px !important; max-width: 120px !important; }
  .song-artist { font-size: 10px !important; }
  .control-btn-icon { font-size: 16px !important; padding: 4px !important; }
  .control-btn-icon.main-play { font-size: 22px !important; }
  .volume-slider-container { display: none !important; }
  .playlist-pill-btn {
    font-size: 9px !important;
    padding: 5px 8px !important;
    white-space: nowrap !important;
  }

  /* Playlist menu: anchored above player */
  .glass-playlist-menu {
    position: fixed !important;
    bottom: 82px !important;
    right: 10px !important;
    left: auto !important;
    width: min(290px, 92vw) !important;
    max-height: 52vh !important;
    overflow-y: auto !important;
    z-index: 300 !important;
  }
}
"""

if "MOBILE PANEL SCROLL FIX" not in content:
    content = content.rstrip() + "\n" + SCROLL_FIX
    with open(style_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mobile panel scroll fix appended!")
else:
    # Replace existing
    start = content.find("/* ==========================================================================\n   MOBILE PANEL SCROLL FIX")
    if start != -1:
        # Find the closing of the last rule
        end = content.find("\n}\n", content.find("glass-playlist-menu", start)) + 3
        content = content[:start] + SCROLL_FIX.lstrip() + content[end:]
        with open(style_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Mobile panel scroll fix replaced!")
