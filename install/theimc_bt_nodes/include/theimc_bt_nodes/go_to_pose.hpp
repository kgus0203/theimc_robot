#ifndef THEIMC_BT_NODES__GO_TO_POSE_HPP_
#define THEIMC_BT_NODES__GO_TO_POSE_HPP_

#include <string>

#include "nav2_behavior_tree/bt_action_node.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"

namespace theimc_bt_nodes
{

class GoToPose : public nav2_behavior_tree::BtActionNode<nav2_msgs::action::NavigateToPose>
{
public:
  GoToPose(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  void on_tick() override;
  BT::NodeStatus on_cancelled() override;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__GO_TO_POSE_HPP_
