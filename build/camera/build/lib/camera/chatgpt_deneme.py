# my_camera_pkg/my_camera_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher = self.create_publisher(Image, 'camera/image', 10)
        self.timer = self.create_timer(1.0, self.publish_image)
        self.bridge = CvBridge()

    def publish_image(self):
        # Rastgele bir görüntü oluştur
        image = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8)

        # Görüntüyü ROS 2 Image mesajına dönüştür
        image_msg = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")

        # Görüntüyü yayınla
        self.publisher.publish(image_msg)
        self.get_logger().info("Görüntü yayını yapıldı")


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
