import os

base = r"C:\Users\dvasu\window-seat"

# ─── Widget HTML for each subpage ────────────────────────────────────────────
JAMMU_WIDGET = """      <!-- Floating Theme Explorer Widget -->
      <div class="theme-explorer-widget" id="themeExplorer">
        <button class="theme-explorer-trigger" id="themeExplorerTrigger">
          <span class="theme-explorer-icon">&#127917;</span>
          <span class="theme-explorer-label">Change Vibe</span>
          <span class="theme-explorer-arrow">&#x203a;</span>
        </button>
        <div class="theme-explorer-panel" id="themeExplorerPanel">
          <div class="theme-explorer-header">
            <span>&#10022; Other Vibes</span>
            <button class="theme-explorer-close" id="themeExplorerClose">&times;</button>
          </div>
          <a href="/" class="theme-card theme-card-train">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#128642;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">CLASSIC TRAIN</div>
              <div class="theme-card-desc">Hindi classics &middot; Retro sleeper coach</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
          <a href="/punjab" class="theme-card theme-card-punjab">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#127806;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">SAD PUNJABI</div>
              <div class="theme-card-desc">Sada-e-Hijr &middot; Sufi folk classics</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
          <a href="/english" class="theme-card theme-card-english">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#127925;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">80s ENGLISH R&amp;B</div>
              <div class="theme-card-desc">Timeless music &middot; Rainy city night</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
        </div>
      </div>"""

ENGLISH_WIDGET = """      <!-- Floating Theme Explorer Widget -->
      <div class="theme-explorer-widget" id="themeExplorer">
        <button class="theme-explorer-trigger" id="themeExplorerTrigger">
          <span class="theme-explorer-icon">&#127917;</span>
          <span class="theme-explorer-label">Change Vibe</span>
          <span class="theme-explorer-arrow">&#x203a;</span>
        </button>
        <div class="theme-explorer-panel" id="themeExplorerPanel">
          <div class="theme-explorer-header">
            <span>&#10022; Other Vibes</span>
            <button class="theme-explorer-close" id="themeExplorerClose">&times;</button>
          </div>
          <a href="/" class="theme-card theme-card-train">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#128642;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">CLASSIC TRAIN</div>
              <div class="theme-card-desc">Hindi classics &middot; Retro sleeper coach</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
          <a href="/punjab" class="theme-card theme-card-punjab">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#127806;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">SAD PUNJABI</div>
              <div class="theme-card-desc">Sada-e-Hijr &middot; Sufi folk classics</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
          <a href="/jammu" class="theme-card theme-card-jammu">
            <div class="theme-card-glow"></div>
            <div class="theme-card-icon">&#127956;</div>
            <div class="theme-card-info">
              <div class="theme-card-name">JAMMU (DOGRI)</div>
              <div class="theme-card-desc">Valley folk &middot; Mountain vibes</div>
            </div>
            <div class="theme-card-arrow">&rarr;</div>
          </a>
        </div>
      </div>"""

# ─── Patch jammu.html ─────────────────────────────────────────────────────────
jammu_path = os.path.join(base, "jammu.html")
with open(jammu_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

# Replace from the Plaque comment up to and including </div>\n    </div>\n before SPOTIFY
old_block = """      <!-- Theme/Route Selector Plaque -->
      <div class="time-of-day-card" id="timeOfDayCard">
        <div class="screw-head top-left"></div>
        <div class="screw-head top-right"></div>
        <div class="screw-head bottom-left"></div>
        <div class="screw-head bottom-right"></div>
        



        <label class="control-label">SWITCH THEME / \u0925\u0940\u092e \u092c\u0926\u0932\u0947\u0902</label>
                <div class="route-dropdown-container">
          <button class="route-dropdown-btn" id="btnRouteDropdown">
            \U0001f3d4\ufe0f JAMMU (DOGRI) <span style="font-size: 10px; opacity: 0.6;">\u25bc</span>
          </button>
          <div class="route-dropdown-menu" id="routeDropdownMenu">
            <a href="/" class="route-dropdown-item">\U0001f682 CLASSIC TRAIN</a>
            <a href="/punjab" class="route-dropdown-item">\U0001f33e SAD PUNJABI</a>
            <a href="/jammu" class="route-dropdown-item active">\U0001f3d4\ufe0f JAMMU (DOGRI)</a>
            <a href="/english" class="route-dropdown-item">\U0001f3b5 80s ENGLISH R&B</a>
          </div>
        </div>

        
      </div>
    </div>"""

new_block = JAMMU_WIDGET + "\n    </div>"

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(jammu_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced timeOfDayCard with Change Vibe in jammu.html")
else:
    # Try without extra blank lines
    content2 = content
    start = content2.find("      <!-- Theme/Route Selector Plaque -->")
    end = content2.find("      </div>\n    </div>\n\n        <!-- SPOTIFY-STYLE MUSIC PLAYER BAR -->")
    if end == -1:
        end = content2.find("      </div>\n    </div>\n\n    <!-- SPOTIFY")
    if start != -1 and end != -1:
        before = content2[:start]
        after = content2[end + len("      </div>\n    </div>"):]
        content2 = before + new_block + after
        with open(jammu_path, "w", encoding="utf-8") as f:
            f.write(content2)
        print("Replaced (fallback) timeOfDayCard in jammu.html")
    else:
        print(f"FAILED to patch jammu.html: start={start}, end={end}")

# ─── Patch english.html ───────────────────────────────────────────────────────
english_path = os.path.join(base, "english.html")
with open(english_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

start = content.find("      <!-- Theme/Route Selector Plaque -->")
end = content.find("      </div>\n    </div>\n\n    <!-- SPOTIFY")
if end == -1:
    end = content.find("      </div>\n    </div>\n\n        <!-- SPOTIFY")
if start != -1 and end != -1:
    before = content[:start]
    after = content[end + len("      </div>\n    </div>"):]
    content = before + ENGLISH_WIDGET + "\n    </div>" + after
    with open(english_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced timeOfDayCard with Change Vibe in english.html")
else:
    print(f"FAILED to patch english.html: start={start}, end={end}")

print("Done!")
