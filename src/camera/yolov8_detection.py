import cv2
import torch
import numpy as np

# YOLOv8 modelini yükle
model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='path/to/your/best.pt', force_reload=True)

# Kamerayı aç
cap = cv2.VideoCapture(0)  # 0, varsayılan kamera için

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # OpenCV ile aldığımız görüntüyü PyTorch tensörüne dönüştür
    img = torch.from_numpy(frame).permute(2, 0, 1).float().div(255.0).unsqueeze(0)

    # YOLOv8 modeline görüntüyü besle ve nesneleri tespit et
    results = model(img)

    # Tespit edilen nesneleri al
    detections = results.xyxy[0]

    # Her nesneyi görsel olarak işaretle
    for det in detections:
        bbox = det[0:4].cpu().numpy().astype(int)
        label = int(det[5])
        conf = float(det[4])

        if conf > 0.5:  # Confidence threshold ayarlayabilirsiniz
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"Class: {label}, Confidence: {conf:.2f}", (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Görüntüyü göster
    cv2.imshow('YOLOv8 Object Detection', frame)

    # 'q' tuşuna basılınca döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı kapat ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
