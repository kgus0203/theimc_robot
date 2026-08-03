import threading
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Bool

from interfaces_pkg.action import RailApproach
from interfaces_pkg.msg import RailInfo


class RailApproachActionServer(Node):
    """
    레일 시작점 접근용 단순 상태 머신.

    흐름:
        SEARCH
          -> ALIGN_CENTER
          -> STEP_FORWARD
          -> ALIGN_ANGLE
          -> 다시 ALIGN_CENTER
          -> 가까워지면 FINAL_CHECK
          -> 필요하면 BACKUP
          -> SUCCESS

    핵심 원칙:
    - 중심과 각도를 동시에 섞어서 제어하지 않는다.
    - 연속 회전 대신 짧게 움직이고 다시 인식한다.
    - 가까울수록 허용 오차와 움직임 시간을 줄인다.
    - 가까운 상태에서 크게 틀어지면 후퇴 후 재정렬한다.
    """

    def __init__(self):
        super().__init__('rail_approach_action_server_node')

        self.cb_group = ReentrantCallbackGroup()
        self._goal_lock = threading.Lock()
        self._goal_active = False

        # ---------- ROS topics ----------
        self.declare_parameter(
            'perception_enable_topic',
            '/rail_perception_enable'
        )
        self.declare_parameter('rail_info_topic', '/rail_info')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_rail')
        self.declare_parameter('success_topic', '/rail_approach_success')

        # ---------- Main tuning values ----------
        self.declare_parameter('control_rate_hz', 20.0)
        self.declare_parameter('rail_timeout_sec', 0.5)

        self.declare_parameter('turn_speed', 0.08)
        self.declare_parameter('forward_speed', 0.08)
        self.declare_parameter('backup_speed', 0.05)

        self.declare_parameter('settle_sec', 0.15)
        self.declare_parameter('backup_sec', 0.50)
        self.declare_parameter('success_hold_sec', 0.40)

        # goal 값이 0 이하일 때 사용할 기본 허용 오차
        # x_error는 화면 반폭 기준 정규화 값이다.
        self.declare_parameter('default_x_tolerance', 0.03)
        self.declare_parameter('default_angle_tolerance', 0.8)

        # near 상태에서 이보다 크게 틀어지면 후퇴
        self.declare_parameter('recovery_x_error', 0.10)
        self.declare_parameter('recovery_angle_error', 3.0)

        self.perception_enable_topic = self.get_parameter(
            'perception_enable_topic'
        ).value
        self.rail_info_topic = self.get_parameter('rail_info_topic').value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.success_topic = self.get_parameter('success_topic').value

        self.control_rate_hz = float(
            self.get_parameter('control_rate_hz').value
        )
        self.rail_timeout_sec = float(
            self.get_parameter('rail_timeout_sec').value
        )

        self.turn_speed = float(self.get_parameter('turn_speed').value)
        self.forward_speed = float(self.get_parameter('forward_speed').value)
        self.backup_speed = float(self.get_parameter('backup_speed').value)

        self.settle_sec = float(self.get_parameter('settle_sec').value)
        self.backup_sec = float(self.get_parameter('backup_sec').value)
        self.success_hold_sec = float(
            self.get_parameter('success_hold_sec').value
        )

        self.default_x_tolerance = float(
            self.get_parameter('default_x_tolerance').value
        )
        self.default_angle_tolerance = float(
            self.get_parameter('default_angle_tolerance').value
        )
        self.recovery_x_error = float(
            self.get_parameter('recovery_x_error').value
        )
        self.recovery_angle_error = float(
            self.get_parameter('recovery_angle_error').value
        )

        # ---------- Latest perception ----------
        self.latest_rail_info = None
        self.latest_rail_time = None

        # ---------- ROS I/O ----------
        self.perception_enable_pub = self.create_publisher(
            Bool,
            self.perception_enable_topic,
            10
        )
        self.cmd_pub = self.create_publisher(
            Twist,
            self.cmd_vel_topic,
            10
        )
        self.success_pub = self.create_publisher(
            Bool,
            self.success_topic,
            10
        )

        self.rail_sub = self.create_subscription(
            RailInfo,
            self.rail_info_topic,
            self.rail_info_callback,
            10,
            callback_group=self.cb_group
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

        self.get_logger().info('[RAIL_ACTION] ready')
        self.get_logger().info(
            f'[RAIL_ACTION] rail info : {self.rail_info_topic}'
        )
        self.get_logger().info(
            f'[RAIL_ACTION] cmd_vel   : {self.cmd_vel_topic}'
        )
        self.get_logger().info('[RAIL_ACTION] action    : /rail_approach')

    # ------------------------------------------------------------------
    # ROS callbacks
    # ------------------------------------------------------------------

    def rail_info_callback(self, msg):
        self.latest_rail_info = msg
        self.latest_rail_time = time.monotonic()

    def goal_callback(self, goal_request):
        with self._goal_lock:
            if self._goal_active:
                self.get_logger().warn(
                    '[RAIL_ACTION] another goal is already running'
                )
                return GoalResponse.REJECT

            self._goal_active = True

        self.get_logger().info(
            '[RAIL_ACTION] goal accepted '
            f'timeout={goal_request.timeout_sec:.2f}, '
            f'x_tol={goal_request.x_tolerance:.3f}, '
            f'angle_tol={goal_request.angle_tolerance:.3f}'
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, _goal_handle):
        self.get_logger().warn('[RAIL_ACTION] cancel requested')
        self.stop_robot()
        return CancelResponse.ACCEPT

    # ------------------------------------------------------------------
    # Basic helpers
    # ------------------------------------------------------------------

    @staticmethod
    def get_field(msg, name, default_value):
        return getattr(msg, name, default_value)

    @staticmethod
    def normalize_distance(value):
        distance = str(value).strip().lower()

        if distance in ('near', 'close'):
            return 'near'
        if distance in ('middle', 'mid'):
            return 'middle'
        return 'far'

    def set_perception_enable(self, enable):
        msg = Bool()
        msg.data = bool(enable)

        # 인식 노드가 순간적으로 놓치는 것을 줄이기 위해 짧게 반복 송신
        for _ in range(3):
            self.perception_enable_pub.publish(msg)
            time.sleep(0.02)

    def stop_robot(self):
        cmd = Twist()

        for _ in range(3):
            self.cmd_pub.publish(cmd)
            time.sleep(0.01)

    def publish_success(self):
        msg = Bool()
        msg.data = True
        self.success_pub.publish(msg)

    def get_valid_rail(self):
        if self.latest_rail_info is None or self.latest_rail_time is None:
            return None

        age = time.monotonic() - self.latest_rail_time
        if age > self.rail_timeout_sec:
            return None

        if not bool(self.get_field(self.latest_rail_info, 'has_rail', False)):
            return None

        return self.latest_rail_info

    def extract_errors(self, rail):
        rail_cx = float(self.get_field(rail, 'rail_cx', 0.0))
        img_cx = float(self.get_field(rail, 'img_cx', 0.0))
        img_width = float(self.get_field(rail, 'img_width', 0.0))

        if img_width <= 0.0:
            x_error = 0.0
        else:
            # 양수: 레일이 화면 오른쪽
            # 음수: 레일이 화면 왼쪽
            x_error = (rail_cx - img_cx) / (img_width / 2.0)

        angle_error = float(self.get_field(rail, 'angle_deg', 0.0))
        distance = self.normalize_distance(
            self.get_field(rail, 'distance', 'far')
        )

        return x_error, angle_error, distance

    # ------------------------------------------------------------------
    # Distance-dependent settings
    # ------------------------------------------------------------------

    @staticmethod
    def center_tolerance(distance, near_tolerance):
        return {
            'far': max(near_tolerance, 0.12),
            'middle': max(near_tolerance, 0.06),
            'near': near_tolerance,
        }[distance]

    @staticmethod
    def angle_tolerance(distance, near_tolerance):
        return {
            'far': max(near_tolerance, 1.2),
            'middle': max(near_tolerance, 0.8),
            'near': near_tolerance,
        }[distance]

    @staticmethod
    def forward_duration(distance):
        return {
            'far': 0.80,
            'middle': 0.45,
            'near': 0.20,
        }[distance]

    @staticmethod
    def turn_duration(distance):
        return {
            'far': 0.18,
            'middle': 0.12,
            'near': 0.08,
        }[distance]

    def turn_for_center(self, x_error):
        # 레일이 화면 오른쪽이면 로봇은 오른쪽 회전
        return -self.turn_speed if x_error > 0.0 else self.turn_speed

    def turn_for_angle(self, angle_error):
        # 기존 코드의 angle 부호 기준을 유지한다.
        return self.turn_speed if angle_error > 0.0 else -self.turn_speed

    # ------------------------------------------------------------------
    # Motion and feedback
    # ------------------------------------------------------------------

    def publish_feedback(
        self,
        goal_handle,
        state,
        x_error,
        angle_error,
        distance
    ):
        feedback = RailApproach.Feedback()
        feedback.state = str(state)
        feedback.x_error = float(x_error)
        feedback.angle_error = float(angle_error)
        feedback.distance = str(distance)
        goal_handle.publish_feedback(feedback)

    def run_motion(
        self,
        goal_handle,
        deadline,
        linear_x=0.0,
        angular_z=0.0,
        duration=0.0,
        require_rail=True
    ):
        """
        짧은 이동 명령을 실행한 뒤 정지한다.

        반환값:
            ok, canceled, timeout, shutdown, rail_lost
        """
        cmd = Twist()
        cmd.linear.x = float(linear_x)
        cmd.angular.z = float(angular_z)

        period = 1.0 / self.control_rate_hz
        end_time = time.monotonic() + max(0.0, duration)

        while time.monotonic() < end_time:
            if goal_handle.is_cancel_requested:
                self.stop_robot()
                return 'canceled'

            if time.monotonic() >= deadline:
                self.stop_robot()
                return 'timeout'

            if not rclpy.ok():
                self.stop_robot()
                return 'shutdown'

            if require_rail and self.get_valid_rail() is None:
                self.stop_robot()
                return 'rail_lost'

            self.cmd_pub.publish(cmd)
            time.sleep(period)

        self.stop_robot()

        # 움직임 직후 영상이 안정될 시간을 짧게 준다.
        settle_end = time.monotonic() + self.settle_sec
        while time.monotonic() < settle_end:
            if goal_handle.is_cancel_requested:
                return 'canceled'

            if time.monotonic() >= deadline:
                return 'timeout'

            if not rclpy.ok():
                return 'shutdown'

            time.sleep(period)

        return 'ok'

    # ------------------------------------------------------------------
    # Main action
    # ------------------------------------------------------------------

    def execute_callback(self, goal_handle):
        self.get_logger().info('[RAIL_ACTION] execute start')
        self.set_perception_enable(True)

        goal = goal_handle.request

        timeout_sec = (
            float(goal.timeout_sec)
            if float(goal.timeout_sec) > 0.0
            else 30.0
        )
        near_x_tolerance = (
            float(goal.x_tolerance)
            if float(goal.x_tolerance) > 0.0
            else self.default_x_tolerance
        )
        near_angle_tolerance = (
            float(goal.angle_tolerance)
            if float(goal.angle_tolerance) > 0.0
            else self.default_angle_tolerance
        )

        deadline = time.monotonic() + timeout_sec
        period = 1.0 / self.control_rate_hz

        state = 'SEARCH'
        stable_since = None

        result = RailApproach.Result()

        def finish_terminal(status):
            if status == 'canceled':
                goal_handle.canceled()
                result.success = False
                result.reason = 'canceled'
                return result

            if status == 'timeout':
                goal_handle.abort()
                result.success = False
                result.reason = 'timeout'
                return result

            if status == 'shutdown':
                goal_handle.abort()
                result.success = False
                result.reason = 'rclpy_shutdown'
                return result

            return None

        try:
            while rclpy.ok():
                now = time.monotonic()

                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result.success = False
                    result.reason = 'canceled'
                    return result

                if now >= deadline:
                    goal_handle.abort()
                    result.success = False
                    result.reason = 'timeout'
                    return result

                rail = self.get_valid_rail()

                if rail is None:
                    state = 'SEARCH'
                    stable_since = None
                    self.stop_robot()

                    self.publish_feedback(
                        goal_handle,
                        state,
                        0.0,
                        0.0,
                        'unknown'
                    )
                    time.sleep(period)
                    continue

                x_error, angle_error, distance = self.extract_errors(rail)

                x_tol = self.center_tolerance(
                    distance,
                    near_x_tolerance
                )
                angle_tol = self.angle_tolerance(
                    distance,
                    near_angle_tolerance
                )

                self.publish_feedback(
                    goal_handle,
                    state,
                    x_error,
                    angle_error,
                    distance
                )

                self.get_logger().info(
                    f'[RAIL_ACTION][{state}] '
                    f'distance={distance}, '
                    f'x={x_error:.3f}/{x_tol:.3f}, '
                    f'angle={angle_error:.3f}/{angle_tol:.3f}'
                )

                if state == 'SEARCH':
                    state = 'ALIGN_CENTER'
                    continue

                # 가까운 상태에서 크게 틀어졌다면 제자리 회전하지 않고 후퇴
                if (
                    distance == 'near'
                    and state not in ('BACKUP', 'FINAL_CHECK')
                    and (
                        abs(x_error) > self.recovery_x_error
                        or abs(angle_error) > self.recovery_angle_error
                    )
                ):
                    state = 'BACKUP'
                    continue

                if state == 'ALIGN_CENTER':
                    if abs(x_error) > x_tol:
                        status = self.run_motion(
                            goal_handle=goal_handle,
                            deadline=deadline,
                            angular_z=self.turn_for_center(x_error),
                            duration=self.turn_duration(distance),
                            require_rail=True
                        )

                        terminal = finish_terminal(status)
                        if terminal is not None:
                            return terminal

                        if status == 'rail_lost':
                            state = 'SEARCH'
                        continue

                    if distance == 'near':
                        state = 'ALIGN_ANGLE'
                    else:
                        state = 'STEP_FORWARD'
                    continue

                if state == 'STEP_FORWARD':
                    status = self.run_motion(
                        goal_handle=goal_handle,
                        deadline=deadline,
                        linear_x=self.forward_speed,
                        duration=self.forward_duration(distance),
                        require_rail=True
                    )

                    terminal = finish_terminal(status)
                    if terminal is not None:
                        return terminal

                    state = (
                        'SEARCH'
                        if status == 'rail_lost'
                        else 'ALIGN_ANGLE'
                    )
                    continue

                if state == 'ALIGN_ANGLE':
                    if abs(angle_error) > angle_tol:
                        status = self.run_motion(
                            goal_handle=goal_handle,
                            deadline=deadline,
                            angular_z=self.turn_for_angle(angle_error),
                            duration=self.turn_duration(distance),
                            require_rail=True
                        )

                        terminal = finish_terminal(status)
                        if terminal is not None:
                            return terminal

                        if status == 'rail_lost':
                            state = 'SEARCH'
                        continue

                    if distance == 'near':
                        state = 'FINAL_CHECK'
                    else:
                        state = 'ALIGN_CENTER'
                    continue

                if state == 'FINAL_CHECK':
                    near_ok = (
                        distance == 'near'
                        and abs(x_error) <= near_x_tolerance
                        and abs(angle_error) <= near_angle_tolerance
                    )

                    if near_ok:
                        if stable_since is None:
                            stable_since = now

                        if now - stable_since >= self.success_hold_sec:
                            self.stop_robot()
                            self.publish_success()
                            goal_handle.succeed()

                            result.success = True
                            result.reason = 'rail_approach_success'
                            return result

                        time.sleep(period)
                        continue

                    stable_since = None

                    if distance != 'near':
                        state = 'ALIGN_CENTER'
                    elif (
                        abs(x_error) > self.recovery_x_error
                        or abs(angle_error) > self.recovery_angle_error
                    ):
                        state = 'BACKUP'
                    elif abs(x_error) > near_x_tolerance:
                        state = 'ALIGN_CENTER'
                    else:
                        state = 'ALIGN_ANGLE'

                    continue

                if state == 'BACKUP':
                    status = self.run_motion(
                        goal_handle=goal_handle,
                        deadline=deadline,
                        linear_x=-self.backup_speed,
                        duration=self.backup_sec,
                        require_rail=False
                    )

                    terminal = finish_terminal(status)
                    if terminal is not None:
                        return terminal

                    state = 'ALIGN_CENTER'
                    continue

                # 알 수 없는 상태가 생겼을 때 안전하게 초기화
                self.get_logger().warn(
                    f'[RAIL_ACTION] unknown state: {state}'
                )
                state = 'SEARCH'

            goal_handle.abort()
            result.success = False
            result.reason = 'rclpy_shutdown'
            return result

        finally:
            self.stop_robot()
            self.set_perception_enable(False)

            with self._goal_lock:
                self._goal_active = False

            self.get_logger().info('[RAIL_ACTION] execute finished')


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