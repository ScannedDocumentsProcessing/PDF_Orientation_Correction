from interfaces.orientationpredictor import OrientationPredictor
from interfaces.skewpredictor import SkewPredictor

class Image:
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.__orientation = 0
        self.__skew_orientation = 0
    
    def predict_orientation(self, predictor: OrientationPredictor):
        result_prediction = predictor.process(self.__raw_data)
        self.__orientation = result_prediction["orientation"]
        self.__rotate = result_prediction["rotate"]

    def predict_skew(self, predictor: SkewPredictor):
        self.__skew_orientation = float(predictor.process(self.__raw_data))
    
    def get_predicted_orientation(self):
        return self.__orientation
    
    def get_predicted_skew_orientation(self):
        return self.__skew_orientation