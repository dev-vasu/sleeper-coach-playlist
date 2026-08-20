import json
import re
import html

path = r"C:\Users\dvasu\.gemini\antigravity-cli\brain\c0dc278a-945b-452c-a2e3-ccf5fd593546\.system_generated\steps\5263\content.md"

with open(path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Try finding ytInitialData
match = re.search(r'var ytInitialData\s*=\s*(\{.*?\});', html_content)
if not match:
    match = re.search(r'window\["ytInitialData"\]\s*=\s*(\{.*?\});', html_content)

if match:
    data = json.loads(match.group(1))
    print("ytInitialData parsed successfully!")
    
    found = []
    seen = set()
    
    def search_dict(d, path=""):
        if isinstance(d, dict):
            # Check if it has videoId and is inside a playlist context (like playlistVideoRenderer or similar)
            if "videoId" in d:
                # Get title
                title_text = ""
                if "title" in d:
                    t_val = d["title"]
                    if isinstance(t_val, dict) and "runs" in t_val:
                        runs = t_val["runs"]
                        if runs:
                            title_text = runs[0].get("text", "")
                    elif isinstance(t_val, dict) and "simpleText" in t_val:
                        title_text = t_val["simpleText"]
                    elif isinstance(t_val, str):
                        title_text = t_val
                
                # Check if it has a lengthText or accessibility to ensure it is a real video list item
                if title_text and d["videoId"] not in seen:
                    seen.add(d["videoId"])
                    found.append((title_text, d["videoId"]))
                    
            for k, v in d.items():
                search_dict(v, f"{path}['{k}']")
        elif isinstance(d, list):
            for idx, item in enumerate(d):
                search_dict(item, f"{path}[{idx}]")
                
    search_dict(data)
    print(f"Recursively found {len(found)} videos:")
    
    colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]
    
    with open("jammu_tracks.txt", "w", encoding="utf-8") as out:
        for idx, (title, ytId) in enumerate(found):
            color = colors[idx % len(colors)]
            title_clean = title.replace('"', '\\"').upper()
            # Clean common suffixes like "Official Video", "(Dogri)", etc. to keep titles neat on cassette tape
            title_clean = re.sub(r'\s*\(OFFICIAL\s*(VIDEO|AUDIO|SOND|SONG)?\)', '', title_clean)
            title_clean = re.sub(r'\s*\|.*$', '', title_clean)
            title_clean = re.sub(r'\s*\[OFFICIAL.*$', '', title_clean)
            title_clean = title_clean.strip()
            out.write(f'    "track_{idx + 1}": {{ title: "{title_clean}", ytId: "{ytId}", color: "{color}" }},\n')
            
    print(f"Wrote {len(found)} tracks to jammu_tracks.txt!")
else:
    print("Could not find ytInitialData in markdown!")
