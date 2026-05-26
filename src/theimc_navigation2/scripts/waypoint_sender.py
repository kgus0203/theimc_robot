#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import yaml
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient

class WaypointSender(Node):
    def __init__(self):
        super().__init__('waypoint_sender')

        # Load YAML
        yaml_path = self.declare_parameter('waypoint_file').get_parameter_value().string_value

        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        self.waypoints = data["waypoints"]

        self.client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

        self.timer = self.create_timer(2.0, self.send_waypoints)

    def send_waypoints(self):
        if not self.client.wait_for_server(timeout_sec=1.0):
            return
        
        poses = []
        for wp in self.waypoints:
            ps = PoseStamped()
            ps.header.frame_id = 'map'
            ps.pose.position.x = wp['x']
            ps.pose.position.y = wp['y']
            ps.pose.orientation.z = wp['yaw']  # 간단 처리
            poses.append(ps)

        goal = FollowWaypoints.Goal()
        goal.poses = poses

        self.client.send_goal_async(goal)
        self.get_logger().info("Waypoints sent!")
        self.timer.cancel()

def main():
    rclpy.init()
    node = WaypointSender()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

