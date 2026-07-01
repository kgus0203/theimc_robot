#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation clock if true',
    ),
    DeclareLaunchArgument(
        'enable_d435i_fusion',
        default_value='true',
        choices=['true', 'false'],
        description='Launch D435 RGB-D odometry fusion',
    ),
]


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    enable_d435_fusion = LaunchConfiguration('enable_d435i_fusion')

    pkg_share_bringup = get_package_share_directory('theimc_bringup')
    pkg_share_description = get_package_share_directory('theimc_description')

    params_ydlidar = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'theimc_ydlidar.yaml']
    )
    params_scan_filter = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'vehicle_scan_filter.yaml']
    )
    params_ekf = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'ekf.yaml']
    )

    urdf_file = os.path.join(
        pkg_share_description,
        'urdf',
        'theimc.urdf',
    )
    # URDF에서 base_link collision box 크기 읽기
    urdf_root = ET.parse(urdf_file).getroot()

    base_link = urdf_root.find("./link[@name='base_link']")
    if base_link is None:
        raise RuntimeError("base_link was not found in URDF")

    collision_box = base_link.find("./collision/geometry/box")
    if collision_box is None:
        raise RuntimeError("base_link collision box was not found in URDF")

    body_size = [
        float(value)
        for value in collision_box.attrib["size"].split()
    ]

    body_length = body_size[0]
    body_width = body_size[1]

    half_length = body_length / 2.0
    half_width = body_width / 2.0

    vehicle_polygon = (
        f"[[-{half_length}, -{half_width}], "
        f"[-{half_length}, {half_width}], "
        f"[{half_length}, {half_width}], "
        f"[{half_length}, -{half_width}]]"
    )
    with open(urdf_file, 'r', encoding='utf-8') as urdf_stream:
        robot_description_content = urdf_stream.read()

    motor_drive_cmd = Node(
        package='theimc_bringup',
        executable='bringup_node',
        name='bringup_node',
        output='screen',
    )

    # LiDAR raw scan: /scan_raw
    ydlidar_cmd = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        emulate_tty=True,
        parameters=[params_ydlidar],
        remappings=[
            ('scan', '/scan_raw'),
        ],
    )

    # Filtered scan: /scan
    scan_filter_cmd = Node(
        package='laser_filters',
        executable='scan_to_scan_filter_chain',
        name='scan_filter_chain',
        output='screen',
        emulate_tty=True,
        parameters=[
            params_scan_filter,
            {
                'filter1.params.polygon': vehicle_polygon,
            },
        ],
        remappings=[
            ('scan', '/scan_raw'),
            ('scan_filtered', '/scan'),
        ],
    )

    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': robot_description_content},
        ],
    )

    robot_agent_cmd = Node(
        package='theimc_bringup',
        executable='robot_agent_node',
        name='robot_agent',
        output='screen',
        emulate_tty=True,
    )

    # Intel RealSense D435 driver.
    # Existing URDF publishes base_link -> camera_link.
    # The RealSense driver publishes camera_link -> internal sensor frames.
    realsense_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch',
                'rs_launch.py',
            )
        ),
        condition=IfCondition(enable_d435_fusion),
        launch_arguments={
            'camera_namespace': '',
            'camera_name': 'camera',
            'enable_color': 'true',
            'enable_depth': 'true',
            'enable_gyro': 'false',
            'enable_accel': 'false',
            'unite_imu_method': '0',
            'enable_sync': 'true',
            'align_depth.enable': 'true',
            'publish_tf': 'true',
            'initial_reset': 'true',
            'use_sim_time': use_sim_time,
        }.items(),
    )

    # RGB-D visual odometry.
    # It publishes only /camera/odom. It must not publish odom TF because
    # robot_localization is the single odom -> base_footprint TF publisher.
    rgbd_odometry_cmd = Node(
        package='rtabmap_odom',
        executable='rgbd_odometry',
        name='d435_rgbd_odometry',
        output='screen',
        arguments=['--ros-args', '--log-level', 'warn'],
        condition=IfCondition(enable_d435_fusion),
        parameters=[
            {
                'use_sim_time': use_sim_time,
                'frame_id': 'base_footprint',
                'odom_frame_id': 'odom',
                'publish_tf': False,
                'subscribe_depth': True,
                'subscribe_odom_info': True,
                'approx_sync': False,
                'wait_imu_to_init': False,
            }
        ],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
            (
                'depth/image',
                '/camera/aligned_depth_to_color/image_raw',
            ),
            ('odom', '/camera/odom'),
        ],
    )

    # EKF always runs. When enable_d435i_fusion=false, it continues using
    # wheel odometry only and still publishes /odom and odom TF.
    ekf_cmd = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[
            params_ekf,
            {'use_sim_time': use_sim_time},
        ],
        remappings=[
            ('odometry/filtered', '/odom'),
        ],
    )

    launch_description = LaunchDescription(ARGUMENTS)
    launch_description.add_action(robot_state_publisher_cmd)
    launch_description.add_action(motor_drive_cmd)
    launch_description.add_action(ydlidar_cmd)
    launch_description.add_action(scan_filter_cmd)
    launch_description.add_action(robot_agent_cmd)
    launch_description.add_action(realsense_cmd)
    launch_description.add_action(rgbd_odometry_cmd)
    launch_description.add_action(ekf_cmd)

    return launch_description
