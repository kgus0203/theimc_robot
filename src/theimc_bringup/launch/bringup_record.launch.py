import os
from datetime import datetime
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # ⭐ 1. 현재 날짜/시간으로 기본 폴더 이름을 자동으로 생성합니다.
    # (예: drive_20260716_143522)
    auto_timestamp_name = 'drive_' + datetime.now().strftime('%Y%m%d_%H%M%S')

    # 저장할 bag 파일 폴더 이름을 인자로 설정 (기본값에 자동 생성된 타임스탬프 대입!)
    bag_name_arg = DeclareLaunchArgument(
        'bag_name',
        default_value=auto_timestamp_name,
        description='Name of the output bag directory'
    )
    
    # 2. STM32 통신 및 센서 데이터 발행 노드 실행
    bringup_node = Node(
        package='theimc_bringup',
        executable='bringup_node',
        name='bringup_node',
        output='screen',
        parameters=[{
            'use_stm_odom': True,
            'use_stm_imu': True,
            'use_stm_wheel': True
        }]
    )

    # 3. 자동으로 지정한 핵심 토픽만 골라서 ros2 bag 기록 실행
    record_bag = ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'record',
            '-o', LaunchConfiguration('bag_name'),
            '/wheel/odom',
            '/imu',
            '/tof_distance',
            '/rail_state',
            '/cmd_vel',
            '/cmd_rail',
            'joint_states'
            '/scan'
        ],
        output='screen'
    )

    # 4. 실시간 CSV 기록 스크립트 실행 정의
    csv_logger_script = os.path.expanduser('~/theimc_robot/auto_csv_logger.py')
    record_csv = ExecuteProcess(
        cmd=['python3', csv_logger_script],
        output='screen'
    )

    return LaunchDescription([
        bag_name_arg,
        bringup_node,
        record_bag,
        record_csv  
    ])