#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


DEFAULT_DATABASE_PATH = (
    '/home/jeff/theimc_robot/src/theimc_bringup/rtabmap/'
    'cropbot_rtabmap.db'
)


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation clock if true',
    ),
    DeclareLaunchArgument(
        'database_path',
        default_value=DEFAULT_DATABASE_PATH,
        description='Existing RTAB-Map database to use for localization',
    ),
    DeclareLaunchArgument(
        'publish_tf',
        default_value='false',
        choices=['true', 'false'],
        description=(
            'Publish RTAB-Map map->odom TF. Keep false while AMCL is running.'
        ),
    ),
    DeclareLaunchArgument(
        'start_realsense',
        default_value='true',
        choices=['true', 'false'],
        description='Start the D435 driver in this launch file',
    ),
    DeclareLaunchArgument(
        'start_rtabmap_viz',
        default_value='true',
        choices=['true', 'false'],
        description='Start rtabmap_viz for localization diagnostics',
    ),
    DeclareLaunchArgument(
        'start_pose_validator',
        default_value='true',
        choices=['true', 'false'],
        description='Compare RTAB-Map localization against AMCL after alignment',
    ),
    DeclareLaunchArgument(
        'detection_rate',
        default_value='2.0',
        description='RTAB-Map localization processing rate in Hz',
    ),
]


def launch_setup(context, *args, **kwargs):
    database_path = os.path.expanduser(
        LaunchConfiguration('database_path').perform(context)
    )

    if not os.path.isfile(database_path):
        raise RuntimeError(
            'RTAB-Map database was not found: '
            f'{database_path}'
        )

    database_size = os.path.getsize(database_path)
    if database_size <= 0:
        raise RuntimeError(
            'RTAB-Map database is empty: '
            f'{database_path}'
        )

    use_sim_time = LaunchConfiguration('use_sim_time')
    publish_tf = LaunchConfiguration('publish_tf')
    start_realsense = LaunchConfiguration('start_realsense')
    start_rtabmap_viz = LaunchConfiguration('start_rtabmap_viz')
    start_pose_validator = LaunchConfiguration('start_pose_validator')
    detection_rate = LaunchConfiguration('detection_rate')

    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch',
                'rs_launch.py',
            )
        ),
        condition=IfCondition(start_realsense),
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

    # Group RTAB-Map topics below /rtabmap. Camera and odometry inputs remain
    # absolute so they connect to the existing robot bringup.
    rgbd_sync = Node(
        package='rtabmap_sync',
        executable='rgbd_sync',
        namespace='rtabmap',
        name='rgbd_sync',
        output='screen',
        parameters=[{
            'use_sim_time': ParameterValue(use_sim_time, value_type=bool),
            'approx_sync': True,
            'queue_size': 30,
            'sync_queue_size': 30,
        }],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
        ],
    )

    # Official RTAB-Map localization mode uses IncrementalMemory=false and
    # InitWMWithAllNodes=true. The database is never deleted in this launch.
    rtabmap_localization = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        namespace='rtabmap',
        name='localization',
        output='screen',
        parameters=[{
            'use_sim_time': ParameterValue(use_sim_time, value_type=bool),
            'frame_id': 'base_footprint',
            'map_frame_id': 'map',
            'odom_frame_id': 'odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'publish_tf': ParameterValue(publish_tf, value_type=bool),
            'database_path': database_path,
            'delete_db_on_start': False,
            'approx_sync': True,
            'queue_size': 30,
            'use_saved_map': True,
            'Mem/IncrementalMemory': 'false',
            'Mem/InitWMWithAllNodes': 'true',
            'Rtabmap/DetectionRate': ParameterValue(
                detection_rate,
                value_type=str,
            ),
            'RGBD/NeighborLinkRefining': 'true',
            'RGBD/ProximityBySpace': 'true',
            'Grid/FromDepth': 'true',
            'Grid/RangeMax': '6.0',
        }],
        remappings=[
            ('odom', '/odom'),
        ],
    )

    rtabmap_viz = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        namespace='rtabmap',
        name='viz',
        output='screen',
        condition=IfCondition(start_rtabmap_viz),
        parameters=[{
            'use_sim_time': ParameterValue(use_sim_time, value_type=bool),
            'frame_id': 'base_footprint',
            'odom_frame_id': 'odom',
            'subscribe_rgbd': True,
            'subscribe_odom': True,
            'approx_sync': True,
        }],
        remappings=[
            ('odom', '/odom'),
        ],
    )

    pose_validator = Node(
        package='theimc_bringup',
        executable='rtabmap_pose_validator_node',
        name='rtabmap_pose_validator',
        output='screen',
        condition=IfCondition(start_pose_validator),
        parameters=[{
            'use_sim_time': ParameterValue(use_sim_time, value_type=bool),
            'amcl_pose_topic': '/amcl_pose',
            'rtabmap_pose_topic': '/rtabmap/localization_pose',
            'aligned_pose_topic': '/rtabmap_validation/aligned_pose',
            'max_pair_dt_sec': 0.75,
            'log_period_sec': 2.0,
        }],
    )

    return [
        realsense_launch,
        rgbd_sync,
        rtabmap_localization,
        rtabmap_viz,
        pose_validator,
    ]


def generate_launch_description():
    launch_description = LaunchDescription(ARGUMENTS)
    launch_description.add_action(OpaqueFunction(function=launch_setup))
    return launch_description