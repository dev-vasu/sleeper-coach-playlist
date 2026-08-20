with open(r"C:\Users\dvasu\window-seat\punjab.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

open_braces = 0
unmatched_close = []

for idx, line in enumerate(lines):
    line_num = idx + 1
    for char in line:
        if char == "{":
            open_braces += 1
        elif char == "}":
            open_braces -= 1
            if open_braces < 0:
                unmatched_close.append(line_num)
                open_braces = 0

print(f"Total open braces remaining at end of file: {open_braces}")
print(f"Unmatched closing braces found on lines: {unmatched_close}")
