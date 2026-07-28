#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Point2D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__Point2D__init(msg: *mut Point2D) -> bool;
    fn interfaces_pkg__msg__Point2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Point2D>, size: usize) -> bool;
    fn interfaces_pkg__msg__Point2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Point2D>);
    fn interfaces_pkg__msg__Point2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Point2D>, out_seq: *mut rosidl_runtime_rs::Sequence<Point2D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__Point2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 2D point in pixel coordinates

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Point2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,

}



impl Default for Point2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__Point2D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__Point2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Point2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Point2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Point2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Point2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Point2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Point2D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/Point2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Point2D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Vector2() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__Vector2__init(msg: *mut Vector2) -> bool;
    fn interfaces_pkg__msg__Vector2__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Vector2>, size: usize) -> bool;
    fn interfaces_pkg__msg__Vector2__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Vector2>);
    fn interfaces_pkg__msg__Vector2__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Vector2>, out_seq: *mut rosidl_runtime_rs::Sequence<Vector2>) -> bool;
}

// Corresponds to interfaces_pkg__msg__Vector2
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 2D size in pixel

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Vector2 {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,

}



impl Default for Vector2 {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__Vector2__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__Vector2__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Vector2 {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Vector2__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Vector2__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Vector2__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Vector2 {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Vector2 where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/Vector2";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Vector2() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Pose2D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__Pose2D__init(msg: *mut Pose2D) -> bool;
    fn interfaces_pkg__msg__Pose2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Pose2D>, size: usize) -> bool;
    fn interfaces_pkg__msg__Pose2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Pose2D>);
    fn interfaces_pkg__msg__Pose2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Pose2D>, out_seq: *mut rosidl_runtime_rs::Sequence<Pose2D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__Pose2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 2D position in pixel coordinates

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Pose2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: super::super::msg::rmw::Point2D,


    // This member is not documented.
    #[allow(missing_docs)]
    pub theta: f64,

}



impl Default for Pose2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__Pose2D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__Pose2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Pose2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Pose2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Pose2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Pose2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Pose2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Pose2D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/Pose2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Pose2D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__BoundingBox2D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__BoundingBox2D__init(msg: *mut BoundingBox2D) -> bool;
    fn interfaces_pkg__msg__BoundingBox2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox2D>, size: usize) -> bool;
    fn interfaces_pkg__msg__BoundingBox2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox2D>);
    fn interfaces_pkg__msg__BoundingBox2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BoundingBox2D>, out_seq: *mut rosidl_runtime_rs::Sequence<BoundingBox2D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__BoundingBox2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 2D position and orientation of the bounding box center

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoundingBox2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub center: super::super::msg::rmw::Pose2D,

    /// total size of the bounding box, in pixels, surrounding the object's center
    pub size: super::super::msg::rmw::Vector2,

}



impl Default for BoundingBox2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__BoundingBox2D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__BoundingBox2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BoundingBox2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BoundingBox2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BoundingBox2D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/BoundingBox2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__BoundingBox2D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__BoundingBox3D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__BoundingBox3D__init(msg: *mut BoundingBox3D) -> bool;
    fn interfaces_pkg__msg__BoundingBox3D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox3D>, size: usize) -> bool;
    fn interfaces_pkg__msg__BoundingBox3D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox3D>);
    fn interfaces_pkg__msg__BoundingBox3D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BoundingBox3D>, out_seq: *mut rosidl_runtime_rs::Sequence<BoundingBox3D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__BoundingBox3D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 3D position and orientation of the bounding box center

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoundingBox3D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub center: geometry_msgs::msg::rmw::Pose,

    /// total size of the bounding box, in meters, surrounding the object's center
    pub size: geometry_msgs::msg::rmw::Vector3,

    /// frame reference
    pub frame_id: rosidl_runtime_rs::String,

}



impl Default for BoundingBox3D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__BoundingBox3D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__BoundingBox3D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BoundingBox3D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox3D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox3D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__BoundingBox3D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BoundingBox3D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BoundingBox3D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/BoundingBox3D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__BoundingBox3D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Mask() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__Mask__init(msg: *mut Mask) -> bool;
    fn interfaces_pkg__msg__Mask__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Mask>, size: usize) -> bool;
    fn interfaces_pkg__msg__Mask__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Mask>);
    fn interfaces_pkg__msg__Mask__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Mask>, out_seq: *mut rosidl_runtime_rs::Sequence<Mask>) -> bool;
}

// Corresponds to interfaces_pkg__msg__Mask
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// segmentation mask for one instance

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Mask {
    /// size of the original image
    pub height: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub width: i32,

    /// mask data represeted by the points of the border of the mask
    pub data: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Point2D>,

}



impl Default for Mask {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__Mask__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__Mask__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Mask {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Mask__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Mask__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Mask__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Mask {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Mask where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/Mask";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Mask() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint2D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__KeyPoint2D__init(msg: *mut KeyPoint2D) -> bool;
    fn interfaces_pkg__msg__KeyPoint2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2D>, size: usize) -> bool;
    fn interfaces_pkg__msg__KeyPoint2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2D>);
    fn interfaces_pkg__msg__KeyPoint2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeyPoint2D>, out_seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__KeyPoint2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// one keypoint for human pose estimation

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyPoint2D {
    /// id of the keypoint
    pub id: i32,

    /// 2D point in pixels
    pub point: super::super::msg::rmw::Point2D,

    /// conf of the keypoint
    pub score: f64,

}



impl Default for KeyPoint2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__KeyPoint2D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__KeyPoint2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeyPoint2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeyPoint2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeyPoint2D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/KeyPoint2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint2D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint2DArray() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__KeyPoint2DArray__init(msg: *mut KeyPoint2DArray) -> bool;
    fn interfaces_pkg__msg__KeyPoint2DArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2DArray>, size: usize) -> bool;
    fn interfaces_pkg__msg__KeyPoint2DArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2DArray>);
    fn interfaces_pkg__msg__KeyPoint2DArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeyPoint2DArray>, out_seq: *mut rosidl_runtime_rs::Sequence<KeyPoint2DArray>) -> bool;
}

// Corresponds to interfaces_pkg__msg__KeyPoint2DArray
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// represents all the keypoints for human pose estimation

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyPoint2DArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyPoint2D>,

}



impl Default for KeyPoint2DArray {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__KeyPoint2DArray__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__KeyPoint2DArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeyPoint2DArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2DArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2DArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint2DArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeyPoint2DArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeyPoint2DArray where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/KeyPoint2DArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint2DArray() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint3D() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__KeyPoint3D__init(msg: *mut KeyPoint3D) -> bool;
    fn interfaces_pkg__msg__KeyPoint3D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3D>, size: usize) -> bool;
    fn interfaces_pkg__msg__KeyPoint3D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3D>);
    fn interfaces_pkg__msg__KeyPoint3D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeyPoint3D>, out_seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3D>) -> bool;
}

// Corresponds to interfaces_pkg__msg__KeyPoint3D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// one keypoint for human pose estimation

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyPoint3D {
    /// id of the keypoint
    pub id: i32,

    /// 3D point in meters
    pub point: geometry_msgs::msg::rmw::Point,

    /// conf of the keypoint
    pub score: f64,

}



impl Default for KeyPoint3D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__KeyPoint3D__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__KeyPoint3D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeyPoint3D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeyPoint3D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeyPoint3D where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/KeyPoint3D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint3D() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint3DArray() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__KeyPoint3DArray__init(msg: *mut KeyPoint3DArray) -> bool;
    fn interfaces_pkg__msg__KeyPoint3DArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3DArray>, size: usize) -> bool;
    fn interfaces_pkg__msg__KeyPoint3DArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3DArray>);
    fn interfaces_pkg__msg__KeyPoint3DArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeyPoint3DArray>, out_seq: *mut rosidl_runtime_rs::Sequence<KeyPoint3DArray>) -> bool;
}

// Corresponds to interfaces_pkg__msg__KeyPoint3DArray
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// represents all the keypoints for human pose estimation in meters

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyPoint3DArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyPoint3D>,

    /// frame reference
    pub frame_id: rosidl_runtime_rs::String,

}



impl Default for KeyPoint3DArray {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__KeyPoint3DArray__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__KeyPoint3DArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeyPoint3DArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3DArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3DArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__KeyPoint3DArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeyPoint3DArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeyPoint3DArray where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/KeyPoint3DArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__KeyPoint3DArray() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Detection() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__Detection__init(msg: *mut Detection) -> bool;
    fn interfaces_pkg__msg__Detection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Detection>, size: usize) -> bool;
    fn interfaces_pkg__msg__Detection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Detection>);
    fn interfaces_pkg__msg__Detection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Detection>, out_seq: *mut rosidl_runtime_rs::Sequence<Detection>) -> bool;
}

// Corresponds to interfaces_pkg__msg__Detection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// defines a YOLOv8 detection result

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Detection {
    /// class probability
    pub class_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub class_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub score: f64,

    /// ID for tracking
    pub id: rosidl_runtime_rs::String,

    /// 2D bounding box surrounding the object in pixels
    pub bbox: super::super::msg::rmw::BoundingBox2D,

    /// 3D bounding box surrounding the object in meters
    pub bbox3d: super::super::msg::rmw::BoundingBox3D,

    /// segmentation mask of the detected object
    /// it is only the boundary of the segmented object
    pub mask: super::super::msg::rmw::Mask,

    /// keypoints for human pose estimation
    pub keypoints: super::super::msg::rmw::KeyPoint2DArray,

    /// keypoints for human pose estimation
    pub keypoints3d: super::super::msg::rmw::KeyPoint3DArray,

}



impl Default for Detection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__Detection__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__Detection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Detection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Detection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Detection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__Detection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Detection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Detection where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/Detection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__Detection() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__DetectionArray() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__DetectionArray__init(msg: *mut DetectionArray) -> bool;
    fn interfaces_pkg__msg__DetectionArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DetectionArray>, size: usize) -> bool;
    fn interfaces_pkg__msg__DetectionArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DetectionArray>);
    fn interfaces_pkg__msg__DetectionArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DetectionArray>, out_seq: *mut rosidl_runtime_rs::Sequence<DetectionArray>) -> bool;
}

// Corresponds to interfaces_pkg__msg__DetectionArray
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// represents all YOLOv8 detections in one frame

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetectionArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub detections: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Detection>,

}



impl Default for DetectionArray {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__DetectionArray__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__DetectionArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DetectionArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__DetectionArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__DetectionArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__DetectionArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DetectionArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DetectionArray where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/DetectionArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__DetectionArray() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__LaneInfo() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__LaneInfo__init(msg: *mut LaneInfo) -> bool;
    fn interfaces_pkg__msg__LaneInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>, size: usize) -> bool;
    fn interfaces_pkg__msg__LaneInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>);
    fn interfaces_pkg__msg__LaneInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LaneInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<LaneInfo>) -> bool;
}

// Corresponds to interfaces_pkg__msg__LaneInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LaneInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub slope: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_points: rosidl_runtime_rs::Sequence<super::super::msg::rmw::TargetPoint>,

}



impl Default for LaneInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__LaneInfo__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__LaneInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LaneInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__LaneInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__LaneInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__LaneInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LaneInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LaneInfo where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/LaneInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__LaneInfo() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__RailInfo() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__RailInfo__init(msg: *mut RailInfo) -> bool;
    fn interfaces_pkg__msg__RailInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RailInfo>, size: usize) -> bool;
    fn interfaces_pkg__msg__RailInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RailInfo>);
    fn interfaces_pkg__msg__RailInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RailInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<RailInfo>) -> bool;
}

// Corresponds to interfaces_pkg__msg__RailInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RailInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_rail: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rail_cx: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rail_cy: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_cx: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_cy: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_width: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_height: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub angle_deg: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rail_bbox_width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rail_bbox_height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rail_bbox_area_ratio: f32,

}



impl Default for RailInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__RailInfo__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__RailInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RailInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__RailInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__RailInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__RailInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RailInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RailInfo where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/RailInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__RailInfo() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__MotionCommand() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__MotionCommand__init(msg: *mut MotionCommand) -> bool;
    fn interfaces_pkg__msg__MotionCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotionCommand>, size: usize) -> bool;
    fn interfaces_pkg__msg__MotionCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotionCommand>);
    fn interfaces_pkg__msg__MotionCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotionCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<MotionCommand>) -> bool;
}

// Corresponds to interfaces_pkg__msg__MotionCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub steering: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub left_speed: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub right_speed: i32,

}



impl Default for MotionCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__MotionCommand__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__MotionCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotionCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__MotionCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__MotionCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__MotionCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotionCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotionCommand where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/MotionCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__MotionCommand() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__TargetPoint() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__TargetPoint__init(msg: *mut TargetPoint) -> bool;
    fn interfaces_pkg__msg__TargetPoint__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TargetPoint>, size: usize) -> bool;
    fn interfaces_pkg__msg__TargetPoint__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TargetPoint>);
    fn interfaces_pkg__msg__TargetPoint__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TargetPoint>, out_seq: *mut rosidl_runtime_rs::Sequence<TargetPoint>) -> bool;
}

// Corresponds to interfaces_pkg__msg__TargetPoint
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TargetPoint {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_x: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_y: i64,

}



impl Default for TargetPoint {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__TargetPoint__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__TargetPoint__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TargetPoint {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__TargetPoint__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__TargetPoint__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__TargetPoint__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TargetPoint {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TargetPoint where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/TargetPoint";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__TargetPoint() }
  }
}


#[link(name = "interfaces_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__PathPlanningResult() -> *const std::ffi::c_void;
}

#[link(name = "interfaces_pkg__rosidl_generator_c")]
extern "C" {
    fn interfaces_pkg__msg__PathPlanningResult__init(msg: *mut PathPlanningResult) -> bool;
    fn interfaces_pkg__msg__PathPlanningResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PathPlanningResult>, size: usize) -> bool;
    fn interfaces_pkg__msg__PathPlanningResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PathPlanningResult>);
    fn interfaces_pkg__msg__PathPlanningResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PathPlanningResult>, out_seq: *mut rosidl_runtime_rs::Sequence<PathPlanningResult>) -> bool;
}

// Corresponds to interfaces_pkg__msg__PathPlanningResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// PathPlanningResult.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PathPlanningResult {
    /// 경로의 각 점들의 x 좌표
    pub x_points: rosidl_runtime_rs::Sequence<f64>,

    /// 경로의 각 점들의 y 좌표
    pub y_points: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for PathPlanningResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces_pkg__msg__PathPlanningResult__init(&mut msg as *mut _) {
        panic!("Call to interfaces_pkg__msg__PathPlanningResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PathPlanningResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__PathPlanningResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__PathPlanningResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces_pkg__msg__PathPlanningResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PathPlanningResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PathPlanningResult where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces_pkg/msg/PathPlanningResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces_pkg__msg__PathPlanningResult() }
  }
}


