#include "theimc_bt_nodes/wait_for_rail_state.hpp"

#include <algorithm>
#include <cctype>
#include <string>

namespace theimc_bt_nodes
{

namespace
{
std::string normalize(std::string value)
{
  value.erase(
    std::remove_if(
      value.begin(), value.end(),
      [](unsigned char character) {return std::isspace(character);}),
    value.end());
  std::transform(
    value.begin(), value.end(), value.begin(),
    [](unsigned char character) {return std::toupper(character);});
  return value;
}
}  // namespace

WaitForRailState::WaitForRailState(
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
  subscription_ = node_->create_subscription<std_msgs::msg::String>(
    "/rail_state",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::String::SharedPtr msg) {
      std::lock_guard<std::mutex> lock(mutex_);
      latest_state_ = normalize(msg->data);
      ++latest_sequence_;
    },
    options);
}

BT::PortsList WaitForRailState::providedPorts()
{
  return {
    BT::InputPort<std::string>("state", "Expected rail state"),
    BT::InputPort<bool>("accept_stale", false, "Accept a state received before this node started"),
    BT::InputPort<double>("timeout_sec", 0.0, "Timeout in seconds, or 0 for no timeout"),
  };
}

BT::NodeStatus WaitForRailState::onStart()
{
  std::string state;
  if (!getInput("state", state) || state.empty()) {
    RCLCPP_ERROR(node_->get_logger(), "WaitForRailState requires a non-empty state");
    return BT::NodeStatus::FAILURE;
  }

  getInput("accept_stale", accept_stale_);
  getInput("timeout_sec", timeout_sec_);
  expected_state_ = normalize(state);
  start_time_ = node_->now();

  {
    std::lock_guard<std::mutex> lock(mutex_);
    start_sequence_ = latest_sequence_;
  }

  return checkState();
}

BT::NodeStatus WaitForRailState::onRunning()
{
  return checkState();
}

void WaitForRailState::onHalted()
{
}

BT::NodeStatus WaitForRailState::checkState()
{
  callback_group_executor_.spin_some();

  std::lock_guard<std::mutex> lock(mutex_);
  const bool has_expected_state = latest_state_ == expected_state_;
  const bool is_new_message = latest_sequence_ > start_sequence_;
  if (has_expected_state && (accept_stale_ || is_new_message)) {
    return BT::NodeStatus::SUCCESS;
  }

  if (timeout_sec_ > 0.0 && (node_->now() - start_time_).seconds() >= timeout_sec_) {
    RCLCPP_ERROR(
      node_->get_logger(),
      "Timed out waiting for rail state [%s]. Latest state was [%s]",
      expected_state_.c_str(), latest_state_.c_str());
    return BT::NodeStatus::FAILURE;
  }

  return BT::NodeStatus::RUNNING;
}

}  // namespace theimc_bt_nodes
