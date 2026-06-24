#include "theimc_bt_nodes/go_to_pose.hpp"

#include <cmath>
#include <string>

namespace theimc_bt_nodes
{

GoToPose::GoToPose(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: nav2_behavior_tree::BtActionNode<nav2_msgs::action::NavigateToPose>(
    xml_tag_name, "/navigate_to_pose", config)
{
}

BT::PortsList GoToPose::providedPorts()
{
  return providedBasicPorts(
    {
      BT::InputPort<double>("x", "Goal x coordinate in the map frame"),
      BT::InputPort<double>("y", "Goal y coordinate in the map frame"),
      BT::InputPort<double>("yaw", "Goal yaw in radians"),
    });
}

void GoToPose::on_tick()
{
  double x = 0.0;
  double y = 0.0;
  double yaw = 0.0;

  if (!getInput("x", x) || !getInput("y", y) || !getInput("yaw", yaw)) {
    RCLCPP_ERROR(node_->get_logger(), "GoToPose requires x, y, and yaw input ports");
    should_send_goal_ = false;
    return;
  }

  goal_.pose.header.frame_id = "map";
  goal_.pose.header.stamp = node_->now();
  goal_.pose.pose.position.x = x;
  goal_.pose.pose.position.y = y;
  goal_.pose.pose.position.z = 0.0;

  const double half_yaw = yaw * 0.5;
  goal_.pose.pose.orientation.x = 0.0;
  goal_.pose.pose.orientation.y = 0.0;
  goal_.pose.pose.orientation.z = std::sin(half_yaw);
  goal_.pose.pose.orientation.w = std::cos(half_yaw);
}

BT::NodeStatus GoToPose::on_cancelled()
{
  return BT::NodeStatus::FAILURE;
}

}  // namespace theimc_bt_nodes
