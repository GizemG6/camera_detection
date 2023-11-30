import cv2
from ultralytics import YOLO
import pandas as pd


face_cascade = cv2.CascadeClassifier('src/camera/camera/cascade/haarcascade_frontalface_default.xml')
gzmModel = YOLO('/src/camera/camera/cascade/bestttt.pt')

# capture frames from a camera
cap = cv2.VideoCapture(0)

# reads frames from a camera
ret, frame = cap.read()

# convert to gray scale of each frames
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detects faces of different sizes in the input image
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

results = gzmModel.predict(frame)
a = results[0].boxes.data.cpu()
px = pd.DataFrame(a).astype("float")
for index, row in px.iterrows():
    x1 = int(row[0])
    y1 = int(row[1])
    x2 = int(row[2])
    y2 = int(row[3])
    d = int(row[5])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    if cv2.rectangle == True:
        print("selam guzellik")
    elif cv2.rectangle == False:
        if faces.any():
	        print("selam")
        


