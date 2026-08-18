import os

os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_enable_pir_in_executor"] = "0"

import cv2
import numpy as np
import logging
import paddle
from paddleocr import PaddleOCR

paddle.set_device('cpu')

logging.getLogger('ppocr').setLevel(logging.ERROR)

ocr_engine = PaddleOCR(
    use_angle_cls=True, 
    lang='en', 
    enable_mkldnn=False
)

def extract_text_from_image(image_bytes: bytes) -> str:
    if not image_bytes:
        return ""

    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return ""

        result = ocr_engine.ocr(img)
        extracted_text = []
        
        if result and len(result) > 0:
            first_page = result[0]
            
            if isinstance(first_page, dict) and 'rec_texts' in first_page:
                extracted_text = first_page['rec_texts']
                
            elif isinstance(first_page, list):
                lines_with_coords = []
                
                for line in first_page:
                    if isinstance(line, list) and len(line) > 1:
                        box = line[0]
                        text = line[1][0]
                        
                        top_left_x = box[0][0]
                        top_left_y = box[0][1]
                        
                        lines_with_coords.append({
                            "x": top_left_x,
                            "y": top_left_y,
                            "text": text
                        })
                
                y_tolerance = 15  
                lines_with_coords.sort(key=lambda item: (round(item['y'] / y_tolerance), item['x']))
                
                for item in lines_with_coords:
                    extracted_text.append(item["text"])
                
        return "\n".join(extracted_text)
    
    except Exception as e:
        print(f"PaddleOCR Extraction Error: {e}")
        return ""