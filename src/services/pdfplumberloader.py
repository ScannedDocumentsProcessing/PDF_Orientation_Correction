import pdfplumber
import cv2
import numpy as np
from io import BytesIO
from interfaces.pdffileloader import PDFFileLoader


class PDFPlumberLoader(PDFFileLoader):

    def process(self, filename):
        pages = []
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                if len(page.images) > 0:
                    images = []
                    for image_file_object in page.images:
                        try:
                            nparr = np.fromstring(image_file_object["stream"].get_rawdata(), np.uint8)
                            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            if img is None:
                                print(f"Warning: Failed to decode image on page {page.page_number}")
                                continue  # Skip invalid images
                            images.append(img)
                        except Exception as e:
                            print(f"Error decoding image on page {page.page_number}: {str(e)}")
                            continue
                    if images:  # Only add the page if there are valid images
                        pages.append({"page_number": page.page_number, "rotation": page.rotation, "images": images})
            pdf.close()
        if not pages:
            raise ValueError("The PDF file does not contain any valid images.")
        return pages

    def processBytes(self, pdf_data: bytes):
        return self.process(BytesIO(pdf_data))
        
