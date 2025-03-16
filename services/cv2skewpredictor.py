import cv2
import numpy as np

from interfaces.skewpredictor import SkewPredictor

class CV2SkewPredictor[SkewPredictor]:
    
    def image_with_lines(self, raw_img, lines):
        img = raw_img.copy()
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
        
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
        return img
    
    def image_with_linesP(self, raw_img, lines):
        img = raw_img.copy()
        angles = []
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
        return img
    
    def display_image(self, raw_img):
        cv2.imshow("Img", raw_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculate_angles(self, lines):
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                angle = (theta * 180 / np.pi) - 90 
                angles.append(angle)
        return angles
    
    def calculate_anglesP(self, lines):
        angles = []
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                dx = x2 - x1
                dy = y2 - y1
                angle = np.arctan2(dy, dx) * 180 / np.pi  
                angles.append(angle)
        return angles

    def process(self, raw_img): 
        # blurred = cv2.GaussianBlur(raw_img, (3, 3), 0)     
        # self.display_image(blurred)
        #self.display_image(raw_img)
        edges = cv2.Canny(raw_img, 50, 150, apertureSize=3, L2gradient=True)
        self.display_image(edges)

        # lines = cv2.HoughLines(edges, 1, np.pi / 180, 300)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=120, maxLineGap=10)
        img_with_lines = self.image_with_linesP(edges, lines)
        self.display_image(img_with_lines)

        angles = self.calculate_anglesP(lines)
        print(angles)

        if angles:
            avg_angle = np.median(angles)
            return avg_angle
        else:
            return 0 
