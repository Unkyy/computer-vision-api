import easyocr 
import cv2
from numpy import array

class OcrModel():
    """
    Initialize the reader with an image.

    Parameters:
     -image/frame: numpy array
     -languages: list of languages to use for OCR, default is ['en', 'it']
    """

    def __init__(self, gpu=False, languages=['fr', 'en']):
        self.reader = easyocr.Reader(languages, gpu=gpu)
        

    def read_text(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        adapted = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
        result = self.reader.readtext(gray)
        text = []
        boxes = []
        for detection in result:
            # print(detection)
            top_left = detection[0][0]
            bottom_right = detection[0][2]
            # print(top_left)
            text.append(detection[1])
            boxes.append([top_left,bottom_right])
            # print(detection[1])
            # print([top_left,bottom_right])
            # try:
            #     image = cv2.rectangle(image,top_left,bottom_right,(0,255,0),2)
            # except:
            #     continue
        return text,boxes

    def read_video(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return self.reader.readtext(gray)