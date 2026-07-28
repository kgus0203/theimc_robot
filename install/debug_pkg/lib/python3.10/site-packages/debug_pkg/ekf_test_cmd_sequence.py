#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class EkfTestCmdSequence(Node):
    def __init__(self):
        super().__init__('ekf_test_cmd_sequence')

        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('linear_speed', 0.08)
        self.declare_parameter('angular_speed', 0.25)
        self.declare_parameter('forward_sec', 15.0)
        self.declare_parameter('turn_sec', 12.57)
        self.declare_parameter('stop_sec', 2.0)
        self.declare_parameter('rate_hz', 20.0)
        self.declare_parameter('turn_direction', 1.0)

        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        linear_speed = float(self.get_parameter('linear_speed').value)
        angular_speed = float(self.get_parameter('angular_speed').value)
        forward_sec = float(self.get_parameter('forward_sec').value)
        turn_sec = float(self.get_parameter('turn_sec').value)
        stop_sec = float(self.get_parameter('stop_sec').value)
        rate_hz = float(self.get_parameter('rate_hz').value)
        turn_direction = float(self.get_parameter('turn_direction').value)

        if turn_direction >= 0.0:
            turn_direction = 1.0
        else:
            turn_direction = -1.0

        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.steps = [
            ('forward_out', forward_sec, linear_speed, 0.0),
            ('stop_after_forward', stop_sec, 0.0, 0.0),
            ('turn_180_out', turn_sec, 0.0, turn_direction * angular_speed),
            ('stop_after_turn_1', stop_sec, 0.0, 0.0),
            ('forward_back', forward_sec, linear_speed, 0.0),
            ('stop_after_return', stop_sec, 0.0, 0.0),
            ('turn_180_home', turn_sec, 0.0, turn_direction * angular_speed),
            ('final_stop', stop_sec, 0.0, 0.0),
        ]
        self.step_index = 0
        self.step_start_time = self.get_clock().now()
        self.done = False

        self.timer = self.create_timer(1.0 / rate_hz, self.on_timer)
        self.get_logger().info(
            'Publishing deterministic EKF test sequence to '
            f'{cmd_vel_topic}. forward_sec={forward_sec:.2f}, '
            f'turn_sec={turn_sec:.2f}, linear={linear_speed:.3f}, '
            f'angular={turn_direction * angular_speed:.3f}'
        )

    def publish_cmd(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.cmd_pub.publish(msg)

    def on_timer(self):
        if self.done:
            self.publish_cmd(0.0, 0.0)
            return

        now = self.get_clock().now()
        name, duration, linear_x, angular_z = self.steps[self.step_index]
        elapsed = (now - self.step_start_time).nanoseconds / 1e9

        if elapsed >= duration:
            self.step_index += 1
            self.step_start_time = now
            self.publish_cmd(0.0, 0.0)

            if self.step_index >= len(self.steps):
                self.done = True
                self.get_logger().info('EKF test command sequence finished.')
                return

            next_name = self.steps[self.step_index][0]
            self.get_logger().info(f'Next step: {next_name}')
            return

        self.publish_cmd(linear_x, angular_z)


def main():
    rclpy.init()
    node = EkfTestCmdSequence()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_cmd(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
