import os
import csv
import math
from datetime import datetime
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan

class AutoCSVLogger(Node):
    def __init__(self):
        super().__init__('auto_csv_logger')
        
        # 1. 저장할 폴더 생성 (홈 디렉토리 아래 csv_logs)
        self.save_dir = os.path.expanduser('~/theimc_robot/csv_logs')
        os.makedirs(self.save_dir, exist_ok=True)
        
        # 2. 현재 날짜/시간으로 고유한 파일 이름 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.odom_file_path = os.path.join(self.save_dir, f'odom_{timestamp}.csv')
        self.imu_file_path = os.path.join(self.save_dir, f'imu_{timestamp}.csv')
        self.scan_file_path = os.path.join(self.save_dir, f'scan_{timestamp}.csv')
        
        # 3. CSV 파일 초기화 (Odom, IMU)
        self.odom_file = open(self.odom_file_path, 'w', newline='')
        self.odom_writer = csv.writer(self.odom_file)
        self.odom_writer.writerow([
            'time_sec', 'pos_x', 'pos_y', 'pos_z', 
            'ori_x', 'ori_y', 'ori_z', 'ori_w', 
            'linear_vel_x', 'angular_vel_z'
        ])
        
        self.imu_file = open(self.imu_file_path, 'w', newline='')
        self.imu_writer = csv.writer(self.imu_file)
        self.imu_writer.writerow([
            'time_sec', 'accel_x', 'accel_y', 'accel_z', 
            'gyro_x', 'gyro_y', 'gyro_z', 'ori_x', 'ori_y', 'ori_z', 'ori_w'
        ])
        
        # ⭐ 라이다용 CSV 파일 지연 초기화 (첫 데이터를 수신할 때 채널 수를 확인하여 생성)
        self.scan_file = None
        self.scan_writer = None
        
        # 기준 시작 시간 기록
        self.start_time = self.get_clock().now()
        
        # 4. 토픽 구독 설정 (오도메트리, IMU, 그리고 라이다 추가)
        self.odom_sub = self.create_subscription(Odometry, '/wheel/odom', self.odom_callback, 10)
        self.imu_sub = self.create_subscription(Imu, '/imu', self.imu_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        self.get_logger().info('==================================================')
        self.get_logger().info(f'💾 [자동 CSV 기록 개시] LiDAR(/scan) 기록이 통합되었습니다.')
        self.get_logger().info(f'📂 저장 경로: {self.save_dir}')
        self.get_logger().info(f'⏱️ 생성 시간 키: {timestamp}')
        self.get_logger().info('==================================================')

    def get_relative_time(self):
        now = self.get_clock().now()
        diff = now - self.start_time
        return diff.nanoseconds / 1e9

    def odom_callback(self, msg):
        time_sec = self.get_relative_time()
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation
        linear = msg.twist.twist.linear
        angular = msg.twist.twist.angular
        
        self.odom_writer.writerow([
            time_sec, pos.x, pos.y, pos.z,
            ori.x, ori.y, ori.z, ori.w,
            linear.x, angular.z
        ])
        self.odom_file.flush()

    def imu_callback(self, msg):
        time_sec = self.get_relative_time()
        accel = msg.linear_acceleration
        gyro = msg.angular_velocity
        ori = msg.orientation
        
        self.imu_writer.writerow([
            time_sec, accel.x, accel.y, accel.z,
            gyro.x, gyro.y, gyro.z, ori.x, ori.y, ori.z, ori.w
        ])
        self.imu_file.flush()

    # ⭐ 라이다 데이터 처리 콜백 추가
    def scan_callback(self, msg):
        time_sec = self.get_relative_time()
        
        # 첫 메시지 수신 시 라이다 채널 크기에 맞추어 헤더 자동 생성
        if self.scan_writer is None:
            num_ranges = len(msg.ranges)
            self.scan_file = open(self.scan_file_path, 'w', newline='')
            self.scan_writer = csv.writer(self.scan_file)
            
            # 헤더 구성
            header = ['time_sec', 'angle_min', 'angle_max', 'angle_increment', 'range_min', 'range_max']
            header += [f'range_{i}' for i in range(num_ranges)]
            self.scan_writer.writerow(header)
            self.get_logger().info(f'📡 [LiDAR 데이터 수집 개시] 감지된 데이터 채널 수: {num_ranges}개')
            
        # inf, nan 등 측정 실패 값을 0.0으로 정제하고 소수점 4자리까지 반올림
        processed_ranges = []
        for r in msg.ranges:
            if math.isnan(r) or math.isinf(r):
                processed_ranges.append(0.0)
            else:
                processed_ranges.append(round(r, 4))
                
        # 데이터 행 작성
        row = [time_sec, msg.angle_min, msg.angle_max, msg.angle_increment, msg.range_min, msg.range_max] + processed_ranges
        self.scan_writer.writerow(row)
        self.scan_file.flush()

    def destroy_node(self):
        self.odom_file.close()
        self.imu_file.close()
        if self.scan_file is not None:
            self.scan_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = AutoCSVLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('💾 기록을 중단하고 파일을 안전하게 닫았습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()