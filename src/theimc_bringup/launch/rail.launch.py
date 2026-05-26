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
                    'cmd_vel_topic': '/cmd_vel_rail',

                    # 제어 주기
                    # 20Hz = 1초에 20번 속도 명령 계산
                    'control_rate_hz': 10.0,

                    # 화면 중심 x 오차에 대한 P 게인
                    # x_error가 클수록 더 강하게 회전해서 중심을 맞춤
                    'kp_x': 0.35,

                    # 화면 중심 x 오차에 대한 D 게인
                    # x_error 변화량을 보고 흔들림을 줄이는 역할
                    'kd_x': 0.08,

                    # 레일 각도 오차에 대한 P 게인
                    # angle_error가 클수록 더 강하게 회전해서 각도를 맞춤
                    'kp_angle': 0.012,

                    # 레일 각도 오차에 대한 D 게인
                    # angle_error 변화량을 보고 각도 보정 시 흔들림을 줄임
                    'kd_angle': 0.004,

                    # 최대 직선 속도 제한
                    # 단위는 m/s
                    'max_linear': 0.12,

                    # 최대 회전 속도 제한
                    # 단위는 rad/s
                    'max_angular': 0.15,

                    # 전진할 때 최소 직선 속도
                    # 너무 작은 속도 명령 때문에 모터가 안 움직이는 것을 방지
                    'min_forward_speed': 0.035,

                    # 레일 정보를 못 찾았을 때 제자리 회전 탐색 속도
                    # /rail_info가 없거나 has_rail=false이면 이 속도로 회전
                    'search_angular_speed': 0.08,

                    # 레일이 멀리 있을 때 접근 속도
                    # distance == 'far'일 때 사용
                    'far_speed': 0.09,

                    # 레일이 중간 거리에 있을 때 접근 속도
                    # distance == 'middle'일 때 사용
                    'middle_speed': 0.06,

                    # 레일이 가까울 때 접근 속도
                    # distance == 'near'일 때 사용
                    'near_speed': 0.035,

                    # rail_info가 이 시간 이상 갱신되지 않으면 레일을 잃어버렸다고 판단
                    # 단위는 초
                    'rail_timeout_sec': 0.7,

                    # 성공 판정 유지 시간
                    # near 상태이면서 x 오차와 angle 오차가 허용 범위 안에
                    # 이 시간 동안 유지되면 action 성공 처리
                    'success_hold_sec': 0.8,
                }
            ]
        ),
    ])