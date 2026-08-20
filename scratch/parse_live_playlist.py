import urllib.request
import re
import json
import html

url = "https://www.youtube.com/playlist?list=PLfTZYIwCm-itGqun7vm2loLL5dYoBux8o"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

print(f"Downloading playlist page from {url}...")
try:
    with urllib.request.urlopen(req) as response:
        html_content = response.read().decode('utf-8')
    print("Page downloaded successfully!")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Find ytInitialData
match = re.search(r'var ytInitialData\s*=\s*(\{.*?\});', html_content)
if not match:
    # Try another pattern
    match = re.search(r'window\["ytInitialData"\]\s*=\s*(\{.*?\});', html_content)

if not match:
    print("Could not find ytInitialData in HTML!")
    # Let's save a snippet of the page to inspect
    with open("page_snippet.html", "w", encoding="utf-8") as f:
        f.write(html_content[:100000])
    print("Saved page snippet for inspection.")
    exit(1)

data_str = match.group(1)
try:
    data = json.loads(data_str)
    print("Parsed JSON successfully!")
except Exception as e:
    print(f"JSON parsing error: {e}")
    exit(1)

# Navigate to tracks
# In standard YouTube Playlist ytInitialData:
# data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
try:
    contents = data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
except Exception as e:
    # Try alternative paths
    contents = []
    print(f"Primary JSON path failed: {e}")
    # Let's write the keys to see what is there
    print("Data keys:", list(data.keys()))

tracks = []
colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]

if contents:
    for idx, item in enumerate(contents):
        video_renderer = item.get('playlistVideoRenderer')
        if not video_renderer:
            continue
        ytId = video_renderer.get('videoId')
        title_runs = video_renderer.get('title', {}).get('runs', [])
        title = title_runs[0].get('text') if title_runs else "Unknown Title"
        # Sanitize title
        title = title.replace('"', '\\"').upper()
        color = colors[idx % len(colors)]
        tracks.append((title, ytId, color))

print(f"Found {len(tracks)} tracks via JSON navigation!")

# If JSON navigation failed, try regex fallback on the whole page content!
if not tracks:
    print("Trying regex fallback parsing...")
    # Find all occurrences of "playlistVideoRenderer":{"videoId":"XXX"...
    # We can search for '"playlistVideoRenderer":{.*?"videoId":"([a-zA-Z0-9_-]{11})".*?"title":{"runs":\[{"text":"(.*?)"\}\]'
    matches = re.finditer(r'"playlistVideoRenderer":\s*\{.*?"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})".*?"title"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"', html_content)
    seen = set()
    for idx, m in enumerate(matches):
        vid = m.group(1)
        title = m.group(2)
        if vid not in seen:
            seen.add(vid)
            # Unescape html entities
            title = html.unescape(title).replace('"', '\\"').upper()
            color = colors[idx % len(colors)]
            tracks.append((title, vid, color))
    print(f"Found {len(tracks)} tracks via regex fallback!")

# Let's write them formatted to a file
with open("jammu_tracks.txt", "w", encoding="utf-8") as out:
    for idx, (title, ytId, color) in enumerate(tracks):
        out.write(f'    "track_{idx + 1}": {{ title: "{title}", ytId: "{ytId}", color: "{color}" }},\n')

print(f"Wrote {len(tracks)} tracks to jammu_tracks.txt")
