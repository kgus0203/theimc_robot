import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

from geometry_msgs.msg import Twist

from time import sleep, time


class GlobalLocalizationManager(Node):
    def __init__(self):
        super().__init__('global_localization_manager')

        # =========================================================
        # AMCL 파티클 설정
        # =========================================================

        # 평소 주행용 파티클 수
        self.default_min_particles = 500
        self.default_max_particles = 1500

        # 글로벌 로컬라이제이션용 파티클 수
        self.global_min_particles = 2000
        self.global_max_particles = 10000

        # =========================================================
        # 제자리 회전 설정
        # =========================================================
        # 너무 빠르면 AMCL이 더 헷갈릴 수 있음
        self.rotate_speed = 0.15       # rad/s
        self.rotate_duration = 60.0    # seconds

        # =========================================================
        # ROS Client / Publisher
        # =========================================================
        self.relocalization_client = self.create_client(
            Empty,
            '/reinitialize_global_localization'
        )

        self.param_client = self.create_client(
            SetParameters,
            '/amcl/set_parameters'
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.ready = True

        if not self.relocalization_client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('/reinitialize_global_localization 서비스 없음!')
            self.ready = False

        if not self.param_client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('/amcl/set_parameters 서비스 없음!')
            self.ready = False

    # =========================================================
    # AMCL parameter 하나씩 설정
    # =========================================================
    def set_amcl_int_param(self, name, value):
        param = Parameter(
            name=name,
            value=ParameterValue(
                type=ParameterType.PARAMETER_INTEGER,
                integer_value=int(value)
            )
        )

        request = SetParameters.Request()
        request.parameters = [param]

        future = self.param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is None:
            self.get_logger().error(f'{name}={value} 설정 실패: 응답 없음')
            return False

        if len(future.result().results) == 0:
            self.get_logger().error(f'{name}={value} 설정 실패: 결과 없음')
            return False

        result = future.result().results[0]

        if not result.successful:
            self.get_logger().error(
                f'{name}={value} 설정 거절됨: {result.reason}'
            )
            return False

        self.get_logger().info(f'{name}={value} 설정 성공')
        return True

    # =========================================================
    # AMCL min/max particles 설정
    # =========================================================
    def set_amcl_particles(self, min_particles, max_particles):
        """
        중요:
        - 파티클 수를 늘릴 때는 max_particles 먼저 설정
        - 파티클 수를 줄일 때는 min_particles 먼저 설정

        이유:
        현재 min_particles가 2000인데 max_particles를 1500으로 먼저 줄이면
        순간적으로 max < min 상태가 되어 AMCL이 거절할 수 있음.
        """

        min_particles = int(min_particles)
        max_particles = int(max_particles)

        self.get_logger().info(
            f'AMCL 파티클 변경 요청: min={min_particles}, max={max_particles}'
        )

        # 글로벌용처럼 max가 큰 경우: max 먼저 증가
        if max_particles > self.default_max_particles:
            ok1 = self.set_amcl_int_param('max_particles', max_particles)
            sleep(0.2)
            ok2 = self.set_amcl_int_param('min_particles', min_particles)

        # 기본값 복원처럼 줄이는 경우: min 먼저 감소
        else:
            ok1 = self.set_amcl_int_param('min_particles', min_particles)
            sleep(0.2)
            ok2 = self.set_amcl_int_param('max_particles', max_particles)

        if ok1 and ok2:
            self.get_logger().info(
                f'AMCL 파티클 설정 완료: min={min_particles}, max={max_particles}'
            )
            return True

        self.get_logger().error(
            f'AMCL 파티클 설정 일부 실패: min={min_particles}, max={max_particles}'
        )
        return False

    # =========================================================
    # Global Localization 호출
    # =========================================================
    def call_global_localization_service(self):
        if not self.relocalization_client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('/reinitialize_global_localization 서비스 없음!')
            return False

        req = Empty.Request()
        future = self.relocalization_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is None:
            self.get_logger().error('Global Localization 호출 실패')
            return False

        self.get_logger().info('Global Localization 호출 완료')
        return True

    # =========================================================
    # 로봇 정지
    # =========================================================
    def stop_robot(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0

        for _ in range(10):
            self.cmd_pub.publish(msg)
            sleep(0.05)

        self.get_logger().info('로봇 정지 명령 전송 완료')

    # =========================================================
    # 제자리 회전
    # =========================================================
    def rotate_in_place(self):
        self.get_logger().info(
            f'제자리 회전 시작: speed={self.rotate_speed}, duration={self.rotate_duration}s'
        )

        start_time = time()
        rate_hz = 20.0
        dt = 1.0 / rate_hz

        while rclpy.ok() and (time() - start_time) < self.rotate_duration:
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = self.rotate_speed

            self.cmd_pub.publish(msg)

            rclpy.spin_once(self, timeout_sec=0.01)
            sleep(dt)

        self.stop_robot()
        self.get_logger().info('제자리 회전 완료')

    # =========================================================
    # 전체 실행 루틴
    # =========================================================
    def run(self):
        if not self.ready:
            self.get_logger().error('노드 준비 실패. 종료합니다.')
            return

        try:
            # 1. 글로벌 로컬라이제이션용 파티클 수 증가
            ok = self.set_amcl_particles(
                self.global_min_particles,
                self.global_max_particles
            )

            if not ok:
                self.get_logger().error('글로벌용 파티클 수 설정 실패')
                return

            sleep(1.0)

            # 2. 글로벌 로컬라이제이션 호출
            ok = self.call_global_localization_service()

            if not ok:
                self.get_logger().error('Global Localization 실패')
                return

            sleep(1.0)

            # 3. 로봇 제자리 회전
            self.rotate_in_place()

            # 4. AMCL 안정화 대기
            self.get_logger().info('AMCL 안정화 대기 중...')
            sleep(3.0)

        finally:
            # 5. 무조건 기본 파티클 수로 복원 시도
            self.get_logger().info('AMCL 파티클 수 기본값 복원 시도')

            self.set_amcl_particles(
                self.default_min_particles,
                self.default_max_particles
            )

            self.stop_robot()

            self.get_logger().info('Global Localization 루틴 종료')
            self.get_logger().info(
                '확인 명령어: ros2 param get /amcl min_particles'
            )
            self.get_logger().info(
                '확인 명령어: ros2 param get /amcl max_particles'
            )


def main(args=None):
    rclpy.init(args=args)

    node = GlobalLocalizationManager()

    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().warn('KeyboardInterrupt 감지됨. 로봇 정지 후 종료합니다.')
        node.stop_robot()
        node.set_amcl_particles(
            node.default_min_particles,
            node.default_max_particles
        )
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()