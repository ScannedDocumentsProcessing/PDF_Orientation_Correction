import sys 
import utils
import predict
import numpy as np
import os
import json
from pathlib import Path
from models.pdffile import PDFFile
from services.pdfplumberloader import PDFPlumberLoader
from sklearn.metrics import mean_squared_error, confusion_matrix, classification_report, ConfusionMatrixDisplay


def evaluate_performance(true_labels, predictions):
    result = {}
    section = 'orientation'
    result[section] = {}
    result[section]['classification_report'] = classification_report(true_labels[section], predictions[section], zero_division=np.nan, output_dict=True)

    section = 'skew_orientation'
    result[section] = {}
    result[section]['mean_squared_error'] = mean_squared_error(true_labels[section], predictions[section])

    return result


def prepare_labels_and_predictions_dict(sections):
    result = {}
    for section in sections:
        result[section] = []
    return result


def append_to_dict(dict, values):
    for section in dict.keys():
        dict[section].extend(values[section])


def main():
    '''
    Evaluate orientation predictions on a folder containing a dataset of PDF files.
    Each PDF file must have a corresponding JSON file that contains the true labels.

    The JSON file must have the same name as the PDF file. For instance:
    - PDF file: scan.pdf
    - JSON file: scan.pdf.json

    True labels follow the same format as the predict.py result.
    Example for a file with 3 pages, first with 0° orientation,
    second with 180° orientation and third with 1.5° skew orientation:
    
    {
        'orientation': [0, 180, 0],
        'skew_orientation': [0.0, 0.0, 1.5]
    }
    '''

    if len(sys.argv) != 2:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate.py <dataset-folder>\n")
        sys.exit(1)
    folder = sys.argv[1]

    all_pdf_filenames = utils.get_pdf_filenames_for_evaluation(folder)
    pdfLoader = PDFPlumberLoader()

    predictions_experiments = ['orientation', 'skew_orientation']
    all_true_labels = prepare_labels_and_predictions_dict(predictions_experiments)
    all_predictions = prepare_labels_and_predictions_dict(predictions_experiments)

    # Load PDFs and perform predictions
    for filename in all_pdf_filenames:
        pdf = PDFFile.of(filename, pdfLoader)
        true_labels = utils.load_true_labels_for_pdf(filename)
        predictions = predict.perform_predictions(pdf, True, True, False)

        append_to_dict(all_true_labels, true_labels)
        append_to_dict(all_predictions, predictions)

    performance_report = evaluate_performance(all_predictions, all_true_labels)

    # Create folder and save performance report
    evaluation_folder = Path("evaluation")
    evaluation_folder.mkdir(exist_ok=True)

    orientation_labels = [0, 90, 180, 270]
    cm = confusion_matrix(true_labels['orientation'], predictions['orientation'], labels=orientation_labels)
    disp = ConfusionMatrixDisplay(cm, display_labels=orientation_labels)
    disp.plot().figure_.savefig(os.path.join(evaluation_folder, 'orientation_confusion_matrix.png'))

    with open(os.path.join(evaluation_folder, "performance.json"), "w") as file:
        json.dump(performance_report, file)
        print(f"Evaluation metrics files saved at {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
