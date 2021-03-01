import cv2
import numpy as np

class object_detection:

    def __init__(self):
        self.net = cv2.dnn.readNet("Data/yolov3.weights", "yolov3.cfg")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.classes = []
        with open("Data/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        layer_names = self.net.getLayerNames()
        self.outputlayers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def __distance(self, img_height, object_height):
        focal_lenght = 31
        sensor_size = focal_lenght/2.4
        r_height = 1470
        ret = (focal_lenght * r_height * img_height) / (sensor_size * object_height)
        return ret

    def detect_objects(self, img, confidence_lvl, count_distance):
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.outputlayers)
        height, width, channels = img.shape

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
        font = cv2.FONT_HERSHEY_PLAIN
        boxes_ret = []
        for i in indexes:
            x, y, w, h = boxes[int(i)]
            label = str(self.classes[class_ids[int(i)]])
            if label != "car" and label != "truck" and label != "motorbike" and label != "bus":
                continue

            boxes_ret.append(boxes[int(i)])
            if(count_distance):
                distance = self.__distance(height, h)
                label = label + " " + str(round(distance, 2))

#            color = self.colors[class_ids[int(i)]]
            color = (0, 0, 255)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
#            cv2.putText(img, label, (x, y - 10), font, 1.5, (0, 0, 150), 2)

        return img, boxes_ret

