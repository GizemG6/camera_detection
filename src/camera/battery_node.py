import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial


class BatteryStatusPublisher(Node):
    def __init__(self):
        super().__init__('battery_status_publisher')
        self.publisher_ = self.create_publisher(String, '/message_topic', 10)
        self.timer = self.create_timer(3.0, self.publish_battery_status)
        self.timer = self.create_timer(60.0, self.publish_average_battery_percentage)
        self.ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=10)
        self.battery_percentages = []  # keep an incoming voltage every 3 seconds on a list of 60 seconds
        self.time_elapsed = 0

    def publish_average_battery_percentage(self):
        self.time_elapsed += 1  # until 60 seconds
        if self.battery_percentages:
            average_percentage = sum(self.battery_percentages) / len(
                self.battery_percentages)  # calculate average percentage
            self.publish_battery_percentage(average_percentage)
            self.get_logger().info('Published average battery percentage: {:.2f}%'.format(average_percentage))
            self.battery_percentages = []  # reset list

    def publish_battery_status(self):
        raw_bytes = self.ser.readline()
        if raw_bytes:
            data = raw_bytes.decode('ascii').strip()
            try:
                current_voltage = float(data)
                min_battery_voltage = 22  # min voltage
                max_battery_voltage = 29.2  # max voltage

                battery_percentage = self.calculate_battery_percentage(current_voltage, min_battery_voltage,
                                                                       max_battery_voltage)
                self.battery_percentages.append(battery_percentage)
            except ValueError:
                self.get_logger().error('Invalid voltage data: {}'.format(data))

    def publish_battery_percentage(self, percentage):
        msg = String()
        msg.data = "{:.2f}%".format(percentage)
        self.publisher_.publish(msg)
        self.get_logger().info('Published battery percentage: %s' % msg.data)

    def calculate_battery_percentage(self, voltage, min_voltage, max_voltage):

        data = max(min_voltage, min(voltage, max_voltage))

        percentage = ((data - min_voltage) / (max_voltage - min_voltage)) * 100.0  # calculate percentage

        return percentage


def main(args=None):
    rclpy.init(args=args)
    battery_publisher = BatteryStatusPublisher()
    rclpy.spin(battery_publisher)
    battery_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
