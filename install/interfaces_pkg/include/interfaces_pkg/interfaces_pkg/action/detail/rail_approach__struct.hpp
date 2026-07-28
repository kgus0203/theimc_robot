// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces_pkg:action/RailApproach.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_HPP_
#define INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_Goal __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_Goal __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_Goal_
{
  using Type = RailApproach_Goal_<ContainerAllocator>;

  explicit RailApproach_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timeout_sec = 0.0f;
      this->x_tolerance = 0.0f;
      this->angle_tolerance = 0.0f;
      this->allow_reverse_align = false;
    }
  }

  explicit RailApproach_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timeout_sec = 0.0f;
      this->x_tolerance = 0.0f;
      this->angle_tolerance = 0.0f;
      this->allow_reverse_align = false;
    }
  }

  // field types and members
  using _timeout_sec_type =
    float;
  _timeout_sec_type timeout_sec;
  using _x_tolerance_type =
    float;
  _x_tolerance_type x_tolerance;
  using _angle_tolerance_type =
    float;
  _angle_tolerance_type angle_tolerance;
  using _allow_reverse_align_type =
    bool;
  _allow_reverse_align_type allow_reverse_align;

  // setters for named parameter idiom
  Type & set__timeout_sec(
    const float & _arg)
  {
    this->timeout_sec = _arg;
    return *this;
  }
  Type & set__x_tolerance(
    const float & _arg)
  {
    this->x_tolerance = _arg;
    return *this;
  }
  Type & set__angle_tolerance(
    const float & _arg)
  {
    this->angle_tolerance = _arg;
    return *this;
  }
  Type & set__allow_reverse_align(
    const bool & _arg)
  {
    this->allow_reverse_align = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Goal
    std::shared_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Goal
    std::shared_ptr<interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_Goal_ & other) const
  {
    if (this->timeout_sec != other.timeout_sec) {
      return false;
    }
    if (this->x_tolerance != other.x_tolerance) {
      return false;
    }
    if (this->angle_tolerance != other.angle_tolerance) {
      return false;
    }
    if (this->allow_reverse_align != other.allow_reverse_align) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_Goal_

// alias to use template instance with default allocator
using RailApproach_Goal =
  interfaces_pkg::action::RailApproach_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg


#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_Result __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_Result __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_Result_
{
  using Type = RailApproach_Result_<ContainerAllocator>;

  explicit RailApproach_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
    }
  }

  explicit RailApproach_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Result
    std::shared_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Result
    std::shared_ptr<interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_Result_

// alias to use template instance with default allocator
using RailApproach_Result =
  interfaces_pkg::action::RailApproach_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg


#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_Feedback __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_Feedback_
{
  using Type = RailApproach_Feedback_<ContainerAllocator>;

  explicit RailApproach_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->x_error = 0.0f;
      this->angle_error = 0.0f;
      this->distance = "";
    }
  }

  explicit RailApproach_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : state(_alloc),
    distance(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->x_error = 0.0f;
      this->angle_error = 0.0f;
      this->distance = "";
    }
  }

  // field types and members
  using _state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _state_type state;
  using _x_error_type =
    float;
  _x_error_type x_error;
  using _angle_error_type =
    float;
  _angle_error_type angle_error;
  using _distance_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _distance_type distance;

  // setters for named parameter idiom
  Type & set__state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__x_error(
    const float & _arg)
  {
    this->x_error = _arg;
    return *this;
  }
  Type & set__angle_error(
    const float & _arg)
  {
    this->angle_error = _arg;
    return *this;
  }
  Type & set__distance(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->distance = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Feedback
    std::shared_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_Feedback
    std::shared_ptr<interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_Feedback_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    if (this->x_error != other.x_error) {
      return false;
    }
    if (this->angle_error != other.angle_error) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_Feedback_

// alias to use template instance with default allocator
using RailApproach_Feedback =
  interfaces_pkg::action::RailApproach_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "interfaces_pkg/action/detail/rail_approach__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Request __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_SendGoal_Request_
{
  using Type = RailApproach_SendGoal_Request_<ContainerAllocator>;

  explicit RailApproach_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit RailApproach_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const interfaces_pkg::action::RailApproach_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Request
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Request
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_SendGoal_Request_

// alias to use template instance with default allocator
using RailApproach_SendGoal_Request =
  interfaces_pkg::action::RailApproach_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Response __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_SendGoal_Response_
{
  using Type = RailApproach_SendGoal_Response_<ContainerAllocator>;

  explicit RailApproach_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit RailApproach_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Response
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_SendGoal_Response
    std::shared_ptr<interfaces_pkg::action::RailApproach_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_SendGoal_Response_

// alias to use template instance with default allocator
using RailApproach_SendGoal_Response =
  interfaces_pkg::action::RailApproach_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg

namespace interfaces_pkg
{

namespace action
{

struct RailApproach_SendGoal
{
  using Request = interfaces_pkg::action::RailApproach_SendGoal_Request;
  using Response = interfaces_pkg::action::RailApproach_SendGoal_Response;
};

}  // namespace action

}  // namespace interfaces_pkg


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Request __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_GetResult_Request_
{
  using Type = RailApproach_GetResult_Request_<ContainerAllocator>;

  explicit RailApproach_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit RailApproach_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Request
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Request
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_GetResult_Request_

// alias to use template instance with default allocator
using RailApproach_GetResult_Request =
  interfaces_pkg::action::RailApproach_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg


// Include directives for member types
// Member 'result'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Response __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_GetResult_Response_
{
  using Type = RailApproach_GetResult_Response_<ContainerAllocator>;

  explicit RailApproach_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit RailApproach_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    interfaces_pkg::action::RailApproach_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const interfaces_pkg::action::RailApproach_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Response
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_GetResult_Response
    std::shared_ptr<interfaces_pkg::action::RailApproach_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_GetResult_Response_

// alias to use template instance with default allocator
using RailApproach_GetResult_Response =
  interfaces_pkg::action::RailApproach_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg

namespace interfaces_pkg
{

namespace action
{

struct RailApproach_GetResult
{
  using Request = interfaces_pkg::action::RailApproach_GetResult_Request;
  using Response = interfaces_pkg::action::RailApproach_GetResult_Response;
};

}  // namespace action

}  // namespace interfaces_pkg


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__action__RailApproach_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__action__RailApproach_FeedbackMessage __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct RailApproach_FeedbackMessage_
{
  using Type = RailApproach_FeedbackMessage_<ContainerAllocator>;

  explicit RailApproach_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit RailApproach_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const interfaces_pkg::action::RailApproach_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_FeedbackMessage
    std::shared_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__action__RailApproach_FeedbackMessage
    std::shared_ptr<interfaces_pkg::action::RailApproach_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RailApproach_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const RailApproach_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RailApproach_FeedbackMessage_

// alias to use template instance with default allocator
using RailApproach_FeedbackMessage =
  interfaces_pkg::action::RailApproach_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace interfaces_pkg

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace interfaces_pkg
{

namespace action
{

struct RailApproach
{
  /// The goal message defined in the action definition.
  using Goal = interfaces_pkg::action::RailApproach_Goal;
  /// The result message defined in the action definition.
  using Result = interfaces_pkg::action::RailApproach_Result;
  /// The feedback message defined in the action definition.
  using Feedback = interfaces_pkg::action::RailApproach_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = interfaces_pkg::action::RailApproach_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = interfaces_pkg::action::RailApproach_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = interfaces_pkg::action::RailApproach_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct RailApproach RailApproach;

}  // namespace action

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_HPP_
