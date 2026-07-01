#ifndef THEIMC_BT_NODES__PUBLISH_RAIL_COMMAND_HPP_
#define THEIMC_BT_NODES__PUBLISH_RAIL_COMMAND_HPP_

#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

namespace theimc_bt_nodes
{

class PublishRailCommand : public BT::SyncActionNode
{
public:
  PublishRailCommand(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus tick() override;

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__PUBLISH_RAIL_COMMAND_HPP_
