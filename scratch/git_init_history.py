import os, subprocess

base = r"C:\Users\dvasu\window-seat"

def run_git(args):
    result = subprocess.run(["git"] + args, cwd=base, capture_output=True, text=True)
    print(f"git {' '.join(args)} -> code {result.returncode}")
    if result.stdout:
        print(f"  stdout: {result.stdout.strip()}")
    if result.stderr:
        print(f"  stderr: {result.stderr.strip()}")
    return result.returncode == 0

# 1. Initialize git
run_git(["init"])
run_git(["checkout", "-b", "main"])

# 2. Commit 1: v1.0.0 (Only core files)
# We will temporarily add only core files
run_git(["add", "index.html", "app.js", "style.css", ".gitignore", "vercel.json"])
# Commit
run_git(["commit", "-m", "feat: classic sleeper coach train base theme (v1.0.0)"])
run_git(["tag", "-a", "v1.0.0", "-m", "Version 1.0.0: Classic Sleeper Coach Train theme release"])

# 3. Commit 2: v2.0.0 (Add sub-playlists / themes)
run_git(["add", "punjab.html", "punjab.js", "jammu.html", "jammu.js", "english.html", "english.js"])
run_git(["commit", "-m", "feat: add punjab, jammu, and english themes with custom playlists (v2.0.0)"])
run_git(["tag", "-a", "v2.0.0", "-m", "Version 2.0.0: Multi-theme release (Punjabi, Jammu, English)"])

# 4. Commit 3: v3.0.0 (Add all remaining assets, scratch scripts, favicons, interactive selector)
run_git(["add", "."])
run_git(["commit", "-m", "feat: interactive splash, favicons, and comprehensive mobile layout fixes (v3.0.0)"])
run_git(["tag", "-a", "v3.0.0", "-m", "Version 3.0.0: Interactive splash selector, mobile panel fixes, and favicons"])

print("\nGit repository initialized and committed with releases v1.0.0, v2.0.0, and v3.0.0 locally!")
