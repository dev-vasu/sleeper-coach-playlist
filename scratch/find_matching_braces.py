with open(r"C:\Users\dvasu\window-seat\punjab.js", "r", encoding="utf-8") as f:
    content = f.read()

stack = []
errors = []

for idx, char in enumerate(content):
    if char in "({[":
        stack.append((char, idx))
    elif char in ")}]":
        if not stack:
            errors.append(f"Unmatched closing {char} at char index {idx}")
            continue
        top_char, top_idx = stack.pop()
        # check match
        if (char == ")" and top_char != "(") or \
           (char == "}" and top_char != "{") or \
           (char == "]" and top_char != "["):
            errors.append(f"Mismatched {char} at char {idx} matching {top_char} at {top_idx}")

# Print remaining open stack
print(f"Errors found: {errors}")
print(f"Stack size at end: {len(stack)}")
for item in stack[-10:]:
    char, idx = item
    # get line number of index
    line_num = content[:idx].count("\n") + 1
    line_content = content[:idx].split("\n")[-1] + char + content[idx+1:].split("\n")[0]
    print(f"Open {char} on line {line_num}: {line_content.strip()}")
