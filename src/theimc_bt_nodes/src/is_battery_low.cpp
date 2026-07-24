#include "theimc_bt_nodes/is_battery_low.hpp"

namespace theimc_bt_nodes {

IsBatteryLow::IsBatteryLow(
    const std::string& xml_tag_name, 
    const BT::NodeConfiguration& config)
: BT::ConditionNode(xml_tag_name, config) {
    node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");

    subscription_ = node_->create_subscription<sensor_msgs::msg::BatteryState>(
        "/battery_state", rclcpp::QoS(10),
        [this](const sensor_msgs::msg::BatteryState::SharedPtr msg) {
            std::lock_guard<std::mutex> lock(mutex_);
            current_battery_ = msg->percentage * 100.0; 
        });
}

BT::PortsList IsBatteryLow::providedPorts() {
    return {

        BT::InputPort<double>("threshold", 20.0, "Battery percentage threshold to consider low"),
        BT::InputPort<double>("recovery_threshold", 90.0, "Battery percentage threshold to consider recovered")
    };
}

BT::NodeStatus IsBatteryLow::tick() {
    double threshold = 20.0;
    double recovery_threshold = 90.0;
    getInput("threshold", threshold);
    getInput("recovery_threshold", recovery_threshold);

    std::lock_guard<std::mutex> lock(mutex_);


    if (is_battery_low_) {
        if (current_battery_ >= recovery_threshold) {
            RCLCPP_INFO(node_->get_logger(), "Battery has recovered: %.2f%%", current_battery_);
            is_battery_low_ = false;
            return BT::NodeStatus::FAILURE;
        } else {
            RCLCPP_WARN(node_->get_logger(), "Battery is still low: %.2f%%", current_battery_);
            return BT::NodeStatus::SUCCESS;
        }
    }

    if (current_battery_ < threshold) {
        RCLCPP_WARN(node_->get_logger(), "Battery is low: %.2f%%", current_battery_);
        is_battery_low_ = true;
        return BT::NodeStatus::SUCCESS;
    }
    
    return BT::NodeStatus::FAILURE;
} 

}  // namespace theimc_bt_nodes