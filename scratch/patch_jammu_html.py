with open(r"C:\Users\dvasu\window-seat\jammu.html", "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split('<script src="/jammu.js?v=1.0"></script>')
if len(parts) > 1:
    modal_code = """  <!-- Diary Zoom Modal -->
  <div class="diary-zoom-card" id="diaryZoomCard">
    <button class="diary-close" id="closeDiary">&times;</button>
    <h2 style="margin-top: 0; color: #5c4033; font-family: 'Rozha One', serif; font-size: 26px; border-bottom: 2px dashed rgba(92,64,51,0.2); padding-bottom: 8px;">मिठड़ी बोली <span style="font-size:16px; font-weight:normal; display:block; color:#8b795e; margin-top:4px;">(डोगरें दी बोली)</span></h2>
    <p style="font-family: 'Hind', sans-serif; font-size: 14px; line-height: 1.6; color: #4a3b32; margin-top: 15px;">
      यह प्लेलिस्ट जम्मू की हसीन वादियों, तवी नदी के किनारे बहती ठंडी हवाओं और डोगरा संस्कृति के मीठे पारंपरिक सुरों को समर्पित है।
    </p>
    <div class="diary-poetry" style="font-style: italic; font-size: 16px; line-height: 1.6; margin-top: 15px; border-left: 3px solid #8b795e; padding-left: 12px; font-family: 'Hind', sans-serif; color: #5c4033;">
      "इर्खा ते गोह ओले पक्के हे,<br>
      जदूं घर कच्चे पर लोक सच्चे हे।"
    </div>
  </div>

  <script src="/jammu.js?v=1.0"></script>"""
  
    new_content = parts[0] + modal_code + parts[1]
    with open(r"C:\Users\dvasu\window-seat\jammu.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully patched jammu.html with the diary modal!")
else:
    print("WARNING: script tag not found in jammu.html!")
