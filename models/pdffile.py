from typing import List
from models.page import Page
from models.image import Image
from interfaces.pdffileloader import PDFFileLoader
from interfaces.orientationpredictor import OrientationPredictor

class PDFFile:
    def __init__(self, pages):
        self.__pages: List[Page] = pages
        # for page in self.__pages:
        #     print(f"Rotation : {page.rotation}")
    
    def predict_orientation(self, predictor: OrientationPredictor):
        for page in self.__pages:
            page.predict_orientation(predictor)

    @classmethod
    def of(cls, filename: str, loader: PDFFileLoader):
        dict_pages = loader.process(filename)
        pages = []
        for dpage in dict_pages:
            images = []
            for img in dpage['images']:
                images.append(Image(img))
            pages.append(Page(dpage['page_number'], dpage["rotation"], images))
        return PDFFile(pages)


