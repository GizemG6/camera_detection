import face_recognition
import os

# Eğitim veri setinin yolu
training_dir = "/home/gizemgunes/ros2_ws/src/camera/camera/Atatürk"

# Eğitim veri setini yükle
known_faces = []
known_names = []

for filename in os.listdir(training_dir):
    if filename.endswith(".jpg"):
        image = face_recognition.load_image_file(os.path.join(training_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(filename.split('.')[0])  # Dosya adını kullanıcı adı olarak ekle

# Modeli eğit
face_recognition_model = face_recognition.api.face_recognition_model_v1(known_faces, tolerance=0.6)

# Eğitim sonrası modeli kaydet
face_recognition_model.save("ataturk_model.clf")
