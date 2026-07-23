import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


def quaternion_multiply(left, right):
    lx, ly, lz, lw = left
    rx, ry, rz, rw = right

    return [
        lw * rx + lx * rw + ly * rz - lz * ry,
        lw * ry - lx * rz + ly * rw + lz * rx,
        lw * rz + lx * ry - ly * rx + lz * rw,
        lw * rw - lx * rx - ly * ry - lz * rz,
    ]


def quaternion_inverse(quaternion):
    x, y, z, w = quaternion
    norm = x * x + y * y + z * z + w * w

    if norm <= 0.0:
        return [0.0, 0.0, 0.0, 1.0]

    return [-x / norm, -y / norm, -z / norm, w / norm]


def quaternion_normalize(quaternion):
    x, y, z, w = quaternion
    norm = math.sqrt(x * x + y * y + z * z + w * w)

    if norm <= 0.0:
        return [0.0, 0.0, 0.0, 1.0]

    return [x / norm, y / norm, z / norm, w / norm]


def rotate_vector(quaternion, vector):
    q_vector = [vector[0], vector[1], vector[2], 0.0]
    rotated = quaternion_multiply(
        quaternion_multiply(quaternion, q_vector),
        quaternion_inverse(quaternion),
    )

    return rotated[:3]


def covariance_from_diagonal(diagonal):
    covariance = [0.0] * 36

    for index, value in enumerate(diagonal[:6]):
        covariance[index * 6 + index] = float(value)

    return covariance


class IsaacVslamOdomAdapter(Node):
    def __init__(self):
        super().__init__('isaac_vslam_odom_adapter')

        self.declare_parameter(
            'input_topic',
            '/visual_slam/tracking/odometry',
        )
        self.declare_parameter('output_topic', '/isaac_vslam/odom_base')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('camera_frame', 'camera_link')
        self.declare_parameter('tf_timeout_sec', 0.1)
        self.declare_parameter(
            'pose_covariance_diagonal',
            [0.05, 0.05, 1000000.0, 1000000.0, 1000000.0, 0.10],
        )
        self.declare_parameter(
            'twist_covariance_diagonal',
            [1000000.0] * 6,
        )

        self.base_frame = self.get_parameter('base_frame').value
        self.camera_frame = self.get_parameter('camera_frame').value
        self.tf_timeout_sec = self.get_parameter('tf_timeout_sec').value
        self.pose_covariance = covariance_from_diagonal(
            self.get_parameter('pose_covariance_diagonal').value
        )
        self.twist_covariance = covariance_from_diagonal(
            self.get_parameter('twist_covariance_diagonal').value
        )

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        input_topic = self.get_parameter('input_topic').value
        output_topic = self.get_parameter('output_topic').value

        self.publisher = self.create_publisher(Odometry, output_topic, 20)
        self.subscription = self.create_subscription(
            Odometry,
            input_topic,
            self.odom_callback,
            20,
        )

        self.get_logger().info(
            f'Converting {input_topic} ({self.camera_frame}) '
            f'to {output_topic} ({self.base_frame}).'
        )

    def odom_callback(self, message):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                self.camera_frame,
                Time(),
                timeout=Duration(seconds=self.tf_timeout_sec),
            )
        except TransformException as error:
            self.get_logger().warn(
                f'Missing {self.base_frame} -> {self.camera_frame} TF: '
                f'{error}',
                throttle_duration_sec=2.0,
            )
            return

        camera_position = [
            message.pose.pose.position.x,
            message.pose.pose.position.y,
            message.pose.pose.position.z,
        ]
        odom_camera_rotation = quaternion_normalize([
            message.pose.pose.orientation.x,
            message.pose.pose.orientation.y,
            message.pose.pose.orientation.z,
            message.pose.pose.orientation.w,
        ])

        base_camera_translation = [
            transform.transform.translation.x,
            transform.transform.translation.y,
            transform.transform.translation.z,
        ]
        base_camera_rotation = quaternion_normalize([
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w,
        ])

        odom_base_rotation = quaternion_normalize(
            quaternion_multiply(
                odom_camera_rotation,
                quaternion_inverse(base_camera_rotation),
            )
        )
        rotated_offset = rotate_vector(
            odom_base_rotation,
            base_camera_translation,
        )

        output = Odometry()
        output.header = message.header
        output.child_frame_id = self.base_frame
        output.pose.pose.position.x = camera_position[0] - rotated_offset[0]
        output.pose.pose.position.y = camera_position[1] - rotated_offset[1]
        output.pose.pose.position.z = camera_position[2] - rotated_offset[2]
        output.pose.pose.orientation.x = odom_base_rotation[0]
        output.pose.pose.orientation.y = odom_base_rotation[1]
        output.pose.pose.orientation.z = odom_base_rotation[2]
        output.pose.pose.orientation.w = odom_base_rotation[3]
        output.pose.covariance = self.pose_covariance
        output.twist.covariance = self.twist_covariance

        self.publisher.publish(output)


def main(args=None):
    rclpy.init(args=args)
    node = IsaacVslamOdomAdapter()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
