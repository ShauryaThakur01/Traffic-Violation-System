import cv2
import numpy as np
from plate.ocr import image_to_text
import os
cwd = os.getcwd()
print(cwd)

# Load YOLO model
net = cv2.dnn.readNet(os.path.join(cwd,"darknet-yolov3.cfg"),os.path.join(cwd, "lapi.weights"))

# Load COCO labels
with open(os.path.join(cwd,"classes.names", "r")) as f:
    classes = f.read().strip().split("\n")

# Load video file
video_file = 'aziz3.MP4'
cap = cv2.VideoCapture(video_file)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    frame = cv2.resize(frame,(1920,1080))
    # Get frame dimensions
    height, width = frame.shape[:2]

    # Preprocess the frame for the model
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Get output layer names
    layer_names = net.getUnconnectedOutLayersNames()

    # Run forward pass
    outs = net.forward(layer_names)

    # Initialize lists for detected objects, their bounding boxes, and confidence scores
    class_ids = []
    confidences = []
    boxes = []

    # Set a confidence threshold to filter out weak detections
    confidence_threshold = 0.8

    # Loop through the outputs and collect detected license plates
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                # Scale the bounding box coordinates to match the original frame size
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Apply non-maximum suppression to remove overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)

    # Draw bounding boxes and labels on the frame
    for i in indices:
        box = boxes[i]
        x, y, w, h = box
        plate_number = frame[y:y+h, x:x+w]  # Extract the license plate region
        plate_number = cv2.cvtColor(plate_number, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, plate_number = cv2.threshold(plate_number, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply threshold
        # pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        # custom_config = r'--oem 3 --psm 6'
        # plate_text = pytesseract.image_to_string(plate_number, config=custom_config)  # Use Tesseract OCR to recognize text
        # import re
        #
        # # Example of text cleaning
        # plate_text = re.sub('[^A-Z0-9]', '', plate_text)
        # print(plate_text)
        char = image_to_text.segment_characters(plate_number)
        plate_text= image_to_text.show_results(char)
        color = (0, 255, 0)  # Green color for bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"License Plate: {plate_text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the frame with license plate recognition
    cv2.imshow("License Plate Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
