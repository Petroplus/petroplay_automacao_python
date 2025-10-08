import easyocr
import re
import cv2

class Find_plate_in_image_bgr:
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['pt', 'en'], gpu=False) 
        self.PLATE_REGEX = re.compile(r'\b([A-Z]{3}\d{4}|[A-Z]{3}\d[A-Z]\d{2})\b')

    def initialize(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        results = self.ocr_reader.readtext(img_rgb)
        candidates = []
        for bbox, text, prob in results:
            t = re.sub(r'[^A-Z0-9]', '', text.upper())
            m = self.PLATE_REGEX.search(t)
            if m:
                candidates.append((m.group(1), float(prob)))
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0] 