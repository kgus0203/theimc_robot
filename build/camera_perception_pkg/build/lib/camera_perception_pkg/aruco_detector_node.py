import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from cv_bridge import CvBridge
import cv2
import numpy as np
import tf_transformations  

class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__('aruco_detector_node')

        # --- 파라미터 선언 ---
        self.declare_parameter('image_topic', '/image_raw')
        self.declare_parameter('pose_topic', '/aruco_pose')
        self.declare_parameter('marker_size', 0.10)  # 마커의 실제 물리적 크기 (단위: 미터, 예: 10cm)
        self.declare_parameter('marker_id_to_detect', 0)  # 충전 스테이션에 부착된 마커 ID

        self.image_topic = self.get_parameter('image_topic').value
        self.pose_topic = self.get_parameter('pose_topic').value
        self.marker_size = self.get_parameter('marker_size').value
        self.target_id = self.get_parameter('marker_id_to_detect').value

        # --- [필수] 카메라 캘리브레이션 파라미터 입력 ---
        # RealSense D435 기본 해상도(640x480) 기준 예시 값입니다. 
        # 실제 카메라의 Calibration 값을 넣어야 mm 단위의 정밀 제어가 가능합니다.
        self.camera_matrix = np.array([[530.0,   0.0, 320.0],
                                       [  0.0, 530.0, 240.0],
                                       [  0.0,   0.0,   1.0]], dtype=np.float32)
        self.dist_coeffs = np.zeros((5, 1), dtype=np.float32)  # 왜곡 계수 [k1, k2, p1, p2, k3]

        # --- ROS 2 구성 ---
        self.bridge = CvBridge()
        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=1
        )
        self.subscription = self.create_subscription(
            Image, 
            self.image_topic, 
            self.image_callback, 
            self.qos_profile 
        )
        self.pose_pub = self.create_publisher(PoseStamped, self.pose_topic, 10)

        # ArUco 사전 정의 및 파라미터 (DICT_6X6_250 권장)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.aruco_params = cv2.aruco.DetectorParameters()
        
        # OpenCV 4.7.0 이상 대응 객체 생성
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        # 3D 마커 코너 좌표 정의 (마커 중심 기준)
        s = self.marker_size / 2.0
        self.marker_3d_edges = np.array([
            [-s,  s, 0],  # 좌상단
            [ s,  s, 0],  # 우상단
            [ s, -s, 0],  # 우하단
            [-s, -s, 0]   # 좌하단
        ], dtype=np.float32)

        self.get_logger().info(f"ArucoDetectorNode started. Target ID: {self.target_id}")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # 마커 검출
        corners, ids, rejected = self.detector.detectMarkers(gray)

        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id == self.target_id:
                    # solvePnP를 이용한 3D Pose 추정 (회전 벡터 rvec, 평행이동 벡터 tvec)
                    success, rvec, tvec = cv2.solvePnP(
                        self.marker_3d_edges, 
                        corners[i][0], 
                        self.camera_matrix, 
                        self.dist_coeffs
                    )

                    if success:
                        # 3D 거리 좌표 (카메라 기준 마커의 위치)
                        x, y, z = tvec[0][0], tvec[1][0], tvec[2][0]

                        # rvec(로드리게스 벡터)을 쿼터니언 회전 정보로 변환
                        rmat, _ = cv2.Rodrigues(rvec)
                        # tf_transformations를 사용한 변환 예시
                        # (모듈이 없을 경우 아래 yaw, pitch, roll 공식을 커스텀 적용 가능)
                        transform_matrix = np.eye(4)
                        transform_matrix[:3, :3] = rmat
                        quat = tf_transformations.quaternion_from_matrix(transform_matrix)

                        # PoseStamped 메시지 퍼블리시
                        pose_msg = PoseStamped()
                        pose_msg.header = msg.header
                        pose_msg.pose.position.x = float(x)
                        pose_msg.pose.position.y = float(y)
                        pose_msg.pose.position.z = float(z)
                        pose_msg.pose.orientation.x = quat[0]
                        pose_msg.pose.orientation.y = quat[1]
                        pose_msg.pose.orientation.z = quat[2]
                        pose_msg.pose.orientation.w = quat[3]

                        self.pose_pub.publish(pose_msg)

                        # 디버그 로그 (X, Y, Z 거리 출력)
                        self.get_logger().info(
                            f"Marker Found! ID: {marker_id} | dist(m) -> X:{x:.3f}, Y:{y:.3f}, Z(거리):{z:.3f}",
                            throttle_duration_sec=0.5
                        )

                        # 카메라 피드 시각화 (옵션)
                        cv2.drawFrameAxes(cv_image, self.camera_matrix, self.dist_coeffs, rvec, tvec, 0.05)
                        cv2.aruco.drawDetectedMarkers(cv_image, corners)
                        
        # 필요 시 디버그용 이미지 윈도우 활성화
        # cv2.imshow("ArUco Debug", cv_image)
        # cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()