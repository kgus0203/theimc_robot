// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces_pkg:msg/RailInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__TRAITS_HPP_
#define INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces_pkg/msg/detail/rail_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace interfaces_pkg
{

namespace msg
{

inline void to_flow_style_yaml(
  const RailInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: has_rail
  {
    out << "has_rail: ";
    rosidl_generator_traits::value_to_yaml(msg.has_rail, out);
    out << ", ";
  }

  // member: rail_cx
  {
    out << "rail_cx: ";
    rosidl_generator_traits::value_to_yaml(msg.rail_cx, out);
    out << ", ";
  }

  // member: rail_cy
  {
    out << "rail_cy: ";
    rosidl_generator_traits::value_to_yaml(msg.rail_cy, out);
    out << ", ";
  }

  // member: img_cx
  {
    out << "img_cx: ";
    rosidl_generator_traits::value_to_yaml(msg.img_cx, out);
    out << ", ";
  }

  // member: img_cy
  {
    out << "img_cy: ";
    rosidl_generator_traits::value_to_yaml(msg.img_cy, out);
    out << ", ";
  }

  // member: img_width
  {
    out << "img_width: ";
    rosidl_generator_traits::value_to_yaml(msg.img_width, out);
    out << ", ";
  }

  // member: img_height
  {
    out << "img_height: ";
    rosidl_generator_traits::value_to_yaml(msg.img_height, out);
    out << ", ";
  }

  // member: angle_deg
  {
    out << "angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_deg, out);
    out << ", ";
  }

  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RailInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: has_rail
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "has_rail: ";
    rosidl_generator_traits::value_to_yaml(msg.has_rail, out);
    out << "\n";
  }

  // member: rail_cx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rail_cx: ";
    rosidl_generator_traits::value_to_yaml(msg.rail_cx, out);
    out << "\n";
  }

  // member: rail_cy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rail_cy: ";
    rosidl_generator_traits::value_to_yaml(msg.rail_cy, out);
    out << "\n";
  }

  // member: img_cx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_cx: ";
    rosidl_generator_traits::value_to_yaml(msg.img_cx, out);
    out << "\n";
  }

  // member: img_cy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_cy: ";
    rosidl_generator_traits::value_to_yaml(msg.img_cy, out);
    out << "\n";
  }

  // member: img_width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_width: ";
    rosidl_generator_traits::value_to_yaml(msg.img_width, out);
    out << "\n";
  }

  // member: img_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_height: ";
    rosidl_generator_traits::value_to_yaml(msg.img_height, out);
    out << "\n";
  }

  // member: angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_deg, out);
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

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RailInfo & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::msg::RailInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::msg::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::msg::RailInfo & msg)
{
  return interfaces_pkg::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::msg::RailInfo>()
{
  return "interfaces_pkg::msg::RailInfo";
}

template<>
inline const char * name<interfaces_pkg::msg::RailInfo>()
{
  return "interfaces_pkg/msg/RailInfo";
}

template<>
struct has_fixed_size<interfaces_pkg::msg::RailInfo>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces_pkg::msg::RailInfo>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces_pkg::msg::RailInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__TRAITS_HPP_
