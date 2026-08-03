#ifndef THEIMC_BT_NODES__WAIT_FOR_CHARGE_HPP_
#define THEIMC_BT_NODES__WAIT_FOR_CHARGE_HPP_

#include <mutex>
#include <string>
#include <behaviortree_cpp_v3/action_node.h>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/battery_state.hpp>


namespace theimc_bt_nodes {

class WaitForCharge : public BT::StatefulActionNode {
public:
    WaitForCharge(const std::string& xml_tag_name, const BT::NodeConfiguration& config);

    static BT::PortsList providedPorts();

    BT::NodeStatus onStart() override;
    BT::NodeStatus onRunning() override;
    void onHalted() override;

private:
    rclcpp::Node::SharedPtr node_;
    rclcpp::Subscription<sensor_msgs::msg::BatteryState>::SharedPtr subscription_;
    std::mutex mutex_;
    
    double current_battery_{0.0};
    double target_battery_{90.0};
    bool has_received_data_{false};
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__WAIT_FOR_CHARGE_HPP_