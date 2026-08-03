#ifndef THEIMC_BT_NODES__WAIT_FOR_RAIL_STATE_HPP_
#define THEIMC_BT_NODES__WAIT_FOR_RAIL_STATE_HPP_

#include <chrono>
#include <cstdint>
#include <mutex>
#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

namespace theimc_bt_nodes
{

class WaitForRailState : public BT::StatefulActionNode
{
public:
  WaitForRailState(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  BT::NodeStatus checkState();

  rclcpp::Node::SharedPtr node_;
  rclcpp::CallbackGroup::SharedPtr callback_group_;
  rclcpp::executors::SingleThreadedExecutor callback_group_executor_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;

  std::mutex mutex_;
  std::string latest_state_;
  std::uint64_t latest_sequence_{0};
  std::uint64_t start_sequence_{0};
  std::string expected_state_;
  bool accept_stale_{false};
  double timeout_sec_{0.0};
  rclcpp::Time start_time_;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__WAIT_FOR_RAIL_STATE_HPP_
