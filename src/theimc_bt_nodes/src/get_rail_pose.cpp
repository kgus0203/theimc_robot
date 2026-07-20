#include "theimc_bt_nodes/get_rail_pose.hpp"

#include <exception>
#include <string>

#include "yaml-cpp/yaml.h"

namespace theimc_bt_nodes
{

GetRailPose::GetRailPose(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & config)
: BT::SyncActionNode(xml_tag_name, config)
{
  node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");
  try {
    yaml_path_ = config.blackboard->get<std::string>("rails_yaml");
    loadRailPoses(yaml_path_);
  } catch (const std::exception & exception) {
    load_error_ = exception.what();
    RCLCPP_ERROR(
      node_->get_logger(), "GetRailPose failed to load rails YAML: %s", load_error_.c_str());
  }
}

BT::PortsList GetRailPose::providedPorts()
{
  return {
    BT::InputPort<int>("rail_id", "Rail ID in the range 1..12"),
    BT::OutputPort<double>("x", "Rail approach x coordinate"),
    BT::OutputPort<double>("y", "Rail approach y coordinate"),
    BT::OutputPort<double>("yaw", "Rail approach yaw in radians"),
  };
}

void GetRailPose::loadRailPoses(const std::string & yaml_path)
{
  const YAML::Node root = YAML::LoadFile(yaml_path);
  const YAML::Node rails = root["rails"];
  if (!rails || !rails.IsMap()) {
    throw std::runtime_error("missing top-level 'rails' map in " + yaml_path);
  }

  for (const auto & entry : rails) {
    const int rail_id = entry.first.as<int>();
    const YAML::Node pose = entry.second;
    if (!pose["x"] || !pose["y"] || !pose["yaw"]) {
      throw std::runtime_error(
              "rail " + std::to_string(rail_id) + " requires x, y, and yaw in " + yaml_path);
    }
    rail_poses_[rail_id] = RailPose{
      pose["x"].as<double>(), pose["y"].as<double>(), pose["yaw"].as<double>()};
  }

  RCLCPP_INFO(
    node_->get_logger(), "GetRailPose loaded %zu rail poses from %s",
    rail_poses_.size(), yaml_path.c_str());
}

BT::NodeStatus GetRailPose::tick()
{
  if (!load_error_.empty()) {
    RCLCPP_ERROR(
      node_->get_logger(), "GetRailPose cannot run because YAML loading failed: %s",
      load_error_.c_str());
    return BT::NodeStatus::FAILURE;
  }

  int rail_id = 0;
  if (!getInput("rail_id", rail_id)) {
    RCLCPP_ERROR(node_->get_logger(), "GetRailPose requires rail_id input");
    return BT::NodeStatus::FAILURE;
  }

  const auto pose = rail_poses_.find(rail_id);
  if (pose == rail_poses_.end()) {
    RCLCPP_ERROR(
      node_->get_logger(), "GetRailPose rail ID %d does not exist in %s",
      rail_id, yaml_path_.c_str());
    return BT::NodeStatus::FAILURE;
  }

  if (!setOutput("x", pose->second.x) || !setOutput("y", pose->second.y) ||
    !setOutput("yaw", pose->second.yaw))
  {
    RCLCPP_ERROR(node_->get_logger(), "GetRailPose failed to write pose outputs for rail %d", rail_id);
    return BT::NodeStatus::FAILURE;
  }

  RCLCPP_INFO(
    node_->get_logger(), "GetRailPose rail %d: x=%.3f, y=%.3f, yaw=%.3f",
    rail_id, pose->second.x, pose->second.y, pose->second.yaw);
  return BT::NodeStatus::SUCCESS;
}

}  // namespace theimc_bt_nodes
