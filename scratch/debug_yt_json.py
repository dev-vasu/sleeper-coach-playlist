import json
import re

# Read data from var ytInitialData in HTML
with open(r"C:\Users\dvasu\window-seat\scratch\parse_live_playlist.py", "r", encoding="utf-8") as f:
    # Run the retrieval block inline to get the json dict
    pass

# Let's write a script that reads the downloaded page, extracts json, and searches it
import urllib.request

url = "https://www.youtube.com/playlist?list=PLfTZYIwCm-itGqun7vm2loLL5dYoBux8o"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        html_content = response.read().decode('utf-8')
except Exception as e:
    print(f"Error: {e}")
    exit(1)

match = re.search(r'var ytInitialData\s*=\s*(\{.*?\});', html_content)
if match:
    data = json.loads(match.group(1))
    
    # Recursively find all dicts that contain videoId
    found = []
    
    def search_dict(d, path=""):
        if isinstance(d, dict):
            if "videoId" in d and "title" in d:
                # Get title text
                title_text = "Unknown"
                if isinstance(d.get("title"), dict):
                    runs = d["title"].get("runs", [])
                    if runs:
                        title_text = runs[0].get("text", "Unknown")
                elif isinstance(d.get("title"), str):
                    title_text = d["title"]
                found.append((d["videoId"], title_text, path))
            for k, v in d.items():
                search_dict(v, f"{path}['{k}']")
        elif isinstance(d, list):
            for idx, item in enumerate(d):
                search_dict(item, f"{path}[{idx}]")
                
    search_dict(data)
    print(f"Found {len(found)} videos:")
    for vid, title, path in found[:10]:
        print(f"- {vid}: {title} (at {path[:100]})")
        
    # Write all found tracks
    colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]
    seen = set()
    unique_tracks = []
    for vid, title, path in found:
        if vid not in seen:
            seen.add(vid)
            unique_tracks.append((title, vid))
            
    with open("jammu_tracks.txt", "w", encoding="utf-8") as out:
        for idx, (title, ytId) in enumerate(unique_tracks):
            color = colors[idx % len(colors)]
            title_clean = title.replace('"', '\\"').upper()
            out.write(f'    "track_{idx + 1}": {{ title: "{title_clean}", ytId: "{ytId}", color: "{color}" }},\n')
    print(f"Wrote {len(unique_tracks)} unique tracks to jammu_tracks.txt")
else:
    print("No ytInitialData found!")
