#ifndef THEIMC_BT_NODES__FOR_EACH_RAIL_HPP_
#define THEIMC_BT_NODES__FOR_EACH_RAIL_HPP_

#include <cstddef>
#include <string>
#include <vector>

#include "behaviortree_cpp_v3/decorator_node.h"
#include "rclcpp/rclcpp.hpp"

namespace theimc_bt_nodes
{

class ForEachRail : public BT::DecoratorNode
{
public:
  ForEachRail(
    const std::string & xml_tag_name,
    const BT::NodeConfiguration & config);

  static BT::PortsList providedPorts();

  BT::NodeStatus tick() override;
  void halt() override;

private:
  bool initializeRailList();
  void clearState();

  rclcpp::Node::SharedPtr node_;
  std::vector<int> rail_ids_;
  std::size_t current_index_{0};
  bool initialized_{false};
};

}  // namespace theimc_bt_nodes

#endif  // THEIMC_BT_NODES__FOR_EACH_RAIL_HPP_
