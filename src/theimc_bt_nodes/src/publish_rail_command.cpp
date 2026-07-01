#include "theimc_bt_nodes/publish_rail_command.hpp"

namespace theimc_bt_nodes
{

PublishRailCommand::PublishRailCommand(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::SyncActionNode(xml_tag_name, config)
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
  publisher_ = node_->create_publisher<std_msgs::msg::String>("/rail_command", rclcpp::QoS(10));
}

BT::PortsList PublishRailCommand::providedPorts()
{
  return {
    BT::InputPort<std::string>("command", "Rail command to publish"),
  };
}

BT::NodeStatus PublishRailCommand::tick()
{
  std::string command;
  if (!getInput("command", command) || command.empty()) {
    RCLCPP_ERROR(node_->get_logger(), "PublishRailCommand requires a non-empty command");
    return BT::NodeStatus::FAILURE;
  }

  std_msgs::msg::String msg;
  msg.data = command;
  publisher_->publish(msg);
  return BT::NodeStatus::SUCCESS;
}

}  // namespace theimc_bt_nodes
