#include <string>
#include <memory>
#include "behaviortree_cpp_v3/condition_node.h"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"

namespace nav2_behavior_tree
{

class CheckButtonCondition : public BT::ConditionNode
{
public:
  CheckButtonCondition(const std::string& name, const BT::NodeConfiguration& config)
  : BT::ConditionNode(name, config), button_pressed_(false)
  {
    // ROS2 노드 생성 및 구독자 설정
    node_ = rclcpp::Node::make_shared("check_button_condition_node");
    sub_ = node_->create_subscription<std_msgs::msg::Bool>(
      "/button_trigger", 10,
      [this](const std_msgs::msg::Bool::SharedPtr msg) {
        button_pressed_ = msg->data;
      });
  }

  static BT::PortsList providedPorts() { return {}; }

  BT::NodeStatus tick() override
  {
    // 토픽 콜백 처리를 위해 spin_some 호출
    rclcpp::spin_some(node_);

    if (button_pressed_) {
      return BT::NodeStatus::SUCCESS;
    }
    return BT::NodeStatus::FAILURE;
  }

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr sub_;
  bool button_pressed_;
};

}  // namespace nav2_behavior_tree

#include "behaviortree_cpp_v3/bt_factory.h"
BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<nav2_behavior_tree::CheckButtonCondition>("CheckButton");
}
