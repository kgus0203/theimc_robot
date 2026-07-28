
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to interfaces_pkg__action__RailApproach_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_sec: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_tolerance: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub angle_tolerance: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub allow_reverse_align: bool,

}



impl Default for RailApproach_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Goal {
  type RmwMsg = super::action::rmw::RailApproach_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timeout_sec: msg.timeout_sec,
        x_tolerance: msg.x_tolerance,
        angle_tolerance: msg.angle_tolerance,
        allow_reverse_align: msg.allow_reverse_align,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      timeout_sec: msg.timeout_sec,
      x_tolerance: msg.x_tolerance,
      angle_tolerance: msg.angle_tolerance,
      allow_reverse_align: msg.allow_reverse_align,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timeout_sec: msg.timeout_sec,
      x_tolerance: msg.x_tolerance,
      angle_tolerance: msg.angle_tolerance,
      allow_reverse_align: msg.allow_reverse_align,
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for RailApproach_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_Result::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Result {
  type RmwMsg = super::action::rmw::RailApproach_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_error: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub angle_error: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance: std::string::String,

}



impl Default for RailApproach_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Feedback {
  type RmwMsg = super::action::rmw::RailApproach_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: msg.state.as_str().into(),
        x_error: msg.x_error,
        angle_error: msg.angle_error,
        distance: msg.distance.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: msg.state.as_str().into(),
      x_error: msg.x_error,
      angle_error: msg.angle_error,
        distance: msg.distance.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      state: msg.state.to_string(),
      x_error: msg.x_error,
      angle_error: msg.angle_error,
      distance: msg.distance.to_string(),
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::RailApproach_Feedback,

}



impl Default for RailApproach_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_FeedbackMessage {
  type RmwMsg = super::action::rmw::RailApproach_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::RailApproach_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::RailApproach_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::RailApproach_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to interfaces_pkg__action__RailApproach_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::RailApproach_Goal,

}



impl Default for RailApproach_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_SendGoal_Request {
  type RmwMsg = super::action::rmw::RailApproach_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::RailApproach_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::RailApproach_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::RailApproach_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for RailApproach_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_SendGoal_Response {
  type RmwMsg = super::action::rmw::RailApproach_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for RailApproach_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_GetResult_Request {
  type RmwMsg = super::action::rmw::RailApproach_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to interfaces_pkg__action__RailApproach_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::RailApproach_Result,

}



impl Default for RailApproach_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RailApproach_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RailApproach_GetResult_Response {
  type RmwMsg = super::action::rmw::RailApproach_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::RailApproach_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::RailApproach_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::RailApproach_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to interfaces_pkg__action__RailApproach_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct RailApproach_SendGoal;

impl rosidl_runtime_rs::Service for RailApproach_SendGoal {
    type Request = RailApproach_SendGoal_Request;
    type Response = RailApproach_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal() }
    }
}




#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__interfaces_pkg__action__RailApproach_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to interfaces_pkg__action__RailApproach_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct RailApproach_GetResult;

impl rosidl_runtime_rs::Service for RailApproach_GetResult {
    type Request = RailApproach_GetResult_Request;
    type Response = RailApproach_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__interfaces_pkg__action__RailApproach_GetResult() }
    }
}






#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__interfaces_pkg__action__RailApproach() -> *const std::ffi::c_void;
}

// Corresponds to interfaces_pkg__action__RailApproach
#[allow(missing_docs, non_camel_case_types)]
pub struct RailApproach;

impl rosidl_runtime_rs::Action for RailApproach {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = RailApproach_Goal;

  /// The result message defined in the action definition.
  type Result = RailApproach_Result;

  /// The feedback message defined in the action definition.
  type Feedback = RailApproach_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::RailApproach_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::RailApproach_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::RailApproach_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__interfaces_pkg__action__RailApproach() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::RailApproach_Goal,
  ) -> super::action::rmw::RailApproach_SendGoal_Request {
   super::action::rmw::RailApproach_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::RailApproach_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::RailApproach_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::RailApproach_SendGoal_Response {
   super::action::rmw::RailApproach_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::RailApproach_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::RailApproach_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::RailApproach_Feedback,
  ) -> super::action::rmw::RailApproach_FeedbackMessage {
    let mut message = super::action::rmw::RailApproach_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::RailApproach_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::RailApproach_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::RailApproach_GetResult_Request {
   super::action::rmw::RailApproach_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::RailApproach_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::RailApproach_Result,
  ) -> super::action::rmw::RailApproach_GetResult_Response {
   super::action::rmw::RailApproach_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::RailApproach_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::RailApproach_Result,
  ) {
    (response.status, response.result)
  }
}


