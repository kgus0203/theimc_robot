#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
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
        default_value=os.path.expanduser('~/.ros/cropbot_rtabmap.db'),
        description='RTAB-Map database output path',
    ),
    DeclareLaunchArgument(
        'delete_db_on_start',
        default_value='false',
        choices=['true', 'false'],
        description='Delete the existing database before mapping',
    ),
    DeclareLaunchArgument(
        'start_rviz',
        default_value='false',
        choices=['true', 'false'],
        description='Start rtabmap_viz for mapping diagnostics',
    ),
]


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    database_path = LaunchConfiguration('database_path')
    delete_db_on_start = LaunchConfiguration('delete_db_on_start')
    start_rviz = LaunchConfiguration('start_rviz')

    realsense_launch = IncludeLaunchDescription(
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

    # Synchronize color, aligned depth and camera calibration into one RGB-D msg.
    rgbd_sync = Node(
        package='rtabmap_sync',
        executable='rgbd_sync',
        name='rtabmap_rgbd_sync',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'approx_sync': True,
            'approx_sync_max_interval': 0.01,
            'topic_queue_size': 10,
            'sync_queue_size': 10,
        }],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
            ('rgbd_image', '/rtabmap/rgbd_image'),
        ],
    )

    # Stage 1 records a visual/depth map while AMCL remains the global localizer.
    # Therefore RTAB-Map must not publish map->odom TF in this stage.
    rtabmap = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'base_footprint',
            'map_frame_id': 'rtabmap_map',
            'odom_frame_id': 'odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'publish_tf': True,
            'database_path': database_path,
            'delete_db_on_start': delete_db_on_start,
            'approx_sync': True,
            'queue_size': 30,
            'Mem/IncrementalMemory': 'true',
            'Mem/InitWMWithAllNodes': 'false',
            'Reg/Force3DoF': 'true',
            'RGBD/ForceOdom3DoF': 'true',
            'RGBD/NeighborLinkRefining': 'false',
            'RGBD/ProximityBySpace': 'false',
            'Grid/Sensor': '1',
            'Grid/RangeMax': '2.5',
            'Grid/NoiseFilteringRadius': '0.05',
            'Grid/NoiseFilteringMinNeighbors': '5',
            'Vis/MaxDepth': '2.5',
            'Kp/MaxDepth': '2.5'
        }],
        remappings=[
            ('rgbd_image', '/rtabmap/rgbd_image'),
            ('odom', '/camera/odom'),
        ],
    )

    rtabmap_viz = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        name='rtabmap_viz',
        output='screen',
        condition=IfCondition(start_rviz),
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'base_footprint',
            'odom_frame_id': 'odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'approx_sync': True,
        }],
        remappings=[
            ('rgbd_image', '/rtabmap/rgbd_image'),
            ('odom', '/odom'),
        ],
    )

    launch_description = LaunchDescription(ARGUMENTS)
    # launch_description.add_action(realsense_launch)
    launch_description.add_action(rgbd_sync)
    launch_description.add_action(rtabmap)
    launch_description.add_action(rtabmap_viz)
    return launch_description