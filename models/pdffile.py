from typing import List
from models.page import Page
from models.image import Image
from interfaces.pdffileloader import PDFFileLoader
from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor

class PDFFile:
    def __init__(self, pages):
        self.__pages: List[Page] = pages
        # for page in self.__pages:
        #     print(f"Rotation : {page.rotation}")
    
    def predict_orientation(self, predictor: OrientationPredictor):
        for page in self.__pages:
            page.predict_orientation(predictor)

    def predict_skew(self, predictor: SkewPredictor):
        for page in self.__pages:
            page.predict_skew(predictor)

    @classmethod
    def of(cls, filename: str, loader: PDFFileLoader):
        dict_pages = loader.process(filename)
        pages = []
        for dpage in dict_pages:
            img = Image(dpage['image'])
            pages.append(Page(dpage['page_number'], dpage["rotation"], img))
        return PDFFile(pages)
    
    def get_pages_orientations(self):
        pages_orientations = []
        for page in self.__pages:
            pages_orientations.append(page.get_predicted_orientation())
        return pages_orientations
    
    def get_pages_skew_orientations(self):
        pages_skew_orientations = []
        for page in self.__pages:
            pages_skew_orientations.append(page.get_predicted_skew_orientation())
        return pages_skew_orientations


