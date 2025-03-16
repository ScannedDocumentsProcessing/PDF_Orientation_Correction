import pytesseract
from pytesseract import Output 

class TesseractOrientationPredictor[OrientationPredictor]:
    
    def process(self, raw_img):
        osd_result = pytesseract.image_to_osd(raw_img, output_type=Output.DICT)
        print(osd_result)
        return osd_result
