import cv2
from ultralytics import YOLO

model = YOLO('/home/gizemgunes/ros2_ws/src/camera/camera/cascade/best.pt')

# capture frames from a camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # predict objects in the frame
    results = model.predict(frame)

    # Ensure there are detections available
    if len(results) > 0 and results[0].boxes is not None:
        boxes = results[0].boxes.xyxy[0]  # Accessing bounding box information

        for box in boxes:
            x1, y1, x2, y2, conf, cls = box.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Press 'q' to exit loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
