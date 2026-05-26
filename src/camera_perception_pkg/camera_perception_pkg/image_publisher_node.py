import os
import sys
import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy

from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge

try:
    import pyrealsense2 as rs
except ImportError:
    rs = None


# --------------- Variable Setting ---------------
PUB_TOPIC_NAME = 'image_raw'

# realsense / image / video
DATA_SOURCE = 'realsense'

IMAGE_DIRECTORY_PATH = 'src/camera_perception_pkg/camera_perception_pkg/lib/Collected_Datasets/sample_dataset'
VIDEO_FILE_PATH = 'src/camera_perception_pkg/camera_perception_pkg/lib/Collected_Datasets/sangju.mp4'

SHOW_IMAGE = False

# 30 FPS ~= 0.0333, 15 FPS ~= 0.0667
TIMER = 1.0 / 30.0

# RealSense D435 권장 시작값
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_FPS = 30

FRAME_ID = 'camera_color_optical_frame'

# 여러 대 연결했을 때 특정 카메라 serial 지정용
# 비워두면 첫 번째 RealSense 사용
REALSENSE_SERIAL = ''
# ------------------------------------------------


class ImagePublisherNode(Node):
    def __init__(
        self,
        data_source=DATA_SOURCE,
        img_dir=IMAGE_DIRECTORY_PATH,
        video_path=VIDEO_FILE_PATH,
        pub_topic=PUB_TOPIC_NAME,
        logger=SHOW_IMAGE,
        timer=TIMER,
        frame_width=FRAME_WIDTH,
        frame_height=FRAME_HEIGHT,
        camera_fps=CAMERA_FPS,
        frame_id=FRAME_ID,
        realsense_serial=REALSENSE_SERIAL,
    ):
        super().__init__('image_publisher_node')

        self.declare_parameter('data_source', data_source)
        self.declare_parameter('img_dir', img_dir)
        self.declare_parameter('video_path', video_path)
        self.declare_parameter('pub_topic', pub_topic)
        self.declare_parameter('logger', logger)
        self.declare_parameter('timer', timer)
        self.declare_parameter('frame_width', frame_width)
        self.declare_parameter('frame_height', frame_height)
        self.declare_parameter('camera_fps', camera_fps)
        self.declare_parameter('frame_id', frame_id)
        self.declare_parameter('realsense_serial', realsense_serial)

        self.data_source = self.get_parameter('data_source').get_parameter_value().string_value
        self.img_dir = self.get_parameter('img_dir').get_parameter_value().string_value
        self.video_path = self.get_parameter('video_path').get_parameter_value().string_value
        self.pub_topic = self.get_parameter('pub_topic').get_parameter_value().string_value
        self.logger = self.get_parameter('logger').get_parameter_value().bool_value
        self.timer_period = self.get_parameter('timer').get_parameter_value().double_value
        self.frame_width = self.get_parameter('frame_width').get_parameter_value().integer_value
        self.frame_height = self.get_parameter('frame_height').get_parameter_value().integer_value
        self.camera_fps = self.get_parameter('camera_fps').get_parameter_value().integer_value
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        self.realsense_serial = self.get_parameter('realsense_serial').get_parameter_value().string_value

        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=1
        )

        self.br = CvBridge()

        self.cap = None
        self.pipeline = None
        self.rs_config = None

        self.img_list = []
        self.img_num = 0

        if self.data_source == 'realsense':
            self._init_realsense()
        elif self.data_source == 'video':
            self._init_video()
        elif self.data_source == 'image':
            self._init_image_dir()
        else:
            self.get_logger().error(
                f"Wrong data source: {self.data_source}. Use 'realsense', 'image', or 'video'."
            )
            rclpy.shutdown()
            sys.exit(1)

        self.publisher = self.create_publisher(Image, self.pub_topic, self.qos_profile)
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        topic_text = self.pub_topic if self.pub_topic.startswith('/') else '/' + self.pub_topic
        self.get_logger().info(
            f"ImagePublisherNode started | source={self.data_source} | topic={topic_text}"
        )

    def _init_realsense(self):
        if rs is None:
            self.get_logger().error(
                "pyrealsense2 is not installed. Install Intel RealSense SDK first."
            )
            rclpy.shutdown()
            sys.exit(1)

        ctx = rs.context()
        devices = ctx.query_devices()

        if len(devices) == 0:
            self.get_logger().error("No RealSense device found.")
            rclpy.shutdown()
            sys.exit(1)

        self.get_logger().info(f"Found {len(devices)} RealSense device(s).")

        for dev in devices:
            name = dev.get_info(rs.camera_info.name)
            serial = dev.get_info(rs.camera_info.serial_number)
            self.get_logger().info(f"RealSense device: {name}, serial={serial}")

        self.pipeline = rs.pipeline()
        self.rs_config = rs.config()

        if self.realsense_serial:
            self.rs_config.enable_device(self.realsense_serial)
            self.get_logger().info(f"Using RealSense serial: {self.realsense_serial}")

        self.rs_config.enable_stream(
            rs.stream.color,
            self.frame_width,
            self.frame_height,
            rs.format.bgr8,
            self.camera_fps
        )

        try:
            profile = self.pipeline.start(self.rs_config)
        except Exception as e:
            self.get_logger().error(f"Failed to start RealSense pipeline: {e}")
            rclpy.shutdown()
            sys.exit(1)

        stream_profile = profile.get_stream(rs.stream.color).as_video_stream_profile()
        intr = stream_profile.get_intrinsics()

        self.get_logger().info(
            f"RealSense color stream started | "
            f"{intr.width}x{intr.height}@{self.camera_fps} | "
            f"fx={intr.fx:.2f}, fy={intr.fy:.2f}, "
            f"ppx={intr.ppx:.2f}, ppy={intr.ppy:.2f}"
        )

        # 자동 노출은 기본적으로 켜져 있음.
        # 필요하면 아래처럼 sensor option 설정 가능.
        try:
            device = profile.get_device()
            color_sensor = device.query_sensors()[1]
            if color_sensor.supports(rs.option.enable_auto_exposure):
                color_sensor.set_option(rs.option.enable_auto_exposure, 1)
                self.get_logger().info("RealSense auto exposure enabled.")
        except Exception as e:
            self.get_logger().warning(f"Could not set RealSense sensor options: {e}")

    def _init_video(self):
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            self.get_logger().error(f'Cannot open video file: {self.video_path}')
            rclpy.shutdown()
            sys.exit(1)

    def _init_image_dir(self):
        if not os.path.isdir(self.img_dir):
            self.get_logger().error(f'Not a directory: {self.img_dir}')
            rclpy.shutdown()
            sys.exit(1)

        self.img_list = sorted(os.listdir(self.img_dir))
        self.img_num = 0

        if len(self.img_list) == 0:
            self.get_logger().error(f'No files in directory: {self.img_dir}')
            rclpy.shutdown()
            sys.exit(1)

    def _publish_frame(self, frame):
        image_msg = self.br.cv2_to_imgmsg(frame, encoding='bgr8')
        image_msg.header = Header()
        image_msg.header.stamp = self.get_clock().now().to_msg()
        image_msg.header.frame_id = self.frame_id

        self.publisher.publish(image_msg)

        if self.logger:
            cv2.imshow('Image Publisher', frame)
            cv2.waitKey(1)

    def _read_realsense_frame(self):
        try:
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            color_frame = frames.get_color_frame()

            if not color_frame:
                self.get_logger().warning('No RealSense color frame')
                return None

            frame = np.asanyarray(color_frame.get_data())
            return frame

        except Exception as e:
            self.get_logger().warning(f'Failed to read RealSense frame: {e}')
            return None

    def timer_callback(self):
        if self.data_source == 'realsense':
            frame = self._read_realsense_frame()

            if frame is None:
                return

            self._publish_frame(frame)

        elif self.data_source == 'image':
            if self.img_num >= len(self.img_list):
                self.img_num = 0

            img_file = self.img_list[self.img_num]
            img_path = os.path.join(self.img_dir, img_file)
            img = cv2.imread(img_path)

            if img is None:
                self.get_logger().warning(f'Skipping non-image file: {img_file}')
            else:
                img = cv2.resize(img, (self.frame_width, self.frame_height))
                self._publish_frame(img)

                if self.logger:
                    self.get_logger().info(f'Published image: {img_file}')

            self.img_num += 1

        elif self.data_source == 'video':
            ret, frame = self.cap.read()

            if not ret or frame is None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return

            frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            self._publish_frame(frame)

    def destroy_node(self):
        if self.pipeline is not None:
            try:
                self.pipeline.stop()
                self.get_logger().info("RealSense pipeline stopped.")
            except Exception:
                pass

        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisherNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nshutdown\n")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
# import os
# import sys
# import cv2

# import rclpy
# from rclpy.node import Node
# from rclpy.qos import QoSProfile
# from rclpy.qos import QoSHistoryPolicy
# from rclpy.qos import QoSDurabilityPolicy
# from rclpy.qos import QoSReliabilityPolicy

# from sensor_msgs.msg import Image
# from std_msgs.msg import Header
# from cv_bridge import CvBridge


# # --------------- Variable Setting ---------------
# PUB_TOPIC_NAME = 'image_raw'
# DATA_SOURCE = 'camera'
# CAM_NUM = 4

# IMAGE_DIRECTORY_PATH = 'src/camera_perception_pkg/camera_perception_pkg/lib/Collected_Datasets/sample_dataset'
# VIDEO_FILE_PATH = 'src/camera_perception_pkg/camera_perception_pkg/lib/Collected_Datasets/sangju.mp4'

# SHOW_IMAGE = False

# # 30 FPS ~= 0.0333, 15 FPS ~= 0.0667
# TIMER = 1.0 / 30.0

# # D435용 권장 시작값
# FRAME_WIDTH = 640
# FRAME_HEIGHT = 480
# CAMERA_FPS = 30
# # ------------------------------------------------


# class ImagePublisherNode(Node):
#     def __init__(
#         self,
#         data_source=DATA_SOURCE,
#         cam_num=CAM_NUM,
#         img_dir=IMAGE_DIRECTORY_PATH,
#         video_path=VIDEO_FILE_PATH,
#         pub_topic=PUB_TOPIC_NAME,
#         logger=SHOW_IMAGE,
#         timer=TIMER,
#         frame_width=FRAME_WIDTH,
#         frame_height=FRAME_HEIGHT,
#         camera_fps=CAMERA_FPS,
#     ):
#         super().__init__('image_publisher_node')

#         self.declare_parameter('data_source', data_source)
#         self.declare_parameter('cam_num', cam_num)
#         self.declare_parameter('img_dir', img_dir)
#         self.declare_parameter('video_path', video_path)
#         self.declare_parameter('pub_topic', pub_topic)
#         self.declare_parameter('logger', logger)
#         self.declare_parameter('timer', timer)
#         self.declare_parameter('frame_width', frame_width)
#         self.declare_parameter('frame_height', frame_height)
#         self.declare_parameter('camera_fps', camera_fps)

#         self.data_source = self.get_parameter('data_source').get_parameter_value().string_value
#         self.cam_num = self.get_parameter('cam_num').get_parameter_value().integer_value
#         self.img_dir = self.get_parameter('img_dir').get_parameter_value().string_value
#         self.video_path = self.get_parameter('video_path').get_parameter_value().string_value
#         self.pub_topic = self.get_parameter('pub_topic').get_parameter_value().string_value
#         self.logger = self.get_parameter('logger').get_parameter_value().bool_value
#         self.timer_period = self.get_parameter('timer').get_parameter_value().double_value
#         self.frame_width = self.get_parameter('frame_width').get_parameter_value().integer_value
#         self.frame_height = self.get_parameter('frame_height').get_parameter_value().integer_value
#         self.camera_fps = self.get_parameter('camera_fps').get_parameter_value().integer_value

#         self.qos_profile = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             history=QoSHistoryPolicy.KEEP_LAST,
#             durability=QoSDurabilityPolicy.VOLATILE,
#             depth=1
#         )

#         self.br = CvBridge()
#         self.cap = None
#         self.img_list = []
#         self.img_num = 0

#         if self.data_source == 'camera':
#             self._init_camera()
#         elif self.data_source == 'video':
#             self._init_video()
#         elif self.data_source == 'image':
#             self._init_image_dir()
#         else:
#             self.get_logger().error(
#                 f"Wrong data source: {self.data_source}. Use 'camera', 'image', or 'video'."
#             )
#             rclpy.shutdown()
#             sys.exit(1)

#         self.publisher = self.create_publisher(Image, self.pub_topic, self.qos_profile)
#         self.timer = self.create_timer(self.timer_period, self.timer_callback)

#         self.get_logger().info(
#             f"ImagePublisherNode started | source={self.data_source} "
#             f"| topic=/{self.pub_topic if not self.pub_topic.startswith('/') else self.pub_topic}"
#         )

#     def _init_camera(self):
#         self.cap = cv2.VideoCapture(self.cam_num, cv2.CAP_V4L2)

#         if not self.cap.isOpened():
#             self.get_logger().error(f'Cannot open camera: /dev/video{self.cam_num}')
#             rclpy.shutdown()
#             sys.exit(1)

#         # 지연 줄이기용
#         try:
#             self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#         except Exception:
#             pass

#         # 실제 캡처 해상도/FPS 요청
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
#         self.cap.set(cv2.CAP_PROP_FPS, self.camera_fps)

#         actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

#         self.get_logger().info(
#             f'Camera opened: /dev/video{self.cam_num} | '
#             f'requested={self.frame_width}x{self.frame_height}@{self.camera_fps} | '
#             f'actual={actual_w}x{actual_h}@{actual_fps:.2f}'
#         )

#     def _init_video(self):
#         self.cap = cv2.VideoCapture(self.video_path)
#         if not self.cap.isOpened():
#             self.get_logger().error(f'Cannot open video file: {self.video_path}')
#             rclpy.shutdown()
#             sys.exit(1)

#     def _init_image_dir(self):
#         if not os.path.isdir(self.img_dir):
#             self.get_logger().error(f'Not a directory: {self.img_dir}')
#             rclpy.shutdown()
#             sys.exit(1)

#         self.img_list = sorted(os.listdir(self.img_dir))
#         self.img_num = 0

#         if len(self.img_list) == 0:
#             self.get_logger().error(f'No files in directory: {self.img_dir}')
#             rclpy.shutdown()
#             sys.exit(1)

#     def _publish_frame(self, frame):
#         image_msg = self.br.cv2_to_imgmsg(frame, encoding='bgr8')
#         image_msg.header = Header()
#         image_msg.header.stamp = self.get_clock().now().to_msg()
#         image_msg.header.frame_id = 'image_frame'
#         self.publisher.publish(image_msg)

#         if self.logger:
#             cv2.imshow('Image Publisher', frame)
#             cv2.waitKey(1)

#     def timer_callback(self):
#         if self.data_source == 'camera':
#             ret, frame = self.cap.read()
#             if not ret or frame is None:
#                 self.get_logger().warning('Failed to read frame from camera')
#                 return

#             # camera는 실제 캡처 해상도를 낮췄으므로 resize 하지 않음
#             self._publish_frame(frame)

#         elif self.data_source == 'image':
#             if self.img_num >= len(self.img_list):
#                 self.img_num = 0

#             img_file = self.img_list[self.img_num]
#             img_path = os.path.join(self.img_dir, img_file)
#             img = cv2.imread(img_path)

#             if img is None:
#                 self.get_logger().warning(f'Skipping non-image file: {img_file}')
#             else:
#                 img = cv2.resize(img, (self.frame_width, self.frame_height))
#                 self._publish_frame(img)
#                 if self.logger:
#                     self.get_logger().info(f'Published image: {img_file}')

#             self.img_num += 1

#         elif self.data_source == 'video':
#             ret, frame = self.cap.read()
#             if not ret or frame is None:
#                 self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 return

#             frame = cv2.resize(frame, (self.frame_width, self.frame_height))
#             self._publish_frame(frame)


# def main(args=None):
#     rclpy.init(args=args)
#     node = ImagePublisherNode()

#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         print("\nshutdown\n")
#     finally:
#         node.destroy_node()
#         if node.cap is not None and node.cap.isOpened():
#             node.cap.release()
#         cv2.destroyAllWindows()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()