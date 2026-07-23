#ifndef THEIMC_BT_NODES__SAVE_CURRENT_POSE_HPP_
#define THEIMC_BT_NODES__SAVE_CURRENT_POSE_HPP_

#include <memory>
#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"

namespace theimc_bt_nodes
{

class SaveCurrentPose : public BT::SyncActionNode
{
public:
  SaveCurrentPose(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus tick() override;

private:
  rclcpp::Node::SharedPtr node_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
  
  std::string global_frame_;
  std::string robot_base_frame_;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__SAVE_CURRENT_POSE_HPP_