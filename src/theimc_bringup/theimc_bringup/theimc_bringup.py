import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist, PoseStamped, TransformStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
import math
import serial
import time
import sys

def quaternion_from_euler(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    q = [0] * 4
    q[0] = cy * cp * sr - sy * sp * cr
    q[1] = sy * cp * sr + cy * sp * cr
    q[2] = sy * cp * cr - cy * sp * sr
    q[3] = cy * cp * cr + sy * sp * sr
    return q

class OdomPose(object):
    x = 0.0
    y = 0.0
    theta = 0.0

class Joint:
    def __init__(self):
        self.joint_name = ['wheel_left_joint', 'wheel_right_joint']
        self.joint_pos = [0.0, 0.0]
        self.joint_vel = [0.0, 0.0]

class BringUp(Node):
    def __init__(self):
        super().__init__('bring_up')
        
        # --- 시리얼 포트 설정 ---
        self.serial_port = "/dev/stm32_link" 
        self.baud_rate = 576000
        self.serial_timeout = 0.1

        try:
            self.pico_serial = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=self.serial_timeout
            )
            self.pico_serial.reset_input_buffer()
            self.pico_serial.reset_output_buffer()
            self.get_logger().info(f"Connected to {self.serial_port}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial: {e}")
            sys.exit(1)
            
        # --- 로봇 파라미터 ---
        self.wheel_separation = 1.0
        self.wheel_radius = 0.085
        self.max_lin_vel_x = 0.5
        self.max_ang_vel_z = 1.0

        # --- 변수 초기화 ---
        self.odom_pose = OdomPose()
        self.joint = Joint()
        self.timestamp_previous = self.get_clock().now()
        
        # [중요] 안전장치용: 마지막으로 명령 받은 시간
        self.last_cmd_time = time.time()

        # QoS 설정
        qos_profile = QoSProfile(
            depth=20,
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST
        )

        # Subscriber & Publisher
        self.sub_cmd_vel = self.create_subscription(Twist, 'cmd_vel', self.cb_cmd_vel_msg, qos_profile)
        self.sub_rail_cmd = self.create_subscription(String, 'rail_command', self.cb_rail_cmd_msg, qos_profile)
        self.pub_rail_status = self.create_publisher(String, 'rail_status', qos_profile)
        self.pub_joint_states = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.pub_odom = self.create_publisher(Odometry, 'odom', qos_profile)
        self.pub_odom_tf = TransformBroadcaster(self)

        self.create_timer(0.05, self.update_robot)


    def cb_cmd_vel_msg(self, cmd_vel_msg):
        #self.last_cmd_time = time.time() # 명령 받은 시간 갱신

        vx = cmd_vel_msg.linear.x
        wz = cmd_vel_msg.angular.z

        # 데드존 처리
        if abs(vx) < 0.01: vx = 0.0
        if abs(wz) < 0.01: wz = 0.0

        # 속도 제한
        vx = max(-self.max_lin_vel_x, min(self.max_lin_vel_x, vx))
        wz = max(-self.max_ang_vel_z, min(self.max_ang_vel_z, wz))

        # [수정] 값이 변했는지 확인하지 않고 무조건 전송 (패킷 손실 방지)
        self.send_serial_command("CMD", vx, wz)

    def cb_rail_cmd_msg(self, msg):
        command = msg.data.strip().upper() # 대소문자 무방하도록 처리
        
        if command == "DETECTED":
            try:
                # STM32 파싱 형태에 맞춰 패킷 뒤에 \n을 붙여 송신
                self.pico_serial.write(b"DETECTED\n")
                self.get_logger().info("Sent [DETECTED] command to STM32.")
            except serial.SerialException as e:
                self.get_logger().error(f"Failed to send DETECTED: {e}")
                
        elif command == "BACK":
            try:
                self.pico_serial.write(b"BACK\n")
                self.get_logger().info("Sent [BACK] command to STM32.")
            except serial.SerialException as e:
                self.get_logger().error(f"Failed to send BACK: {e}")

        elif command == "FORWARD":
            try:
                self.pico_serial.write(b"FORWARD\n")
                self.get_logger().info("Sent [FORWARD] command to STM32.")
            except serial.SerialException as e:
                self.get_logger().error(f"Failed to send FORWARD: {e}")
        
        elif command == "STOP":
            try:
                self.pico_serial.write(b"STOP\n")
                self.get_logger().info("Sent [STOP] command to STM32.")
            except serial.SerialException as e:
                self.get_logger().error(f"Failed to send STOP: {e}")
        else:
            self.get_logger().warn(f"Unknown rail command received: {command}")


    def send_serial_command(self, cmd_type, val1, val2):
        try:
            cmd = f"{cmd_type},{val1:.3f},{val2:.3f}\n"
            self.pico_serial.write(cmd.encode('utf-8'))
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write failed: {e}")

    def update_robot(self):
        """STM32 데이터 수신 및 Odom 발행"""
        self.timestamp_now = self.get_clock().now()
        dt = (self.timestamp_now - self.timestamp_previous).nanoseconds * 1e-9

        if self.pico_serial.in_waiting > 0:
            try:
                latest_odom_line = None
                
                while self.pico_serial.in_waiting > 0:
                    line = self.pico_serial.readline().decode('utf-8', errors='ignore').strip()
                    if "ODOM" in line:
                        latest_odom_line = line

                    elif "STATE" in line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            status_msg = String()
                            status_msg.data = parts[1].strip()
                            self.pub_rail_status.publish(status_msg)
                            self.get_logger().info(f"Published rail status: {status_msg.data}")

                # 최신 ODOM 데이터가 존재할 경우에만 파싱 및 Publish 진행
                if latest_odom_line:
                    parts = latest_odom_line.split(',')
                    
                    if len(parts) >= 6:
                        try:
                            idx = parts.index("ODOM")
                            self.odom_pose.x = float(parts[idx+1])
                            self.odom_pose.y = float(parts[idx+2])
                            self.odom_pose.theta = float(parts[idx+3])
                            v = float(parts[idx+4])
                            w = float(parts[idx+5])

                            # 최신 데이터로 업데이트
                            self.publish_odometry(v, w)
                            self.update_joint_states(v, w, dt)
                            self.timestamp_previous = self.timestamp_now
                            
                        except (ValueError, IndexError):
                            pass # 파싱 에러 시 무시하고 넘어감
                            
            except Exception as e:
                self.get_logger().warn(f"Receive error: {e}")
    def publish_odometry(self, v, w):
        q = quaternion_from_euler(0, 0, self.odom_pose.theta)
        
        # Odom Msg
        odom = Odometry()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_footprint"
        odom.header.stamp = self.timestamp_now.to_msg()
        odom.pose.pose.position.x = self.odom_pose.x
        odom.pose.pose.position.y = self.odom_pose.y
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = w
        self.pub_odom.publish(odom)

        # TF
        tf = TransformStamped()
        tf.header.frame_id = "odom"
        tf.child_frame_id = "base_footprint"
        tf.header.stamp = self.timestamp_now.to_msg()
        tf.transform.translation.x = self.odom_pose.x
        tf.transform.translation.y = self.odom_pose.y
        tf.transform.translation.z = 0.0
        tf.transform.rotation.x = q[0]
        tf.transform.rotation.y = q[1]
        tf.transform.rotation.z = q[2]
        tf.transform.rotation.w = q[3]
        self.pub_odom_tf.sendTransform(tf)

    def update_joint_states(self, v, w, dt):
        vl = v - (w * self.wheel_separation / 2.0)
        vr = v + (w * self.wheel_separation / 2.0)
        wl = vl / self.wheel_radius
        wr = vr / self.wheel_radius

        self.joint.joint_pos[0] += wl * dt
        self.joint.joint_pos[1] += wr * dt
        self.joint.joint_vel = [wl, wr]

        msg = JointState()
        msg.header.stamp = self.timestamp_now.to_msg()
        msg.header.frame_id = "base_link"
        msg.name = self.joint.joint_name
        msg.position = self.joint.joint_pos
        msg.velocity = self.joint.joint_vel
        self.pub_joint_states.publish(msg)

    def _send_stop_commands(self):
        self.send_serial_command("CMD", 0.0, 0.0)

def main(args=None):
    rclpy.init(args=args)
    node = BringUp()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._send_stop_commands()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
