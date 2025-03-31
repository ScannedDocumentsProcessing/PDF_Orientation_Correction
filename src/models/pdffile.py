from typing import List
from models.page import Page
from models.image import Image
from interfaces.pdffileloader import PDFFileLoader
from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor
import json

class PDFFile:
    def __init__(self, pages):
        self.__pages: List[Page] = pages
    
    def predict_orientation(self, predictor: OrientationPredictor):
        for page in self.__pages:
            page.predict_orientation(predictor)

    def predict_skew(self, predictor: SkewPredictor):
        for page in self.__pages:
            page.predict_skew(predictor)

    @classmethod
    def of(cls, pdf_data: bytes, loader: PDFFileLoader):
        dict_pages = loader.process(pdf_data)  # Pass bytes to the loader
        pages = []
        for dpage in dict_pages:
            images = []
            for img in dpage['images']:
                images.append(Image(img))
            pages.append(Page(dpage['page_number'], dpage["rotation"], images))
        return PDFFile(pages)

    def to_json(self):
        if not self.__pages:
            return json.dumps({"result": "No images found in PDF"})
        result = []
        for page in self.__pages:
            page_data = {
                "page_number": page.page_number,
                "rotation": page.rotation,
                "skew_angles": [img.skew_angle for img in page.images]
            }
            result.append(page_data)
        return json.dumps(result)