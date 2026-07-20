#include "theimc_bt_nodes/wait_for_mission_trigger.hpp"

#include <algorithm>
#include <cctype>
#include <functional>
#include <string>

namespace theimc_bt_nodes
{
namespace
{

std::string trim(const std::string & value)
{
  const auto first = std::find_if_not(
    value.begin(), value.end(), [](unsigned char character) {return std::isspace(character);});
  if (first == value.end()) {
    return {};
  }
  const auto last = std::find_if_not(
    value.rbegin(), value.rend(), [](unsigned char character) {return std::isspace(character);})
    .base();
  return std::string(first, last);
}

}  // namespace

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
  selected_rails_subscription_ = node_->create_subscription<std_msgs::msg::String>(
    "/selected_rails",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::String::SharedPtr msg) {
      const auto selected_rails = trim(msg->data);
      {
        std::lock_guard<std::mutex> lock(state_mutex_);
        latest_selected_rails_ = selected_rails;
      }
      if (selected_rails.empty()) {
        RCLCPP_WARN(node_->get_logger(), "Received an empty selected rail list");
      } else {
        RCLCPP_INFO(
          node_->get_logger(), "Received selected rail list: '%s'", selected_rails.c_str());
      }
    },
    options);

  trigger_subscription_ = node_->create_subscription<std_msgs::msg::Bool>(
    "/mission_trigger",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::Bool::SharedPtr msg) {
      if (msg->data) {
        std::lock_guard<std::mutex> lock(state_mutex_);
        if (latest_selected_rails_.empty()) {
          RCLCPP_WARN(
            node_->get_logger(),
            "Ignoring mission trigger because no selected rails have been received");
          return;
        }
        triggered_selected_rails_ = latest_selected_rails_;
        triggered_ = true;
        RCLCPP_INFO(
          node_->get_logger(), "Mission triggered with selected rails: '%s'",
          triggered_selected_rails_.c_str());
      }
    },
    options);
}

BT::PortsList WaitForMissionTrigger::providedPorts()
{
  return {
    BT::OutputPort<std::string>(
      "selected_rails", "Selected rail list captured when the mission is triggered"),
  };
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
  std::lock_guard<std::mutex> lock(state_mutex_);
  triggered_ = false;
  triggered_selected_rails_.clear();
  RCLCPP_INFO(node_->get_logger(), "WaitForMissionTrigger halted");
}

BT::NodeStatus WaitForMissionTrigger::checkTrigger()
{
  callback_group_executor_.spin_some();
  std::lock_guard<std::mutex> lock(state_mutex_);
  if (triggered_) {
    if (!setOutput("selected_rails", triggered_selected_rails_)) {
      RCLCPP_ERROR(node_->get_logger(), "Failed to write selected_rails output");
      triggered_ = false;
      triggered_selected_rails_.clear();
      return BT::NodeStatus::FAILURE;
    }
    triggered_ = false;
    triggered_selected_rails_.clear();
    return BT::NodeStatus::SUCCESS;
  }
  return BT::NodeStatus::RUNNING;
}

}  // namespace theimc_bt_nodes
