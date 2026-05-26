import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

from geometry_msgs.msg import Twist
from std_msgs.msg import String 

from interfaces_pkg.msg import RailInfo
from interfaces_pkg.action import RailApproach

from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor


class RailApproachActionServer(Node):
    def __init__(self):
        super().__init__('rail_approach_action_server_node')

        self.cb_group = ReentrantCallbackGroup()

        # ===== Parameters =====
        self.declare_parameter('rail_info_topic', '/rail_info')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_rail')

        self.declare_parameter('control_rate_hz', 20.0)

        # x 중심 정렬용 게인
        self.declare_parameter('kp_x', 0.35)
        self.declare_parameter('kd_x', 0.08)

        # angle은 이번 버전에서 제어에는 사용하지 않고 확인용으로만 사용
        self.declare_parameter('kp_angle', 0.012)
        self.declare_parameter('kd_angle', 0.004)

        self.declare_parameter('max_linear', 0.12)
        self.declare_parameter('max_angular', 0.15)

        self.declare_parameter('min_forward_speed', 0.035)
        self.declare_parameter('search_angular_speed', 0.08)

        self.declare_parameter('far_speed', 0.09)
        self.declare_parameter('middle_speed', 0.06)
        self.declare_parameter('near_speed', 0.035)

        self.declare_parameter('rail_timeout_sec', 0.7)
        self.declare_parameter('success_hold_sec', 0.3)

        # x_error가 맞았을 때 1초씩 전진/후진
        self.declare_parameter('burst_drive_sec', 5.0)

        # ===== Read parameters =====
        self.rail_info_topic = self.get_parameter('rail_info_topic').value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value

        self.control_rate_hz = float(self.get_parameter('control_rate_hz').value)

        self.kp_x = float(self.get_parameter('kp_x').value)
        self.kd_x = float(self.get_parameter('kd_x').value)

        self.kp_angle = float(self.get_parameter('kp_angle').value)
        self.kd_angle = float(self.get_parameter('kd_angle').value)

        self.max_linear = float(self.get_parameter('max_linear').value)
        self.max_angular = float(self.get_parameter('max_angular').value)

        self.min_forward_speed = float(self.get_parameter('min_forward_speed').value)
        self.search_angular_speed = float(self.get_parameter('search_angular_speed').value)

        self.far_speed = float(self.get_parameter('far_speed').value)
        self.middle_speed = float(self.get_parameter('middle_speed').value)
        self.near_speed = float(self.get_parameter('near_speed').value)

        self.rail_timeout_sec = float(self.get_parameter('rail_timeout_sec').value)
        self.success_hold_sec = float(self.get_parameter('success_hold_sec').value)

        self.burst_drive_sec = float(self.get_parameter('burst_drive_sec').value)

        # ===== Runtime state =====
        self.latest_rail_info = None
        self.latest_rail_time = None

        self.prev_x_error = 0.0
        self.prev_angle_error = 0.0
        self.prev_time = None

        self.success_start_time = None

        # burst 상태
        # burst_direction = 1.0  -> 전진
        # burst_direction = -1.0 -> 후진
        self.burst_active = False
        self.burst_end_time = None
        self.burst_direction = 0.0

        # ===== ROS I/O =====
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

        self.pub_rail_cmd = self.create_publisher(
            String,
            '/rail_command',
            10
        )

        self.get_logger().info('[RAIL_ACTION] ready')
        self.get_logger().info(f'[RAIL_ACTION] subscribe: {self.rail_info_topic}')
        self.get_logger().info(f'[RAIL_ACTION] publish  : {self.cmd_vel_topic}')
        self.get_logger().info('[RAIL_ACTION] action   : /rail_approach')

    def rail_info_callback(self, msg):
        self.latest_rail_info = msg
        self.latest_rail_time = time.time()

    def goal_callback(self, goal_request):
        self.get_logger().info(
            '[RAIL_ACTION] goal received '
            f'timeout={goal_request.timeout_sec}, '
            f'x_tol={goal_request.x_tolerance}, '
            f'angle_tol={goal_request.angle_tolerance}, '
            f'allow_reverse={goal_request.allow_reverse_align}'
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().warn('[RAIL_ACTION] cancel requested')
        self.stop_robot()
        return CancelResponse.ACCEPT

    def stop_robot(self):
        cmd = Twist()
        for _ in range(5):
            self.cmd_pub.publish(cmd)
            time.sleep(0.02)

    def clamp(self, value, min_value, max_value):
        return max(min_value, min(max_value, value))

    def get_field(self, msg, name, default_value):
        if hasattr(msg, name):
            return getattr(msg, name)
        return default_value

    def is_rail_info_alive(self):
        if self.latest_rail_info is None or self.latest_rail_time is None:
            return False

        age = time.time() - self.latest_rail_time
        return age <= self.rail_timeout_sec

    def get_speed_by_distance(self, distance):
        if distance == 'near':
            return self.near_speed
        if distance == 'middle':
            return self.middle_speed
        return self.far_speed

    def reset_burst(self):
        self.burst_active = False
        self.burst_end_time = None
        self.burst_direction = 0.0

    def start_burst(self, now, direction):
        self.burst_active = True
        self.burst_end_time = now + self.burst_drive_sec
        self.burst_direction = direction

    def fill_feedback(self, feedback_msg, goal_handle, state, x_error, angle_error, distance):
        feedback_msg.state = state
        feedback_msg.x_error = float(x_error)
        feedback_msg.angle_error = float(angle_error)
        feedback_msg.distance = str(distance)
        goal_handle.publish_feedback(feedback_msg)

    def execute_callback(self, goal_handle):
        self.get_logger().info('[RAIL_ACTION] execute start')

        goal = goal_handle.request

        timeout_sec = float(goal.timeout_sec)
        x_tolerance = float(goal.x_tolerance)
        angle_tolerance = float(goal.angle_tolerance)
        allow_reverse_align = bool(goal.allow_reverse_align)

        if timeout_sec <= 0.0:
            timeout_sec = 20.0

        if x_tolerance <= 0.0:
            x_tolerance = 0.08

        if angle_tolerance <= 0.0:
            angle_tolerance = 5.0

        start_time = time.time()

        self.prev_x_error = 0.0
        self.prev_angle_error = 0.0
        self.prev_time = time.time()
        self.success_start_time = None
        self.reset_burst()

        rate_period = 1.0 / self.control_rate_hz

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

            # ===== No rail info =====
            if not self.is_rail_info_alive():
                self.reset_burst()
                self.success_start_time = None

                state = 'SEARCHING'

                cmd = Twist()
                cmd.angular.z = self.search_angular_speed
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
                    f'[RAIL_ACTION][{state}] no rail info, searching...'
                )

                time.sleep(rate_period)
                continue

            rail = self.latest_rail_info

            # ===== RailInfo parsing =====
            has_rail = bool(self.get_field(rail, 'has_rail', True))

            if not has_rail:
                self.reset_burst()
                self.success_start_time = None

                state = 'SEARCHING'

                cmd = Twist()
                cmd.angular.z = self.search_angular_speed
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
                    f'[RAIL_ACTION][{state}] has_rail=false, searching...'
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

            dt = now - self.prev_time if self.prev_time is not None else rate_period
            if dt <= 0.0:
                dt = rate_period

            dx = (x_error - self.prev_x_error) / dt
            dangle = (angle_error - self.prev_angle_error) / dt

            self.prev_x_error = x_error
            self.prev_angle_error = angle_error
            self.prev_time = now

            abs_x = abs(x_error)
            abs_angle = abs(angle_error)

            cmd = Twist()

            # =========================================================
            # Success check 먼저
            # near 상태에서 x가 맞으면 더 움직이지 않고 성공 hold
            # angle은 확인용이므로 성공 조건에 넣지 않음
            # =========================================================
            success_condition = (
                distance == 'near'
                and abs_x <= x_tolerance
            )

            if success_condition:
                self.reset_burst()

                state = 'SUCCESS_HOLD'

                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.cmd_pub.publish(cmd)

                if self.success_start_time is None:
                    self.success_start_time = now

                hold_time = now - self.success_start_time

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
                    f'dist={distance}, '
                    f'hold={hold_time:.2f}/{self.success_hold_sec:.2f}'
                )

                if hold_time >= self.success_hold_sec:
                    self.stop_robot()
                    goal_handle.succeed()

                    result.success = True
                    result.reason = 'rail_approach_success'

                    #######################################
                    # rail_approach_success 이후 레일 진입 명령 전송
                    cmd_msg = String()
                    cmd_msg.data = "DETECTED"
                    self.pub_rail_cmd
                    self.pub_rail_cmd.publish(cmd_msg)

                    self.get_logger().info('[RAIL_ACTION] rail cmd published: DETECTED')
                    #######################################

                    return result

                time.sleep(rate_period)
                continue

            else:
                self.success_start_time = None

            # =========================================================
            # State machine
            # =========================================================

            # near인데 x가 안 맞으면 너무 가까워서 정렬이 어려운 상태
            # allow_reverse_align=True일 때만 1초 후진해서 공간을 만든다.
            too_close_and_not_aligned = (
                distance == 'near'
                and abs_x > x_tolerance
                and allow_reverse_align
            )

            if self.burst_active:
                if now < self.burst_end_time:
                    drive_speed = self.get_speed_by_distance(distance)
                    drive_speed = self.clamp(
                        drive_speed,
                        self.min_forward_speed,
                        self.max_linear
                    )

                    if self.burst_direction > 0.0:
                        state = 'FORWARD_BURST'
                        cmd.linear.x = drive_speed
                        cmd.angular.z = 0.0

                    else:
                        state = 'REVERSE_BURST'
                        cmd.linear.x = -drive_speed
                        cmd.angular.z = 0.0

                else:
                    self.reset_burst()
                    state = 'RECHECK_AFTER_BURST'
                    cmd.linear.x = 0.0
                    cmd.angular.z = 0.0

            else:
                if too_close_and_not_aligned:
                    state = 'START_REVERSE_BURST'

                    self.start_burst(now, direction=-1.0)

                    reverse_speed = self.get_speed_by_distance(distance)
                    reverse_speed = self.clamp(
                        reverse_speed,
                        self.min_forward_speed,
                        self.max_linear
                    )

                    cmd.linear.x = -reverse_speed
                    cmd.angular.z = 0.0

                elif abs_x > x_tolerance:
                    state = 'ALIGN_X'

                    # 이전 테스트에서 부호가 반대였으므로 - 적용
                    # x_error > 0일 때 현재 로봇 기준으로 중앙으로 오도록 회전
                    angular = -(self.kp_x * x_error + self.kd_x * dx)
                    angular = self.clamp(
                        angular,
                        -self.max_angular,
                        self.max_angular
                    )

                    cmd.linear.x = 0.0
                    cmd.angular.z = angular

                else:
                    # x가 맞으면 angle은 확인만 하고 1초 전진
                    if abs_angle > angle_tolerance:
                        state = 'START_FORWARD_BURST_ANGLE_CHECK'
                    else:
                        state = 'START_FORWARD_BURST'

                    self.start_burst(now, direction=1.0)

                    forward_speed = self.get_speed_by_distance(distance)
                    forward_speed = self.clamp(
                        forward_speed,
                        self.min_forward_speed,
                        self.max_linear
                    )

                    cmd.linear.x = forward_speed
                    cmd.angular.z = 0.0

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
                f'allow_reverse={allow_reverse_align}, '
                f'x_err={x_error:.3f}, '
                f'ang_err={angle_error:.3f}, '
                f'abs_angle={abs_angle:.3f}, '
                f'angle_tol={angle_tolerance:.3f}, '
                f'dist={distance}, '
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