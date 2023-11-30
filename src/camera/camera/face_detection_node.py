import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import String
import numpy as np

class FaceDetectionNode(Node):
    def __init__(self):
        super().__init__('face_detection_node')
        self.cap = cv2.VideoCapture(0)
        self.mycascade = cv2.CascadeClassifier('~/camera_package/camera_package/haarcascade_frontalface_default.xml')
        self.font1 = cv2.FONT_HERSHEY_SIMPLEX
        self.bridge = CvBridge()
        self.face_publisher = self.create_publisher(String, 'face_detection/status', 10)
        self.timer = self.create_timer(0.1, self.detect_face)

    def detect_face(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        pencils = self.mycascade.detectMultiScale(gray, 1.3, 7)
        face_detected = False
        for (x, y, w, h) in pencils:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "FACE", (x, y), self.font1, 1, (255, 0, 0), cv2.LINE_4)
            face_detected = True

        face_status_msg = String()
        if face_detected:
            face_status_msg.data = "Yüz algılandı!"
            print("selam")
        else:
            face_status_msg.data = "Yüz algılanamadı."
        self.face_publisher.publish(face_status_msg)

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    face_detection_node = FaceDetectionNode()
    try:
        rclpy.spin(face_detection_node)
    except KeyboardInterrupt:
        pass
    finally:
        face_detection_node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
