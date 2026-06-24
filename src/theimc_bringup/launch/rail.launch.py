from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='camera_perception_pkg',
            executable='image_publisher_node',
            name='image_publisher_node',
            output='screen',
        ),
        Node(
            package='camera_perception_pkg',
            executable='yolov8_node',
            name='yolov8_node',
            output='screen',
        ),
        Node(
            package='camera_perception_pkg',
            executable='rail_info_extractor_node',
            name='rail_info_extractor_node',
            output='screen',
            parameters=[
                {
                    # rail_start 검출이 사라지면 0.5초 안에 has_rail=false로 전환
                    'hold_sec': 0.5,
                    'ema_alpha_bbox': 0.35,
                }
            ],
        ),
        Node(
            package='decision_making_pkg',
            executable='rail_approach_action_server_node',
            name='rail_approach_action_server_node',
            output='screen',
            parameters=[
                {
                    # 레일 인식 결과를 받는 토픽
                    # rail_info_extractor_node 같은 노드가 이 토픽으로 RailInfo 메시지를 publish해야 함
                    'rail_info_topic': '/rail_info',

                    # 로봇 속도 명령을 내보낼 토픽
                    # 지금은 바로 /cmd_vel로 보내므로 실제 로봇이 바로 움직일 수 있음
                    # Nav2와 같이 쓸 경우에는 /cmd_vel_rail로 두고 twist_mux를 거쳐 /cmd_vel로 합치는 게 더 안전함
                    'cmd_vel_topic': '/cmd_vel',

                    # 제어 주기
                    'control_rate_hz': 20.0,

                    # ALIGN 상태에서 제자리 회전 속도
                    'angular_speed': 0.08,

                    # PULSE_FORWARD 상태: 짧게 전진
                    'pulse_linear_speed': 0.08,
                    'pulse_forward_sec': 0.2,

                    # rail_info가 이 시간 이상 갱신되지 않으면 즉시 정지
                    'rail_timeout_sec': 0.5,

                    # rail_start bbox 면적이 화면에서 이 비율 이상이면 가까워졌다고 판단
                    'close_bbox_area_ratio': 0.18,

                    # 성공 알림 토픽
                    'success_topic': '/rail_approach_success',

                    # 레일 진입 명령 토픽
                    'rail_command_topic': '/rail_command',
                }
            ]
        ),
    ])
