from functools import partial as _partial
from typing import Tuple

from .coordinates import to_divider as _to_divider
from .core import linear as _linear
from .core.hints import (QuaternaryPointFunction as _QuaternaryPointFunction,
                         TernaryPointFunction as _TernaryPointFunction)
from .functions import to_cross_producer as _to_cross_producer
from .geometries import to_point_cls as _to_point_cls
from .hints import Point as _Point

SegmentsRelationship = _linear.SegmentsRelationship


def to_connected_segments_intersector() -> _QuaternaryPointFunction[_Point]:
    return _partial(_linear.segments_intersection, _to_cross_producer(),
                    _to_divider(), _to_point_cls())


def to_segment_containment_checker() -> _TernaryPointFunction[bool]:
    return _partial(_linear.segment_contains_point, _to_cross_producer())


def to_segments_intersector() -> _QuaternaryPointFunction[Tuple[_Point, ...]]:
    return _partial(_linear.segments_intersections, _to_cross_producer(),
                    _to_divider(), _to_point_cls())


def to_segments_relater() -> _QuaternaryPointFunction[SegmentsRelationship]:
    return _partial(_linear.segments_relationship, _to_cross_producer())
