#ifndef THEIMC_BT_NODES__WAIT_FOR_MISSION_TRIGGER_HPP_
#define THEIMC_BT_NODES__WAIT_FOR_MISSION_TRIGGER_HPP_

#include <memory>
#include <mutex>
#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include "std_msgs/msg/string.hpp"

namespace theimc_bt_nodes
{

class WaitForMissionTrigger : public BT::StatefulActionNode
{
public:
  WaitForMissionTrigger(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  BT::NodeStatus checkTrigger();

  std::mutex state_mutex_;
  bool triggered_{false};
  std::string latest_selected_rails_;
  std::string triggered_selected_rails_;
  rclcpp::Node::SharedPtr node_;
  rclcpp::CallbackGroup::SharedPtr callback_group_;
  rclcpp::executors::SingleThreadedExecutor callback_group_executor_;
  rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr trigger_subscription_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr selected_rails_subscription_;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__WAIT_FOR_MISSION_TRIGGER_HPP_
