import re
import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np

class CvModel:
    
    # Based on https://github.com/tensorflow/examples/blob/master/lite/examples/object_detection/raspberry_pi/README.md
    def __init__(self):
        
      self.self.CAMERA_WIDTH = 640
      self.self.CAMERA_HEIGHT = 480
    def load_labels(path='labels.txt'):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels

    def set_input_tensor(interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = np.expand_dims((image-255)/255, axis=0)


    def get_output_tensor(interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor


    def detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()
        # Get all output details
        boxes = self.get_output_tensor(interpreter, 0)
        classes = self.get_output_tensor(interpreter, 1)
        scores = self.get_output_tensor(interpreter, 2)
        count = int(self.get_output_tensor(interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results

    def read_object(self,image):
        labels = self.load_labels()
        interpreter = Interpreter('detect.tflite')
        interpreter.allocate_tensors()
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

        # cap = cv2.VideoCapture(0)
        # while cap.isOpened():
        #     ret, frame = cap.read()
        img = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (input_height,input_width))
        res = self.detect_objects(interpreter, img, 0.8)

        for result in res:
            ymin, xmin, ymax, xmax = result['bounding_box']
            xmin = int(max(1,xmin * self.CAMERA_WIDTH))
            xmax = int(min(self.CAMERA_WIDTH, xmax * self.CAMERA_WIDTH))
            ymin = int(max(1, ymin * self.CAMERA_HEIGHT))
            ymax = int(min(self.CAMERA_HEIGHT, ymax * self.CAMERA_HEIGHT))
        print(res)
            #     cv2.rectangle(frame,(xmin, ymin),(xmax, ymax),(0,255,0),3)
            #     cv2.putText(frame,labels[int(result['class_id'])],(xmin, min(ymax, self.CAMERA_HEIGHT-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA) 

            # cv2.imshow('Pi Feed', frame)
        return 0,0
            # if cv2.waitKey(10) & 0xFF ==ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()

