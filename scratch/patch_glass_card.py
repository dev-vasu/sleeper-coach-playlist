import os

style_path = r"C:\Users\dvasu\window-seat\style.css"
print("Appending glassmorphic card overrides to style.css...")
with open(style_path, "r", encoding="utf-8") as f:
    style_content = f.read()

glass_card_css = """
/* Glassmorphic Card overrides for Room Themes (removing railway beige metal plaque) */
.route-punjab #timeOfDayCard,
.route-jammu #timeOfDayCard,
.route-english #timeOfDayCard {
  background: rgba(25, 25, 25, 0.45) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-radius: 10px !important;
  padding: 20px 18px !important;
  color: #fff !important;
}

/* Hide screws on room cards */
.route-punjab #timeOfDayCard .screw-head,
.route-jammu #timeOfDayCard .screw-head,
.route-english #timeOfDayCard .screw-head {
  display: none !important;
}

/* Label overrides for room cards */
.route-punjab #timeOfDayCard .control-label,
.route-jammu #timeOfDayCard .control-label,
.route-english #timeOfDayCard .control-label {
  color: rgba(255, 255, 255, 0.8) !important;
  text-shadow: none !important;
  font-size: 11px !important;
  letter-spacing: 1.5px !important;
  font-weight: 600 !important;
}
"""

if "/* Glassmorphic Card overrides for Room Themes" not in style_content:
    with open(style_path, "a", encoding="utf-8") as f:
        f.write(glass_card_css)
    print("Glass card CSS overrides successfully appended!")
else:
    print("Glass card CSS overrides already present.")
