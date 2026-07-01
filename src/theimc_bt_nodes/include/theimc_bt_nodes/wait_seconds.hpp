#ifndef THEIMC_BT_NODES__WAIT_SECONDS_HPP_
#define THEIMC_BT_NODES__WAIT_SECONDS_HPP_

#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "rclcpp/rclcpp.hpp"

namespace theimc_bt_nodes
{

class WaitSeconds : public BT::StatefulActionNode
{
public:
  WaitSeconds(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Time start_time_;
  double seconds_{0.0};
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__WAIT_SECONDS_HPP_
