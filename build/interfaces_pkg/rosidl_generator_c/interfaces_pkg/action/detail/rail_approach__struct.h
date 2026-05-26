// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:action/RailApproach.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_H_
#define INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_Goal
{
  float timeout_sec;
  float x_tolerance;
  float angle_tolerance;
  bool allow_reverse_align;
} interfaces_pkg__action__RailApproach_Goal;

// Struct for a sequence of interfaces_pkg__action__RailApproach_Goal.
typedef struct interfaces_pkg__action__RailApproach_Goal__Sequence
{
  interfaces_pkg__action__RailApproach_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_Result
{
  bool success;
  rosidl_runtime_c__String reason;
} interfaces_pkg__action__RailApproach_Result;

// Struct for a sequence of interfaces_pkg__action__RailApproach_Result.
typedef struct interfaces_pkg__action__RailApproach_Result__Sequence
{
  interfaces_pkg__action__RailApproach_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'state'
// Member 'distance'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_Feedback
{
  rosidl_runtime_c__String state;
  float x_error;
  float angle_error;
  rosidl_runtime_c__String distance;
} interfaces_pkg__action__RailApproach_Feedback;

// Struct for a sequence of interfaces_pkg__action__RailApproach_Feedback.
typedef struct interfaces_pkg__action__RailApproach_Feedback__Sequence
{
  interfaces_pkg__action__RailApproach_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "interfaces_pkg/action/detail/rail_approach__struct.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  interfaces_pkg__action__RailApproach_Goal goal;
} interfaces_pkg__action__RailApproach_SendGoal_Request;

// Struct for a sequence of interfaces_pkg__action__RailApproach_SendGoal_Request.
typedef struct interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence
{
  interfaces_pkg__action__RailApproach_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} interfaces_pkg__action__RailApproach_SendGoal_Response;

// Struct for a sequence of interfaces_pkg__action__RailApproach_SendGoal_Response.
typedef struct interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence
{
  interfaces_pkg__action__RailApproach_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} interfaces_pkg__action__RailApproach_GetResult_Request;

// Struct for a sequence of interfaces_pkg__action__RailApproach_GetResult_Request.
typedef struct interfaces_pkg__action__RailApproach_GetResult_Request__Sequence
{
  interfaces_pkg__action__RailApproach_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__struct.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_GetResult_Response
{
  int8_t status;
  interfaces_pkg__action__RailApproach_Result result;
} interfaces_pkg__action__RailApproach_GetResult_Response;

// Struct for a sequence of interfaces_pkg__action__RailApproach_GetResult_Response.
typedef struct interfaces_pkg__action__RailApproach_GetResult_Response__Sequence
{
  interfaces_pkg__action__RailApproach_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "interfaces_pkg/action/detail/rail_approach__struct.h"

/// Struct defined in action/RailApproach in the package interfaces_pkg.
typedef struct interfaces_pkg__action__RailApproach_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  interfaces_pkg__action__RailApproach_Feedback feedback;
} interfaces_pkg__action__RailApproach_FeedbackMessage;

// Struct for a sequence of interfaces_pkg__action__RailApproach_FeedbackMessage.
typedef struct interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence
{
  interfaces_pkg__action__RailApproach_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__ACTION__DETAIL__RAIL_APPROACH__STRUCT_H_
