#ifndef THEIMC_BT_NODES__RETURN_HOME_REQUESTED_HPP_
#define THEIMC_BT_NODES__RETURN_HOME_REQUESTED_HPP_

#include <mutex>
#include <string>

#include "behaviortree_cpp_v3/condition_node.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include "std_msgs/msg/string.hpp"

namespace theimc_bt_nodes
{

class ReturnHomeRequested : public BT::ConditionNode
{
public:
  ReturnHomeRequested(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus tick() override;

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::CallbackGroup::SharedPtr callback_group_;
  rclcpp::executors::SingleThreadedExecutor callback_group_executor_;
  rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr return_home_subscription_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr rail_state_subscription_;

  std::mutex mutex_;
  bool return_home_requested_{false};
  std::string latest_rail_state_;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__RETURN_HOME_REQUESTED_HPP_
