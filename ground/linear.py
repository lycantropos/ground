from functools import partial as _partial
from typing import (Callable,
                    Tuple)

from . import hints as _hints
from .coordinates import to_divider as _to_divider
from .core import linear as _linear
from .functions import to_cross_producer as _to_cross_producer
from .geometries import to_point_cls as _to_point_cls

SegmentsRelationship = _linear.SegmentsRelationship


def to_segment_contains_point() -> Callable[[_hints.Point, _hints.Point,
                                             _hints.Point], bool]:
    return _partial(_linear.segment_contains_point, _to_cross_producer())


def to_segments_intersection() -> Callable[[_hints.Point, _hints.Point,
                                            _hints.Point, _hints.Point],
                                           _hints.Point]:
    return _partial(_linear.segments_intersection, _to_cross_producer(),
                    _to_divider(), _to_point_cls())


def to_segments_intersections() -> Callable[[_hints.Point, _hints.Point,
                                             _hints.Point, _hints.Point],
                                            Tuple[_hints.Point, ...]]:
    return _partial(_linear.segments_intersections, _to_cross_producer(),
                    _to_divider(), _to_point_cls())


def to_segments_relationship() -> Callable[[_hints.Point, _hints.Point,
                                            _hints.Point, _hints.Point],
                                           SegmentsRelationship]:
    return _partial(_linear.segments_relationship, _to_cross_producer())
