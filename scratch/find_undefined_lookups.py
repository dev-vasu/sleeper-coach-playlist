import re

with open(r"C:\Users\dvasu\window-seat\punjab.js", "r", encoding="utf-8") as f:
    content = f.read()

# Match document.getElementById('...').addEventListener
pattern = r"document\.getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)\.addEventListener"

matches = re.findall(pattern, content)
print("Unwrapped event listeners on getElementById found:")
for m in matches:
    print(f"- {m}")
