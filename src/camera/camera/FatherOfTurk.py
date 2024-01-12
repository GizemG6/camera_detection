import face_recognition
import cv2
import pygame
import threading

known_image = face_recognition.load_image_file("/home/gizemgunes/ros2_ws/src/camera/camera/faces/mustafa-kemal-ataturk.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

video_capture = cv2.VideoCapture(2)
#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
pygame.init()
music_path = "/home/gizemgunes/ros2_ws/src/camera/camera/music/hosgelislerola.mp3"
pygame.mixer.music.load(music_path)

#def face_recognition_thread():
while True:
    ret, frame = video_capture.read()
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        results = face_recognition.compare_faces([known_encoding], face_encodings[0])
        if results[0]:
            # print("Selamün aleyküm ve rahmetullah ve berekatüh Mehmet Kemal bin Cevat El Manyasi Efendi hazretleri")
            # print("selam murat")
            print("Father Of Turks")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            # else:
            # print("Tanıdık bir yüz bulunamadı.")

#def capture_thread():
#while True:
    #ret, frame = video_capture.read()
    #if ret:
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#recognition_thread = threading.Thread(target=face_recognition_thread)
#recognition_thread.start()

#capture_thread = threading.Thread(target=capture_thread)
#capture_thread.start()

video_capture.release()
cv2.destroyAllWindows()
