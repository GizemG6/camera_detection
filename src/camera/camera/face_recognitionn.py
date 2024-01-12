import face_recognition
import cv2

#known_imageGizem = face_recognition.load_image_file("/home/gizemgunes/ros2_ws/src/camera/camera/faces/gizo.jpg")
known_imageMehmet = face_recognition.load_image_file("/home/gizemgunes/ros2_ws/src/camera/camera/faces/gizo.jpg")
#known_encodingGizem = face_recognition.face_encodings(known_imageGizem)[0]
known_encodingMehmet = face_recognition.face_encodings(known_imageMehmet)[0]

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        #resultsG = face_recognition.compare_faces([known_encodingGizem], face_encodings[0])
        resultsM = face_recognition.compare_faces([known_encodingMehmet], face_encodings[0])
        #if resultsG[0]:
            #print("selam gizem")
        if resultsM[0]:
            print("selam mehmet")

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
