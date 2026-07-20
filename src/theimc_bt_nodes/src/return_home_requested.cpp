#include "theimc_bt_nodes/return_home_requested.hpp"

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

ReturnHomeRequested::ReturnHomeRequested(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::ConditionNode(xml_tag_name, config)
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
  callback_group_ = node_->create_callback_group(
    rclcpp::CallbackGroupType::MutuallyExclusive, false);
  callback_group_executor_.add_callback_group(
    callback_group_, node_->get_node_base_interface());

  rclcpp::SubscriptionOptions options;
  options.callback_group = callback_group_;

  rail_state_subscription_ = node_->create_subscription<std_msgs::msg::String>(
    "/rail_state",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::String::SharedPtr msg) {
      std::lock_guard<std::mutex> lock(mutex_);
      latest_rail_state_ = normalize(msg->data);
    },
    options);

  return_home_subscription_ = node_->create_subscription<std_msgs::msg::Bool>(
    "/return_home",
    rclcpp::QoS(10),
    [this](const std_msgs::msg::Bool::SharedPtr msg) {
      if (!msg->data) {
        return;
      }
      std::lock_guard<std::mutex> lock(mutex_);
      return_home_requested_ = true;
      RCLCPP_WARN(node_->get_logger(), "Return-home request received");
    },
    options);
}

BT::PortsList ReturnHomeRequested::providedPorts()
{
  return {
    BT::OutputPort<std::string>(
      "return_mode", "ON_RAIL when the robot must leave the rail, otherwise DIRECT"),
  };
}

BT::NodeStatus ReturnHomeRequested::tick()
{
  callback_group_executor_.spin_some();

  std::lock_guard<std::mutex> lock(mutex_);
  if (!return_home_requested_) {
    return BT::NodeStatus::FAILURE;
  }

  const std::string return_mode =
    latest_rail_state_ == "ON_RAIL" ? "ON_RAIL" : "DIRECT";
  if (!setOutput("return_mode", return_mode)) {
    RCLCPP_ERROR(node_->get_logger(), "Failed to write return_mode output");
    return BT::NodeStatus::FAILURE;
  }

  return_home_requested_ = false;
  RCLCPP_WARN(
    node_->get_logger(),
    "Starting return-home flow: mode=%s, latest_rail_state=%s",
    return_mode.c_str(),
    latest_rail_state_.empty() ? "UNKNOWN" : latest_rail_state_.c_str());
  return BT::NodeStatus::SUCCESS;
}

}  // namespace theimc_bt_nodes
