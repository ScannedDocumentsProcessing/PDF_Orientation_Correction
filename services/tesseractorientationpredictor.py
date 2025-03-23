import pytesseract
from pytesseract import Output 

from interfaces.orientationpredictor import OrientationPredictor

class TesseractOrientationPredictor[OrientationPredictor]:
    
    def process(self, raw_img):
        osd_result = pytesseract.image_to_osd(raw_img, output_type=Output.DICT)
        result = {}
        result["orientation"] = osd_result['orientation']
        result["rotate"] = osd_result['rotate']
        return result
