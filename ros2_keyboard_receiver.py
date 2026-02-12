#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import can
import struct
import time

class SteeringReceiver(Node):

    def __init__(self):
        super().__init__('steering_receiver')

        # --- Steering parameters ---
        self.steering_angle = 0          # degrees
        self.step_size = 5               # 5° per press
        self.max_angle = 30              # safety limit

        # --- Setup CAN ---
        try:
            self.bus = can.interface.Bus(
                channel='can_usb0',
                bustype='socketcan',
                bitrate=500000
            )
            self.get_logger().info("CAN interface connected.")
        except Exception as e:
            self.get_logger().error(f"CAN connection failed: {e}")
            exit(1)

        # --- Activate steering relais ---
        self.activate_relais()

        # --- ROS2 subscriber ---
        self.subscription = self.create_subscription(
            Float64,
            '/keyboard_input',
            self.listener_callback,
            10
        )

        self.get_logger().info("Steering receiver node started.")

    # ------------------------------
    # Activate steering relais
    # ------------------------------
    def activate_relais(self):
        msg = can.Message(
            arbitration_id=0x16,
            data=[0x01, 0, 0, 0, 0, 0, 0, 0],
            is_extended_id=False
        )
        self.bus.send(msg)
        self.get_logger().info("Steering relais activated.")
        time.sleep(0.2)

    # ------------------------------
    # ROS2 callback
    # ------------------------------
    def listener_callback(self, msg):

        value = msg.data

        if value == 0.5:          # D key
            self.steering_angle += self.step_size

        elif value == -0.5:       # A key
            self.steering_angle -= self.step_size

        else:
            return

        # Clamp to limits
        self.steering_angle = max(
            min(self.steering_angle, self.max_angle),
            -self.max_angle
        )

        self.get_logger().info(
            f"New steering angle: {self.steering_angle}°"
        )

        self.send_steering_angle()

    # ------------------------------
    # Send steering angle via CAN
    # ------------------------------
    def send_steering_angle(self):

        # Factor 10 (as specified)
        angle_int = int(self.steering_angle * 10)

        # Convert to int16 little endian
        data_bytes = struct.pack('<h', angle_int)

        msg = can.Message(
            arbitration_id=0x17,
            data=[data_bytes[0], data_bytes[1], 0, 0, 0, 0, 0, 0],
            is_extended_id=False
        )

        try:
            self.bus.send(msg)
            self.get_logger().info("Steering command sent.")
        except can.CanError:
            self.get_logger().error("Failed to send CAN message.")


def main(args=None):
    rclpy.init(args=args)
    node = SteeringReceiver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
