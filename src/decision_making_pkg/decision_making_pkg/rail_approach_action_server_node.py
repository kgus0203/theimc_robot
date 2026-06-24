import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, String

from interfaces_pkg.msg import RailInfo
from interfaces_pkg.action import RailApproach

from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor


class RailApproachActionServer(Node):
    def __init__(self):
        super().__init__('rail_approach_action_server_node')

        self.cb_group = ReentrantCallbackGroup()

        self.declare_parameter('perception_enable_topic', '/rail_perception_enable')
        self.perception_enable_topic = self.get_parameter(
            'perception_enable_topic'
        ).get_parameter_value().string_value

        # ===== Parameters =====
        self.declare_parameter('rail_info_topic', '/rail_info')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_rail')

        self.declare_parameter('control_rate_hz', 20.0)

        self.declare_parameter('pulse_linear_speed', 0.1) # 찔끔찔끔 직진
        self.declare_parameter('pulse_forward_sec', 1.0)

        self.declare_parameter('angular_speed', 0.08)
        self.declare_parameter('rail_timeout_sec', 0.5)
        self.declare_parameter('success_topic', '/rail_approach_success')
        self.declare_parameter('rail_command_topic', '/rail_command')

        # ===== Read parameters =====
        self.rail_info_topic = self.get_parameter('rail_info_topic').value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value

        self.control_rate_hz = float(self.get_parameter('control_rate_hz').value)

        self.pulse_linear_speed = float(
            self.get_parameter('pulse_linear_speed').value
        )
        self.pulse_forward_sec = float(
            self.get_parameter('pulse_forward_sec').value
        )

        self.angular_speed = float(self.get_parameter('angular_speed').value)
        self.rail_timeout_sec = float(self.get_parameter('rail_timeout_sec').value)
        self.success_topic = str(self.get_parameter('success_topic').value)
        self.rail_command_topic = str(
            self.get_parameter('rail_command_topic').value
        )

        # ===== Runtime state =====
        self.latest_rail_info = None
        self.latest_rail_time = None

        # ===== ROS I/O =====
        self.perception_enable_pub = self.create_publisher(
            Bool,
            self.perception_enable_topic,
            10
        )

        self.rail_sub = self.create_subscription(
            RailInfo,
            self.rail_info_topic,
            self.rail_info_callback,
            10,
            callback_group=self.cb_group
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            self.cmd_vel_topic,
            10
        )

        self.action_server = ActionServer(
            self,
            RailApproach,
            'rail_approach',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.cb_group
        )

        self.success_pub = self.create_publisher(
            Bool,
            self.success_topic,
            10
        )
        self.pub_rail_cmd = self.create_publisher(
            String,
            self.rail_command_topic,
            10
        )

        self.get_logger().info('[RAIL_ACTION] ready')
        self.get_logger().info(f'[RAIL_ACTION] subscribe: {self.rail_info_topic}')
        self.get_logger().info(f'[RAIL_ACTION] publish  : {self.cmd_vel_topic}')
        self.get_logger().info('[RAIL_ACTION] action   : /rail_approach')
        self.get_logger().info(f'[RAIL_ACTION] success  : {self.success_topic}')
        self.get_logger().info(f'[RAIL_ACTION] rail cmd : {self.rail_command_topic}')

    def set_perception_enable(self, enable: bool):
        msg = Bool()
        msg.data = enable

        # subscriber가 순간적으로 못 받을 수도 있어서 여러 번 publish
        for _ in range(3):
            self.perception_enable_pub.publish(msg)
            time.sleep(0.02)

        if enable:
            self.get_logger().info('[RAIL_ACTION] Perception ENABLED')
        else:
            self.get_logger().info('[RAIL_ACTION] Perception DISABLED')

    def rail_info_callback(self, msg):
        self.latest_rail_info = msg
        self.latest_rail_time = time.time()

    def goal_callback(self, goal_request):
        self.get_logger().info(
            '[RAIL_ACTION] goal received '
            f'timeout={goal_request.timeout_sec}, '
            f'x_tol={goal_request.x_tolerance}, '
            f'angle_tol={goal_request.angle_tolerance}'
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().warn('[RAIL_ACTION] cancel requested')
        self.stop_robot()
        self.set_perception_enable(False)
        return CancelResponse.ACCEPT

    def stop_robot(self):
        cmd = Twist()
        for _ in range(5):
            self.cmd_pub.publish(cmd)
            time.sleep(0.02)

    def clamp(self, value, min_value, max_value):
        return max(min_value, min(max_value, value))

    def get_angle_turn_speed(self, angle_error):
        if abs(angle_error) < 1e-6:
            return 0.0

        if angle_error > 0.0:
            return self.angular_speed
        return -self.angular_speed

    def get_x_turn_speed(self, x_error):
        if abs(x_error) < 1e-6:
            return 0.0

        # x_error > 0 means the rail is on the right side of the image.
        if x_error > 0.0:
            return -self.angular_speed
        return self.angular_speed

    def get_proportional_turn_speed(self, angle_error, x_error, k_angle, k_x):
        angular = k_angle * angle_error - k_x * x_error
        return self.clamp(angular, -self.angular_speed, self.angular_speed)

    def get_field(self, msg, name, default_value):
        if hasattr(msg, name):
            return getattr(msg, name)
        return default_value

    def is_rail_info_alive(self):
        if self.latest_rail_info is None or self.latest_rail_time is None:
            return False

        age = time.time() - self.latest_rail_time
        return age <= self.rail_timeout_sec

    def fill_feedback(self, feedback_msg, goal_handle, state, x_error, angle_error, distance):
        feedback_msg.state = state
        feedback_msg.x_error = float(x_error)
        feedback_msg.angle_error = float(angle_error)
        feedback_msg.distance = str(distance)
        goal_handle.publish_feedback(feedback_msg)

    def publish_success(self):
        msg = Bool()
        msg.data = True
        self.success_pub.publish(msg)
        self.get_logger().info('[RAIL_ACTION] success published: true')

    def publish_detected(self):
        cmd_msg = String()
        cmd_msg.data = 'DETECTED'
        self.pub_rail_cmd.publish(cmd_msg)
        self.get_logger().info('[RAIL_ACTION] rail cmd published: DETECTED')

    def execute_callback(self, goal_handle):
        self.get_logger().info('[RAIL_ACTION] execute start')

        # Action이 실제 시작되면 YOLO/레일 인식 ON
        self.set_perception_enable(True)
    
        goal = goal_handle.request

        timeout_sec = float(goal.timeout_sec)
        x_tolerance = float(goal.x_tolerance)
        angle_tolerance = float(goal.angle_tolerance)

        if timeout_sec <= 0.0:
            timeout_sec = 20.0

        if x_tolerance <= 0.0:
            x_tolerance = 0.25

        if angle_tolerance <= 0.0:
            angle_tolerance = 5.0

        pulse_angle_tolerance = max(angle_tolerance + 3.0, angle_tolerance * 1.6)
        pulse_x_tolerance = max(x_tolerance + 0.15, x_tolerance * 1.6)
        forward_start_x_tolerance = max(x_tolerance, 0.35)
        close_x_tolerance = forward_start_x_tolerance

        forward_linear_speed = self.pulse_linear_speed * 0.8
        forward_k_angle = 0.01
        forward_k_x = 0.16
        align_k_angle = 0.008
        align_k_x = 0.10

        start_time = time.time()

        rate_period = 1.0 / self.control_rate_hz
        state = 'SEARCH'
        pulse_end_time = None

        feedback_msg = RailApproach.Feedback()
        result = RailApproach.Result()

        while rclpy.ok():
            now = time.time()

            # ===== Cancel =====
            if goal_handle.is_cancel_requested:
                self.stop_robot()
                goal_handle.canceled()

                result.success = False
                result.reason = 'canceled'

                self.get_logger().warn('[RAIL_ACTION] canceled')
                return result

            # ===== Timeout =====
            if now - start_time > timeout_sec:
                self.stop_robot()
                goal_handle.abort()

                result.success = False
                result.reason = 'timeout'

                self.get_logger().error('[RAIL_ACTION] failed: timeout')
                return result

            rail_alive = self.is_rail_info_alive()
            rail = self.latest_rail_info if rail_alive else None
            has_rail = bool(self.get_field(rail, 'has_rail', False)) if rail else False

            if not rail_alive or not has_rail:
                state = 'SEARCH'
                pulse_end_time = None
                cmd = Twist()
                self.cmd_pub.publish(cmd)

                self.fill_feedback(
                    feedback_msg,
                    goal_handle,
                    state,
                    0.0,
                    0.0,
                    'unknown'
                )

                self.get_logger().info(
                    f'[RAIL_ACTION][{state}] rail missing, stop'
                )

                time.sleep(rate_period)
                continue

            rail_cx = float(self.get_field(rail, 'rail_cx', 0.0))
            img_cx = float(self.get_field(rail, 'img_cx', 0.0))
            img_width = float(self.get_field(rail, 'img_width', 1.0))

            # x_error 계산
            # rail_cx == img_cx -> 0
            # rail_cx > img_cx  -> 양수, 레일이 화면 오른쪽
            # rail_cx < img_cx  -> 음수, 레일이 화면 왼쪽
            if img_width > 0.0:
                x_error = (rail_cx - img_cx) / (img_width / 2.0)
            else:
                x_error = 0.0

            angle_error = float(self.get_field(rail, 'angle_deg', 0.0))
            distance = str(self.get_field(rail, 'distance', 'far'))

            abs_x = abs(x_error)
            abs_angle = abs(angle_error)
            angle_ok = abs_angle <= angle_tolerance
            x_ok = abs_x <= x_tolerance
            forward_start_x_ok = abs_x <= forward_start_x_tolerance
            pulse_angle_ok = abs_angle <= pulse_angle_tolerance
            pulse_x_ok = abs_x <= pulse_x_tolerance
            close_enough = distance == 'near' and abs_x <= close_x_tolerance

            cmd = Twist()

            if state == 'SEARCH':
                state = 'ALIGN'

            if state == 'ALIGN':
                if not angle_ok:
                    cmd.angular.z = self.get_proportional_turn_speed(
                        angle_error,
                        x_error,
                        align_k_angle,
                        align_k_x
                    )
                elif not forward_start_x_ok:
                    cmd.angular.z = self.get_proportional_turn_speed(
                        0.0,
                        x_error,
                        align_k_angle,
                        align_k_x
                    )
                elif close_enough:
                    self.stop_robot()
                    self.publish_detected()
                    self.publish_success()
                    goal_handle.succeed()

                    result.success = True
                    result.reason = 'rail_approach_success'
                    return result
                else:
                    state = 'PULSE_FORWARD'
                    pulse_end_time = now + self.pulse_forward_sec
                    cmd.linear.x = forward_linear_speed
                    cmd.angular.z = self.clamp(
                        forward_k_angle * angle_error - forward_k_x * x_error,
                        -self.angular_speed,
                        self.angular_speed
                    )

            elif state == 'PULSE_FORWARD':
                if not pulse_angle_ok or not pulse_x_ok:
                    state = 'ALIGN'
                    pulse_end_time = None
                elif close_enough:
                    self.stop_robot()
                    self.publish_detected()
                    self.publish_success()
                    goal_handle.succeed()

                    result.success = True
                    result.reason = 'rail_approach_success'
                    return result
                elif pulse_end_time is not None and now < pulse_end_time:
                    cmd.linear.x = forward_linear_speed
                    cmd.angular.z = self.clamp(
                        forward_k_angle * angle_error - forward_k_x * x_error,
                        -self.angular_speed,
                        self.angular_speed
                    )
                else:
                    state = 'ALIGN'
                    pulse_end_time = None

            self.cmd_pub.publish(cmd)

            self.fill_feedback(
                feedback_msg,
                goal_handle,
                state,
                x_error,
                angle_error,
                distance
            )

            self.get_logger().info(
                f'[RAIL_ACTION][{state}] '
                f'x_err={x_error:.3f}, '
                f'ang_err={angle_error:.3f}, '
                f'abs_angle={abs_angle:.3f}, '
                f'angle_tol={angle_tolerance:.3f}, '
                f'pulse_angle_tol={pulse_angle_tolerance:.3f}, '
                f'x_tol={x_tolerance:.3f}, '
                f'forward_start_x_tol={forward_start_x_tolerance:.3f}, '
                f'close_x_tol={close_x_tolerance:.3f}, '
                f'pulse_x_tol={pulse_x_tolerance:.3f}, '
                f'dist={distance}, '
                f'close_enough={close_enough}, '
                f'lin={cmd.linear.x:.3f}, '
                f'ang={cmd.angular.z:.3f}'
            )

            time.sleep(rate_period)

        self.stop_robot()
        goal_handle.abort()

        result.success = False
        result.reason = 'rclpy_shutdown'
        return result


def main(args=None):
    rclpy.init(args=args)

    node = RailApproachActionServer()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().warn('[RAIL_ACTION] keyboard interrupt')
    finally:
        node.stop_robot()
        executor.shutdown()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
