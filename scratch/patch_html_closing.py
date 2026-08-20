with open(r"C:\Users\dvasu\window-seat\punjab.html", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure it ends cleanly with the script, body, and html tags
parts = content.split('<!-- Diary Zoom Modal -->')
if len(parts) > 1:
    diary_content = """<!-- Diary Zoom Modal -->
  <div class="diary-zoom-card" id="diaryZoomCard">
    <button class="diary-close" id="closeDiary">&times;</button>
    <h2 style="margin-top: 0; color: #5c4033; font-family: 'Rozha One', serif; font-size: 26px; border-bottom: 2px dashed rgba(92,64,51,0.2); padding-bottom: 8px;">सदा-ए-हिज्र <span style="font-size:16px; font-weight:normal; display:block; color:#8b795e; margin-top:4px;">(पंजाब दी हूक)</span></h2>
    <p style="font-family: 'Hind', sans-serif; font-size: 14px; line-height: 1.6; color: #4a3b32; margin-top: 15px;">
      यह संगीत केवल सुर और ताल नहीं है... यह उन टूटे हुए दिलों की दास्ताँ है जो पंजाब की मिट्टी से उपजी है। गुरदास मान के 'छल्ला' की तड़प से लेकर पुराने देहाती लोक गीतों के दर्द तक, यह सफ़र गुज़रे ज़माने की यादों और बिछड़े हुए साजन की दास्ताँ बयान करता है।
    </p>
    <div class="diary-poetry" style="font-style: italic; font-size: 16px; line-height: 1.6; margin-top: 15px; border-left: 3px solid #8b795e; padding-left: 12px; font-family: 'Hind', sans-serif; color: #5c4033;">
      "लिख लिख चिट्ठियां यार वल्ल पावां,<br>
      भेजां दस्तख़त कर के,<br>
      इक हिज्र तवे ते रोटी वांगूं,<br>
      लूह गया जीवे मर के..."
    </div>
  </div>

  <script src="/punjab.js?v=1.0"></script>
</body>
</html>"""

    new_content = parts[0] + diary_content
    with open(r"C:\Users\dvasu\window-seat\punjab.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully corrected closing tags of punjab.html!")
else:
    print("Diary Zoom Modal tag not found, performing end injection")
    # find the last </div> and inject
    parts = content.split('  </div>\n\n\n')
    new_content = parts[0] + '  </div>\n' + diary_content
    with open(r"C:\Users\dvasu\window-seat\punjab.html", "w", encoding="utf-8") as f:
         f.write(new_content)
    print("Injected tags at end!")
