import cv2
import numpy as np

from interfaces.skewpredictor import SkewPredictor

class CV2SkewPredictor[SkewPredictor]:

    def __init__(self, display_images=False):
        self.display_images = display_images
    
    def image_with_lines(self, raw_img, lines):
        img = raw_img.copy()
        line_length = 500
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + line_length * (-b))
                y1 = int(y0 + line_length * (a))
                x2 = int(x0 - line_length * (-b))
                y2 = int(y0 - line_length * (a))
        
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        return img
    
    def image_with_linesP(self, raw_img, lines):
        img = raw_img.copy()
        angles = []
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        return img
    
    def display_image(self, raw_img):
        if not self.display_images:
            return
        cv2.imshow("Img", raw_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculate_angles(self, lines):
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                angle = (theta * 180 / np.pi) - 90 
                angles.append(angle)
        return np.array(angles)
    
    def calculate_anglesP(self, lines):
        angles = []
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                dx = x2 - x1
                dy = y2 - y1
                angle = np.arctan2(dy, dx) * 180 / np.pi  
                angles.append(angle)
        return np.array(angles)
    
    def lines_with_vertical_filter(self, lines, threshold):
        np_lines = np.array(lines)
        angles = np.zeros(lines.shape[0])
        if lines is not None:
            for i in range(lines.shape[0]):
                rho, theta = lines[i, 0]
                angles[i] = (theta * 180 / np.pi) - 90
            index = self.get_index_filtered_vertical_angles(angles, threshold)
            np_lines = np_lines[index]
        return np_lines
    
    def lines_with_vertical_filterP(self, lines, threshold):
        np_lines = np.array(lines)
        angles = np.zeros(lines.shape[0])
        if lines is not None:
            for i in range(lines.shape[0]):
                x1, y1, x2, y2 = lines[i, 0]
                dx = x2 - x1
                dy = y2 - y1
                angles[i] = np.arctan2(dy, dx) * 180 / np.pi
            index = self.get_index_filtered_vertical_angles(angles, threshold)
            np_lines = np_lines[index]
        return np_lines
            
    def get_index_filtered_vertical_angles(self, angles, threshold):
        arounde_0 = np.abs(angles - 0) < threshold
        around_180 = np.abs(angles - 180) < threshold
        filtered_angles = np.any([arounde_0, around_180], axis=0)
        return filtered_angles

    def filter_vertical_angles(self, angles, threshold=10):
        return np.array(angles)[self.get_index_filtered_vertical_angles(angles, threshold)]
    
        
    def process(self, raw_img): 
        # blurred = cv2.GaussianBlur(raw_img, (3, 3), 0)     
        # self.display_image(blurred)
        #self.display_image(raw_img)
        edges = cv2.Canny(raw_img, 50, 150, apertureSize=3, L2gradient=True)
        self.display_image(raw_img)

        #lines = cv2.HoughLines(edges, 1, np.pi / 180, 250)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=120, maxLineGap=10)
        img_with_lines = self.image_with_linesP(edges, lines)
        self.display_image(img_with_lines)

        lines_filtered = self.lines_with_vertical_filterP(lines, 10)
        img_with_lines = self.image_with_linesP(edges, lines_filtered)
        self.display_image(img_with_lines)

        angles = self.calculate_anglesP(lines)
        angles = self.filter_vertical_angles(angles, 10)

        if np.size(angles) > 0:
            return np.median(angles)
        else:
            return 0 
