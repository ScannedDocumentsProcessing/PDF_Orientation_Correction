from typing import List

from models.image import Image
from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor

class Page:
    def __init__(self, page_number, rotation, image):
        self.page_number: int = page_number
        self.rotation: int = rotation
        self.__image = image
    
    def predict_orientation(self, predictor: OrientationPredictor):
        self.__image.predict_orientation(predictor)

    def predict_skew(self, predictor: SkewPredictor):
        self.__image.predict_skew(predictor)
    
    def get_predicted_orientation(self):
        return self.__image.get_predicted_orientation()
    
    def get_predicted_skew_orientation(self):
        return self.__image.get_predicted_skew_orientation()
