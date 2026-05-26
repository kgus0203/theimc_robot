import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import TimerAction


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation (Gazebo) clock if true'
    ),
]


def generate_launch_description():

    pkg_share_navigation2 = get_package_share_directory('theimc_navigation2')
    pkg_share_nav2_bringup = get_package_share_directory('nav2_bringup')  # 이건 nav2 원래 있는 거

    # RViz
    # params_nav2_rviz = PathJoinSubstitution([pkg_share_navigation2, 'rviz', 'nav2_default_view.rviz'])
    # params_nav2_rviz = PathJoinSubstitution([pkg_share_nav2_bringup, 'rivz', 'nav2_default_view.rviz'])

    # Map
    params_nav2_map = PathJoinSubstitution([pkg_share_navigation2, 'maps', 'map.yaml'])

    # Nav2 params
    params_nav2 = PathJoinSubstitution([pkg_share_navigation2, 'params', 'theimc_nav2_params.yaml'])

    # Twist mux params
    params_twist_mux = PathJoinSubstitution([pkg_share_navigation2, 'params', 'twist_mux.yaml'])

    # Keepout filter params
    params_keepout_filter = os.path.join(
        pkg_share_navigation2,
        'params',
        'keepout_filter.yaml'
    )

    # Bringup launch
    launch_nav2_bringup = PathJoinSubstitution([pkg_share_nav2_bringup, 'launch', 'bringup_launch.py'])

    # Launch Config
    map_yaml = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    keepout_params_file = LaunchConfiguration('filter_mask_params_file')

    # Declare Launch Args
    dla_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=params_nav2_map,
        description='Full path to map yaml file to load'
    )

    dla_params_nav2_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=params_nav2,
        description='Full path to the ROS2 parameters file to use for all launched nodes'
    )

    declare_filter_mask_params_file_cmd = DeclareLaunchArgument(
        'filter_mask_params_file',
        default_value=params_keepout_filter,
        description='Full path to keepout filter yaml file'
    )

    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_nav2_bringup]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_yaml,
            'params_file': params_file,
            'autostart': 'true'
        }.items()
    )

    # ---------------------------------------------------------
    # [추가] Keepout Filter Mask Map Server
    # keepout mask map을 publish하는 map_server
    # ---------------------------------------------------------
    filter_mask_server_cmd = Node(
        package='nav2_map_server',
        executable='map_server',
        name='filter_mask_server',
        output='screen',
        parameters=[
            keepout_params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    # ---------------------------------------------------------
    # [추가] Costmap Filter Info Server
    # Nav2 costmap filter가 mask 정보를 받을 수 있게 해주는 서버
    # ---------------------------------------------------------
    costmap_filter_info_server_cmd = Node(
        package='nav2_map_server',
        executable='costmap_filter_info_server',
        name='costmap_filter_info_server',
        output='screen',
        parameters=[
            keepout_params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    # ---------------------------------------------------------
    # [추가] Keepout Filter Lifecycle Manager
    # filter_mask_server, costmap_filter_info_server를 active 상태로 만들어줌
    # ---------------------------------------------------------
    filter_lifecycle_manager_cmd = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_costmap_filters',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': True},
            {'node_names': [
                'filter_mask_server',
                'costmap_filter_info_server'
            ]}
        ]
    )

    # ---------------------------------------------------------
    # [추가] Docking Server Node
    # ---------------------------------------------------------
    # docking_server_cmd = Node(
    #     package='opennav_docking',
    #     executable='docking_server',
    #     name='docking_server',
    #     output='screen',
    #     parameters=[
    #         params_file,  # docking_server 설정이 들어있는 파라미터 파일
    #         {'use_sim_time': use_sim_time}
    #     ]
    # )

    # ---------------------------------------------------------
    # [추가] Docking Lifecycle Manager
    # docking_server를 활성화(Active) 상태로 만들어줍니다.
    # ---------------------------------------------------------
    # docking_lifecycle_manager = Node(
    #     package='nav2_lifecycle_manager',
    #     executable='lifecycle_manager',
    #     name='lifecycle_manager_docking',
    #     output='screen',
    #     parameters=[
    #         {'use_sim_time': use_sim_time},
    #         {'autostart': True},
    #         {'node_names': ['docking_server']}
    #     ]
    # )

    # 3. Route Server (주석 처리됨)
    # route_server_cmd = Node(...)

    # 4. Route Server Lifecycle Manager (주석 처리됨)
    # route_server_lifecycle_manager = Node(...)

    # 5. Waypoint Follower
    # waypoint_yaml = PathJoinSubstitution([pkg_share_navigation2, 'params', 'waypoints.yaml'])
    # waypoint_follower_cmd = Node(
    #     package='nav2_waypoint_follower',
    #     executable='waypoint_follower',
    #     name='waypoint_follower',
    #     output='screen',
    #     parameters=[{'use_sim_time': use_sim_time},
    #                 {'waypoints_file': waypoint_yaml}]
    # )

    # Launch Description
    ld = LaunchDescription(ARGUMENTS)

    ld.add_action(dla_map_yaml_cmd)
    ld.add_action(dla_params_nav2_cmd)
    ld.add_action(declare_filter_mask_params_file_cmd)

    # Nav2 실행
    ld.add_action(nav2_bringup_launch)

    # Keepout filter 실행
    ld.add_action(filter_mask_server_cmd)
    ld.add_action(costmap_filter_info_server_cmd)
    ld.add_action(filter_lifecycle_manager_cmd)

    return ld