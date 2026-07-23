'''
아루코 마커 위치 찾기 test에 사용 launch 파일 실행 후
ros2 service call /toggle_docking std_srvs/srv/SetBool "{data: true}”
'''
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    
    # 1. 카메라 이미지 퍼블리셔 노드 (파라미터 포함)
    camera_node = Node(
        package='camera_perception_pkg',
        executable='image_publisher_node',
        name='image_publisher_node',
        output='screen',
        parameters=[
            {'realsense_timeout_ms': 1000}
        ]
    )

    # 2. ArUco 마커 디텍터 노드
    detector_node = Node(
        package='camera_perception_pkg',
        executable='aruco_detector_node',
        name='aruco_detector_node',
        output='screen'
    )

    # 3. ArUco 도킹 제어 노드
    docker_node = Node(
        package='decision_making_pkg',
        executable='aruco_docker_node',
        name='aruco_docker_node',
        output='screen'
    )

    # # 4. 자동 도킹 시작 서비스 콜 (명령어 실행)
    # start_docking_cmd = ExecuteProcess(
    #     cmd=['ros2', 'service', 'call', '/toggle_docking', 'std_srvs/srv/SetBool', '{data: true}'],
    #     output='screen'
    # )
    
    # # 노드들이 켜질 시간을 벌어주기 위해 3초 지연 후 서비스 콜 실행
    # delayed_service_call = TimerAction(
    #     period=3.0, 
    #     actions=[start_docking_cmd]
    # )

    # 5. LaunchDescription에 모든 액션 추가
    return LaunchDescription([
        camera_node,
        detector_node,
        docker_node,
        # delayed_service_call
    ])