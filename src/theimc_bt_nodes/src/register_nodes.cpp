#include "behaviortree_cpp_v3/bt_factory.h"
#include "theimc_bt_nodes/go_to_pose.hpp"
#include "theimc_bt_nodes/wait_for_mission_trigger.hpp"

BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<theimc_bt_nodes::GoToPose>("GoToPose");
  factory.registerNodeType<theimc_bt_nodes::WaitForMissionTrigger>("WaitForMissionTrigger");
}
