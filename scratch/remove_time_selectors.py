import os

html_files = ["punjab.html", "jammu.html", "english.html"]

target_block = """        <label class="control-label">TIME OF DAY / समय समय</label>
        <div class="time-selector">
          <button class="time-btn" data-time="morning">🌅 MORNING</button>
          <button class="time-btn active" data-time="day">🌞 DAY</button>
          <button class="time-btn" data-time="sunset">🌇 SUNSET</button>
          <button class="time-btn" data-time="night">🌙 NIGHT</button>
        </div>

        <hr class="card-section-divider">"""

for fn in html_files:
    path = os.path.join(r"C:\Users\dvasu\window-seat", fn)
    if not os.path.exists(path):
        continue
        
    print(f"Removing Time of Day block from {fn}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if target_block in content:
        content = content.replace(target_block, "")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully removed Time of Day block from {fn}!")
    else:
        # Try a more loose regex-based removal in case formatting differs
        import re
        pattern = r'\s*<label class="control-label">TIME OF DAY / समय समय</label>.*?<hr class="card-section-divider">'
        new_content, count = re.subn(pattern, "", content, flags=re.DOTALL)
        if count > 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully removed Time of Day block using regex from {fn}!")
        else:
            print(f"WARNING: Time of Day block not found in {fn}")

print("All HTML files processed!")
