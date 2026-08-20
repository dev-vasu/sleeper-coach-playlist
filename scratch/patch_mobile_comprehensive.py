import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

# Remove any previously appended mobile fix to avoid conflicts, then append clean version
with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# Strip previous mobile fix attempts
STRIP_MARKERS = [
    "/* ==========================================================================\n   MOBILE FIXES — Subpage panels",
]
for marker in STRIP_MARKERS:
    idx = content.find(marker)
    if idx != -1:
        content = content[:idx]
        print(f"Stripped previous mobile fix starting at index {idx}")

MOBILE_CSS = """

/* ==========================================================================
   COMPREHENSIVE MOBILE RESPONSIVE STYLES — ALL 4 THEMES
   Breakpoints:
     Portrait mobile   → max-aspect-ratio: 13/10
     Landscape mobile  → max-height: 540px
     Small portrait    → max-width: 480px
     Tiny screens      → max-width: 360px
   ========================================================================== */

/* ── 1. Portrait Layout (all pages) ──────────────────────────────────────── */
@media (max-aspect-ratio: 13/10) {

  /* Root layout: 2-row grid — scene on top, console on bottom */
  .train-compartment {
    display: grid !important;
    grid-template-rows: 46vh 1fr !important;
    height: 100dvh !important;
    width: 100vw !important;
    overflow: hidden !important;
  }

  /* Top: scene viewport */
  .compartment-visuals {
    grid-row: 1 !important;
    position: relative !important;
    width: 100vw !important;
    height: 46vh !important;
    overflow: hidden !important;
    left: 0 !important;
    top: 0 !important;
    flex-shrink: 0 !important;
  }

  /* Bottom: control panels — scrollable column */
  .compartment-panels {
    grid-row: 2 !important;
    position: relative !important;
    left: auto !important; top: auto !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    padding: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    background: #0b0f14 !important;
    border-top: 1.5px solid rgba(255,255,255,0.08) !important;
    box-sizing: border-box !important;
    padding-bottom: 80px !important; /* space for fixed player bar */
    -webkit-overflow-scrolling: touch;
  }

  /* ─── Tab Navigation ─────────────────────────────────────────────────── */
  .mobile-tabs-nav {
    display: flex !important;
    position: sticky !important;
    top: 0 !important;
    width: 100% !important;
    z-index: 50 !important;
    background: #0b0f14 !important;
    border-bottom: 1.5px solid rgba(255,255,255,0.08) !important;
    flex-shrink: 0 !important;
  }

  .tab-nav-btn {
    flex: 1 !important;
    background: transparent !important;
    border: none !important;
    color: rgba(255,255,255,0.4) !important;
    padding: 13px 0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    text-align: center !important;
    transition: all 0.2s ease !important;
    border-bottom: 2px solid transparent !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
  }
  .tab-nav-btn.active {
    color: #e2b865 !important;
    border-bottom-color: #e2b865 !important;
  }

  /* Tab-gated visibility */
  #switchboardPanel, #timeOfDayCard, #clampedTicket, #vintagePoster {
    display: none !important;
  }
  .compartment-panels.active-tab-console #switchboardPanel { display: flex !important; }
  .compartment-panels.active-tab-schedule #timeOfDayCard  { display: block !important; }
  .compartment-panels.active-tab-ticket #clampedTicket,
  .compartment-panels.active-tab-ticket #vintagePoster    { display: flex !important; }

  /* ─── Panel cards: stack full-width ─────────────────────────────────── */
  .glass-control-panel,
  .time-of-day-card,
  .clamped-ticket-hotspot,
  .vintage-frame {
    position: relative !important;
    left: auto !important; top: auto !important;
    width: 100% !important;
    height: auto !important;
    transform: none !important;
    margin: 0 !important;
    max-width: none !important;
    box-shadow: none !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    border-radius: 0 !important;
    border-left: none !important;
    border-right: none !important;
  }

  /* Switchboard: 2-column grid */
  .glass-control-panel {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1px !important;
    padding: 12px !important;
  }
  .panel-header {
    grid-column: span 2 !important;
    font-size: 10px !important;
    padding-bottom: 6px !important;
    margin-bottom: 4px !important;
  }
  .glass-switch-item {
    padding: 10px 12px !important;
    border-radius: 10px !important;
  }
  .switch-title { font-size: 11px !important; }
  .switch-desc  { display: none !important; }
  .glass-toggle {
    width: 32px !important;
    height: 17px !important;
    flex-shrink: 0 !important;
  }
  .toggle-nob {
    width: 13px !important;
    height: 13px !important;
  }

  /* Console switches on subpages (Punjab/Jammu/English) — same grid treatment */
  .console-switches {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1px !important;
    padding: 12px !important;
    background: #0b0f14 !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }

  /* ─── Ticket card ────────────────────────────────────────────────────── */
  .clamped-ticket-hotspot {
    background: transparent !important;
    border: none !important;
    padding: 12px !important;
  }
  .clamped-ticket-hotspot .ticket-zoom-card {
    display: block !important;
    position: relative !important;
    width: 100% !important;
    left: auto !important; top: auto !important;
    transform: none !important;
    opacity: 1 !important;
    margin: 0 !important;
  }

  /* ─── Vintage poster ─────────────────────────────────────────────────── */
  .vintage-frame {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    background: rgba(15,23,42,0.5) !important;
    border: none !important;
    padding: 16px !important;
    box-sizing: border-box !important;
  }
  .vintage-frame .frame-glass { width: 130px !important; }

  /* ─── Fixed player bar at bottom ─────────────────────────────────────── */
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
  .album-art-container {
    width: 36px !important;
    height: 36px !important;
    font-size: 18px !important;
  }
  .song-title  { font-size: 12px !important; max-width: 120px !important; }
  .song-artist { font-size: 10px !important; }
  .control-btn-icon       { font-size: 16px !important; padding: 4px !important; }
  .control-btn-icon.main-play { font-size: 22px !important; }
  .volume-slider-container { display: none !important; } /* hidden on mobile */
  .playlist-pill-btn {
    font-size: 9px !important;
    padding: 5px 8px !important;
    white-space: nowrap !important;
  }

  /* ─── Playlist dropdown menu ─────────────────────────────────────────── */
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

  /* ─── Theme Explorer Widget — bottom-right, above player ─────────────── */
  .theme-explorer-widget {
    position: fixed !important;
    bottom: 82px !important;
    left: 10px !important;
    right: auto !important;
    z-index: 250 !important;
  }
  .theme-explorer-trigger {
    padding: 9px 14px 9px 11px !important;
    font-size: 11px !important;
    border-radius: 40px !important;
  }
  .theme-explorer-label { font-size: 10px !important; }
  .theme-explorer-panel {
    width: min(250px, 88vw) !important;
    bottom: 100% !important;
    top: auto !important;
  }
  .theme-explorer-widget.open .theme-explorer-panel {
    max-height: 50vh !important;
    overflow-y: auto !important;
  }
  .theme-card { padding: 9px 10px !important; gap: 8px !important; }
  .theme-card-icon { font-size: 20px !important; width: 28px !important; }
  .theme-card-name { font-size: 11px !important; }
  .theme-card-desc { font-size: 10px !important; }

  /* ─── Sky title on subpages ──────────────────────────────────────────── */
  .window-sky-title {
    top: 12% !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    text-align: center !important;
    width: 92vw !important;
  }
  .window-sky-title .line1,
  .window-sky-title .line2 {
    font-size: clamp(24px, 8vw, 48px) !important;
    line-height: 1.1 !important;
    letter-spacing: 1px !important;
  }
  .window-sky-title .line3 {
    font-size: clamp(10px, 3vw, 13px) !important;
    max-width: 85vw !important;
    line-height: 1.5 !important;
  }

  /* ─── Clock & online counter ─────────────────────────────────────────── */
  .sky-clock {
    font-size: 14px !important;
    top: 8px !important;
    left: 10px !important;
  }
  .sky-online-counter {
    font-size: 11px !important;
    top: 10px !important;
    right: 10px !important;
  }

  /* ─── Splash screen grid ─────────────────────────────────────────────── */
  .theme-splash-inner { padding: 32px 16px 24px !important; gap: 24px !important; }
  .theme-splash-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px !important;
  }
  .theme-splash-card { min-height: 150px !important; border-radius: 14px !important; }
  .theme-splash-card-emoji { font-size: 26px !important; }
  .theme-splash-card-name  { font-size: 12px !important; }
  .theme-splash-card-sub   { font-size: 10px !important; }
  .theme-splash-title { font-size: clamp(22px, 7vw, 36px) !important; }
  .theme-splash-subtitle { font-size: 11px !important; }
}

/* ── 2. Landscape Mobile (short screens) ─────────────────────────────────── */
@media (max-height: 500px) and (orientation: landscape) {
  .spotify-glass-player {
    height: 48px !important;
    bottom: 6px !important;
    padding: 0 10px !important;
    border-radius: 24px !important;
  }
  .album-art-container { width: 30px !important; height: 30px !important; }
  .song-title  { font-size: 11px !important; }
  .song-artist { display: none !important; }
  .progress-container { display: none !important; }

  .glass-playlist-menu {
    bottom: 60px !important;
    max-height: 55vh !important;
    width: min(260px, 50vw) !important;
    right: 8px !important;
  }
  .theme-explorer-widget {
    bottom: 60px !important;
    left: 8px !important;
  }
  .theme-explorer-panel {
    max-height: 55vh !important;
    overflow-y: auto !important;
  }
  .window-sky-title {
    top: 6% !important;
  }
  .window-sky-title .line1 { font-size: 20px !important; }
  .window-sky-title .line2 { font-size: 16px !important; }
  .window-sky-title .line3 { display: none !important; }
}

/* ── 3. Very small portrait phones (≤ 380px wide) ────────────────────────── */
@media (max-width: 380px) and (max-aspect-ratio: 13/10) {
  .theme-splash-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
  }
  .theme-splash-card { min-height: 120px !important; }
  .theme-splash-card-name { font-size: 11px !important; }
  .theme-splash-card-sub  { display: none !important; }

  .song-title { max-width: 90px !important; }
  .control-btn-icon { padding: 2px !important; }
}
"""

content = content.rstrip() + MOBILE_CSS

with open(style_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Comprehensive mobile CSS written successfully!")
