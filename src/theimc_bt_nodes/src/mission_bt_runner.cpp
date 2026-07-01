#include <chrono>
#include <memory>
#include <string>
#include <vector>

#include "ament_index_cpp/get_package_share_directory.hpp"
#include "behaviortree_cpp_v3/bt_factory.h"
#include "nav2_behavior_tree/behavior_tree_engine.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("mission_bt_runner");

  const auto default_bt_xml =
    ament_index_cpp::get_package_share_directory("theimc_bt_nodes") +
    "/bt_xml/simple_home_rail_3times_bt.xml";
  const auto bt_xml = node->declare_parameter<std::string>("bt_xml", default_bt_xml);
  const auto bt_loop_duration = std::chrono::milliseconds(
    node->declare_parameter<int>("bt_loop_duration", 100));
  const auto server_timeout = std::chrono::milliseconds(
    node->declare_parameter<int>("server_timeout", 20));
  const auto wait_for_service_timeout = std::chrono::milliseconds(
    node->declare_parameter<int>("wait_for_service_timeout", 10000));

  auto blackboard = BT::Blackboard::create();
  blackboard->set<rclcpp::Node::SharedPtr>("node", node);
  blackboard->set<std::chrono::milliseconds>("bt_loop_duration", bt_loop_duration);
  blackboard->set<std::chrono::milliseconds>("server_timeout", server_timeout);
  blackboard->set<std::chrono::milliseconds>(
    "wait_for_service_timeout", wait_for_service_timeout);
  blackboard->set<int>("number_recoveries", 0);

  try {
    nav2_behavior_tree::BehaviorTreeEngine engine({"theimc_bt_nodes"});
    auto tree = engine.createTreeFromFile(bt_xml, blackboard);

    RCLCPP_INFO(
      node->get_logger(),
      "Mission BT started. Waiting for std_msgs/msg/Bool true on /mission_trigger");

    rclcpp::WallRate loop_rate(bt_loop_duration);

    while (rclcpp::ok()) {
      auto status = BT::NodeStatus::RUNNING;
      while (rclcpp::ok() && status == BT::NodeStatus::RUNNING) {
        status = tree.tickRoot();
        loop_rate.sleep();
      }

      if (!rclcpp::ok()) {
        break;
      }

      if (status == BT::NodeStatus::SUCCESS) {
        RCLCPP_INFO(
          node->get_logger(),
          "Mission BT completed successfully. Waiting for next /mission_trigger");
      } else {
        RCLCPP_ERROR(
          node->get_logger(),
          "Mission BT failed. Resetting tree and waiting for next /mission_trigger");
      }

      tree.haltTree();
    }

    tree.haltTree();
    RCLCPP_INFO(node->get_logger(), "Mission BT stopped");
  } catch (const std::exception & exception) {
    RCLCPP_FATAL(node->get_logger(), "Mission BT error: %s", exception.what());
    rclcpp::shutdown();
    return 1;
  }

  rclcpp::shutdown();
  return 0;
}
