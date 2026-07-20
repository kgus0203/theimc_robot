
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Goal() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_Goal__init(msg: *mut RailApproach_Goal) -> bool;
    fn interfaces_pkg__action__RailApproach_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Goal>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Goal>);
    fn interfaces_pkg__action__RailApproach_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Goal>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_Goal__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Goal() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Result() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_Result__init(msg: *mut RailApproach_Result) -> bool;
    fn interfaces_pkg__action__RailApproach_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Result>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Result>);
    fn interfaces_pkg__action__RailApproach_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Result>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for RailApproach_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_Result__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_Result where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Result() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_Feedback__init(msg: *mut RailApproach_Feedback) -> bool;
    fn interfaces_pkg__action__RailApproach_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Feedback>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Feedback>);
    fn interfaces_pkg__action__RailApproach_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_Feedback>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_error: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub angle_error: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance: rosidl_runtime_rs::String,

}



impl Default for RailApproach_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_Feedback__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_Feedback() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_FeedbackMessage__init(msg: *mut RailApproach_FeedbackMessage) -> bool;
    fn interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_FeedbackMessage>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_FeedbackMessage>);
    fn interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_FeedbackMessage>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::RailApproach_Feedback,

}



impl Default for RailApproach_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_FeedbackMessage() }
  }
}




#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_SendGoal_Request__init(msg: *mut RailApproach_SendGoal_Request) -> bool;
    fn interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Request>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Request>);
    fn interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Request>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::RailApproach_Goal,

}



impl Default for RailApproach_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal_Request() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_SendGoal_Response__init(msg: *mut RailApproach_SendGoal_Response) -> bool;
    fn interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Response>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Response>);
    fn interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_SendGoal_Response>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for RailApproach_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_SendGoal_Response() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_GetResult_Request__init(msg: *mut RailApproach_GetResult_Request) -> bool;
    fn interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Request>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Request>);
    fn interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Request>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for RailApproach_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_GetResult_Request() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__action__RailApproach_GetResult_Response__init(msg: *mut RailApproach_GetResult_Response) -> bool;
    fn interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Response>, size: usize) -> bool;
    fn interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Response>);
    fn interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailApproach_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RailApproach_GetResult_Response>) -> bool;
}

// Corresponds to interfaces_pkg__action__RailApproach_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailApproach_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::RailApproach_Result,

}



impl Default for RailApproach_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__action__RailApproach_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__action__RailApproach_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailApproach_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__action__RailApproach_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailApproach_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailApproach_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/action/RailApproach_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__action__RailApproach_GetResult_Response() }
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


