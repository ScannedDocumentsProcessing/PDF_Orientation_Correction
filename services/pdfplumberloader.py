import pdfplumber
import cv2
import numpy as np
import sys
from interfaces.pdffileloader import PDFFileLoader

class PDFPlumberLoader[PDFFileLoader]:

    def process(self, filename: str):
        pages = []
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                if len(page.images) > 0:
                    images = []
                    for image_file_object in page.images:
                        nparr = np.fromstring(image_file_object["stream"].get_rawdata(), np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        images.append(img)
                    pages.append({"page_number": page.page_number, "rotation": page.rotation, "images": images})
                else:
                    print("This PDF file doesn't contain any image.")
                    sys.exit(1)
            pdf.close()
        return pages

