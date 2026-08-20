import os

base = r"C:\Users\dvasu\window-seat"

pages = {
    "index.html":   ("/favicon-train.svg",   "Sleeper Coach Playlist"),
    "punjab.html":  ("/favicon-punjab.svg",  "Sad Punjabi | Sleeper Coach"),
    "jammu.html":   ("/favicon-jammu.svg",   "Jammu Dogri | Sleeper Coach"),
    "english.html": ("/favicon-english.svg", "80's English R&B | Sleeper Coach"),
}

FAVICON_TAG = '<link rel="icon" type="image/svg+xml" href="{icon}">\n  <link rel="alternate icon" href="{icon}">'

for filename, (icon, title) in pages.items():
    path = os.path.join(base, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    favicon_html = FAVICON_TAG.format(icon=icon)

    # Insert favicon after <meta name="viewport"> line
    insert_after = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    if insert_after in content:
        if "favicon" not in content:
            content = content.replace(insert_after, insert_after + "\n  " + favicon_html)
            print(f"Added favicon to {filename}")
        else:
            print(f"Favicon already present in {filename}, updating...")
            # Replace existing favicon tag
            import re
            content = re.sub(r'<link rel="icon"[^\n]+\n\s*<link rel="alternate icon"[^\n]+', favicon_html, content)
            print(f"  Updated favicon in {filename}")
    else:
        print(f"Viewport meta not found in {filename}")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("\nAll favicons wired!")
