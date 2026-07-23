#!/usr/bin/env python3
'''
STM 출력
WHEEL,0.000,0.000 
IMU,3.10,-0.24,2.26

여기서 WHEEL 다음에 오는 건 오른쪽 바퀴, 왼쪽 바퀴 m/s
IMU는 해당 코드에서는 사용 안하는 중 -> 그래서 해당 bringup에서는 ekf가 의미 없음
'''

import os
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation clock if true',
    ),
]


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_share_bringup = get_package_share_directory('theimc_bringup')
    pkg_share_description = get_package_share_directory('theimc_description')

    params_ydlidar = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'theimc_ydlidar.yaml']
    )
    params_scan_filter = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'vehicle_scan_filter.yaml']
    )
    params_ekf = PathJoinSubstitution(
        [pkg_share_bringup, 'params', 'ekf_basic.yaml']
    )

    urdf_file = os.path.join(
        pkg_share_description,
        'urdf',
        'theimc.urdf',
    )
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

    half_length = body_size[0] / 2.0
    half_width = body_size[1] / 2.0

    vehicle_polygon = (
        f"[[-{half_length}, -{half_width}], "
        f"[-{half_length}, {half_width}], "
        f"[{half_length}, {half_width}], "
        f"[{half_length}, -{half_width}]]"
    )
    with open(urdf_file, 'r', encoding='utf-8') as urdf_stream:
        robot_description_content = urdf_stream.read()

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

    stm_wheel_cmd = Node(
        package='theimc_bringup',
        executable='bringup_node',
        name='bringup_node',
        output='screen',
        parameters=[
            {'use_stm_odom': False},
            {'use_stm_imu': False},
            {'use_stm_wheel': True},
        ],
    )

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
    launch_description.add_action(stm_wheel_cmd)
    launch_description.add_action(ydlidar_cmd)
    launch_description.add_action(scan_filter_cmd)
    launch_description.add_action(ekf_cmd)

    return launch_description
