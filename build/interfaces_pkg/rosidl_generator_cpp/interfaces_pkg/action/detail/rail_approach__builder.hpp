// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:action/RailApproach.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__BUILDER_HPP_
#define INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/action/detail/rail_approach__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_Goal_allow_reverse_align
{
public:
  explicit Init_RailApproach_Goal_allow_reverse_align(::interfaces_pkg::action::RailApproach_Goal & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_Goal allow_reverse_align(::interfaces_pkg::action::RailApproach_Goal::_allow_reverse_align_type arg)
  {
    msg_.allow_reverse_align = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Goal msg_;
};

class Init_RailApproach_Goal_angle_tolerance
{
public:
  explicit Init_RailApproach_Goal_angle_tolerance(::interfaces_pkg::action::RailApproach_Goal & msg)
  : msg_(msg)
  {}
  Init_RailApproach_Goal_allow_reverse_align angle_tolerance(::interfaces_pkg::action::RailApproach_Goal::_angle_tolerance_type arg)
  {
    msg_.angle_tolerance = std::move(arg);
    return Init_RailApproach_Goal_allow_reverse_align(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Goal msg_;
};

class Init_RailApproach_Goal_x_tolerance
{
public:
  explicit Init_RailApproach_Goal_x_tolerance(::interfaces_pkg::action::RailApproach_Goal & msg)
  : msg_(msg)
  {}
  Init_RailApproach_Goal_angle_tolerance x_tolerance(::interfaces_pkg::action::RailApproach_Goal::_x_tolerance_type arg)
  {
    msg_.x_tolerance = std::move(arg);
    return Init_RailApproach_Goal_angle_tolerance(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Goal msg_;
};

class Init_RailApproach_Goal_timeout_sec
{
public:
  Init_RailApproach_Goal_timeout_sec()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_Goal_x_tolerance timeout_sec(::interfaces_pkg::action::RailApproach_Goal::_timeout_sec_type arg)
  {
    msg_.timeout_sec = std::move(arg);
    return Init_RailApproach_Goal_x_tolerance(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_Goal>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_Goal_timeout_sec();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_Result_reason
{
public:
  explicit Init_RailApproach_Result_reason(::interfaces_pkg::action::RailApproach_Result & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_Result reason(::interfaces_pkg::action::RailApproach_Result::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Result msg_;
};

class Init_RailApproach_Result_success
{
public:
  Init_RailApproach_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_Result_reason success(::interfaces_pkg::action::RailApproach_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_RailApproach_Result_reason(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_Result>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_Result_success();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_Feedback_distance
{
public:
  explicit Init_RailApproach_Feedback_distance(::interfaces_pkg::action::RailApproach_Feedback & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_Feedback distance(::interfaces_pkg::action::RailApproach_Feedback::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Feedback msg_;
};

class Init_RailApproach_Feedback_angle_error
{
public:
  explicit Init_RailApproach_Feedback_angle_error(::interfaces_pkg::action::RailApproach_Feedback & msg)
  : msg_(msg)
  {}
  Init_RailApproach_Feedback_distance angle_error(::interfaces_pkg::action::RailApproach_Feedback::_angle_error_type arg)
  {
    msg_.angle_error = std::move(arg);
    return Init_RailApproach_Feedback_distance(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Feedback msg_;
};

class Init_RailApproach_Feedback_x_error
{
public:
  explicit Init_RailApproach_Feedback_x_error(::interfaces_pkg::action::RailApproach_Feedback & msg)
  : msg_(msg)
  {}
  Init_RailApproach_Feedback_angle_error x_error(::interfaces_pkg::action::RailApproach_Feedback::_x_error_type arg)
  {
    msg_.x_error = std::move(arg);
    return Init_RailApproach_Feedback_angle_error(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Feedback msg_;
};

class Init_RailApproach_Feedback_state
{
public:
  Init_RailApproach_Feedback_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_Feedback_x_error state(::interfaces_pkg::action::RailApproach_Feedback::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_RailApproach_Feedback_x_error(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_Feedback>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_Feedback_state();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_SendGoal_Request_goal
{
public:
  explicit Init_RailApproach_SendGoal_Request_goal(::interfaces_pkg::action::RailApproach_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_SendGoal_Request goal(::interfaces_pkg::action::RailApproach_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_SendGoal_Request msg_;
};

class Init_RailApproach_SendGoal_Request_goal_id
{
public:
  Init_RailApproach_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_SendGoal_Request_goal goal_id(::interfaces_pkg::action::RailApproach_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RailApproach_SendGoal_Request_goal(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_SendGoal_Request>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_SendGoal_Request_goal_id();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_SendGoal_Response_stamp
{
public:
  explicit Init_RailApproach_SendGoal_Response_stamp(::interfaces_pkg::action::RailApproach_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_SendGoal_Response stamp(::interfaces_pkg::action::RailApproach_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_SendGoal_Response msg_;
};

class Init_RailApproach_SendGoal_Response_accepted
{
public:
  Init_RailApproach_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_SendGoal_Response_stamp accepted(::interfaces_pkg::action::RailApproach_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_RailApproach_SendGoal_Response_stamp(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_SendGoal_Response>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_SendGoal_Response_accepted();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_GetResult_Request_goal_id
{
public:
  Init_RailApproach_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces_pkg::action::RailApproach_GetResult_Request goal_id(::interfaces_pkg::action::RailApproach_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_GetResult_Request>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_GetResult_Request_goal_id();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_GetResult_Response_result
{
public:
  explicit Init_RailApproach_GetResult_Response_result(::interfaces_pkg::action::RailApproach_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_GetResult_Response result(::interfaces_pkg::action::RailApproach_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_GetResult_Response msg_;
};

class Init_RailApproach_GetResult_Response_status
{
public:
  Init_RailApproach_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_GetResult_Response_result status(::interfaces_pkg::action::RailApproach_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RailApproach_GetResult_Response_result(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_GetResult_Response>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_GetResult_Response_status();
}

}  // namespace interfaces_pkg


namespace interfaces_pkg
{

namespace action
{

namespace builder
{

class Init_RailApproach_FeedbackMessage_feedback
{
public:
  explicit Init_RailApproach_FeedbackMessage_feedback(::interfaces_pkg::action::RailApproach_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::action::RailApproach_FeedbackMessage feedback(::interfaces_pkg::action::RailApproach_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_FeedbackMessage msg_;
};

class Init_RailApproach_FeedbackMessage_goal_id
{
public:
  Init_RailApproach_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RailApproach_FeedbackMessage_feedback goal_id(::interfaces_pkg::action::RailApproach_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RailApproach_FeedbackMessage_feedback(msg_);
  }

private:
  ::interfaces_pkg::action::RailApproach_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::action::RailApproach_FeedbackMessage>()
{
  return interfaces_pkg::action::builder::Init_RailApproach_FeedbackMessage_goal_id();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__BUILDER_HPP_
