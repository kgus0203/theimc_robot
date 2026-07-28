#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


def wrap_angle(rad: float) -> float:
    return math.atan2(math.sin(rad), math.cos(rad))


def quaternion_to_yaw(q) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class OdomStraightChecker(Node):
    def __init__(self):
        super().__init__('odom_straight_checker')

        self.start_x = None
        self.start_y = None
        self.start_yaw = None
        self.last_print_sec = 0.0

        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info(
            'Waiting for /odom. Keep robot stopped first, then drive forward/backward only.'
        )

    def odom_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        yaw = quaternion_to_yaw(msg.pose.pose.orientation)

        now_sec = self.get_clock().now().nanoseconds / 1e9

        if self.start_x is None:
            self.start_x = x
            self.start_y = y
            self.start_yaw = yaw
            self.get_logger().info(
                f'Start saved: x={x:.3f}, y={y:.3f}, yaw={math.degrees(yaw):.2f} deg'
            )
            return

        dx = x - self.start_x
        dy = y - self.start_y

        # 시작 시점의 로봇 정면 방향 기준 이동량
        forward = (
            math.cos(self.start_yaw) * dx
            + math.sin(self.start_yaw) * dy
        )
        lateral = (
            -math.sin(self.start_yaw) * dx
            + math.cos(self.start_yaw) * dy
        )
        yaw_error_deg = math.degrees(wrap_angle(yaw - self.start_yaw))
        angular_z = msg.twist.twist.angular.z

        if now_sec - self.last_print_sec >= 0.2:
            self.last_print_sec = now_sec

            print(
                f'forward={forward:+.3f} m | '
                f'lateral={lateral:+.3f} m | '
                f'yaw_change={yaw_error_deg:+.2f} deg | '
                f'odom_wz={angular_z:+.3f} rad/s'
            )


def main():
    rclpy.init()
    node = OdomStraightChecker()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()