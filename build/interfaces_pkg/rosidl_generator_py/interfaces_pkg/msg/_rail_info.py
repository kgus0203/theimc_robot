# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interfaces_pkg:msg/RailInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RailInfo(type):
    """Metaclass of message 'RailInfo'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces_pkg')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces_pkg.msg.RailInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__rail_info
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__rail_info
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__rail_info
            cls._TYPE_SUPPORT = module.type_support_msg__msg__rail_info
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__rail_info

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RailInfo(metaclass=Metaclass_RailInfo):
    """Message class 'RailInfo'."""

    __slots__ = [
        '_header',
        '_has_rail',
        '_rail_cx',
        '_rail_cy',
        '_img_cx',
        '_img_cy',
        '_img_width',
        '_img_height',
        '_angle_deg',
        '_distance',
        '_confidence',
        '_rail_bbox_width',
        '_rail_bbox_height',
        '_rail_bbox_area_ratio',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'has_rail': 'boolean',
        'rail_cx': 'float',
        'rail_cy': 'float',
        'img_cx': 'float',
        'img_cy': 'float',
        'img_width': 'uint32',
        'img_height': 'uint32',
        'angle_deg': 'float',
        'distance': 'string',
        'confidence': 'float',
        'rail_bbox_width': 'float',
        'rail_bbox_height': 'float',
        'rail_bbox_area_ratio': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.has_rail = kwargs.get('has_rail', bool())
        self.rail_cx = kwargs.get('rail_cx', float())
        self.rail_cy = kwargs.get('rail_cy', float())
        self.img_cx = kwargs.get('img_cx', float())
        self.img_cy = kwargs.get('img_cy', float())
        self.img_width = kwargs.get('img_width', int())
        self.img_height = kwargs.get('img_height', int())
        self.angle_deg = kwargs.get('angle_deg', float())
        self.distance = kwargs.get('distance', str())
        self.confidence = kwargs.get('confidence', float())
        self.rail_bbox_width = kwargs.get('rail_bbox_width', float())
        self.rail_bbox_height = kwargs.get('rail_bbox_height', float())
        self.rail_bbox_area_ratio = kwargs.get('rail_bbox_area_ratio', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.has_rail != other.has_rail:
            return False
        if self.rail_cx != other.rail_cx:
            return False
        if self.rail_cy != other.rail_cy:
            return False
        if self.img_cx != other.img_cx:
            return False
        if self.img_cy != other.img_cy:
            return False
        if self.img_width != other.img_width:
            return False
        if self.img_height != other.img_height:
            return False
        if self.angle_deg != other.angle_deg:
            return False
        if self.distance != other.distance:
            return False
        if self.confidence != other.confidence:
            return False
        if self.rail_bbox_width != other.rail_bbox_width:
            return False
        if self.rail_bbox_height != other.rail_bbox_height:
            return False
        if self.rail_bbox_area_ratio != other.rail_bbox_area_ratio:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def has_rail(self):
        """Message field 'has_rail'."""
        return self._has_rail

    @has_rail.setter
    def has_rail(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'has_rail' field must be of type 'bool'"
        self._has_rail = value

    @builtins.property
    def rail_cx(self):
        """Message field 'rail_cx'."""
        return self._rail_cx

    @rail_cx.setter
    def rail_cx(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rail_cx' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rail_cx' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rail_cx = value

    @builtins.property
    def rail_cy(self):
        """Message field 'rail_cy'."""
        return self._rail_cy

    @rail_cy.setter
    def rail_cy(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rail_cy' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rail_cy' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rail_cy = value

    @builtins.property
    def img_cx(self):
        """Message field 'img_cx'."""
        return self._img_cx

    @img_cx.setter
    def img_cx(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'img_cx' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'img_cx' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._img_cx = value

    @builtins.property
    def img_cy(self):
        """Message field 'img_cy'."""
        return self._img_cy

    @img_cy.setter
    def img_cy(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'img_cy' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'img_cy' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._img_cy = value

    @builtins.property
    def img_width(self):
        """Message field 'img_width'."""
        return self._img_width

    @img_width.setter
    def img_width(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'img_width' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'img_width' field must be an unsigned integer in [0, 4294967295]"
        self._img_width = value

    @builtins.property
    def img_height(self):
        """Message field 'img_height'."""
        return self._img_height

    @img_height.setter
    def img_height(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'img_height' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'img_height' field must be an unsigned integer in [0, 4294967295]"
        self._img_height = value

    @builtins.property
    def angle_deg(self):
        """Message field 'angle_deg'."""
        return self._angle_deg

    @angle_deg.setter
    def angle_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'angle_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'angle_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._angle_deg = value

    @builtins.property
    def distance(self):
        """Message field 'distance'."""
        return self._distance

    @distance.setter
    def distance(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'distance' field must be of type 'str'"
        self._distance = value

    @builtins.property
    def confidence(self):
        """Message field 'confidence'."""
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._confidence = value

    @builtins.property
    def rail_bbox_width(self):
        """Message field 'rail_bbox_width'."""
        return self._rail_bbox_width

    @rail_bbox_width.setter
    def rail_bbox_width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rail_bbox_width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rail_bbox_width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rail_bbox_width = value

    @builtins.property
    def rail_bbox_height(self):
        """Message field 'rail_bbox_height'."""
        return self._rail_bbox_height

    @rail_bbox_height.setter
    def rail_bbox_height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rail_bbox_height' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rail_bbox_height' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rail_bbox_height = value

    @builtins.property
    def rail_bbox_area_ratio(self):
        """Message field 'rail_bbox_area_ratio'."""
        return self._rail_bbox_area_ratio

    @rail_bbox_area_ratio.setter
    def rail_bbox_area_ratio(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rail_bbox_area_ratio' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rail_bbox_area_ratio' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rail_bbox_area_ratio = value
