#include "theimc_bt_nodes/save_current_pose.hpp"

#include "tf2/utils.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"

namespace theimc_bt_nodes
{

SaveCurrentPose::SaveCurrentPose(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::SyncActionNode(xml_tag_name, config),
  global_frame_("map"),
  robot_base_frame_("base_link")
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
  
  // Initialize TF Buffer and Listener to get the robot's current pose
  tf_buffer_ = std::make_shared<tf2_ros::Buffer>(node_->get_clock());
  tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
}

BT::PortsList SaveCurrentPose::providedPorts()
{
  return {
    BT::OutputPort<double>("save_x", "Saved X coordinate in the map frame"),
    BT::OutputPort<double>("save_y", "Saved Y coordinate in the map frame"),
    BT::OutputPort<double>("save_yaw", "Saved Yaw in radians"),
  };
}

BT::NodeStatus SaveCurrentPose::tick()
{
  geometry_msgs::msg::TransformStamped transform_stamped;

  try {
    // Look up the latest transform from the global frame to the robot base frame
    transform_stamped = tf_buffer_->lookupTransform(
      global_frame_, robot_base_frame_, tf2::TimePointZero, rclcpp::Duration::from_seconds(1.0));
  } catch (const tf2::TransformException & ex) {
    RCLCPP_ERROR(
      node_->get_logger(),
      "SaveCurrentPose failed to get transform from %s to %s: %s",
      global_frame_.c_str(), robot_base_frame_.c_str(), ex.what());
    return BT::NodeStatus::FAILURE;
  }

  // Extract translation (x, y)
  double current_x = transform_stamped.transform.translation.x;
  double current_y = transform_stamped.transform.translation.y;

  // Extract rotation (yaw)
  double current_yaw = tf2::getYaw(transform_stamped.transform.rotation);

  // Write values to the Blackboard
  if (!setOutput("save_x", current_x) || 
      !setOutput("save_y", current_y) || 
      !setOutput("save_yaw", current_yaw)) 
  {
    RCLCPP_ERROR(node_->get_logger(), "SaveCurrentPose failed to write outputs to the Blackboard");
    return BT::NodeStatus::FAILURE;
  }

  RCLCPP_INFO(
    node_->get_logger(),
    "SaveCurrentPose successfully saved robot pose: x=%.3f, y=%.3f, yaw=%.3f",
    current_x, current_y, current_yaw);

  return BT::NodeStatus::SUCCESS;
}

}  // namespace theimc_bt_nodes