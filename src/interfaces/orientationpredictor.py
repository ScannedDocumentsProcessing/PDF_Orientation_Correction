from abc import ABC, abstractmethod

class OrientationPredictor(ABC): 
    
    @abstractmethod
    def process(self, raw_img):
        """Overrides this method to process a raw image correctly."""
        pass
