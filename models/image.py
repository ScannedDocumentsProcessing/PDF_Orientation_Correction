from interfaces.orientationpredictor import OrientationPredictor

class Image:
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.__orientation = 0
    
    def predict_orientation(self, predictor: OrientationPredictor):
        result_prediction = predictor.process(self.__raw_data)
        self.__orientation = result_prediction["orientation"]
        self.__rotate = result_prediction["rotate"]
