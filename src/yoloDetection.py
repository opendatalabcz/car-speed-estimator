import cv2
import numpy as np
import os

class object_detection:

    def __init__(self):
        location = os.path.realpath(os.path.join(os.getcwd()))
        print(location)
        self.net = cv2.dnn.readNet(location + "/config/yolov3.weights", location + "/config/yolov3.cfg")
        self.classes = []
        with open(location + "/config/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.outputlayers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_objects(self, img, confidence_lvl):
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.outputlayers)
        height, width, _ = img.shape

        # Showing information
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confidence_lvl:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        boxes_ret = []

        for i in indexes:
            label = str(self.classes[class_ids[int(i)]])
            if label != "car" and label != "truck" and label != "motorbike" and label != "bus":
                continue
            boxes_ret.append(boxes[int(i)])

        return img, boxes_ret

