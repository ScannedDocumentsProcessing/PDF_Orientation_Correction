import sys 
import utils
from models.pdffile import PDFFile
from services.tesseractorientationpredictor import TesseractOrientationPredictor
from services.pdfplumberloader import PDFPlumberLoader
from services.cv2skewpredictor import CV2SkewPredictor


def perform_predictions(pdf, predict_orientation, predict_skew, display_images):
    result = {}

    if predict_orientation:
        orientation_predictor = TesseractOrientationPredictor()
        pdf.predict_orientation(orientation_predictor)
        result['orientation'] = pdf.get_pages_orientations()

    if predict_skew:
        skew_predictor = CV2SkewPredictor(display_images)
        pdf.predict_skew(skew_predictor)
        result['skew_orientation'] = pdf.get_pages_skew_orientations()
    
    return result


def main():
    '''
    Predict orientation on a single PDF file.
    Print the prediction as a JSON.

    Example for a file with 3 pages, first with 0° orientation,
    second with 180° orientation and third with 1.5° skew orientation:
    
    {
        'orientation': [0, 180, 0],
        'skew_orientation': [0.0, 0.0, 1.5]
    }
    '''

    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print("Arguments error. Usage:\n")
        print("\tpython3 predict.py <pdf-file> [predict_orientation] [predict_skew] [display_images]\n")
        sys.exit(1)
    filename = sys.argv[1]
    predict_orientation = utils.parse_boolean_arg(sys.argv, 2, True)
    predict_skew = utils.parse_boolean_arg(sys.argv, 3, True)
    display_images = utils.parse_boolean_arg(sys.argv, 4, False)

    pdfLoader = PDFPlumberLoader()
    pdf = PDFFile.of(filename, pdfLoader)
    print(perform_predictions(pdf, predict_orientation, predict_skew, display_images))


if __name__ == "__main__":
    main()
