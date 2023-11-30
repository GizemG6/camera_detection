import cv2
import numpy as np
import tensorflow as tf

# TensorFlow modelinin yüklenmesi
model = tf.keras.applications.MobileNetV2(weights="imagenet", input_shape=(224, 224, 3))

# Modelin sınıf etiketlerinin yüklenmesi
class_labels = tf.keras.utils.get_file("ImageNetLabels.txt", "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt")
class_labels = np.array(open(class_labels).read().splitlines())

# Kamera veya video akışını açın
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü yeniden boyutlandırın ve model için hazırlayın
    input_frame = cv2.resize(frame, (224, 224))
    input_frame = tf.keras.applications.mobilenet_v2.preprocess_input(input_frame)
    input_frame = np.expand_dims(input_frame, axis=0)

    # Nesne sınıfını tahmin edin
    predictions = model.predict(input_frame)
    predicted_label = class_labels[np.argmax(predictions)]

    # Sonucu ekranda gösterin
    cv2.putText(frame, predicted_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
