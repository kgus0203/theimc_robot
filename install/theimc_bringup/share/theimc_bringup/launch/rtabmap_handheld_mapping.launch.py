#!/usr/bin/env python3

"""Handheld 6-DoF RGB-D mapping with an Intel RealSense camera."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation clock if true',
    ),
    DeclareLaunchArgument(
        'database_path',
        default_value=(
            '/home/jeff/theimc_robot/src/theimc_bringup/rtabmap/'
            'handheld_rtabmap.db'
        ),
        description='RTAB-Map database output path',
    ),
    DeclareLaunchArgument(
        'delete_db_on_start',
        default_value='false',
        choices=['true', 'false'],
        description='Delete the existing database before mapping',
    ),
    DeclareLaunchArgument(
        'start_viz',
        default_value='true',
        choices=['true', 'false'],
        description='Start rtabmap_viz',
    ),
    DeclareLaunchArgument(
        'start_rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Start RViz2 with the handheld mapping configuration',
    ),
]


def prepare_database_directory(context):
    """Create the database parent directory before RTAB-Map starts."""
    path = LaunchConfiguration('database_path').perform(context)
    parent = os.path.dirname(os.path.abspath(os.path.expanduser(path)))
    os.makedirs(parent, exist_ok=True)
    return []


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    database_path = LaunchConfiguration('database_path')
    delete_db_on_start = LaunchConfiguration('delete_db_on_start')
    start_viz = LaunchConfiguration('start_viz')
    start_rviz = LaunchConfiguration('start_rviz')

    # Start the camera in this launch file so it can run independently of the
    # robot bringup. The driver also publishes camera_link -> optical-frame TFs.
    realsense = IncludeLaunchDescription(
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
            'rgb_camera.color_profile': '640x480x30',
            'depth_module.depth_profile': '640x480x30',
            'enable_sync': 'true',
            'align_depth.enable': 'true',
            'publish_tf': 'true',
            'initial_reset': 'true',
            'use_sim_time': use_sim_time,
        }.items(),
    )

    # Create one synchronized RGB-D message shared by odometry and SLAM.
    rgbd_sync = Node(
        package='rtabmap_sync',
        executable='rgbd_sync',
        name='handheld_rgbd_sync',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'approx_sync': True,
            'approx_sync_max_interval': 0.02,
            'topic_queue_size': 20,
            'sync_queue_size': 20,
        }],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
            ('rgbd_image', '/handheld/rgbd_image'),
        ],
    )

    # Estimate the camera's full 6-DoF motion from RGB and depth. This node is
    # the sole publisher of handheld_odom -> camera_link.
    rgbd_odometry = Node(
        package='rtabmap_odom',
        executable='rgbd_odometry',
        name='handheld_rgbd_odometry',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'camera_link',
            'odom_frame_id': 'handheld_odom',
            'publish_tf': True,
            'subscribe_rgbd': True,
            'approx_sync': False,
            'wait_imu_to_init': False,
            'Vis/MaxDepth': '4.0',
            'Kp/MaxDepth': '4.0',
        }],
        remappings=[
            ('rgbd_image', '/handheld/rgbd_image'),
            ('odom', '/handheld/odom'),
        ],
    )

    # Build a 3-D map and publish handheld_map -> handheld_odom. No 3-DoF
    # constraint is used, because a hand-carried camera can pitch and roll.
    rtabmap = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='handheld_rtabmap',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'camera_link',
            'map_frame_id': 'handheld_map',
            'odom_frame_id': 'handheld_odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'publish_tf': True,
            'database_path': database_path,
            'delete_db_on_start': delete_db_on_start,
            'approx_sync': False,
            'Mem/IncrementalMemory': 'true',
            'Mem/InitWMWithAllNodes': 'false',
            'RGBD/NeighborLinkRefining': 'true',
            'RGBD/ProximityBySpace': 'true',
            'Grid/Sensor': '1',
            'Grid/RangeMax': '4.0',
            'Vis/MaxDepth': '4.0',
            'Kp/MaxDepth': '4.0',
        }],
        remappings=[
            ('rgbd_image', '/handheld/rgbd_image'),
            ('odom', '/handheld/odom'),
        ],
    )

    rtabmap_viz = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        name='handheld_rtabmap_viz',
        output='screen',
        condition=IfCondition(start_viz),
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'camera_link',
            'odom_frame_id': 'handheld_odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'approx_sync': False,
        }],
        remappings=[
            ('rgbd_image', '/handheld/rgbd_image'),
            ('odom', '/handheld/odom'),
        ],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='handheld_mapping_rviz',
        output='screen',
        condition=IfCondition(start_rviz),
        arguments=[
            '-d',
            os.path.join(
                get_package_share_directory('theimc_bringup'),
                'rviz',
                'rtabmap_handheld_mapping.rviz',
            ),
        ],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    launch_description = LaunchDescription(ARGUMENTS)
    launch_description.add_action(OpaqueFunction(
        function=prepare_database_directory,
    ))
    launch_description.add_action(realsense)
    launch_description.add_action(rgbd_sync)
    launch_description.add_action(rgbd_odometry)
    launch_description.add_action(rtabmap)
    launch_description.add_action(rtabmap_viz)
    launch_description.add_action(rviz)
    return launch_description
