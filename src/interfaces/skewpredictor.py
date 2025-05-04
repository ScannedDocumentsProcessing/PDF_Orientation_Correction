from abc import ABC, abstractmethod


class SkewPredictor(ABC):

    @abstractmethod
    def process(self, raw_img):
        """Override this method to process a raw image correctly."""
        pass
