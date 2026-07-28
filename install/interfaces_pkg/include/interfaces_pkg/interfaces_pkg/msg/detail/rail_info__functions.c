// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces_pkg:msg/RailInfo.idl
// generated code does not contain a copyright notice
#include "interfaces_pkg/msg/detail/rail_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `distance`
#include "rosidl_runtime_c/string_functions.h"

bool
interfaces_pkg__msg__RailInfo__init(interfaces_pkg__msg__RailInfo * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    interfaces_pkg__msg__RailInfo__fini(msg);
    return false;
  }
  // has_rail
  // rail_cx
  // rail_cy
  // img_cx
  // img_cy
  // img_width
  // img_height
  // angle_deg
  // distance
  if (!rosidl_runtime_c__String__init(&msg->distance)) {
    interfaces_pkg__msg__RailInfo__fini(msg);
    return false;
  }
  // confidence
  // rail_bbox_width
  // rail_bbox_height
  // rail_bbox_area_ratio
  return true;
}

void
interfaces_pkg__msg__RailInfo__fini(interfaces_pkg__msg__RailInfo * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // has_rail
  // rail_cx
  // rail_cy
  // img_cx
  // img_cy
  // img_width
  // img_height
  // angle_deg
  // distance
  rosidl_runtime_c__String__fini(&msg->distance);
  // confidence
  // rail_bbox_width
  // rail_bbox_height
  // rail_bbox_area_ratio
}

bool
interfaces_pkg__msg__RailInfo__are_equal(const interfaces_pkg__msg__RailInfo * lhs, const interfaces_pkg__msg__RailInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // has_rail
  if (lhs->has_rail != rhs->has_rail) {
    return false;
  }
  // rail_cx
  if (lhs->rail_cx != rhs->rail_cx) {
    return false;
  }
  // rail_cy
  if (lhs->rail_cy != rhs->rail_cy) {
    return false;
  }
  // img_cx
  if (lhs->img_cx != rhs->img_cx) {
    return false;
  }
  // img_cy
  if (lhs->img_cy != rhs->img_cy) {
    return false;
  }
  // img_width
  if (lhs->img_width != rhs->img_width) {
    return false;
  }
  // img_height
  if (lhs->img_height != rhs->img_height) {
    return false;
  }
  // angle_deg
  if (lhs->angle_deg != rhs->angle_deg) {
    return false;
  }
  // distance
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->distance), &(rhs->distance)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // rail_bbox_width
  if (lhs->rail_bbox_width != rhs->rail_bbox_width) {
    return false;
  }
  // rail_bbox_height
  if (lhs->rail_bbox_height != rhs->rail_bbox_height) {
    return false;
  }
  // rail_bbox_area_ratio
  if (lhs->rail_bbox_area_ratio != rhs->rail_bbox_area_ratio) {
    return false;
  }
  return true;
}

bool
interfaces_pkg__msg__RailInfo__copy(
  const interfaces_pkg__msg__RailInfo * input,
  interfaces_pkg__msg__RailInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // has_rail
  output->has_rail = input->has_rail;
  // rail_cx
  output->rail_cx = input->rail_cx;
  // rail_cy
  output->rail_cy = input->rail_cy;
  // img_cx
  output->img_cx = input->img_cx;
  // img_cy
  output->img_cy = input->img_cy;
  // img_width
  output->img_width = input->img_width;
  // img_height
  output->img_height = input->img_height;
  // angle_deg
  output->angle_deg = input->angle_deg;
  // distance
  if (!rosidl_runtime_c__String__copy(
      &(input->distance), &(output->distance)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // rail_bbox_width
  output->rail_bbox_width = input->rail_bbox_width;
  // rail_bbox_height
  output->rail_bbox_height = input->rail_bbox_height;
  // rail_bbox_area_ratio
  output->rail_bbox_area_ratio = input->rail_bbox_area_ratio;
  return true;
}

interfaces_pkg__msg__RailInfo *
interfaces_pkg__msg__RailInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__RailInfo * msg = (interfaces_pkg__msg__RailInfo *)allocator.allocate(sizeof(interfaces_pkg__msg__RailInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces_pkg__msg__RailInfo));
  bool success = interfaces_pkg__msg__RailInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces_pkg__msg__RailInfo__destroy(interfaces_pkg__msg__RailInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces_pkg__msg__RailInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces_pkg__msg__RailInfo__Sequence__init(interfaces_pkg__msg__RailInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__RailInfo * data = NULL;

  if (size) {
    data = (interfaces_pkg__msg__RailInfo *)allocator.zero_allocate(size, sizeof(interfaces_pkg__msg__RailInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces_pkg__msg__RailInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces_pkg__msg__RailInfo__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
interfaces_pkg__msg__RailInfo__Sequence__fini(interfaces_pkg__msg__RailInfo__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      interfaces_pkg__msg__RailInfo__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

interfaces_pkg__msg__RailInfo__Sequence *
interfaces_pkg__msg__RailInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__RailInfo__Sequence * array = (interfaces_pkg__msg__RailInfo__Sequence *)allocator.allocate(sizeof(interfaces_pkg__msg__RailInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces_pkg__msg__RailInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces_pkg__msg__RailInfo__Sequence__destroy(interfaces_pkg__msg__RailInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces_pkg__msg__RailInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces_pkg__msg__RailInfo__Sequence__are_equal(const interfaces_pkg__msg__RailInfo__Sequence * lhs, const interfaces_pkg__msg__RailInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces_pkg__msg__RailInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces_pkg__msg__RailInfo__Sequence__copy(
  const interfaces_pkg__msg__RailInfo__Sequence * input,
  interfaces_pkg__msg__RailInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(interfaces_pkg__msg__RailInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces_pkg__msg__RailInfo * data =
      (interfaces_pkg__msg__RailInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces_pkg__msg__RailInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces_pkg__msg__RailInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces_pkg__msg__RailInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
