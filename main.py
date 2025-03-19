import sys 
import os
from models.pdffile import PDFFile
from services.tesseractorientationpredictor import TesseractOrientationPredictor
from services.pdfplumberloader import PDFPlumberLoader
from services.cv2skewpredictor import CV2SkewPredictor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a PDF file path as an argument.")
        sys.exit(1)
    filename = sys.argv[1]
    pdfLoader = PDFPlumberLoader()
    pdf = PDFFile.of(filename, pdfLoader)
    #orientation_predictor = TesseractOrientationPredictor()
    #pdf.predict_orientation(orientation_predictor)
    skew_predictor = CV2SkewPredictor()
    pdf.predict_skew(skew_predictor)

