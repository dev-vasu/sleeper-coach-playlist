with open(r"C:\Users\dvasu\window-seat\app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace double commas
fixed = content.replace(",,", ",")
# Wait, let's verify if there are any other double commas left
fixed = fixed.replace(",\n,", ",\n")

with open(r"C:\Users\dvasu\window-seat\app.js", "w", encoding="utf-8") as f:
    f.write(fixed)

print("Double commas fixed successfully!")
