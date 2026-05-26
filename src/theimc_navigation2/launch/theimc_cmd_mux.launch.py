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
        description='Use simulation clock if true'
    ),
]


def generate_launch_description():
    pkg_share_navigation2 = get_package_share_directory('theimc_navigation2')

    use_sim_time = LaunchConfiguration('use_sim_time')

    params_twist_mux = PathJoinSubstitution([
        pkg_share_navigation2,
        'params',
        'twist_mux.yaml'
    ])

    twist_mux_cmd = Node(
        package='twist_mux',
        executable='twist_mux',
        name='twist_mux',
        output='screen',
        parameters=[
            params_twist_mux,
            {'use_sim_time': use_sim_time}
        ],
        remappings=[
            ('cmd_vel_out', '/cmd_vel'),
        ]
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(twist_mux_cmd)

    return ld