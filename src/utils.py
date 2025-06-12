import sys 
import os
import json
from models.pdffile import PDFFile
from services.tesseractorientationpredictor import TesseractOrientationPredictor
from services.pdfplumberloader import PDFPlumberLoader
from services.cv2skewpredictor import CV2SkewPredictor


def parse_boolean_arg(argv, index, default):
    if len(argv) <= index:
        return default
    value = argv[index]
    lower = value.lower()
    if lower == 'true':
        return True
    if lower == 'false':
        return False
    print("Invalid boolean value:", value)
    sys.exit(1)


def get_true_labels_file_path(pdf_path):
    return os.path.join(pdf_path + '.json')


def get_pdf_filenames_for_evaluation(folder):
    '''
    Return the PDF filenames in folder that can be used for evaluation, i.e. they
    have a corresponding JSON file (which is expected to contain the labels)
    '''
    pdf_filenames = []

    for filename in os.listdir(folder):
        if not filename.endswith(".pdf"):
            continue
        pdf_path = os.path.join(folder, filename)
        labels_file_path = get_true_labels_file_path(pdf_path)
        if not os.path.isfile(labels_file_path):
            print(f'Missing labels file {labels_file_path}. Skipping the PDF file')
            continue
        pdf_filenames.append(pdf_path)

    return pdf_filenames


def load_true_labels_for_pdf(pdf_path):
    '''
    For a given PDF file path, return the corresponding JSON file path (which is expected to contain the labels)
    '''
    labels_file_path = get_true_labels_file_path(pdf_path)
    with open(labels_file_path) as file:
        return json.load(file)


