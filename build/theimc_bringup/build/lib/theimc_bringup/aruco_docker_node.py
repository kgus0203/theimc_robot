import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from std_srvs.srv import SetBool  # 서비스 타입 추가

class ArucoDockerNode(Node):
    def __init__(self):
        super().__init__('aruco_docker_node')

        # --- [0] 도킹 활성화 상태 플래그 (기본값: False) ---
        self.is_docking_active = False

        # --- [1] 목표 위치 파라미터 (카메라 좌표계 기준, 단위: m) ---
        self.target_z = 0.025  # 카메라 앞 2.5cm
        self.target_x = 0.016  # 카메라 우측 1.6cm
        
        # --- [2] 제어 허용 오차 (Tolerance) ---
        self.tol_z = 0.005  # 거리 오차 허용범위: 5mm
        self.tol_x = 0.005  # 좌우 오차 허용범위: 5mm
        
        # --- [3] P 제어기 게인(Gain) 및 속도 제한 ---
        self.k_linear = 0.8
        self.k_angular = 2.0
        
        self.max_linear_vel = 0.15   # 최대 직진 속도 (m/s)
        self.max_angular_vel = 0.30  # 최대 회전 속도 (rad/s)

        # 토픽 구독 및 퍼블리시
        self.subscription = self.create_subscription(
            PoseStamped,
            '/aruco_pose',
            self.pose_callback,
            10
        )
        
        # 추후 twist_mux 사용 시 '/cmd_vel'을 '/dock_vel' 등으로 변경하세요.
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # --- [4] 서비스 서버 생성 ---
        self.srv = self.create_service(
            SetBool, 
            'toggle_docking', 
            self.toggle_callback
        )

        self.get_logger().info("Aruco Docker Node Started! (Status: Standby)")

    def toggle_callback(self, request, response):
        """
        도킹 모드를 켜거나 끄는 서비스 콜백 함수
        """
        self.is_docking_active = request.data
        
        if self.is_docking_active:
            self.get_logger().info("▶️ 도킹 모드가 활성화되었습니다.")
            response.message = "Docking activated"
        else:
            self.get_logger().info("⏸️ 도킹 모드가 비활성화되었습니다. 로봇을 정지합니다.")
            # 비활성화 시 즉시 로봇 정지 명령 발행
            stop_cmd = Twist()
            self.cmd_pub.publish(stop_cmd)
            response.message = "Docking deactivated and robot stopped"
            
        response.success = True
        return response

    def pose_callback(self, msg):
        # 도킹 모드가 비활성화 상태면 아무 행동도 하지 않고 리턴
        if not self.is_docking_active:
            return

        current_z = msg.pose.position.z
        current_x = msg.pose.position.x
        
        # 오차(Error) 계산
        error_z = current_z - self.target_z
        error_x = current_x - self.target_x
        
        cmd = Twist()
        
        # 목표 위치 도달 확인
        if abs(error_z) <= self.tol_z and abs(error_x) <= self.tol_x:
            self.get_logger().info("✅ 도킹 완료! 목표 위치에 도달했습니다.", throttle_duration_sec=1.0)
            self.cmd_pub.publish(cmd)  # 모든 속도 0으로 정지
            
            # 도킹 완료 후 안전을 위해 스스로 비활성화
            self.is_docking_active = False 
            self.get_logger().info("도킹이 완료되어 도킹 모드를 자동 대기상태로 전환합니다.")
            return
            
        # P 제어 (비례 제어) 수식 적용
        raw_linear_x = self.k_linear * error_z
        raw_angular_z = -self.k_angular * error_x
        
        # 속도 제한 (클램핑)
        cmd.linear.x = max(min(raw_linear_x, self.max_linear_vel), -self.max_linear_vel)
        cmd.angular.z = max(min(raw_angular_z, self.max_angular_vel), -self.max_angular_vel)
        
        self.cmd_pub.publish(cmd)
        
        # 디버그용 출력
        self.get_logger().info(
            f"Err Z: {error_z:.3f}m, Err X: {error_x:.3f}m | Cmd V: {cmd.linear.x:.3f}, W: {cmd.angular.z:.3f}",
            throttle_duration_sec=0.5
        )

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDockerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 종료 시 로봇 정지
        stop_cmd = Twist()
        node.cmd_pub.publish(stop_cmd)
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()