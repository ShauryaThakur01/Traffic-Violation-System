import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

video_path = 'test.mp4'
output_path = 'output_video.mp4'  # Path to save the output video

# YOLO configuration and weights
weights1_path = 'new/yolov3-obj_2400.weights'
configuration1_path = 'new/yolov3-obj.cfg'
probability_minimum = 0.7
threshold = 0.5

# Load YOLO network
network1 = cv2.dnn.readNetFromDarknet(configuration1_path, weights1_path)
layers_names1_all = network1.getLayerNames()
layers_names1_output = [layers_names1_all[i - 1] for i in network1.getUnconnectedOutLayers()]
labels1 = open('new/obj.names').read().strip().split('\n')

cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))
#out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    network1.setInput(blob)

    output_from_network1 = network1.forward(layers_names1_output)

    bounding_boxes1 = []
    confidences1 = []
    class_numbers1 = []

    for result in output_from_network1:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]
            if confidence_current > probability_minimum:
                box_current = detection[0:4] * np.array([w, h, w, h])
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes1.append([x_min, y_min, int(box_width), int(box_height)])
                confidences1.append(float(confidence_current))
                class_numbers1.append(class_current)

    results1 = cv2.dnn.NMSBoxes(bounding_boxes1, confidences1, probability_minimum, threshold)

    if len(results1) > 0:
        for i in results1.flatten():
            x_min, y_min = bounding_boxes1[i][0], bounding_boxes1[i][1]
            box_width, box_height = bounding_boxes1[i][2], bounding_boxes1[i][3]
            cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), (0, 255, 0), 5)
            text_box_current1 = '{}: {:.4f}'.format(labels1[int(class_numbers1[i])], confidences1[i])
            cv2.putText(frame, text_box_current1, (x_min, y_min - 7), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 5)
    cv2.imshow("w",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
