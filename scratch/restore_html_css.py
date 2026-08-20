import urllib.request
import os

files = ["index.html", "style.css"]

for fn in files:
    url = f"https://sleeper-coach-playlist.vercel.app/{fn}"
    dest = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    print(f"Downloading clean {fn} from {url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Successfully restored {fn}!")
    except Exception as e:
        print(f"Error downloading {fn}: {e}")

print("Restoration complete!")
