import numbers as _numbers
from contextvars import ContextVar
from fractions import Fraction as _Fraction
from functools import partial as _partial
from typing import (Tuple,
                    Type)

from reprit.base import generate_repr

from ground import geometrical as _geometrical
from . import hints as _hints
from .core import (angular as _angular,
                   enums as _enums,
                   geometries as _geometries,
                   incircle as _incircle,
                   linear as _linear,
                   vector as _vector)
from .core.hints import QuaternaryPointFunction as _QuaternaryPointFunction
from .core.utils import robust_inverse as _robust_inverse

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Coordinate]
Kind = _enums.Kind
Orientation = _enums.Orientation
SegmentsRelationship = _enums.SegmentsRelationship


class Context:
    __slots__ = '_geometries', '_incircle', '_inverse', '_vector'

    def __init__(self, geometries: _geometrical.Context) -> None:
        self.geometries = geometries

    __repr__ = generate_repr(__init__)

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self.geometries.coordinate_cls

    @property
    def cross_product(self) -> _QuaternaryFunction:
        return self._vector.cross_product

    @property
    def dot_product(self) -> _QuaternaryFunction:
        return self._vector.dot_product

    @property
    def geometries(self) -> _geometrical.Context:
        return self._geometries

    @geometries.setter
    def geometries(self, value: _geometrical.Context) -> None:
        self._geometries = value
        exact = issubclass(self._geometries.coordinate_cls, _numbers.Rational)
        self._inverse = (_partial(_Fraction, 1)
                         if exact
                         else (1..__truediv__
                               if issubclass(self._geometries.coordinate_cls,
                                             float)
                               else _robust_inverse))
        self._incircle, self._vector = (
            (_incircle.plain_context, _vector.plain_context)
            if exact
            else (_incircle.robust_context, _vector.robust_context))
    @property
    def point_cls(self) -> Type[_hints.Point]:
        return self.geometries.point_cls

    @property
    def point_point_point_incircle_test(self) -> _QuaternaryFunction:
        return self._incircle.point_point_point_test

    def kind(self,
             vertex: _hints.Point,
             first_ray_point: _hints.Point,
             second_ray_point: _hints.Point) -> Kind:
        return _angular.kind(self.dot_product, vertex, first_ray_point,
                             second_ray_point)

    def orientation(self,
                    vertex: _hints.Point,
                    first_ray_point: _hints.Point,
                    second_ray_point: _hints.Point) -> Orientation:
        return _angular.orientation(self.dot_product, vertex, first_ray_point,
                                    second_ray_point)

    def segments_intersection(self,
                              first_start: _hints.Point,
                              first_end: _hints.Point,
                              second_start: _hints.Point,
                              second_end: _hints.Point) -> _hints.Point:
        return _linear.segments_intersection(
                self.cross_product, self._inverse, self.point_cls, first_start,
                first_end, second_start, second_end)

    def segments_intersections(self,
                               first_start: _hints.Point,
                               first_end: _hints.Point,
                               second_start: _hints.Point,
                               second_end: _hints.Point
                               ) -> Tuple[_hints.Point, ...]:
        return _linear.segments_intersections(
                self.cross_product, self._inverse, self.point_cls, first_start,
                first_end, second_start, second_end)

    def segments_relationship(self,
                              first_start: _hints.Point,
                              first_end: _hints.Point,
                              second_start: _hints.Point,
                              second_end: _hints.Point) -> SegmentsRelationship:
        return _linear.segments_relationship(self.cross_product, first_start,
                                             first_end, second_start,
                                             second_end)


_context = ContextVar('context',
                      default=Context(_geometrical.Context(
                              contour_cls=_geometries.Contour,
                              coordinate_cls=_numbers.Real,
                              multipoint_cls=_geometries.Multipoint,
                              multipolygon_cls=_geometries.Multipolygon,
                              multisegment_cls=_geometries.Multisegment,
                              point_cls=_geometries.Point,
                              polygon_cls=_geometries.Polygon,
                              segment_cls=_geometries.Segment)))


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    assert isinstance(context, Context), ('Expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context.set(context)
