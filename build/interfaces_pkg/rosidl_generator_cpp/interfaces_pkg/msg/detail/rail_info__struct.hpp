// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces_pkg:msg/RailInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_HPP_
#define INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__msg__RailInfo __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__msg__RailInfo __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RailInfo_
{
  using Type = RailInfo_<ContainerAllocator>;

  explicit RailInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->has_rail = false;
      this->rail_cx = 0.0f;
      this->rail_cy = 0.0f;
      this->img_cx = 0.0f;
      this->img_cy = 0.0f;
      this->img_width = 0ul;
      this->img_height = 0ul;
      this->angle_deg = 0.0f;
      this->distance = "";
      this->confidence = 0.0f;
    }
  }

  explicit RailInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    distance(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->has_rail = false;
      this->rail_cx = 0.0f;
      this->rail_cy = 0.0f;
      this->img_cx = 0.0f;
      this->img_cy = 0.0f;
      this->img_width = 0ul;
      this->img_height = 0ul;
      this->angle_deg = 0.0f;
      this->distance = "";
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _has_rail_type =
    bool;
  _has_rail_type has_rail;
  using _rail_cx_type =
    float;
  _rail_cx_type rail_cx;
  using _rail_cy_type =
    float;
  _rail_cy_type rail_cy;
  using _img_cx_type =
    float;
  _img_cx_type img_cx;
  using _img_cy_type =
    float;
  _img_cy_type img_cy;
  using _img_width_type =
    uint32_t;
  _img_width_type img_width;
  using _img_height_type =
    uint32_t;
  _img_height_type img_height;
  using _angle_deg_type =
    float;
  _angle_deg_type angle_deg;
  using _distance_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _distance_type distance;
  using _confidence_type =
    float;
  _confidence_type confidence;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__has_rail(
    const bool & _arg)
  {
    this->has_rail = _arg;
    return *this;
  }
  Type & set__rail_cx(
    const float & _arg)
  {
    this->rail_cx = _arg;
    return *this;
  }
  Type & set__rail_cy(
    const float & _arg)
  {
    this->rail_cy = _arg;
    return *this;
  }
  Type & set__img_cx(
    const float & _arg)
  {
    this->img_cx = _arg;
    return *this;
  }
  Type & set__img_cy(
    const float & _arg)
  {
    this->img_cy = _arg;
    return *this;
  }
  Type & set__img_width(
    const uint32_t & _arg)
  {
    this->img_width = _arg;
    return *this;
  }
  Type & set__img_height(
    const uint32_t & _arg)
  {
    this->img_height = _arg;
    return *this;
  }
  Type & set__angle_deg(
    const float & _arg)
  {
    this->angle_deg = _arg;
    return *this;
  }
  Type & set__distance(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::msg::RailInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::msg::RailInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::RailInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::RailInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__msg__RailInfo
    std::shared_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__msg__RailInfo
    std::shared_ptr<interfaces_pkg::msg::RailInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailInfo_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->has_rail != other.has_rail) {
      return false;
    }
    if (this->rail_cx != other.rail_cx) {
      return false;
    }
    if (this->rail_cy != other.rail_cy) {
      return false;
    }
    if (this->img_cx != other.img_cx) {
      return false;
    }
    if (this->img_cy != other.img_cy) {
      return false;
    }
    if (this->img_width != other.img_width) {
      return false;
    }
    if (this->img_height != other.img_height) {
      return false;
    }
    if (this->angle_deg != other.angle_deg) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailInfo_

// alias to use template instance with default allocator
using RailInfo =
  interfaces_pkg::msg::RailInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__STRUCT_HPP_
