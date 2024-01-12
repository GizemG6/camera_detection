import rclpy
from sensor_msgs.msg import PointCloud2
import pcl

def callback(msg):
    # Nokta bulutu verilerini işleme
    cloud = pcl.PointCloud()
    points = [[x, y, z] for x, y, z, i in zip(*[iter(msg.data)] * 4)]
    cloud.from_list(points)

    # Engel tespiti veya diğer işlemler burada yapılabilir
    # Örneğin:
    seg = cloud.make_segmenter()
    seg.set_optimize_coefficients(True)
    # ... (engel tespiti veya diğer işlemler için ayarlamalar)

def main():
    rclpy.init()
    node = rclpy.create_node('obstacle_detection_node')

    # /camera/point_cloud_xyz topic'ini dinleme
    subscription = node.create_subscription(
        PointCloud2,
        '/camera/point_cloud_xyz',
        callback,
        10  # Queue size
    )

    # Ana döngüyü başlatma
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # ROS2 kapatma
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
