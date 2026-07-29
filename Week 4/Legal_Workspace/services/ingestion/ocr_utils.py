import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)

def extract_text_from_image(image_bytes: bytes) -> str:
    if not image_bytes:
        return ""

    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return ""

        result = ocr_engine.ocr(img, cls=True)
        
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                extracted_text.append(text)
                
        return "\n".join(extracted_text)
    
    except Exception as e:
        print(f"PaddleOCR Extraction Error: {e}")
        return ""