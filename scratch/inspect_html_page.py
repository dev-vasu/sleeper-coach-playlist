import urllib.request
import re

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

# Find <title>
title_match = re.search(r'<title>(.*?)</title>', html_content)
if title_match:
    print(f"HTML Title: {title_match.group(1)}")
else:
    print("No HTML Title found!")

# Is there a sign-in or consent page?
if "consent.youtube" in html_content or "Google" in html_content and "Sign in" in html_content:
    print("Detected Google consent / sign-in screen!")

# Print length of HTML content
print(f"HTML Length: {len(html_content)}")
