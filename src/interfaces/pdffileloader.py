from abc import ABC, abstractmethod


class PDFFileLoader(ABC):

    @abstractmethod
    def process(self, filename: str):
        """Override this method with proper PDFFileLoader"""
        pass
