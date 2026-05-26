// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/RailInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'distance'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/RailInfo in the package interfaces_pkg.
typedef struct interfaces_pkg__msg__RailInfo
{
  std_msgs__msg__Header header;
  bool has_rail;
  float rail_cx;
  float rail_cy;
  float img_cx;
  float img_cy;
  uint32_t img_width;
  uint32_t img_height;
  float angle_deg;
  rosidl_runtime_c__String distance;
  float confidence;
} interfaces_pkg__msg__RailInfo;

// Struct for a sequence of interfaces_pkg__msg__RailInfo.
typedef struct interfaces_pkg__msg__RailInfo__Sequence
{
  interfaces_pkg__msg__RailInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__RailInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_H_
