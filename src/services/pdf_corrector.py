import cv2
import numpy as np
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image as PILImage

class PDFCorrector:
    """
    Class to correct orientation and skew in PDF files
    """
    
    def correct_pdf(self, pdf_file, output_stream):
        """
        Takes a PDFFile object with predicted orientation and skew,
        corrects the images, and writes a new PDF to the output_stream
        
        Args:
            pdf_file: PDFFile object with predicted orientation and skew
            output_stream: BytesIO or file-like object to write the corrected PDF to
        """
        # Create a new PDF writer
        pdf_writer = PdfWriter()
        
        # Process each page
        for page in pdf_file._PDFFile__pages:  # Access private member
            # Create a new page for each corrected image
            for i, image in enumerate(page.images):
                # Get the orientation and skew angle
                orientation = image._Image__orientation  # Access private member
                skew_angle = image._Image__skew_orientation  # Access private member
                
                # Get the raw image data
                raw_img = image._Image__raw_data  # Access private member
                
                # Correct the image
                corrected_img = self._correct_image(raw_img, orientation, skew_angle)
                
                # Convert the corrected image to a PDF page
                img_pdf_bytes = self._image_to_pdf(corrected_img)
                
                # Read the image PDF and add it to the output PDF
                img_pdf_reader = PdfReader(BytesIO(img_pdf_bytes))
                pdf_writer.add_page(img_pdf_reader.pages[0])
        
        # Write the final PDF to the output stream
        pdf_writer.write(output_stream)
        output_stream.seek(0)
    
    def _correct_image(self, img, orientation, skew_angle):
        """
        Corrects the orientation and skew of an image
        
        Args:
            img: OpenCV image
            orientation: Orientation angle (0, 90, 180, 270)
            skew_angle: Skew angle in degrees
            
        Returns:
            Corrected OpenCV image
        """
        # Correct orientation (rotate by -orientation degrees)
        if orientation == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif orientation == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif orientation == 270:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
        # Correct skew
        if skew_angle != 0:
            # Get image dimensions
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            
            # Calculate rotation matrix
            M = cv2.getRotationMatrix2D(center, skew_angle, 1.0)
            
            # Calculate new dimensions
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))
            
            # Adjust the rotation matrix
            M[0, 2] += (new_w / 2) - center[0]
            M[1, 2] += (new_h / 2) - center[1]
            
            # Perform the rotation
            img = cv2.warpAffine(img, M, (new_w, new_h), flags=cv2.INTER_CUBIC, 
                                borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        
        return img
    
    def _image_to_pdf(self, img):
        """
        Converts an OpenCV image to a PDF file
        
        Args:
            img: OpenCV image
            
        Returns:
            PDF file as bytes
        """
        # Convert from BGR to RGB
        if len(img.shape) == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_img = PILImage.fromarray(img)
        
        # Save as PDF
        pdf_bytes = BytesIO()
        pil_img.save(pdf_bytes, format='PDF')
        
        return pdf_bytes.getvalue()
