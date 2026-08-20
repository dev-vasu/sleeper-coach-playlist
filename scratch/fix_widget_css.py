import os

style_path = r"C:\Users\dvasu\window-seat\style.css"

with open(style_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove conflicting mobile route-hindi widget overrides we added
STRIP = "/* ── Mobile: fix Change Vibe widget overlapping console on main train page ── */"
idx = content.find(STRIP)
if idx != -1:
    # Strip to next major section (the splash enhancements)
    next_section = content.find("/* ── Splash card per-theme borders", idx)
    if next_section != -1:
        content = content[:idx] + content[next_section:]
        print("Stripped old conflicting mobile route-hindi override")
    else:
        print("Could not find next section to strip to")
else:
    print("No conflicting override found")

WIDGET_DUAL_CSS = """
/* ==========================================================================
   CHANGE VIBE WIDGET — Desktop vs Mobile dual display
   On desktop (landscape): widget sits inside .compartment-visuals, absolutely
   On mobile (portrait):   widget-desktop hidden; widget-mobile shown in panel
   ========================================================================== */

/* Desktop widget (inside compartment-visuals) */
.theme-explorer-widget-desktop {
  display: flex;
}
/* Mobile-panel widget (inside compartment-panels) */
.theme-explorer-widget-mobile {
  display: none;
  flex-direction: column;
  gap: 0;
  margin: 12px 16px 0;
}

@media (max-aspect-ratio: 13/10) {
  /* Hide floating desktop widget on mobile */
  .theme-explorer-widget-desktop {
    display: none !important;
  }
  /* Show inline panel widget on mobile */
  .theme-explorer-widget-mobile {
    display: flex !important;
  }
  /* Mobile widget trigger: full-width pill */
  .theme-explorer-widget-mobile .theme-explorer-trigger {
    width: 100% !important;
    border-radius: 12px !important;
    justify-content: center !important;
    padding: 13px 16px !important;
    font-size: 13px !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
  }
  .theme-explorer-widget-mobile .theme-explorer-panel {
    width: 100% !important;
    position: relative !important;
    bottom: auto !important;
    top: auto !important;
    transform: none !important;
    margin-top: 8px !important;
    max-height: none !important;
    overflow: visible !important;
    pointer-events: auto !important;
  }
  .theme-explorer-widget-mobile.open .theme-explorer-panel {
    opacity: 1 !important;
    transform: none !important;
    pointer-events: auto !important;
  }
  .theme-explorer-widget-mobile .theme-card {
    padding: 12px 14px !important;
    margin-bottom: 6px !important;
    border-radius: 12px !important;
  }
}
"""

content = content.rstrip() + "\n" + WIDGET_DUAL_CSS
with open(style_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Widget dual-display CSS written!")
