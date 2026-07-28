#!/usr/bin/env python3

import math
from typing import Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node
from std_msgs.msg import Float64, UInt32
from std_srvs.srv import Trigger


PlanarPose = Tuple[float, float, float]


def normalize_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def quaternion_to_yaw(x: float, y: float, z: float, w: float) -> float:
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def yaw_to_quaternion(yaw: float) -> Tuple[float, float, float, float]:
    half = yaw * 0.5
    return 0.0, 0.0, math.sin(half), math.cos(half)


def compose_pose(first: PlanarPose, second: PlanarPose) -> PlanarPose:
    x1, y1, yaw1 = first
    x2, y2, yaw2 = second
    c = math.cos(yaw1)
    s = math.sin(yaw1)
    return (
        x1 + c * x2 - s * y2,
        y1 + s * x2 + c * y2,
        normalize_angle(yaw1 + yaw2),
    )


def inverse_pose(pose: PlanarPose) -> PlanarPose:
    x, y, yaw = pose
    c = math.cos(yaw)
    s = math.sin(yaw)
    return (
        -c * x - s * y,
        s * x - c * y,
        normalize_angle(-yaw),
    )


def stamp_to_seconds(msg: PoseWithCovarianceStamped) -> float:
    stamp = msg.header.stamp
    return float(stamp.sec) + float(stamp.nanosec) * 1.0e-9


def msg_to_planar_pose(msg: PoseWithCovarianceStamped) -> PlanarPose:
    position = msg.pose.pose.position
    orientation = msg.pose.pose.orientation
    return (
        float(position.x),
        float(position.y),
        quaternion_to_yaw(
            float(orientation.x),
            float(orientation.y),
            float(orientation.z),
            float(orientation.w),
        ),
    )


class RtabmapPoseValidatorNode(Node):
    """Align RTAB-Map's map frame once, then compare it with AMCL in SE(2)."""

    def __init__(self) -> None:
        super().__init__('rtabmap_pose_validator')

        self.declare_parameter('amcl_pose_topic', '/amcl_pose')
        self.declare_parameter(
            'rtabmap_pose_topic',
            '/rtabmap/localization_pose',
        )
        self.declare_parameter(
            'aligned_pose_topic',
            '/rtabmap_validation/aligned_pose',
        )
        self.declare_parameter('max_pair_dt_sec', 0.75)
        self.declare_parameter('log_period_sec', 2.0)

        amcl_pose_topic = str(self.get_parameter('amcl_pose_topic').value)
        rtabmap_pose_topic = str(
            self.get_parameter('rtabmap_pose_topic').value
        )
        aligned_pose_topic = str(
            self.get_parameter('aligned_pose_topic').value
        )
        self.max_pair_dt_sec = float(
            self.get_parameter('max_pair_dt_sec').value
        )
        log_period_sec = float(self.get_parameter('log_period_sec').value)

        if self.max_pair_dt_sec <= 0.0:
            raise ValueError('max_pair_dt_sec must be greater than zero')
        if log_period_sec <= 0.0:
            raise ValueError('log_period_sec must be greater than zero')

        self.latest_amcl: Optional[PoseWithCovarianceStamped] = None
        self.latest_rtabmap: Optional[PoseWithCovarianceStamped] = None
        self.alignment: Optional[PlanarPose] = None
        self.last_pair_key: Optional[Tuple[int, int, int, int]] = None

        self.sample_count = 0
        self.current_xy_error = math.nan
        self.current_yaw_error = math.nan
        self.xy_squared_sum = 0.0
        self.yaw_squared_sum = 0.0
        self.max_xy_error = 0.0
        self.max_yaw_error = 0.0

        self.create_subscription(
            PoseWithCovarianceStamped,
            amcl_pose_topic,
            self.amcl_callback,
            10,
        )
        self.create_subscription(
            PoseWithCovarianceStamped,
            rtabmap_pose_topic,
            self.rtabmap_callback,
            10,
        )

        self.aligned_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            aligned_pose_topic,
            10,
        )
        self.xy_error_pub = self.create_publisher(
            Float64,
            '/rtabmap_validation/xy_error_m',
            10,
        )
        self.yaw_error_pub = self.create_publisher(
            Float64,
            '/rtabmap_validation/yaw_error_deg',
            10,
        )
        self.sample_count_pub = self.create_publisher(
            UInt32,
            '/rtabmap_validation/sample_count',
            10,
        )

        self.create_service(
            Trigger,
            '~/reset_alignment',
            self.reset_alignment_callback,
        )
        self.create_timer(log_period_sec, self.log_status)

        self.get_logger().info(
            'RTAB-Map pose validator started. '
            f'AMCL={amcl_pose_topic}, RTAB-Map={rtabmap_pose_topic}'
        )
        self.get_logger().warning(
            'The first synchronized pose pair defines a temporary 2D frame '
            'alignment. Reset it after RTAB-Map has visually relocalized.'
        )

    def amcl_callback(self, msg: PoseWithCovarianceStamped) -> None:
        self.latest_amcl = msg
        self.process_latest_pair()

    def rtabmap_callback(self, msg: PoseWithCovarianceStamped) -> None:
        self.latest_rtabmap = msg
        self.process_latest_pair()

    def reset_alignment_callback(
        self,
        request: Trigger.Request,
        response: Trigger.Response,
    ) -> Trigger.Response:
        del request
        self.alignment = None
        self.last_pair_key = None
        self.reset_statistics()
        response.success = True
        response.message = (
            'Alignment cleared. The next synchronized AMCL/RTAB-Map pair '
            'will define a new alignment.'
        )
        self.get_logger().warning(response.message)
        return response

    def reset_statistics(self) -> None:
        self.sample_count = 0
        self.current_xy_error = math.nan
        self.current_yaw_error = math.nan
        self.xy_squared_sum = 0.0
        self.yaw_squared_sum = 0.0
        self.max_xy_error = 0.0
        self.max_yaw_error = 0.0

    def process_latest_pair(self) -> None:
        if self.latest_amcl is None or self.latest_rtabmap is None:
            return

        amcl_stamp = stamp_to_seconds(self.latest_amcl)
        rtabmap_stamp = stamp_to_seconds(self.latest_rtabmap)
        pair_dt = abs(amcl_stamp - rtabmap_stamp)
        if pair_dt > self.max_pair_dt_sec:
            return

        pair_key = (
            self.latest_amcl.header.stamp.sec,
            self.latest_amcl.header.stamp.nanosec,
            self.latest_rtabmap.header.stamp.sec,
            self.latest_rtabmap.header.stamp.nanosec,
        )
        if pair_key == self.last_pair_key:
            return
        self.last_pair_key = pair_key

        amcl_pose = msg_to_planar_pose(self.latest_amcl)
        rtabmap_pose = msg_to_planar_pose(self.latest_rtabmap)
        values = (*amcl_pose, *rtabmap_pose)
        if not all(math.isfinite(value) for value in values):
            self.get_logger().warning('Ignoring a pose pair containing NaN/Inf')
            return

        if self.alignment is None:
            # T_nav_map_rtab_map = T_nav_map_base * inverse(T_rtab_map_base)
            self.alignment = compose_pose(amcl_pose, inverse_pose(rtabmap_pose))
            self.reset_statistics()
            self.get_logger().info(
                '2D map-frame alignment initialized: '
                f'x={self.alignment[0]:.3f} m, '
                f'y={self.alignment[1]:.3f} m, '
                f'yaw={math.degrees(self.alignment[2]):.2f} deg'
            )

        aligned_rtabmap = compose_pose(self.alignment, rtabmap_pose)
        dx = aligned_rtabmap[0] - amcl_pose[0]
        dy = aligned_rtabmap[1] - amcl_pose[1]
        yaw_error = normalize_angle(aligned_rtabmap[2] - amcl_pose[2])
        xy_error = math.hypot(dx, dy)

        self.sample_count += 1
        self.current_xy_error = xy_error
        self.current_yaw_error = yaw_error
        self.xy_squared_sum += xy_error * xy_error
        self.yaw_squared_sum += yaw_error * yaw_error
        self.max_xy_error = max(self.max_xy_error, xy_error)
        self.max_yaw_error = max(self.max_yaw_error, abs(yaw_error))

        self.publish_aligned_pose(aligned_rtabmap)
        self.xy_error_pub.publish(Float64(data=xy_error))
        self.yaw_error_pub.publish(
            Float64(data=math.degrees(abs(yaw_error)))
        )
        self.sample_count_pub.publish(UInt32(data=self.sample_count))

    def publish_aligned_pose(self, pose: PlanarPose) -> None:
        assert self.latest_amcl is not None
        assert self.latest_rtabmap is not None

        output = PoseWithCovarianceStamped()
        output.header.stamp = self.latest_rtabmap.header.stamp
        output.header.frame_id = (
            self.latest_amcl.header.frame_id
            if self.latest_amcl.header.frame_id
            else 'map'
        )
        output.pose.pose.position.x = pose[0]
        output.pose.pose.position.y = pose[1]
        output.pose.pose.position.z = 0.0
        qx, qy, qz, qw = yaw_to_quaternion(pose[2])
        output.pose.pose.orientation.x = qx
        output.pose.pose.orientation.y = qy
        output.pose.pose.orientation.z = qz
        output.pose.pose.orientation.w = qw
        output.pose.covariance = list(self.latest_rtabmap.pose.covariance)
        self.aligned_pose_pub.publish(output)

    def log_status(self) -> None:
        if self.latest_amcl is None:
            self.get_logger().warning('Waiting for /amcl_pose')
            return
        if self.latest_rtabmap is None:
            self.get_logger().warning(
                'Waiting for /rtabmap/localization_pose. '
                'Check DB loading and visual matching.'
            )
            return
        if self.alignment is None or self.sample_count == 0:
            self.get_logger().warning(
                'Pose topics exist, but no synchronized pair has been accepted.'
            )
            return

        xy_rmse = math.sqrt(self.xy_squared_sum / self.sample_count)
        yaw_rmse = math.sqrt(self.yaw_squared_sum / self.sample_count)
        self.get_logger().info(
            'RTAB-Map vs AMCL | '
            f'n={self.sample_count}, '
            f'current_xy={self.current_xy_error:.3f} m, '
            f'xy_rmse={xy_rmse:.3f} m, '
            f'max_xy={self.max_xy_error:.3f} m, '
            f'current_yaw={math.degrees(abs(self.current_yaw_error)):.2f} deg, '
            f'yaw_rmse={math.degrees(yaw_rmse):.2f} deg, '
            f'max_yaw={math.degrees(self.max_yaw_error):.2f} deg'
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RtabmapPoseValidatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()