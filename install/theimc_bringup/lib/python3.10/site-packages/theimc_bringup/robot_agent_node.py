#!/usr/bin/env python3
import json
import math
import time
import queue
from typing import Optional, Dict, Any, List

import paho.mqtt.client as mqtt

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from std_srvs.srv import Trigger
from std_msgs.msg import Bool, String


from interfaces_pkg.action import RailApproach


# ============================================================
# MQTT CONFIG
# ============================================================

MQTT_BROKER = "203.251.85.204"
MQTT_PORT = 1883

ROBOT_ID = "robot_001"

TOPIC_CMD = f"robots/{ROBOT_ID}/cmd"
TOPIC_STATUS = f"robots/{ROBOT_ID}/status"
TOPIC_POSE = f"robots/{ROBOT_ID}/pose"
TOPIC_EVENT = f"robots/{ROBOT_ID}/event"
TOPIC_HEALTH = f"robots/{ROBOT_ID}/health"


# ============================================================
# UTIL
# ============================================================

def now_ts() -> float:
    return time.time()


def yaw_to_quaternion(yaw: float):
    qz = math.sin(yaw / 2.0)
    qw = math.cos(yaw / 2.0)
    return qz, qw


def quaternion_to_yaw(q):
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


# ============================================================
# ROBOT AGENT NODE
# ============================================================

class RobotAgent(Node):
    def __init__(self):
        super().__init__("robot_agent")

        # ====================================================
        # ROS2 ACTION CLIENTS
        # ====================================================

        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            "navigate_to_pose"
        )

        self.rail_client = ActionClient(
            self,
            RailApproach,
            "rail_approach"
        )

        # ====================================================
        # ROS2 SERVICE CLIENTS
        # ====================================================
        # capture_node 쪽에서 /capture_image Trigger service를 열어두는 구조
        # 지금 당장 capture_node가 없으면 capture step은 실패 처리됨

        self.capture_client = self.create_client(
            Trigger,
            "/capture_image"
        )

        # ====================================================
        # ROS2 PUBLISHERS
        # ====================================================

        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            "/initialpose",
            10,
        )

        # twist_mux를 쓴다면 /cmd_vel_web 입력으로 연결 추천
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            # "/cmd_vel_web",
            "/cmd_vel",
            10,
        )

        # 레일 이탈 명령 publisher
        # rail 제어 노드가 이 토픽을 subscribe해서 "EXIT" 등을 처리하는 구조
        self.rail_cmd_pub = self.create_publisher(
            String,
            "/rail_command",
            10,
        )

        # BehaviorTree mission input publishers
        self.selected_rails_pub = self.create_publisher(
            String,
            "/selected_rails",
            10,
        )

        self.mission_trigger_pub = self.create_publisher(
            Bool,
            "/mission_trigger",
            10,
        )

        self.return_home_pub = self.create_publisher(
            Bool,
            "/return_home",
            10,
        )

        # ====================================================
        # ROS2 SUBSCRIBERS
        # ====================================================

        self.amcl_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            "/amcl_pose",
            self.amcl_pose_callback,
            10,
        )

        # ====================================================
        # MODE / STATE
        # ====================================================

        self.mode = "IDLE"
        # IDLE / MANUAL / AUTO / EMERGENCY_STOP / ERROR

        self.task_state = "READY"
        # READY / NAVIGATING / RAIL_APPROACH / CAPTURING / JOGGING / STOPPED / ERROR

        self.last_event = None
        self.last_error = None

        # ====================================================
        # RUNTIME STATE
        # ====================================================

        self.current_pose = None
        self.distance_remaining: Optional[float] = None

        self.nav_goal_handle = None
        self.rail_goal_handle = None

        self.nav_command_id: Optional[str] = None
        self.rail_command_id: Optional[str] = None
        self.capture_command_id: Optional[str] = None
        self.current_command_id: Optional[str] = None

        self.nav_active = False
        self.rail_active = False
        self.capture_active = False

        self.nav_result_data = None
        self.rail_result_data = None
        self.capture_result_data = None

        self.rail_feedback = {
            "state": None,
            "x_error": None,
            "angle_error": None,
            "distance": None,
        }

        # ====================================================
        # MANUAL JOG SAFETY
        # ====================================================

        self.last_jog_vx = 0.0
        self.last_jog_wz = 0.0
        self.last_jog_time = 0.0
        self.jog_timeout_sec = 0.5

        # 안전 속도 제한
        self.max_jog_vx = 0.25
        self.max_jog_wz = 0.35

        # ====================================================
        # ROUTINE STATE
        # ====================================================

        self.active_routine: Optional[List[Dict[str, Any]]] = None
        self.routine_id: Optional[str] = None
        self.routine_command_id: Optional[str] = None
        self.routine_index = 0
        self.routine_running = False
        self.routine_step_active = False
        self.routine_stop_requested = False
        self.current_step = None

        # 기본 저장 pose
        # 웹에서 target을 문자열로 보내면 여기서 찾음
        # 실제로는 DB나 YAML로 빼도 됨
        self.saved_poses = {
            "home": {
                "x": 0.0,
                "y": 0.0,
                "yaw": 0.0,
            },
            "rail_1_start": {
                "x": 1.0,
                "y": 0.0,
                "yaw": 0.0,
            },
            "rail_1_middle": {
                "x": 2.0,
                "y": 0.0,
                "yaw": 0.0,
            },
            "rail_1_end": {
                "x": 3.0,
                "y": 0.0,
                "yaw": 0.0,
            },
        }

        # ====================================================
        # MQTT
        # ====================================================

        self.cmd_queue = queue.Queue()

        self.mqtt_connected = False

        self.mqtt_client = mqtt.Client(
            client_id=f"{ROBOT_ID}_agent"
        )

        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
        self.mqtt_client.on_message = self.on_mqtt_message

        self.mqtt_client.reconnect_delay_set(
            min_delay=1,
            max_delay=10
        )

        # 로봇이 죽거나 네트워크가 끊기면 broker가 자동으로 발행
        self.mqtt_client.will_set(
            TOPIC_EVENT,
            json.dumps({
                "robot_id": ROBOT_ID,
                "event": "ROBOT_AGENT_DISCONNECTED",
                "mode": "UNKNOWN",
                "task_state": "UNKNOWN",
                "stamp": now_ts(),
            }),
            qos=1,
            retain=False,
        )

        # ====================================================
        # TIMERS
        # ====================================================

        self.command_timer = self.create_timer(
            0.05,
            self.process_command_queue
        )

        self.safety_timer = self.create_timer(
            0.1,
            self.safety_tick
        )

        self.routine_timer = self.create_timer(
            0.1,
            self.routine_tick
        )

        self.status_timer = self.create_timer(
            0.5,
            self.publish_status
        )

        self.health_timer = self.create_timer(
            2.0,
            self.publish_health
        )

        self.get_logger().info("robot_agent started")

    # ========================================================
    # MQTT
    # ========================================================

    def start_mqtt(self):
        try:
            self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.mqtt_client.loop_start()
            self.get_logger().info("[MQTT] loop started")
        except Exception as e:
            self.get_logger().error(f"[MQTT] connect error: {e}")
            self.last_error = str(e)

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.mqtt_connected = True
        self.get_logger().info(f"[MQTT] connected rc={rc}")

        client.subscribe(TOPIC_CMD, qos=1)
        self.get_logger().info(f"[MQTT] subscribed: {TOPIC_CMD}")

        self.publish_event("ROBOT_AGENT_CONNECTED")

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.mqtt_connected = False
        self.get_logger().warn(f"[MQTT] disconnected rc={rc}")

    def on_mqtt_message(self, client, userdata, msg):
        # 중요:
        # MQTT callback thread에서 ROS action/publisher를 직접 만지지 말고 queue에 넣는다.
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception as e:
            self.get_logger().error(f"[MQTT] bad json: {e}")
            return

        self.get_logger().info(f"[MQTT] cmd queued: {payload}")
        self.cmd_queue.put(payload)

    def mqtt_publish_json(self, topic: str, payload: dict, qos: int = 0):
        try:
            self.mqtt_client.publish(
                topic,
                json.dumps(payload, ensure_ascii=False),
                qos=qos,
            )
        except Exception as e:
            self.get_logger().error(f"[MQTT] publish error: {e}")
            self.last_error = str(e)

    # ========================================================
    # ROS CALLBACKS
    # ========================================================

    def amcl_pose_callback(self, msg: PoseWithCovarianceStamped):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation

        self.current_pose = {
            "x": float(p.x),
            "y": float(p.y),
            "yaw": float(quaternion_to_yaw(q)),
        }

        self.mqtt_publish_json(TOPIC_POSE, {
            "robot_id": ROBOT_ID,
            "pose": self.current_pose,
            "stamp": now_ts(),
        })

    # ========================================================
    # COMMAND QUEUE
    # ========================================================

    def process_command_queue(self):
        # 한 번에 너무 많이 처리하지 않도록 최대 5개만 처리
        max_process = 5

        for _ in range(max_process):
            if self.cmd_queue.empty():
                return

            try:
                payload = self.cmd_queue.get_nowait()
            except queue.Empty:
                return

            self.handle_command(payload)

    def handle_command(self, payload: dict):
        cmd_type = payload.get("type")
        command_id = payload.get("command_id")
        self.current_command_id = command_id

        self.get_logger().info(f"[CMD] handling: {payload}")

        # emergency 상태에서는 clear_emergency만 허용
        if self.mode == "EMERGENCY_STOP":
            if cmd_type != "clear_emergency":
                self.publish_event("COMMAND_BLOCKED_BY_EMERGENCY", {
                    "command_id": command_id,
                    "cmd_type": cmd_type,
                })
                return

        try:
            if cmd_type == "initial_pose":
                target = payload.get("target", {})
                self.handle_initial_pose(
                    target.get("x", 0.0),
                    target.get("y", 0.0),
                    target.get("yaw", 0.0),
                    command_id,
                )

            elif cmd_type == "navigate_to":
                target = payload.get("target", {})
                target_pose = self.resolve_target_pose(target)

                if target_pose is None:
                    self.publish_event("UNKNOWN_TARGET", {
                        "command_id": command_id,
                        "target": target,
                    })
                    return

                self.handle_navigate_to(
                    target_pose["x"],
                    target_pose["y"],
                    target_pose["yaw"],
                    command_id,
                    source="single",
                )

            elif cmd_type == "rail_approach":
                self.handle_rail_approach(
                    timeout_sec=payload.get("timeout_sec", 30.0),
                    x_tolerance=payload.get("x_tolerance", 0.25),
                    angle_tolerance=payload.get("angle_tolerance", 5.0),
                    allow_reverse_align=payload.get("allow_reverse_align", True),
                    command_id=command_id,
                    source="single",
                )
            
            # elif cmd_type == "rail_exit":
            #     self.handle_rail_exit(
            #         command_id=command_id,
            #         source="single",
            #     )
            elif cmd_type == "rail_motor":
                cmd_type = payload.get("action")
                self.handle_rail_motor(
                    cmd_type = cmd_type,
                    command_id=command_id,
                    source="single",
                )

            elif cmd_type == "capture":
                label = payload.get("label", "manual_capture")
                self.handle_capture(
                    label=label,
                    command_id=command_id,
                    source="single",
                )

            elif cmd_type == "jog":
                vx = payload.get("vx", 0.0)
                wz = payload.get("wz", 0.0)
                self.handle_jog(vx, wz, command_id)

            elif cmd_type == "jog_stop":
                self.handle_jog_stop(command_id)

            elif cmd_type == "stop":
                self.handle_stop(command_id)

            elif cmd_type == "emergency_stop":
                self.handle_emergency_stop(command_id)

            elif cmd_type == "clear_emergency":
                self.handle_clear_emergency(command_id)

            elif cmd_type == "selected_rails":
                self.handle_selected_rails(payload, command_id)

            elif cmd_type == "mission_start":
                self.handle_mission_start(payload, command_id)

            elif cmd_type == "return_home":
                self.handle_return_home(command_id)

            elif cmd_type == "start_routine":
                self.handle_start_routine(payload, command_id)

            elif cmd_type == "stop_routine":
                self.handle_stop_routine(command_id)

            elif cmd_type == "save_pose":
                self.handle_save_pose(payload, command_id)

            else:
                self.publish_event("UNKNOWN_COMMAND", {
                    "command_id": command_id,
                    "cmd_type": cmd_type,
                })

        except Exception as e:
            self.get_logger().error(f"[CMD] handling error: {e}")
            self.mode = "ERROR"
            self.task_state = "ERROR"
            self.last_error = str(e)
            self.publish_event("COMMAND_ERROR", {
                "command_id": command_id,
                "error": str(e),
            })

    # ========================================================
    # TARGET POSE
    # ========================================================

    def resolve_target_pose(self, target):
        # target이 문자열이면 saved_poses에서 찾는다.
        if isinstance(target, str):
            return self.saved_poses.get(target)

        # target이 dict면 x, y, yaw를 직접 사용한다.
        if isinstance(target, dict):
            if "name" in target:
                return self.saved_poses.get(target["name"])

            return {
                "x": float(target.get("x", 0.0)),
                "y": float(target.get("y", 0.0)),
                "yaw": float(target.get("yaw", 0.0)),
            }

        return None

    def handle_save_pose(self, payload: dict, command_id=None):
        name = payload.get("name")

        if not name:
            self.publish_event("SAVE_POSE_FAILED", {
                "command_id": command_id,
                "reason": "name is required",
            })
            return

        target = payload.get("target")

        if target:
            pose = self.resolve_target_pose(target)
        else:
            pose = self.current_pose

        if pose is None:
            self.publish_event("SAVE_POSE_FAILED", {
                "command_id": command_id,
                "reason": "no pose available",
            })
            return

        self.saved_poses[name] = {
            "x": float(pose["x"]),
            "y": float(pose["y"]),
            "yaw": float(pose["yaw"]),
        }

        self.publish_event("POSE_SAVED", {
            "command_id": command_id,
            "name": name,
            "pose": self.saved_poses[name],
        })

    # ========================================================
    # BASIC COMMANDS
    # ========================================================

    def get_selected_rails_data(self, payload: dict) -> Optional[str]:
        data = payload.get("data")
        if isinstance(data, str) and data.strip():
            return data.strip()

        selected_rails = payload.get("selected_rails")
        if isinstance(selected_rails, list):
            rail_values = [
                str(rail_id).strip()
                for rail_id in selected_rails
                if str(rail_id).strip()
            ]
            if rail_values:
                return ",".join(rail_values)

        # mission_start의 commands 배열만 전달되는 경우도 지원
        commands = payload.get("commands")
        if isinstance(commands, list):
            for command in commands:
                if not isinstance(command, dict):
                    continue
                if command.get("ros_topic") != "/selected_rails":
                    continue
                command_data = command.get("data")
                if isinstance(command_data, str) and command_data.strip():
                    return command_data.strip()

        return None

    def publish_selected_rails(self, selected_rails: str):
        msg = String()
        msg.data = selected_rails
        self.selected_rails_pub.publish(msg)
        self.get_logger().info(
            f"[MISSION] selected rails published: {selected_rails}"
        )

    def handle_selected_rails(self, payload: dict, command_id=None):
        selected_rails = self.get_selected_rails_data(payload)
        if selected_rails is None:
            self.publish_event("SELECTED_RAILS_REJECTED", {
                "command_id": command_id,
                "reason": "selected rails list is empty",
            })
            return

        self.publish_selected_rails(selected_rails)
        self.publish_event("SELECTED_RAILS_PUBLISHED", {
            "command_id": command_id,
            "selected_rails": selected_rails,
        })

    def handle_mission_start(self, payload: dict, command_id=None):
        selected_rails = self.get_selected_rails_data(payload)
        if selected_rails is None:
            self.publish_event("MISSION_START_REJECTED", {
                "command_id": command_id,
                "reason": "selected rails list is empty",
            })
            return

        # WaitForMissionTrigger가 최신 목록을 먼저 처리할 시간을 준다.
        self.publish_selected_rails(selected_rails)

        def publish_trigger():
            msg = Bool()
            msg.data = True
            self.mission_trigger_pub.publish(msg)
            self.get_logger().info(
                f"[MISSION] start triggered: {selected_rails}"
            )
            self.publish_event("MISSION_START_TRIGGERED", {
                "command_id": command_id,
                "selected_rails": selected_rails,
            })

        self.create_timer_once(0.2, publish_trigger)

    def handle_return_home(self, command_id=None):
        # robot_agent가 직접 실행 중인 명령과 BT 복귀 동작이 충돌하지 않도록 정리
        self.routine_stop_requested = True
        self.routine_running = False
        self.routine_step_active = False
        self.active_routine = None
        self.current_step = None
        self.cancel_nav_goal()
        self.cancel_rail_goal()
        self.publish_cmd_vel(0.0, 0.0)

        msg = Bool()
        msg.data = True
        self.return_home_pub.publish(msg)
        self.get_logger().warning("[MISSION] return home requested")
        self.publish_event("RETURN_HOME_REQUESTED", {
            "command_id": command_id,
        })

    def handle_initial_pose(self, x: float, y: float, yaw: float, command_id=None):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.pose.pose.position.x = float(x)
        msg.pose.pose.position.y = float(y)
        msg.pose.pose.position.z = 0.0

        qz, qw = yaw_to_quaternion(float(yaw))
        msg.pose.pose.orientation.z = qz
        msg.pose.pose.orientation.w = qw

        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.0685

        self.initial_pose_pub.publish(msg)

        self.mode = "IDLE"
        self.task_state = "INITIAL_POSE_SET"

        self.publish_event("INITIAL_POSE_SET", {
            "command_id": command_id,
            "x": x,
            "y": y,
            "yaw": yaw,
        })

    def handle_stop(self, command_id=None):
        self.routine_stop_requested = True
        self.routine_running = False
        self.routine_step_active = False
        self.active_routine = None
        self.current_step = None

        self.cancel_nav_goal()
        self.cancel_rail_goal()

        self.publish_cmd_vel(0.0, 0.0)

        self.mode = "IDLE"
        self.task_state = "STOPPED"

        self.publish_event("STOPPED", {
            "command_id": command_id,
        })

    def handle_emergency_stop(self, command_id=None):
        self.routine_stop_requested = True
        self.routine_running = False
        self.routine_step_active = False
        self.active_routine = None
        self.current_step = None

        self.cancel_nav_goal()
        self.cancel_rail_goal()

        # 여러 번 0 publish
        for _ in range(3):
            self.publish_cmd_vel(0.0, 0.0)

        self.mode = "EMERGENCY_STOP"
        self.task_state = "EMERGENCY_STOP"

        self.publish_event("EMERGENCY_STOP", {
            "command_id": command_id,
        })

    def handle_clear_emergency(self, command_id=None):
        self.publish_cmd_vel(0.0, 0.0)

        self.mode = "IDLE"
        self.task_state = "READY"
        self.last_error = None

        self.publish_event("EMERGENCY_CLEARED", {
            "command_id": command_id,
        })

    # ========================================================
    # JOG
    # ========================================================

    def handle_jog(self, vx: float, wz: float, command_id=None):
        # 수동 조작은 기존 자동 명령을 끊는다.
        if self.mode == "AUTO":
            self.handle_stop_routine(command_id)

        self.cancel_nav_goal()
        self.cancel_rail_goal()

        self.mode = "MANUAL"
        self.task_state = "JOGGING"

        self.last_jog_time = now_ts()
        self.publish_cmd_vel(vx, wz)

    def handle_jog_stop(self, command_id=None):
        self.publish_cmd_vel(0.0, 0.0)

        self.mode = "IDLE"
        self.task_state = "READY"

        self.publish_event("JOG_STOPPED", {
            "command_id": command_id,
        })

    def safety_tick(self):
        # jog 명령이 끊기면 자동 정지
        if self.mode == "MANUAL" and self.task_state == "JOGGING":
            elapsed = now_ts() - self.last_jog_time

            if elapsed > self.jog_timeout_sec:
                self.publish_cmd_vel(0.0, 0.0)
                self.mode = "IDLE"
                self.task_state = "READY"
                self.publish_event("JOG_TIMEOUT_STOP", {
                    "elapsed": elapsed,
                })

    # ========================================================
    # NAV2 ACTION
    # ========================================================

    def handle_navigate_to(
        self,
        x: float,
        y: float,
        yaw: float,
        command_id=None,
        source="single",
    ):
        # rail approach 중이면 취소
        self.cancel_rail_goal()

        # jog 중일 수 있으니 먼저 정지
        self.publish_cmd_vel(0.0, 0.0)

        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.task_state = "NAV_SERVER_NOT_AVAILABLE"
            self.publish_event("NAV_SERVER_NOT_AVAILABLE", {
                "command_id": command_id,
                "source": source,
            })
            self.finish_current_step(False, "nav server not available")
            return

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        goal_msg.pose.pose.position.x = float(x)
        goal_msg.pose.pose.position.y = float(y)
        goal_msg.pose.pose.position.z = 0.0

        qz, qw = yaw_to_quaternion(float(yaw))
        goal_msg.pose.pose.orientation.z = qz
        goal_msg.pose.pose.orientation.w = qw

        self.nav_command_id = command_id
        self.nav_active = True
        self.nav_result_data = None

        if source == "routine":
            self.mode = "AUTO"
        else:
            self.mode = "IDLE"

        self.task_state = "SENDING_NAV_GOAL"

        send_future = self.nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self.nav_feedback_callback,
        )
        send_future.add_done_callback(self.nav_goal_response_callback)

        self.publish_event("NAV_GOAL_SENT", {
            "command_id": command_id,
            "source": source,
            "x": x,
            "y": y,
            "yaw": yaw,
        })

    def nav_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.distance_remaining = float(feedback.distance_remaining)
        self.task_state = "NAVIGATING"

    def nav_goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.nav_goal_handle = None
            self.nav_active = False
            self.task_state = "NAV_GOAL_REJECTED"

            self.publish_event("NAV_GOAL_REJECTED", {
                "command_id": self.nav_command_id,
            })

            self.finish_current_step(False, "nav goal rejected")
            return

        self.nav_goal_handle = goal_handle
        self.task_state = "NAV_GOAL_ACCEPTED"

        self.publish_event("NAV_GOAL_ACCEPTED", {
            "command_id": self.nav_command_id,
        })

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.nav_result_callback)

    def nav_result_callback(self, future):
        result = future.result()
        status = result.status

        success = status == GoalStatus.STATUS_SUCCEEDED

        if success:
            event = "NAV_GOAL_SUCCEEDED"
            reason = "succeeded"
        else:
            event = "NAV_GOAL_FINISHED"
            reason = f"status={status}"

        self.nav_goal_handle = None
        self.nav_active = False
        self.distance_remaining = None

        self.publish_cmd_vel(0.0, 0.0)

        self.nav_result_data = {
            "success": success,
            "status": status,
            "reason": reason,
        }

        self.publish_event(event, {
            "command_id": self.nav_command_id,
            "status": status,
            "success": success,
        })

        self.finish_current_step(success, reason)

        if not self.routine_running and self.mode != "EMERGENCY_STOP":
            self.mode = "IDLE"
            self.task_state = "READY" if success else "ERROR"

    def cancel_nav_goal(self):
        if self.nav_goal_handle is not None:
            try:
                self.nav_goal_handle.cancel_goal_async()
            except Exception as e:
                self.get_logger().warn(f"[NAV] cancel error: {e}")

            self.nav_goal_handle = None

        self.nav_active = False
        self.distance_remaining = None

    # ========================================================
    # RAIL APPROACH ACTION
    # ========================================================

    def handle_rail_approach(
        self,
        timeout_sec: float = 60.0,
        x_tolerance: float = 0.08,
        angle_tolerance: float = 1.0,
        allow_reverse_align: bool = True,
        command_id=None,
        source="single",
    ):
        # Nav2 goal이 살아있으면 취소
        self.cancel_nav_goal()

        # jog 중일 수 있으니 정지
        self.publish_cmd_vel(0.0, 0.0)

        if not self.rail_client.wait_for_server(timeout_sec=2.0):
            self.task_state = "RAIL_SERVER_NOT_AVAILABLE"
            self.publish_event("RAIL_SERVER_NOT_AVAILABLE", {
                "command_id": command_id,
                "source": source,
            })
            self.finish_current_step(False, "rail server not available")
            return

        goal_msg = RailApproach.Goal()
        goal_msg.timeout_sec = float(timeout_sec)
        goal_msg.x_tolerance = float(x_tolerance)
        goal_msg.angle_tolerance = float(angle_tolerance)
        goal_msg.allow_reverse_align = bool(allow_reverse_align)

        self.rail_command_id = command_id
        self.rail_active = True
        self.rail_result_data = None

        self.rail_feedback = {
            "state": None,
            "x_error": None,
            "angle_error": None,
            "distance": None,
        }

        if source == "routine":
            self.mode = "AUTO"
        else:
            self.mode = "IDLE"

        self.task_state = "RAIL_SENDING_GOAL"

        send_future = self.rail_client.send_goal_async(
            goal_msg,
            feedback_callback=self.rail_feedback_callback,
        )
        send_future.add_done_callback(self.rail_goal_response_callback)

        self.publish_event("RAIL_GOAL_SENT", {
            "command_id": command_id,
            "source": source,
            "timeout_sec": goal_msg.timeout_sec,
            "x_tolerance": goal_msg.x_tolerance,
            "angle_tolerance": goal_msg.angle_tolerance,
            "allow_reverse_align": goal_msg.allow_reverse_align,
        })

    def rail_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.rail_feedback = {
            "state": feedback.state,
            "x_error": float(feedback.x_error),
            "angle_error": float(feedback.angle_error),
            "distance": feedback.distance,
        }

        self.task_state = f"RAIL_{feedback.state}"

        # feedback을 너무 자주 MQTT로 쏘면 부담될 수 있음.
        # 필요하면 0.5초 throttle 추가 가능.
        self.publish_event("RAIL_FEEDBACK", {
            "command_id": self.rail_command_id,
            "rail_state": feedback.state,
            "x_error": float(feedback.x_error),
            "angle_error": float(feedback.angle_error),
            "distance": feedback.distance,
        }, qos=0)

    def rail_goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.rail_goal_handle = None
            self.rail_active = False
            self.task_state = "RAIL_GOAL_REJECTED"

            self.publish_event("RAIL_GOAL_REJECTED", {
                "command_id": self.rail_command_id,
            })

            self.finish_current_step(False, "rail goal rejected")
            return

        self.rail_goal_handle = goal_handle
        self.task_state = "RAIL_GOAL_ACCEPTED"

        self.publish_event("RAIL_GOAL_ACCEPTED", {
            "command_id": self.rail_command_id,
        })

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.rail_result_callback)

    def rail_result_callback(self, future):
        result = future.result()
        status = result.status
        rail_result = result.result

        success = status == GoalStatus.STATUS_SUCCEEDED and bool(rail_result.success)

        if success:
            event = "RAIL_SUCCEEDED"
            reason = rail_result.reason
        else:
            event = "RAIL_FINISHED"
            reason = rail_result.reason

        self.rail_goal_handle = None
        self.rail_active = False

        self.publish_cmd_vel(0.0, 0.0)

        self.rail_result_data = {
            "success": success,
            "status": status,
            "reason": reason,
        }

        self.publish_event(event, {
            "command_id": self.rail_command_id,
            "status": status,
            "success": success,
            "reason": reason,
        })

        self.finish_current_step(success, reason)

        if not self.routine_running and self.mode != "EMERGENCY_STOP":
            self.mode = "IDLE"
            self.task_state = "READY" if success else "ERROR"

    def cancel_rail_goal(self):
        if self.rail_goal_handle is not None:
            try:
                self.rail_goal_handle.cancel_goal_async()
            except Exception as e:
                self.get_logger().warn(f"[RAIL] cancel error: {e}")

            self.rail_goal_handle = None

        self.rail_active = False

    # def handle_rail_exit(self, command_id=None, source="single"):
    #     # Nav2 goal이나 rail approach가 살아있으면 먼저 정리
    #     self.cancel_nav_goal()
    #     self.cancel_rail_goal()

    #     # 혹시 jog/nav 속도 명령이 남아있을 수 있으니 정지
    #     self.publish_cmd_vel(0.0, 0.0)

    #     msg = String()
    #     msg.data = "EXIT"
    #     self.rail_cmd_pub.publish(msg)

    #     if source == "routine":
    #         self.mode = "AUTO"
    #     else:
    #         self.mode = "IDLE"

    #     self.task_state = "RAIL_EXIT_SENT"

    #     self.publish_event("RAIL_EXIT_SENT", {
    #         "command_id": command_id,
    #         "source": source,
    #         "cmd": "EXIT",
    #         "topic": "/rail_command",
    #     })

    #     # 단일 명령이면 여기서 끝
    #     # 루틴 step으로 실행된 경우 다음 step으로 넘어가게 처리
    #     self.finish_current_step(True, "rail exit command sent")
    def handle_rail_motor(self, cmd_type=None,command_id=None, source="single"):
        # Nav2 goal이나 rail approach가 살아있으면 먼저 정리
        self.cancel_nav_goal()
        self.cancel_rail_goal()

        # 혹시 jog/nav 속도 명령이 남아있을 수 있으니 정지
        self.publish_cmd_vel(0.0, 0.0)

        msg = String()
        msg.data = cmd_type
        self.rail_cmd_pub.publish(msg)




    # ========================================================
    # CAPTURE SERVICE
    # ========================================================

    def handle_capture(
        self,
        label: str = "capture",
        command_id=None,
        source="single",
    ):
        self.publish_cmd_vel(0.0, 0.0)

        if not self.capture_client.wait_for_service(timeout_sec=1.0):
            self.task_state = "CAPTURE_SERVER_NOT_AVAILABLE"
            self.publish_event("CAPTURE_SERVER_NOT_AVAILABLE", {
                "command_id": command_id,
                "label": label,
                "source": source,
            })
            self.finish_current_step(False, "capture server not available")
            return

        self.capture_command_id = command_id
        self.capture_active = True
        self.capture_result_data = None

        if source == "routine":
            self.mode = "AUTO"
        else:
            self.mode = "IDLE"

        self.task_state = "CAPTURING"

        req = Trigger.Request()

        future = self.capture_client.call_async(req)
        future.add_done_callback(
            lambda f: self.capture_result_callback(f, label)
        )

        self.publish_event("CAPTURE_REQUESTED", {
            "command_id": command_id,
            "label": label,
            "source": source,
            "pose": self.current_pose,
        })

    def capture_result_callback(self, future, label: str):
        try:
            res = future.result()
            success = bool(res.success)
            message = res.message
        except Exception as e:
            success = False
            message = str(e)

        self.capture_active = False

        self.capture_result_data = {
            "success": success,
            "message": message,
            "label": label,
            "pose": self.current_pose,
        }

        event = "IMAGE_CAPTURED" if success else "CAPTURE_FAILED"

        self.publish_event(event, {
            "command_id": self.capture_command_id,
            "success": success,
            "message": message,
            "label": label,
            "pose": self.current_pose,
        })

        self.finish_current_step(success, message)

        if not self.routine_running and self.mode != "EMERGENCY_STOP":
            self.mode = "IDLE"
            self.task_state = "READY" if success else "ERROR"

    # ========================================================
    # ROUTINE
    # ========================================================

    def handle_start_routine(self, payload: dict, command_id=None):
        routine = payload.get("routine")
        routine_id = payload.get("routine_id", "manual_routine")

        if not isinstance(routine, list) or len(routine) == 0:
            self.publish_event("ROUTINE_START_FAILED", {
                "command_id": command_id,
                "reason": "routine must be non-empty list",
            })
            return

        # 기존 동작 정리
        self.cancel_nav_goal()
        self.cancel_rail_goal()
        self.publish_cmd_vel(0.0, 0.0)

        self.active_routine = routine
        self.routine_id = routine_id
        self.routine_command_id = command_id
        self.routine_index = 0
        self.routine_running = True
        self.routine_step_active = False
        self.routine_stop_requested = False
        self.current_step = None

        self.mode = "AUTO"
        self.task_state = "ROUTINE_STARTED"

        self.publish_event("ROUTINE_STARTED", {
            "command_id": command_id,
            "routine_id": routine_id,
            "total_steps": len(routine),
        })

    def handle_stop_routine(self, command_id=None):
        self.routine_stop_requested = True
        self.routine_running = False
        self.routine_step_active = False
        self.active_routine = None
        self.current_step = None

        self.cancel_nav_goal()
        self.cancel_rail_goal()
        self.publish_cmd_vel(0.0, 0.0)

        self.mode = "IDLE"
        self.task_state = "ROUTINE_STOPPED"

        self.publish_event("ROUTINE_STOPPED", {
            "command_id": command_id,
        })

    def routine_tick(self):
        if not self.routine_running:
            return

        if self.mode == "EMERGENCY_STOP":
            return

        if self.routine_stop_requested:
            self.handle_stop_routine(self.routine_command_id)
            return

        if self.active_routine is None:
            return

        # 현재 step이 실행 중이면 기다림
        if self.routine_step_active:
            return

        # 모든 step 완료
        if self.routine_index >= len(self.active_routine):
            self.publish_cmd_vel(0.0, 0.0)

            self.publish_event("ROUTINE_FINISHED", {
                "command_id": self.routine_command_id,
                "routine_id": self.routine_id,
                "total_steps": len(self.active_routine),
            })

            self.mode = "IDLE"
            self.task_state = "READY"

            self.routine_running = False
            self.active_routine = None
            self.current_step = None
            return

        # 다음 step 실행
        step = self.active_routine[self.routine_index]
        self.current_step = step
        self.routine_step_active = True

        step_type = step.get("type")
        step_command_id = f"{self.routine_command_id}_step_{self.routine_index}"

        self.publish_event("ROUTINE_STEP_STARTED", {
            "command_id": self.routine_command_id,
            "routine_id": self.routine_id,
            "step_index": self.routine_index,
            "step": step,
        })

        if step_type == "navigate_to":
            target = step.get("target")
            target_pose = self.resolve_target_pose(target)

            if target_pose is None:
                self.finish_current_step(False, f"unknown target: {target}")
                return

            self.handle_navigate_to(
                target_pose["x"],
                target_pose["y"],
                target_pose["yaw"],
                step_command_id,
                source="routine",
            )

        elif step_type == "rail_approach":
            self.handle_rail_approach(
                timeout_sec=step.get("timeout_sec", 60.0),
                x_tolerance=step.get("x_tolerance", 0.08),
                angle_tolerance=step.get("angle_tolerance", 1.0),
                allow_reverse_align=step.get("allow_reverse_align", True),
                command_id=step_command_id,
                source="routine",
            )

        elif step_type == "capture":
            self.handle_capture(
                label=step.get("label", f"step_{self.routine_index}"),
                command_id=step_command_id,
                source="routine",
            )

        elif step_type == "wait":
            duration = float(step.get("duration_sec", 1.0))
            self.create_timer_once(
                duration,
                lambda: self.finish_current_step(True, f"waited {duration} sec")
            )

        else:
            self.finish_current_step(False, f"unknown step type: {step_type}")

    def finish_current_step(self, success: bool, reason: str):
        # 루틴 step이 실행 중일 때만 처리
        if not self.routine_running or not self.routine_step_active:
            return

        step = self.current_step or {}
        continue_on_fail = bool(step.get("continue_on_fail", False))

        self.publish_event("ROUTINE_STEP_FINISHED", {
            "command_id": self.routine_command_id,
            "routine_id": self.routine_id,
            "step_index": self.routine_index,
            "success": success,
            "reason": reason,
            "step": step,
        })

        self.routine_step_active = False

        if success or continue_on_fail:
            self.routine_index += 1
            self.task_state = "ROUTINE_NEXT_STEP"
        else:
            self.publish_cmd_vel(0.0, 0.0)

            self.publish_event("ROUTINE_FAILED", {
                "command_id": self.routine_command_id,
                "routine_id": self.routine_id,
                "failed_step_index": self.routine_index,
                "reason": reason,
                "step": step,
            })

            self.routine_running = False
            self.active_routine = None
            self.current_step = None

            self.mode = "ERROR"
            self.task_state = "ROUTINE_FAILED"
            self.last_error = reason

    def create_timer_once(self, delay_sec: float, callback):
        # rclpy에는 one-shot timer가 따로 없으므로 간단히 구현
        timer_holder = {"timer": None}

        def _wrapper():
            timer_holder["timer"].cancel()
            callback()

        timer_holder["timer"] = self.create_timer(delay_sec, _wrapper)

    # ========================================================
    # CMD_VEL
    # ========================================================

    def publish_cmd_vel(self, vx: float, wz: float):
        vx = max(min(float(vx), self.max_jog_vx), -self.max_jog_vx)
        wz = max(min(float(wz), self.max_jog_wz), -self.max_jog_wz)

        self.last_jog_vx = vx
        self.last_jog_wz = wz

        msg = Twist()
        msg.linear.x = vx
        msg.angular.z = wz
        self.cmd_vel_pub.publish(msg)

    # ========================================================
    # STATUS / EVENT / HEALTH
    # ========================================================

    def publish_status(self):
        payload = {
            "robot_id": ROBOT_ID,
            "mode": self.mode,
            "task_state": self.task_state,
            "pose": self.current_pose,
            "distance_remaining": self.distance_remaining,
            "rail_feedback": self.rail_feedback,
            "routine": {
                "routine_id": self.routine_id,
                "running": self.routine_running,
                "index": self.routine_index,
                "total": len(self.active_routine) if self.active_routine else 0,
                "current_step": self.current_step,
            },
            "last_event": self.last_event,
            "last_error": self.last_error,
            "mqtt_connected": self.mqtt_connected,
            "stamp": now_ts(),
        }

        self.mqtt_publish_json(TOPIC_STATUS, payload)

    def publish_health(self):
        nav_available = self.nav_client.server_is_ready()
        rail_available = self.rail_client.server_is_ready()
        capture_available = self.capture_client.service_is_ready()

        localization_ok = self.current_pose is not None

        payload = {
            "robot_id": ROBOT_ID,
            "mode": self.mode,
            "task_state": self.task_state,
            "mqtt_connected": self.mqtt_connected,
            "nav2_available": bool(nav_available),
            "rail_server_available": bool(rail_available),
            "capture_server_available": bool(capture_available),
            "localization_ok": bool(localization_ok),
            "pose_available": self.current_pose is not None,
            "stamp": now_ts(),
        }

        self.mqtt_publish_json(TOPIC_HEALTH, payload)

    def publish_event(self, event: str, extra: Optional[dict] = None, qos: int = 1):
        self.last_event = event

        payload = {
            "robot_id": ROBOT_ID,
            "event": event,
            "mode": self.mode,
            "task_state": self.task_state,
            "stamp": now_ts(),
        }

        if extra:
            payload.update(extra)

        self.mqtt_publish_json(TOPIC_EVENT, payload, qos=qos)


# ============================================================
# MAIN
# ============================================================

def main():
    rclpy.init()

    node = RobotAgent()
    node.start_mqtt()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.publish_cmd_vel(0.0, 0.0)
        node.publish_event("ROBOT_AGENT_SHUTDOWN")

        try:
            node.mqtt_client.loop_stop()
            node.mqtt_client.disconnect()
        except Exception:
            pass

        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
