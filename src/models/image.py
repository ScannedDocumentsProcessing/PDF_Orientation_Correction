from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor


class Image:
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.__orientation = 0
        self.__skew_orientation = 0
        self.__rotate = 0

    @property
    def skew_angle(self) -> float:
        return self.__skew_orientation

    def predict_orientation(self, predictor: OrientationPredictor):
        result_prediction = predictor.process(self.__raw_data)
        self.__orientation = result_prediction["orientation"]
        self.__rotate = result_prediction["rotate"]

    def predict_skew(self, predictor: SkewPredictor):
        self.__skew_orientation = predictor.process(self.__raw_data)