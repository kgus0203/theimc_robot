// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces_pkg:action/RailApproach.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__TRAITS_HPP_
#define INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces_pkg/action/detail/rail_approach__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: timeout_sec
  {
    out << "timeout_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_sec, out);
    out << ", ";
  }

  // member: x_tolerance
  {
    out << "x_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.x_tolerance, out);
    out << ", ";
  }

  // member: angle_tolerance
  {
    out << "angle_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_tolerance, out);
    out << ", ";
  }

  // member: allow_reverse_align
  {
    out << "allow_reverse_align: ";
    rosidl_generator_traits::value_to_yaml(msg.allow_reverse_align, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: timeout_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timeout_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_sec, out);
    out << "\n";
  }

  // member: x_tolerance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.x_tolerance, out);
    out << "\n";
  }

  // member: angle_tolerance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_tolerance, out);
    out << "\n";
  }

  // member: allow_reverse_align
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "allow_reverse_align: ";
    rosidl_generator_traits::value_to_yaml(msg.allow_reverse_align, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_Goal & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_Goal>()
{
  return "interfaces_pkg::action::RailApproach_Goal";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_Goal>()
{
  return "interfaces_pkg/action/RailApproach_Goal";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_Result & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_Result>()
{
  return "interfaces_pkg::action::RailApproach_Result";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_Result>()
{
  return "interfaces_pkg/action/RailApproach_Result";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: x_error
  {
    out << "x_error: ";
    rosidl_generator_traits::value_to_yaml(msg.x_error, out);
    out << ", ";
  }

  // member: angle_error
  {
    out << "angle_error: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_error, out);
    out << ", ";
  }

  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: x_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_error: ";
    rosidl_generator_traits::value_to_yaml(msg.x_error, out);
    out << "\n";
  }

  // member: angle_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle_error: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_error, out);
    out << "\n";
  }

  // member: distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_Feedback & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_Feedback>()
{
  return "interfaces_pkg::action::RailApproach_Feedback";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_Feedback>()
{
  return "interfaces_pkg/action/RailApproach_Feedback";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "interfaces_pkg/action/detail/rail_approach__traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_SendGoal_Request & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_SendGoal_Request>()
{
  return "interfaces_pkg::action::RailApproach_SendGoal_Request";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_SendGoal_Request>()
{
  return "interfaces_pkg/action/RailApproach_SendGoal_Request";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<interfaces_pkg::action::RailApproach_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<interfaces_pkg::action::RailApproach_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_SendGoal_Response & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_SendGoal_Response>()
{
  return "interfaces_pkg::action::RailApproach_SendGoal_Response";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_SendGoal_Response>()
{
  return "interfaces_pkg/action/RailApproach_SendGoal_Response";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_SendGoal>()
{
  return "interfaces_pkg::action::RailApproach_SendGoal";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_SendGoal>()
{
  return "interfaces_pkg/action/RailApproach_SendGoal";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<interfaces_pkg::action::RailApproach_SendGoal_Request>::value &&
    has_fixed_size<interfaces_pkg::action::RailApproach_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<interfaces_pkg::action::RailApproach_SendGoal_Request>::value &&
    has_bounded_size<interfaces_pkg::action::RailApproach_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<interfaces_pkg::action::RailApproach_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<interfaces_pkg::action::RailApproach_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<interfaces_pkg::action::RailApproach_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_GetResult_Request & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_GetResult_Request>()
{
  return "interfaces_pkg::action::RailApproach_GetResult_Request";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_GetResult_Request>()
{
  return "interfaces_pkg/action/RailApproach_GetResult_Request";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_GetResult_Response & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_GetResult_Response>()
{
  return "interfaces_pkg::action::RailApproach_GetResult_Response";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_GetResult_Response>()
{
  return "interfaces_pkg/action/RailApproach_GetResult_Response";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<interfaces_pkg::action::RailApproach_Result>::value> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<interfaces_pkg::action::RailApproach_Result>::value> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_GetResult>()
{
  return "interfaces_pkg::action::RailApproach_GetResult";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_GetResult>()
{
  return "interfaces_pkg/action/RailApproach_GetResult";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<interfaces_pkg::action::RailApproach_GetResult_Request>::value &&
    has_fixed_size<interfaces_pkg::action::RailApproach_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<interfaces_pkg::action::RailApproach_GetResult_Request>::value &&
    has_bounded_size<interfaces_pkg::action::RailApproach_GetResult_Response>::value
  >
{
};

template<>
struct is_service<interfaces_pkg::action::RailApproach_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<interfaces_pkg::action::RailApproach_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<interfaces_pkg::action::RailApproach_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__traits.hpp"

namespace interfaces_pkg
{

namespace action
{

inline void to_flow_style_yaml(
  const RailApproach_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailApproach_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailApproach_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::action::RailApproach_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::action::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::action::RailApproach_FeedbackMessage & msg)
{
  return interfaces_pkg::action::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::action::RailApproach_FeedbackMessage>()
{
  return "interfaces_pkg::action::RailApproach_FeedbackMessage";
}

template<>
inline const char * name<interfaces_pkg::action::RailApproach_FeedbackMessage>()
{
  return "interfaces_pkg/action/RailApproach_FeedbackMessage";
}

template<>
struct has_fixed_size<interfaces_pkg::action::RailApproach_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<interfaces_pkg::action::RailApproach_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<interfaces_pkg::action::RailApproach_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<interfaces_pkg::action::RailApproach_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<interfaces_pkg::action::RailApproach_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<interfaces_pkg::action::RailApproach>
  : std::true_type
{
};

template<>
struct is_action_goal<interfaces_pkg::action::RailApproach_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<interfaces_pkg::action::RailApproach_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<interfaces_pkg::action::RailApproach_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__TRAITS_HPP_
