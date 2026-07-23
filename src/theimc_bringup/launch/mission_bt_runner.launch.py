from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'bt_xml',
            default_value=PathJoinSubstitution([
                FindPackageShare('theimc_bt_nodes'),
                'bt_xml',
                'theimc_bt.xml',
            ]),
            description='Optional absolute path to the mission BT XML',
        ),
        DeclareLaunchArgument(
            'rails_yaml',
            default_value=PathJoinSubstitution([
                FindPackageShare('theimc_bt_nodes'),
                'config',
                'rails.yaml',
            ]),
            description='Absolute path to the rail approach pose YAML file',
        ),
        Node(
            package='theimc_bt_nodes',
            executable='mission_bt_runner',
            name='mission_bt_runner',
            output='screen',
            parameters=[{
                'bt_xml': LaunchConfiguration('bt_xml'),
                'rails_yaml': LaunchConfiguration('rails_yaml'),
            }],
        ),
    ])
