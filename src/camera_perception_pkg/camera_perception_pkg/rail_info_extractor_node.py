import math
import time

import rclpy
from rclpy.node import Node

from interfaces_pkg.msg import DetectionArray, RailInfo


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class RailInfoExtractorNode(Node):
    def __init__(self):
        super().__init__('rail_info_extractor_node')

        self.declare_parameter('detections_topic', '/detections')
        self.declare_parameter('rail_info_topic', '/rail_info')
        self.declare_parameter('target_class_name', 'rail_start')

        self.declare_parameter('img_width', 640)
        self.declare_parameter('img_height', 480)
        self.declare_parameter('near_ratio', 0.85)
        self.declare_parameter('middle_ratio', 0.30)

        self.declare_parameter('publish_hz', 20.0)
        self.declare_parameter('hold_sec', 1.5)
        self.declare_parameter('min_score', 0.25)

        # smoothing: 0에 가까울수록 부드럽고 느림, 1에 가까울수록 즉각 반응
        self.declare_parameter('ema_alpha_cx', 0.35)
        self.declare_parameter('ema_alpha_cy', 0.35)
        self.declare_parameter('ema_alpha_angle', 0.25)

        self.declare_parameter('debug_log', False)

        detections_topic = self.get_parameter('detections_topic').value
        rail_info_topic = self.get_parameter('rail_info_topic').value

        self.target_class_name = str(self.get_parameter('target_class_name').value)
        self.img_width = int(self.get_parameter('img_width').value)
        self.img_height = int(self.get_parameter('img_height').value)
        self.near_ratio = float(self.get_parameter('near_ratio').value)
        self.middle_ratio = float(self.get_parameter('middle_ratio').value)

        self.publish_hz = float(self.get_parameter('publish_hz').value)
        self.hold_sec = float(self.get_parameter('hold_sec').value)
        self.min_score = float(self.get_parameter('min_score').value)

        self.ema_alpha_cx = float(self.get_parameter('ema_alpha_cx').value)
        self.ema_alpha_cy = float(self.get_parameter('ema_alpha_cy').value)
        self.ema_alpha_angle = float(self.get_parameter('ema_alpha_angle').value)

        self.debug_log = bool(self.get_parameter('debug_log').value)

        self.sub = self.create_subscription(
            DetectionArray,
            detections_topic,
            self.detections_callback,
            10
        )
        self.pub = self.create_publisher(RailInfo, rail_info_topic, 10)
        self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_publish)

        self.last_header = None
        self.last_seen_time = None

        self.filtered_cx = None
        self.filtered_cy = None
        self.filtered_angle = 0.0
        self.filtered_conf = 0.0
        self.filtered_distance = 'far'
        self.has_valid_rail = False

        self.get_logger().info(
            f'RailInfoExtractorNode started: target_class_name={self.target_class_name}'
        )

    def detections_callback(self, msg: DetectionArray):
        self.last_header = msg.header

        det = self._select_best_rail_detection(msg)
        if det is None:
            if self.debug_log:
                self.get_logger().info('no matched rail_start in detections')
            return

        score = self._get_confidence(det)
        if score < self.min_score:
            if self.debug_log:
                self.get_logger().info(f'skip low score: {score:.3f}')
            return

        raw_cx = self._get_bbox_center_x(det)
        raw_cy = self._get_bbox_center_y(det)
        raw_angle = self._estimate_angle_deg(det)

        if self.filtered_cx is None:
            self.filtered_cx = raw_cx
            self.filtered_cy = raw_cy
            self.filtered_angle = raw_angle
        else:
            self.filtered_cx = self._ema(self.filtered_cx, raw_cx, self.ema_alpha_cx)
            self.filtered_cy = self._ema(self.filtered_cy, raw_cy, self.ema_alpha_cy)
            self.filtered_angle = self._ema(self.filtered_angle, raw_angle, self.ema_alpha_angle)

        self.filtered_angle = clamp(self.filtered_angle, -30.0, 30.0)
        self.filtered_conf = score
        self.filtered_distance = self._estimate_distance_label(self.filtered_cy)

        self.last_seen_time = time.time()
        self.has_valid_rail = True

        if self.debug_log:
            self.get_logger().info(
                f'update rail: raw_cx={raw_cx:.1f}, raw_cy={raw_cy:.1f}, '
                f'f_cx={self.filtered_cx:.1f}, f_cy={self.filtered_cy:.1f}, '
                f'angle={self.filtered_angle:.2f}, score={score:.3f}, dist={self.filtered_distance}'
            )

    def timer_publish(self):
        rail_info = RailInfo()

        if self.last_header is not None:
            rail_info.header = self.last_header

        rail_info.img_width = self.img_width
        rail_info.img_height = self.img_height
        rail_info.img_cx = float(self.img_width) / 2.0
        rail_info.img_cy = float(self.img_height) / 2.0

        now = time.time()
        alive = (
            self.has_valid_rail and
            self.last_seen_time is not None and
            (now - self.last_seen_time) <= self.hold_sec
        )

        if not alive or self.filtered_cx is None or self.filtered_cy is None:
            rail_info.has_rail = False
            rail_info.rail_cx = 0.0
            rail_info.rail_cy = 0.0
            rail_info.angle_deg = 0.0
            rail_info.distance = 'far'
            rail_info.confidence = 0.0
            self.pub.publish(rail_info)
            return

        rail_info.has_rail = True
        rail_info.rail_cx = float(self.filtered_cx)
        rail_info.rail_cy = float(self.filtered_cy)
        rail_info.angle_deg = float(self.filtered_angle)
        rail_info.distance = self.filtered_distance
        rail_info.confidence = float(self.filtered_conf)

        self.pub.publish(rail_info)

    def _ema(self, prev, new, alpha):
        return (1.0 - alpha) * prev + alpha * new

    def _select_best_rail_detection(self, msg: DetectionArray):
        candidates = []

        img_cx = float(self.img_width) / 2.0

        for det in msg.detections:
            class_name = self._get_class_name(det)
            if class_name != self.target_class_name:
                continue

            score = self._get_confidence(det)
            cx = self._get_bbox_center_x(det)
            cy = self._get_bbox_center_y(det)

            # 중심에서 얼마나 벗어났는지 = 에러 크기
            error_abs = abs(img_cx - cx) / max(img_cx, 1.0)

            # near / middle / far 판정은 고정
            distance_label = self._estimate_distance_label(cy)

            if distance_label == 'near':
                # 가까우면 에러 큰 놈 우선
                rank = error_abs
            else:
                # 멀거나 중간이면 기존처럼 confidence + 아래쪽 약간 우대
                rank = score + 0.001 * cy

            candidates.append((rank, det))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def _estimate_distance_label(self, rail_cy: float) -> str:
        if rail_cy >= self.img_height * self.near_ratio:
            return 'near'
        elif rail_cy >= self.img_height * self.middle_ratio:
            return 'middle'
        else:
            return 'far'

    def _estimate_angle_deg(self, det) -> float:
        """
        rail_start mask가 있으면 mask 점들에 선형 근사해서 각도 추정.
        없으면 keypoints 시도.
        그것도 없으면 0.0
        """
        mask = getattr(det, 'mask', None)
        points = []

        if mask is not None and hasattr(mask, 'data'):
            for p in mask.data:
                x = self._safe_get_xy_x(p)
                y = self._safe_get_xy_y(p)
                if x is not None and y is not None:
                    points.append((x, y))

        if len(points) >= 2:
            return self._fit_angle_from_points(points)

        keypoints = getattr(det, 'keypoints', None)
        if keypoints is not None:
            raw_points = []
            if hasattr(keypoints, 'points'):
                raw_points = keypoints.points
            elif hasattr(keypoints, 'data'):
                raw_points = keypoints.data

            points = []
            for p in raw_points:
                x = self._safe_get_xy_x(p)
                y = self._safe_get_xy_y(p)
                if x is not None and y is not None:
                    points.append((x, y))

            if len(points) >= 2:
                return self._fit_angle_from_points(points)

        return 0.0

    def _fit_angle_from_points(self, points):
        n = len(points)
        mean_x = sum(p[0] for p in points) / n
        mean_y = sum(p[1] for p in points) / n

        sxx = 0.0
        sxy = 0.0
        for x, y in points:
            dx = x - mean_x
            dy = y - mean_y
            sxx += dx * dx
            sxy += dx * dy

        if abs(sxx) < 1e-6:
            return 0.0

        slope = sxy / sxx
        angle_from_x = math.degrees(math.atan(slope))

        # x축 기준 각도를 세로축 기준 비슷한 감각으로 변환
        # 완벽한 기하 보정보다는 안정적인 steering용 근사
        angle_from_vertical = -angle_from_x
        return float(clamp(angle_from_vertical, -30.0, 30.0))

    def _get_class_name(self, det) -> str:
        if hasattr(det, 'class_name'):
            return str(det.class_name)
        if hasattr(det, 'label'):
            return str(det.label)
        if hasattr(det, 'name'):
            return str(det.name)
        return ''

    def _get_confidence(self, det) -> float:
        if hasattr(det, 'score'):
            return float(det.score)
        if hasattr(det, 'confidence'):
            return float(det.confidence)
        if hasattr(det, 'conf'):
            return float(det.conf)
        return 0.0

    def _get_bbox_center_x(self, det) -> float:
        bbox = getattr(det, 'bbox', None)
        if bbox is None:
            return 0.0

        if hasattr(bbox, 'center'):
            center = bbox.center
            if hasattr(center, 'position'):
                pos = center.position
                if hasattr(pos, 'x'):
                    return float(pos.x)
            if hasattr(center, 'x'):
                return float(center.x)

        if hasattr(bbox, 'cx'):
            return float(bbox.cx)

        return 0.0

    def _get_bbox_center_y(self, det) -> float:
        bbox = getattr(det, 'bbox', None)
        if bbox is None:
            return 0.0

        if hasattr(bbox, 'center'):
            center = bbox.center
            if hasattr(center, 'position'):
                pos = center.position
                if hasattr(pos, 'y'):
                    return float(pos.y)
            if hasattr(center, 'y'):
                return float(center.y)

        if hasattr(bbox, 'cy'):
            return float(bbox.cy)

        return 0.0

    def _safe_get_xy_x(self, p):
        if hasattr(p, 'point') and hasattr(p.point, 'x'):
            return float(p.point.x)
        if hasattr(p, 'position') and hasattr(p.position, 'x'):
            return float(p.position.x)
        if hasattr(p, 'x'):
            return float(p.x)
        return None

    def _safe_get_xy_y(self, p):
        if hasattr(p, 'point') and hasattr(p.point, 'y'):
            return float(p.point.y)
        if hasattr(p, 'position') and hasattr(p.position, 'y'):
            return float(p.position.y)
        if hasattr(p, 'y'):
            return float(p.y)
        return None


def main(args=None):
    rclpy.init(args=args)
    node = RailInfoExtractorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()