import subprocess
import json
import re

url = "https://www.youtube.com/playlist?list=RDCLAK5uy_lkc6zoUgat_9ifg8CCcqE_9I4cc8nNZv8"
print(f"Running yt-dlp to dump playlist JSON for English: {url}...")

cmd = ["yt-dlp", "--flat-playlist", "--dump-single-json", url]
try:
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"Error running yt-dlp: {result.stderr}")
        exit(1)
        
    data = json.loads(result.stdout)
    entries = data.get("entries", [])
    print(f"yt-dlp successfully retrieved {len(entries)} tracks for English!")
    
    colors = ["#e74c3c", "#3498db", "#f1c40f", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]
    
    with open("english_tracks.txt", "w", encoding="utf-8") as out:
        for idx, entry in enumerate(entries):
            title = entry.get("title", "Unknown Title")
            ytId = entry.get("id")
            if not ytId:
                continue
                
            color = colors[idx % len(colors)]
            
            # Clean and sanitize titles
            title_clean = title.replace('"', '\\"').upper()
            title_clean = re.sub(r'\s*\(OFFICIAL\s*(VIDEO|AUDIO|SOND|SONG)?\)', '', title_clean)
            title_clean = re.sub(r'\s*\|.*$', '', title_clean)
            title_clean = re.sub(r'\s*\[OFFICIAL.*$', '', title_clean)
            title_clean = re.sub(r'\s*\(LYRICS\)', '', title_clean)
            title_clean = title_clean.strip()
            
            out.write(f'    "track_{idx + 1}": {{ title: "{title_clean}", ytId: "{ytId}", color: "{color}" }},\n')
            
    print(f"Successfully wrote {len(entries)} tracks to english_tracks.txt!")
except Exception as e:
    print(f"Python execution failed: {e}")
