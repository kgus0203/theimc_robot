#include <atomic>
#include <chrono>
#include <memory>
#include <string>
#include <vector>

#include "ament_index_cpp/get_package_share_directory.hpp"
#include "behaviortree_cpp_v3/bt_factory.h"
#include "nav2_behavior_tree/behavior_tree_engine.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"

using namespace std::chrono_literals;

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("mission_bt_runner");

  const auto default_bt_xml =
    ament_index_cpp::get_package_share_directory("theimc_bt_nodes") +
    "/bt_xml/theimc_bt.xml";
  const auto default_rails_yaml =
    ament_index_cpp::get_package_share_directory("theimc_bt_nodes") +
    "/config/rails.yaml";
  const auto bt_xml = node->declare_parameter<std::string>("bt_xml", default_bt_xml);
  const auto rails_yaml = node->declare_parameter<std::string>("rails_yaml", default_rails_yaml);
  const auto bt_loop_duration = std::chrono::milliseconds(
    node->declare_parameter<int>("bt_loop_duration", 100));
  const auto server_timeout = std::chrono::milliseconds(
    node->declare_parameter<int>("server_timeout", 20));
  const auto wait_for_service_timeout = std::chrono::milliseconds(
    node->declare_parameter<int>("wait_for_service_timeout", 10000));

  auto blackboard = BT::Blackboard::create();
  blackboard->set<rclcpp::Node::SharedPtr>("node", node);
  blackboard->set<std::string>("rails_yaml", rails_yaml);
  blackboard->set<std::string>("mission_return_mode", "DIRECT");
  blackboard->set<std::chrono::milliseconds>("bt_loop_duration", bt_loop_duration);
  blackboard->set<std::chrono::milliseconds>("server_timeout", server_timeout);
  blackboard->set<std::chrono::milliseconds>(
    "wait_for_service_timeout", wait_for_service_timeout);
  blackboard->set<int>("number_recoveries", 0);

  std::atomic_bool halt_requested{false};
  auto halt_subscription = node->create_subscription<std_msgs::msg::Bool>(
    "/mission_halt", rclcpp::QoS(10),
    [&halt_requested, node](const std_msgs::msg::Bool::SharedPtr msg) {
      if (msg->data) {
        halt_requested.store(true);
        RCLCPP_WARN(node->get_logger(), "Mission halt requested on /mission_halt");
      }
    });

  try {
    nav2_behavior_tree::BehaviorTreeEngine engine({
      "theimc_bt_nodes",
      "nav2_back_up_action_bt_node",
    });
    auto tree = engine.createTreeFromFile(bt_xml, blackboard);

    RCLCPP_INFO(
      node->get_logger(),
      "Mission BT started with rails YAML: %s", rails_yaml.c_str());
    RCLCPP_INFO(
      node->get_logger(),
      "Publish std_msgs/msg/String on /selected_rails, then Bool true on /mission_trigger");

    rclcpp::WallRate loop_rate(bt_loop_duration);

    while (rclcpp::ok()) {
      auto status = BT::NodeStatus::RUNNING;
      bool mission_halted = false;
      while (rclcpp::ok() && status == BT::NodeStatus::RUNNING) {
        rclcpp::spin_some(node);
        if (halt_requested.exchange(false)) {
          tree.haltTree();
          mission_halted = true;
          RCLCPP_WARN(
            node->get_logger(),
            "Mission halted and tree state reset. Waiting for a new mission trigger");
          break;
        }
        status = tree.tickRoot();
        loop_rate.sleep();
      }

      if (!rclcpp::ok()) {
        break;
      }

      if (mission_halted) {
        continue;
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
