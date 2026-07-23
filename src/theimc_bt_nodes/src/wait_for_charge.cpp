#include "theimc_bt_nodes/wait_for_charge.hpp"

namespace theimc_bt_nodes {

WaitForCharge::WaitForCharge(
    const std::string& xml_tag_name, 
    const BT::NodeConfiguration& config)
: BT::StatefulActionNode(xml_tag_name, config) {
    node_ = config.blackboard->get<rclcpp::Node::SharedPtr>("node");

    // 배터리 상태 토픽 구독 (IsBatteryLow와 동일한 방식 적용)
    subscription_ = node_->create_subscription<sensor_msgs::msg::BatteryState>(
        "/battery_state", rclcpp::QoS(10),
        [this](const sensor_msgs::msg::BatteryState::SharedPtr msg) {
            std::lock_guard<std::mutex> lock(mutex_);
            current_battery_ = msg->percentage * 100.0; 
            has_received_data_ = true;
        });
}

BT::PortsList WaitForCharge::providedPorts() {
    return {
        BT::InputPort<double>("target_battery", 90.0, "Battery percentage to reach before success")
    };
}

BT::NodeStatus WaitForCharge::onStart() {
    if (!getInput("target_battery", target_battery_)) {
        RCLCPP_WARN(node_->get_logger(), "WaitForCharge missing target_battery input, using default %.1f", target_battery_);
    }

    RCLCPP_INFO(node_->get_logger(), "WaitForCharge started. Waiting until battery reaches: %.2f%%", target_battery_);
    return BT::NodeStatus::RUNNING;
}

BT::NodeStatus WaitForCharge::onRunning() {
    std::lock_guard<std::mutex> lock(mutex_);

    // 아직 배터리 데이터를 한 번도 수신하지 못한 경우 계속 대기
    if (!has_received_data_) {
        return BT::NodeStatus::RUNNING;
    }

    // 목표 배터리 잔량에 도달한 경우 성공 반환
    if (current_battery_ >= target_battery_) {
        RCLCPP_INFO(node_->get_logger(), "WaitForCharge complete. Current battery: %.2f%% >= Target: %.2f%%", 
                    current_battery_, target_battery_);
        return BT::NodeStatus::SUCCESS;
    }

    // 터미널 로그 과부하를 막기 위해 10초에 한 번씩만 현재 충전 상태를 출력
    RCLCPP_INFO_THROTTLE(node_->get_logger(), *node_->get_clock(), 10000, 
                        "Charging in progress... Current battery: %.2f%%", current_battery_);

    return BT::NodeStatus::RUNNING;
}

void WaitForCharge::onHalted() {
    RCLCPP_WARN(node_->get_logger(), "WaitForCharge halted before reaching target battery.");
}

}  // namespace theimc_bt_nodes