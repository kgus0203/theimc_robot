#ifndef THEIMC_BT_NODES__DRIVE_CMD_VEL_HPP_
#define THEIMC_BT_NODES__DRIVE_CMD_VEL_HPP_

#include <string>

#include "behaviortree_cpp_v3/action_node.h"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

namespace theimc_bt_nodes
{

class DriveCmdVel : public BT::StatefulActionNode
{
public:
  DriveCmdVel(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus onStart() override;
  BT::NodeStatus onRunning() override;
  void onHalted() override;

private:
  void publishVelocity(double linear_x, double angular_z);
  void stop();

  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Time start_time_;
  double linear_x_{0.0};
  double angular_z_{0.0};
  double seconds_{0.0};
  bool active_{false};
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__DRIVE_CMD_VEL_HPP_
