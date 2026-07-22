#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


EKF_PARAM_FILES = {
    'wheel': 'test_wheel_ekf.yaml',
    'wheel_camera': 'test_wheel_camera_ekf.yaml',
    'wheel_imu': 'test_wheel_imu_ekf.yaml',
    'wheel_camera_imu': 'test_wheel_camera_imu_ekf.yaml',
}


ARGUMENTS = [
    DeclareLaunchArgument(
        'mode',
        default_value='wheel_camera_imu',
        choices=list(EKF_PARAM_FILES.keys()),
        description='EKF sensor combination to test',
    ),
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation clock if true',
    ),
    DeclareLaunchArgument(
        'output_odom',
        default_value='/odom',
        description='Filtered odometry output topic',
    ),
    DeclareLaunchArgument(
        'publish_tf',
        default_value='true',
        choices=['true', 'false'],
        description='Publish odom -> base_footprint TF from EKF',
    ),
    DeclareLaunchArgument(
        'start_bringup',
        default_value='true',
        choices=['true', 'false'],
        description='Start theimc_bringup bringup_node for real robot control',
    ),
    DeclareLaunchArgument(
        'enable_camera_odom',
        default_value='true',
        choices=['true', 'false'],
        description='Launch D435 RealSense and RTAB-Map RGB-D odometry in camera modes',
    ),
    DeclareLaunchArgument(
        'enable_isaac_vslam',
        default_value='false',
        choices=['true', 'false'],
        description='Launch D435 Isaac VSLAM pipeline instead of RTAB-Map camera odometry',
    ),
]


def launch_setup(context, *args, **kwargs):
    mode = LaunchConfiguration('mode').perform(context)
    use_sim_time = LaunchConfiguration('use_sim_time')
    output_odom = LaunchConfiguration('output_odom')
    publish_tf = LaunchConfiguration('publish_tf')
    start_bringup = (
        LaunchConfiguration('start_bringup').perform(context) == 'true'
    )
    enable_camera_odom = (
        LaunchConfiguration('enable_camera_odom').perform(context) == 'true'
    )
    enable_isaac_vslam = (
        LaunchConfiguration('enable_isaac_vslam').perform(context) == 'true'
    )
    use_camera = mode in ('wheel_camera', 'wheel_camera_imu')

    pkg_share_bringup = get_package_share_directory('theimc_bringup')
    pkg_share_description = get_package_share_directory('theimc_description')

    params_ekf = os.path.join(
        pkg_share_bringup,
        'params',
        EKF_PARAM_FILES[mode],
    )
    urdf_file = os.path.join(
        pkg_share_description,
        'urdf',
        'theimc.urdf',
    )
    isaac_vslam_launch = os.path.join(
        pkg_share_bringup,
        'launch',
        'isaac_vslam_d435.launch.py',
    )

    with open(urdf_file, 'r', encoding='utf-8') as urdf_stream:
        robot_description_content = urdf_stream.read()

    actions = [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'robot_description': robot_description_content},
            ],
        ),
    ]

    if start_bringup:
        actions.append(Node(
            package='theimc_bringup',
            executable='bringup_node',
            name='bringup_node',
            output='screen',
            parameters=[
                {'use_stm_odom': True},
                {'use_stm_imu': True},
                {'use_stm_wheel': True},
            ],
        ))

    if use_camera and enable_isaac_vslam:
        actions.extend([
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(isaac_vslam_launch),
            ),
            Node(
                package='theimc_bringup',
                executable='isaac_vslam_odom_adapter_node',
                name='isaac_vslam_odom_adapter',
                output='screen',
                parameters=[
                    {'use_sim_time': use_sim_time},
                    {
                        'input_topic': '/visual_slam/tracking/odometry',
                        'output_topic': '/camera/odom',
                        'base_frame': 'base_footprint',
                        'camera_frame': 'camera_link',
                    },
                ],
            ),
        ])
    elif use_camera and enable_camera_odom:
        actions.extend([
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('realsense2_camera'),
                        'launch',
                        'rs_launch.py',
                    )
                ),
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
            ),
            Node(
                package='rtabmap_odom',
                executable='rgbd_odometry',
                name='d435_rgbd_odometry',
                output='screen',
                arguments=['--ros-args', '--log-level', 'info'],
                parameters=[
                    {
                        'use_sim_time': use_sim_time,
                        'frame_id': 'base_footprint',
                        'odom_frame_id': 'odom',
                        'publish_tf': False,
                        'subscribe_depth': True,
                        'subscribe_odom_info': True,
                        'approx_sync': True,
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
            ),
        ])

    actions.append(
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                params_ekf,
                {'use_sim_time': use_sim_time},
                {'publish_tf': publish_tf},
            ],
            remappings=[
                ('odometry/filtered', output_odom),
            ],
        ),
    )

    return actions


def generate_launch_description():
    launch_description = LaunchDescription(ARGUMENTS)
    launch_description.add_action(OpaqueFunction(function=launch_setup))
    return launch_description
