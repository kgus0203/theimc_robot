#include "theimc_bt_nodes/wait_for_mission_trigger.hpp"

#include <functional>
#include <string>

namespace theimc_bt_nodes
{

WaitForMissionTrigger::WaitForMissionTrigger(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::StatefulActionNode(xml_tag_name, config)
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
  callback_group_ = node_->create_callback_group(
    rclcpp::CallbackGroupType::MutuallyExclusive, false);
  callback_group_executor_.add_callback_group(
    callback_group_, node_->get_node_base_interface());

  rclcpp::SubscriptionOptions options;
  options.callback_group = callback_group_;
  subscription_ = node_->create_subscription<std_msgs::msg::Bool>(
    "/mission_trigger",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::Bool::SharedPtr msg) {
      if (msg->data) {
        triggered_.store(true);
      }
    },
    options);
}

BT::PortsList WaitForMissionTrigger::providedPorts()
{
  return {};
}

BT::NodeStatus WaitForMissionTrigger::onStart()
{
  return checkTrigger();
}

BT::NodeStatus WaitForMissionTrigger::onRunning()
{
  return checkTrigger();
}

void WaitForMissionTrigger::onHalted()
{
}

BT::NodeStatus WaitForMissionTrigger::checkTrigger()
{
  callback_group_executor_.spin_some();
  if (triggered_.exchange(false)) {
    return BT::NodeStatus::SUCCESS;
  }
  return BT::NodeStatus::RUNNING;
}

}  // namespace theimc_bt_nodes
