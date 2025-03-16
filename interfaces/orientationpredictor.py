from abc import ABC, abstractmethod

class OrientationPredictor(ABC): 
    
    @abstractmethod
    def process(self, raw_img):
        """Load an image from a given path"""
        pass
