#ifndef THEIMC_BT_NODES__RAIL_APPROACH_HPP_
#define THEIMC_BT_NODES__RAIL_APPROACH_HPP_

#include <string>

#include "interfaces_pkg/action/rail_approach.hpp"
#include "nav2_behavior_tree/bt_action_node.hpp"

namespace theimc_bt_nodes
{

class RailApproach : public nav2_behavior_tree::BtActionNode<interfaces_pkg::action::RailApproach>
{
public:
  RailApproach(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  void on_tick() override;
  BT::NodeStatus on_success() override;
  BT::NodeStatus on_aborted() override;
  BT::NodeStatus on_cancelled() override;
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__RAIL_APPROACH_HPP_
