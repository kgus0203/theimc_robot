// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/RailInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/rail_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_RailInfo_confidence
{
public:
  explicit Init_RailInfo_confidence(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::RailInfo confidence(::interfaces_pkg::msg::RailInfo::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_distance
{
public:
  explicit Init_RailInfo_distance(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_confidence distance(::interfaces_pkg::msg::RailInfo::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_RailInfo_confidence(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_angle_deg
{
public:
  explicit Init_RailInfo_angle_deg(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_distance angle_deg(::interfaces_pkg::msg::RailInfo::_angle_deg_type arg)
  {
    msg_.angle_deg = std::move(arg);
    return Init_RailInfo_distance(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_img_height
{
public:
  explicit Init_RailInfo_img_height(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_angle_deg img_height(::interfaces_pkg::msg::RailInfo::_img_height_type arg)
  {
    msg_.img_height = std::move(arg);
    return Init_RailInfo_angle_deg(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_img_width
{
public:
  explicit Init_RailInfo_img_width(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_img_height img_width(::interfaces_pkg::msg::RailInfo::_img_width_type arg)
  {
    msg_.img_width = std::move(arg);
    return Init_RailInfo_img_height(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_img_cy
{
public:
  explicit Init_RailInfo_img_cy(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_img_width img_cy(::interfaces_pkg::msg::RailInfo::_img_cy_type arg)
  {
    msg_.img_cy = std::move(arg);
    return Init_RailInfo_img_width(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_img_cx
{
public:
  explicit Init_RailInfo_img_cx(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_img_cy img_cx(::interfaces_pkg::msg::RailInfo::_img_cx_type arg)
  {
    msg_.img_cx = std::move(arg);
    return Init_RailInfo_img_cy(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_rail_cy
{
public:
  explicit Init_RailInfo_rail_cy(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_img_cx rail_cy(::interfaces_pkg::msg::RailInfo::_rail_cy_type arg)
  {
    msg_.rail_cy = std::move(arg);
    return Init_RailInfo_img_cx(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_rail_cx
{
public:
  explicit Init_RailInfo_rail_cx(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_rail_cy rail_cx(::interfaces_pkg::msg::RailInfo::_rail_cx_type arg)
  {
    msg_.rail_cx = std::move(arg);
    return Init_RailInfo_rail_cy(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_has_rail
{
public:
  explicit Init_RailInfo_has_rail(::interfaces_pkg::msg::RailInfo & msg)
  : msg_(msg)
  {}
  Init_RailInfo_rail_cx has_rail(::interfaces_pkg::msg::RailInfo::_has_rail_type arg)
  {
    msg_.has_rail = std::move(arg);
    return Init_RailInfo_rail_cx(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

class Init_RailInfo_header
{
public:
  Init_RailInfo_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailInfo_has_rail header(::interfaces_pkg::msg::RailInfo::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RailInfo_has_rail(msg_);
  }

private:
  ::interfaces_pkg::msg::RailInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::RailInfo>()
{
  return interfaces_pkg::msg::builder::Init_RailInfo_header();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__RAIL_INFO__BUILDER_HPP_
