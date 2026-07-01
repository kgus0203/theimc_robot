#include "behaviortree_cpp_v3/bt_factory.h"
#include "theimc_bt_nodes/go_to_pose.hpp"
#include "theimc_bt_nodes/publish_rail_command.hpp"
#include "theimc_bt_nodes/rail_approach.hpp"
#include "theimc_bt_nodes/wait_for_rail_state.hpp"
#include "theimc_bt_nodes/wait_for_mission_trigger.hpp"
#include "theimc_bt_nodes/wait_seconds.hpp"

BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<theimc_bt_nodes::GoToPose>("GoToPose");
  factory.registerNodeType<theimc_bt_nodes::PublishRailCommand>("PublishRailCommand");
  factory.registerNodeType<theimc_bt_nodes::RailApproach>("RailApproach");
  factory.registerNodeType<theimc_bt_nodes::WaitForRailState>("WaitForRailState");
  factory.registerNodeType<theimc_bt_nodes::WaitForMissionTrigger>("WaitForMissionTrigger");
  factory.registerNodeType<theimc_bt_nodes::WaitSeconds>("WaitSeconds");
}
