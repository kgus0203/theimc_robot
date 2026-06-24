import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from interfaces_pkg.msg import RailInfo


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def approach(current, target, step):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return target


class RailPDControllerNode(Node):
    def __init__(self):
        super().__init__('rail_pd_controller_node')

        self.reverse_heading_locked = False
        self.reverse_locked_angular = 0.0
        
        self.declare_parameter('rail_info_topic', '/rail_info')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_rail')
        self.declare_parameter('control_hz', 20.0)
        self.declare_parameter('enable_control', True)

        # gains
        self.declare_parameter('kp_x', 0.18)
        self.declare_parameter('kd_x', 0.004)
        self.declare_parameter('kp_angle', 0.26)
        self.declare_parameter('kd_angle', 0.006)

        # deadband
        self.declare_parameter('x_deadband', 0.04)
        self.declare_parameter('angle_deadband', 0.03)

        # smoothing
        self.declare_parameter('x_alpha', 0.35)
        self.declare_parameter('angle_alpha', 0.35)

        # speed limits
        self.declare_parameter('max_linear', 0.06)
        self.declare_parameter('max_angular', 0.10)
        self.declare_parameter('min_forward_speed', 0.04)
        self.declare_parameter('min_angular_speed', 0.02)

        # base speeds
        self.declare_parameter('far_speed', 0.055)
        self.declare_parameter('middle_speed', 0.045)
        self.declare_parameter('near_speed', 0.035)

        # ramp
        self.declare_parameter('linear_acc_step', 0.008)
        self.declare_parameter('angular_acc_step', 0.012)
        self.declare_parameter('linear_decay_step', 0.002)
        self.declare_parameter('angular_decay_step', 0.015)

        # timeouts
        self.declare_parameter('hold_timeout', 1.0)
        self.declare_parameter('perception_timeout', 2.0)

        # reverse logic
        self.declare_parameter('reverse_speed', 0.10)
        self.declare_parameter('near_reverse_x_threshold', 0.14)
        self.declare_parameter('near_reverse_angle_threshold', 0.08)
        self.declare_parameter('near_stop_x_threshold', 0.1)
        self.declare_parameter('near_stop_angle_threshold', 0.08)

        # reverse safety
        self.declare_parameter('reverse_min_time', 0.7)
        self.declare_parameter('reverse_max_time', 20.0)

        self.declare_parameter('debug_log', True)

        rail_info_topic = self.get_parameter('rail_info_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        control_hz = float(self.get_parameter('control_hz').value)

        self.enable_control = bool(self.get_parameter('enable_control').value)

        self.kp_x = float(self.get_parameter('kp_x').value)
        self.kd_x = float(self.get_parameter('kd_x').value)
        self.kp_angle = float(self.get_parameter('kp_angle').value)
        self.kd_angle = float(self.get_parameter('kd_angle').value)

        self.x_deadband = float(self.get_parameter('x_deadband').value)
        self.angle_deadband = float(self.get_parameter('angle_deadband').value)

        self.x_alpha = float(self.get_parameter('x_alpha').value)
        self.angle_alpha = float(self.get_parameter('angle_alpha').value)

        self.max_linear = float(self.get_parameter('max_linear').value)
        self.max_angular = float(self.get_parameter('max_angular').value)
        self.min_forward_speed = float(self.get_parameter('min_forward_speed').value)
        self.min_angular_speed = float(self.get_parameter('min_angular_speed').value)

        self.far_speed = float(self.get_parameter('far_speed').value)
        self.middle_speed = float(self.get_parameter('middle_speed').value)
        self.near_speed = float(self.get_parameter('near_speed').value)

        self.linear_acc_step = float(self.get_parameter('linear_acc_step').value)
        self.angular_acc_step = float(self.get_parameter('angular_acc_step').value)
        self.linear_decay_step = float(self.get_parameter('linear_decay_step').value)
        self.angular_decay_step = float(self.get_parameter('angular_decay_step').value)

        self.hold_timeout = float(self.get_parameter('hold_timeout').value)
        self.perception_timeout = float(self.get_parameter('perception_timeout').value)

        self.reverse_speed = float(self.get_parameter('reverse_speed').value)
        self.near_reverse_x_threshold = float(self.get_parameter('near_reverse_x_threshold').value)
        self.near_reverse_angle_threshold = float(self.get_parameter('near_reverse_angle_threshold').value)
        self.near_stop_x_threshold = float(self.get_parameter('near_stop_x_threshold').value)
        self.near_stop_angle_threshold = float(self.get_parameter('near_stop_angle_threshold').value)

        self.reverse_min_time = float(self.get_parameter('reverse_min_time').value)
        self.reverse_max_time = float(self.get_parameter('reverse_max_time').value)

        self.debug_log = bool(self.get_parameter('debug_log').value)

        self.rail_info_sub = self.create_subscription(
            RailInfo, rail_info_topic, self.rail_info_callback, 10
        )
        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.timer = self.create_timer(1.0 / control_hz, self.control_loop)

        self.last_rail_info = None
        self.last_rail_info_time = None

        self.prev_x_error = 0.0
        self.prev_angle_error = 0.0
        self.prev_time = None

        self.filtered_x_error = 0.0
        self.filtered_angle_error = 0.0

        self.current_linear = 0.0
        self.current_angular = 0.0

        self.reverse_align_mode = False
        self.reverse_start_time = None

        self.stopped_at_goal = False

        self.get_logger().info('RailPDControllerNode started')

    def rail_info_callback(self, msg: RailInfo):
        self.last_rail_info = msg
        self.last_rail_info_time = time.time()

    def control_loop(self):
        if not self.enable_control:
            self.soft_stop()
            return

        if self.last_rail_info is None or self.last_rail_info_time is None:
            self.soft_stop()
            return

        now = time.time()
        age = now - self.last_rail_info_time
        msg = self.last_rail_info

        if age > self.perception_timeout:
            self.soft_stop()
            return

        if not msg.has_rail:
            self.soft_stop()
            return

        if age > self.hold_timeout:
            self.hold_and_stabilize()
            return

        if self.prev_time is None:
            dt = 0.05
        else:
            dt = max(now - self.prev_time, 1e-3)
        self.prev_time = now

        img_half_width = max(float(msg.img_width) / 2.0, 1.0)

        raw_x_error = (float(msg.img_cx) - float(msg.rail_cx)) / img_half_width
        raw_angle_error = float(msg.angle_deg) / 25.0

        self.filtered_x_error = (1.0 - self.x_alpha) * self.filtered_x_error + self.x_alpha * raw_x_error
        self.filtered_angle_error = (1.0 - self.angle_alpha) * self.filtered_angle_error + self.angle_alpha * raw_angle_error

        x_error = self.filtered_x_error
        angle_error = self.filtered_angle_error

        if abs(x_error) < self.x_deadband:
            x_error = 0.0
        if abs(angle_error) < self.angle_deadband:
            angle_error = 0.0

        dx = (x_error - self.prev_x_error) / dt
        dangle = (angle_error - self.prev_angle_error) / dt

        self.prev_x_error = x_error
        self.prev_angle_error = angle_error

        # 목표 정지 latch
        if (
            msg.distance == 'near' and
            abs(x_error) < self.near_stop_x_threshold and
            abs(angle_error) < self.near_stop_angle_threshold and
            (not self.reverse_align_mode)
        ):
            self.stopped_at_goal = True

        if self.stopped_at_goal:
            self.current_linear = 0.0
            self.current_angular = 0.0
            self.publish_current()

            if self.debug_log:
                self.get_logger().info(
                    f'[STOP_OK] dist={msg.distance} x_err={x_error:.3f} ang_err={angle_error:.3f}'
                )
            return

        # distance별 gain
        if msg.distance == 'near':
            kp_x_use = self.kp_x * 0.9
            kd_x_use = self.kd_x
            kp_angle_use = self.kp_angle * 1.2
            kd_angle_use = self.kd_angle
            max_angular_use = min(self.max_angular, 0.08)
        elif msg.distance == 'middle':
            kp_x_use = self.kp_x
            kd_x_use = self.kd_x
            kp_angle_use = self.kp_angle
            kd_angle_use = self.kd_angle
            max_angular_use = self.max_angular
        else:
            kp_x_use = self.kp_x
            kd_x_use = self.kd_x
            kp_angle_use = self.kp_angle * 0.9
            kd_angle_use = self.kd_angle
            max_angular_use = self.max_angular

        target_angular = (
            kp_x_use * x_error +
            kd_x_use * dx +
            kp_angle_use * angle_error +
            kd_angle_use * dangle
        )
        target_angular = clamp(target_angular, -max_angular_use, max_angular_use)

        if abs(angle_error) < 0.04 and abs(x_error) < 0.03:
            target_angular = 0.0

        if (abs(x_error) > 0.08 or abs(angle_error) > 0.08) and abs(target_angular) > 1e-4:
            if target_angular > 0.0:
                target_angular = max(target_angular, self.min_angular_speed)
            else:
                target_angular = min(target_angular, -self.min_angular_speed)

        # 후진 시작: near에서 많이 틀어졌을 때
        if (
            (not self.reverse_align_mode) and
            msg.distance == 'near' and
            (
                abs(x_error) > self.near_reverse_x_threshold or
                abs(angle_error) > self.near_reverse_angle_threshold
            )
        ):
            self.reverse_align_mode = True
            self.reverse_start_time = now
            self.reverse_heading_locked = False
            self.reverse_locked_angular = 0.0

        # 후진 종료
        if self.reverse_align_mode:
            reverse_elapsed = now - self.reverse_start_time

            if msg.distance == 'far' and reverse_elapsed > self.reverse_min_time:
                self.reverse_align_mode = False
                self.reverse_heading_locked = False
                self.reverse_locked_angular = 0.0

            elif reverse_elapsed > self.reverse_max_time:
                self.reverse_align_mode = False
                self.reverse_heading_locked = False
                self.reverse_locked_angular = 0.0

        if self.reverse_align_mode:
            reverse_angle_error = angle_error
            reverse_dangle = dangle

            reverse_lock_threshold = 0.02 # 0.05   # 약 1.25도
            reverse_min_angular = 0.03
            reverse_align_speed = -0.04
            reverse_straight_speed = -self.reverse_speed

            # 1) 아직 heading lock 안 됐으면 angle만 0으로 맞춤
            if not self.reverse_heading_locked:
                target_angular = (
                    (kp_angle_use * 1.5) * reverse_angle_error +
                    (kd_angle_use * 1.2) * reverse_dangle
                )
                target_angular = clamp(target_angular, -max_angular_use, max_angular_use)

                if abs(reverse_angle_error) < reverse_lock_threshold:
                    self.reverse_heading_locked = True
                    self.reverse_locked_angular = 0.0
                    target_angular = 0.0
                elif abs(target_angular) > 1e-4:
                    if target_angular > 0.0:
                        target_angular = max(target_angular, reverse_min_angular)
                    else:
                        target_angular = min(target_angular, -reverse_min_angular)

                target_linear = reverse_align_speed

            # 2) 한 번 angle이 맞았으면 각속도 0으로 고정하고 far까지 후진
            else:
                target_linear = reverse_straight_speed
                target_angular = self.reverse_locked_angular

            self.current_linear = approach(self.current_linear, target_linear, self.linear_acc_step)
            self.current_angular = approach(self.current_angular, target_angular, self.angular_acc_step)
            self.publish_current()

            if self.debug_log:
                phase = (
                    'REVERSE_ALIGN_HEADING'
                    if not self.reverse_heading_locked
                    else 'REVERSE_STRAIGHT_LOCKED'
                )
                self.get_logger().info(
                    f'[{phase}] age={age:.3f} dist={msg.distance} '
                    f'x_err={x_error:.3f} ang_err={angle_error:.3f} '
                    f't_lin={target_linear:.3f} t_ang={target_angular:.3f} '
                    f'out_lin={self.current_linear:.3f} out_ang={self.current_angular:.3f}'
                )
            return

        # 전진
        if msg.distance == 'far':
            base_linear = self.far_speed
        elif msg.distance == 'middle':
            base_linear = self.middle_speed
        else:
            base_linear = self.near_speed

        turn_ratio = min(abs(target_angular) / max(max_angular_use, 1e-6), 1.0)
        target_linear = base_linear * (1.0 - 0.15 * turn_ratio)
        target_linear = max(target_linear, self.min_forward_speed)
        target_linear = clamp(target_linear, 0.0, self.max_linear)

        self.current_linear = approach(self.current_linear, target_linear, self.linear_acc_step)
        self.current_angular = approach(self.current_angular, target_angular, self.angular_acc_step)
        self.publish_current()

        if self.debug_log:
            self.get_logger().info(
                f'age={age:.3f} dist={msg.distance} '
                f'x_err={x_error:.3f} ang_err={angle_error:.3f} '
                f't_lin={target_linear:.3f} t_ang={target_angular:.3f} '
                f'out_lin={self.current_linear:.3f} out_ang={self.current_angular:.3f}'
            )

    def hold_and_stabilize(self):
        self.current_angular = approach(self.current_angular, 0.0, self.angular_decay_step)
        self.current_linear = approach(
            self.current_linear,
            max(self.min_forward_speed * 0.8, 0.03),
            self.linear_decay_step
        )
        self.publish_current()

    def soft_stop(self):
        self.current_angular = approach(self.current_angular, 0.0, self.angular_decay_step)
        self.current_linear = approach(self.current_linear, 0.0, self.linear_decay_step)
        self.publish_current()

    def publish_current(self):
        twist = Twist()
        twist.linear.x = self.current_linear
        twist.angular.z = self.current_angular
        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = RailPDControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.current_linear = 0.0
        node.current_angular = 0.0
        node.publish_current()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()