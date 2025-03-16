from interfaces.orientationpredictor import OrientationPredictor

class Image:
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.__orientation_prediction = 0
    
    def predict_orientation(self, predictor: OrientationPredictor):
        self.__orientation_prediction = predictor.process(self.__raw_data)
