#include "theimc_bt_nodes/wait_seconds.hpp"

namespace theimc_bt_nodes
{

WaitSeconds::WaitSeconds(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::StatefulActionNode(xml_tag_name, config)
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
}

BT::PortsList WaitSeconds::providedPorts()
{
  return {
    BT::InputPort<double>("seconds", "Seconds to wait"),
  };
}

BT::NodeStatus WaitSeconds::onStart()
{
  if (!getInput("seconds", seconds_) || seconds_ < 0.0) {
    RCLCPP_ERROR(node_->get_logger(), "WaitSeconds requires seconds >= 0");
    return BT::NodeStatus::FAILURE;
  }

  start_time_ = node_->now();
  return onRunning();
}

BT::NodeStatus WaitSeconds::onRunning()
{
  if ((node_->now() - start_time_).seconds() >= seconds_) {
    return BT::NodeStatus::SUCCESS;
  }
  return BT::NodeStatus::RUNNING;
}

void WaitSeconds::onHalted()
{
}

}  // namespace theimc_bt_nodes
