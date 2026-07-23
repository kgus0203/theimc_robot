#!/usr/bin/env python3

import ctypes
import os

from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import PackageNotFoundError
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
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
]


def check_required_packages(context, *args, **kwargs):
    required_packages = [
        'isaac_ros_visual_slam',
        'realsense2_camera',
        'robot_localization',
        'robot_state_publisher',
        'theimc_description',
    ]
    missing_packages = []

    for package_name in required_packages:
        try:
            get_package_share_directory(package_name)
        except PackageNotFoundError:
            missing_packages.append(package_name)

    if missing_packages:
        missing_text = ', '.join(missing_packages)
        raise RuntimeError(
            f'Missing required package(s): {missing_text}. '
            'Install/source them before running '
            'isaac_vslam_odom_test.launch.py.'
        )

    try:
        ctypes.CDLL('libcudart.so.12')
    except OSError as error:
        raise RuntimeError(
            'Missing CUDA runtime libcudart.so.12 required by '
            'isaac_ros_visual_slam. Run this launch in the Isaac ROS '
            'CUDA-enabled environment or install the matching NVIDIA CUDA '
            f'runtime. Loader error: {error}'
        ) from error


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_share_bringup = get_package_share_directory('theimc_bringup')
    pkg_share_description = get_package_share_directory('theimc_description')

    isaac_vslam_launch = PathJoinSubstitution([
        pkg_share_bringup,
        'launch',
        'isaac_vslam_d435.launch.py',
    ])
    params_ekf = PathJoinSubstitution([
        pkg_share_bringup,
        'params',
        'ekf_isaac_vslam_only.yaml',
    ])

    urdf_file = os.path.join(
        pkg_share_description,
        'urdf',
        'theimc.urdf',
    )

    with open(urdf_file, 'r', encoding='utf-8') as urdf_stream:
        robot_description_content = urdf_stream.read()

    isaac_vslam_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(isaac_vslam_launch),
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

    motor_drive_cmd = Node(
        package='theimc_bringup',
        executable='bringup_node',
        name='bringup_node',
        output='screen',
    )

    isaac_vslam_odom_adapter_cmd = Node(
        package='theimc_bringup',
        executable='isaac_vslam_odom_adapter_node',
        name='isaac_vslam_odom_adapter',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {
                'input_topic': '/visual_slam/tracking/odometry',
                'output_topic': '/isaac_vslam/odom_base',
                'base_frame': 'base_footprint',
                'camera_frame': 'camera_link',
            },
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
    launch_description.add_action(OpaqueFunction(function=check_required_packages))
    launch_description.add_action(isaac_vslam_cmd)
    launch_description.add_action(robot_state_publisher_cmd)
    launch_description.add_action(motor_drive_cmd)
    launch_description.add_action(isaac_vslam_odom_adapter_cmd)
    launch_description.add_action(ekf_cmd)

    return launch_description
