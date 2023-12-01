import cv2
import numpy as np

# YOLO modelinin ağırlıkları ve yapılandırma dosyasının yolu
yol_tanima_cfg = 'yol/to/your/yol.cfg'
yol_tanima_weights = 'yol/to/your/yol.weights'
siniflar = 'yol/to/your/classes.txt'

# YOLO modelini yükleme
yolo = cv2.dnn.readNet(yol_tanima_weights, yol_tanima_cfg)
classes = []
with open(siniflar, 'r') as f:
    classes = f.read().splitlines()

# Kamera yakalama
kamera = cv2.VideoCapture(0)  # Kamera numarası, genellikle 0 veya 1 olabilir

while True:
    ret, frame = kamera.read()

    # Görüntüyü boyutlandırma ve YOLO için hazırlama
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (320, 320), (0, 0, 0), True, crop=False)
    yolo.setInput(blob)
    output_layers_names = yolo.getUnconnectedOutLayersNames()
    layer_outputs = yolo.forward(output_layers_names)

    # Tespit edilen nesneleri çizme
    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.6:  # Güven eşiği (istenilen bir değer seçilebilir)
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Pencereye görüntüyü gösterme
    cv2.imshow('Nesne Tespiti', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kullanılan kaynakları serbest bırakma ve pencereyi kapatma
kamera.release()
cv2.destroyAllWindows()
