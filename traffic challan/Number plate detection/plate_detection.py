import cv2
import numpy as np
from plate.ocr import image_to_text
import os
cwd = os.getcwd()
print(cwd)
net = cv2.dnn.readNet(os.path.join(cwd,"plate\\darknet-yolov3.cfg"), os.path.join(cwd,"plate\\lapi.weights"))

    # Load COCO labels
with open (os.path.join(cwd,"plate\\classes.names") ,"r")as f:
    classes = f.read().strip().split("\n")
# Load YOLO model
def detect(frame):
    frame = cv2.resize(frame,(1920,1080))
    # Get frame dimensions
    height, width = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    layer_names = net.getUnconnectedOutLayersNames()

    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    confidence_threshold = 0.8

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)

    # Draw bounding boxes and labels on the frame
    for i in indices:
        box = boxes[i]
        x, y, w, h = box
        plate_number = frame[y:y+h, x:x+w]  # Extract the license plate region
        plate_number = cv2.cvtColor(plate_number, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, plate_number = cv2.threshold(plate_number, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply threshold
        char = image_to_text.segment_characters(plate_number)
        plate_text= image_to_text.show_results(char)
        return plate_text
    return None
