from typing import List

from models.image import Image
from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor


class Page:
    def __init__(self, page_number, rotation, images):
        self.page_number: int = page_number
        self.rotation: int = rotation
        self.__images: List[Image] = images

    @property
    def images(self) -> List[Image]:
        return self.__images

    def predict_orientation(self, predictor: OrientationPredictor):
        for img in self.__images:
            img.predict_orientation(predictor)

    def predict_skew(self, predictor: SkewPredictor):
        for img in self.__images:
            img.predict_skew(predictor)
