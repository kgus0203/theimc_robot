#include "theimc_bt_nodes/rail_approach.hpp"

#include <string>

namespace theimc_bt_nodes
{

RailApproach::RailApproach(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: nav2_behavior_tree::BtActionNode<interfaces_pkg::action::RailApproach>(
    xml_tag_name, "/rail_approach", config)
{
}

BT::PortsList RailApproach::providedPorts()
{
  return providedBasicPorts(
    {
      BT::InputPort<double>("timeout_sec", 20.0, "Rail approach timeout in seconds"),
      BT::InputPort<double>("x_tolerance", 0.25, "Allowed x error"),
      BT::InputPort<double>("angle_tolerance", 5.0, "Allowed angle error"),
      BT::InputPort<bool>("allow_reverse_align", false, "Allow reverse rail alignment"),
    });
}

void RailApproach::on_tick()
{
  double timeout_sec = 20.0;
  double x_tolerance = 0.25;
  double angle_tolerance = 5.0;
  bool allow_reverse_align = false;

  getInput("timeout_sec", timeout_sec);
  getInput("x_tolerance", x_tolerance);
  getInput("angle_tolerance", angle_tolerance);
  getInput("allow_reverse_align", allow_reverse_align);

  goal_.timeout_sec = static_cast<float>(timeout_sec);
  goal_.x_tolerance = static_cast<float>(x_tolerance);
  goal_.angle_tolerance = static_cast<float>(angle_tolerance);
  goal_.allow_reverse_align = allow_reverse_align;
}

BT::NodeStatus RailApproach::on_success()
{
  if (result_.result->success) {
    return BT::NodeStatus::SUCCESS;
  }

  RCLCPP_ERROR(
    node_->get_logger(),
    "RailApproach failed: %s", result_.result->reason.c_str());
  return BT::NodeStatus::FAILURE;
}

BT::NodeStatus RailApproach::on_aborted()
{
  return BT::NodeStatus::FAILURE;
}

BT::NodeStatus RailApproach::on_cancelled()
{
  return BT::NodeStatus::FAILURE;
}

}  // namespace theimc_bt_nodes
