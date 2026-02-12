ROS2 Steering Control Prototype

This project demonstrates a simple ROS2-based drive-by-wire steering prototype.

A MATLAB node publishes keyboard inputs to the /keyboard_input topic.
A Python ROS2 node subscribes to this topic and sends steering angle commands via CAN (SocketCAN) to the vehicle.

Requirements

ROS2

Python 3

python-can

MATLAB with ROS2 Toolbox

CAN interface (500 kbit/s)

Usage

Enable CAN interface.

Run steering_receiver.py.

Start keyboard_to_ros2.m in MATLAB.

Use A/D keys to steer.

⚠ For research and controlled testing only.
