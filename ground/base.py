import numbers as _numbers
from contextvars import ContextVar
from fractions import Fraction as _Fraction
from typing import (Sequence,
                    Tuple,
                    Type)

from reprit.base import generate_repr

from . import hints as _hints
from .core import (angular as _angular,
                   boxed as _boxed,
                   centroidal as _centroidal,
                   discrete as _discrete,
                   enums as _enums,
                   geometries as _geometries,
                   incircle as _incircle,
                   linear as _linear,
                   vector as _vector)
from .core.hints import QuaternaryPointFunction as _QuaternaryPointFunction

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Coordinate]
Kind = _enums.Kind
Orientation = _enums.Orientation
SegmentsRelationship = _enums.SegmentsRelationship


class Context:
    __slots__ = ('_box_cls', '_centroidal', '_contour_cls', '_coordinate_cls',
                 '_incircle', '_inverse', '_multicontour_cls',
                 '_multipoint_cls', '_multipolygon_cls', '_multisegment_cls',
                 '_point_cls', '_polygon_cls', '_segment_cls', '_vector')

    def __init__(self,
                 *,
                 box_cls: Type[_hints.Box] = _geometries.Box,
                 contour_cls: Type[_hints.Contour] = _geometries.Contour,
                 coordinate_cls: Type[_hints.Coordinate] = _numbers.Real,
                 multicontour_cls: Type[_hints.Multicontour]
                 = _geometries.Multicontour,
                 multipoint_cls: Type[_hints.Multipoint]
                 = _geometries.Multipoint,
                 multipolygon_cls: Type[_hints.Multipolygon]
                 = _geometries.Multipolygon,
                 multisegment_cls: Type[_hints.Multisegment]
                 = _geometries.Multisegment,
                 point_cls: Type[_hints.Point] = _geometries.Point,
                 polygon_cls: Type[_hints.Polygon] = _geometries.Polygon,
                 segment_cls: Type[_hints.Segment] = _geometries.Segment
                 ) -> None:
        self._box_cls = box_cls
        self._contour_cls = contour_cls
        self._coordinate_cls = coordinate_cls
        self._multicontour_cls = multicontour_cls
        self._multipoint_cls = multipoint_cls
        self._multipolygon_cls = multipolygon_cls
        self._multisegment_cls = multisegment_cls
        self._point_cls = point_cls
        self._polygon_cls = polygon_cls
        self._segment_cls = segment_cls
        self._inverse = (1.
                         if issubclass(coordinate_cls, float)
                         else _Fraction(1)).__truediv__
        self._centroidal, self._incircle, self._vector = (
            (_centroidal.plain_context, _incircle.plain_context,
             _vector.plain_context)
            if issubclass(coordinate_cls, _numbers.Rational)
            else (_centroidal.robust_context, _incircle.robust_context,
                  _vector.robust_context))

    __repr__ = generate_repr(__init__)

    @property
    def box_cls(self) -> Type[_hints.Box]:
        return self._box_cls

    @property
    def contour_cls(self) -> Type[_hints.Contour]:
        return self._contour_cls

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self._coordinate_cls

    @property
    def cross_product(self) -> _QuaternaryFunction:
        return self._vector.cross_product

    @property
    def dot_product(self) -> _QuaternaryFunction:
        return self._vector.dot_product

    @property
    def multicontour_cls(self) -> Type[_hints.Multicontour]:
        return self._multicontour_cls

    @property
    def multipoint_cls(self) -> Type[_hints.Multipoint]:
        return self._multipoint_cls

    @property
    def multipolygon_cls(self) -> Type[_hints.Multipolygon]:
        return self._multipolygon_cls

    @property
    def multisegment_cls(self) -> Type[_hints.Multisegment]:
        return self._multisegment_cls

    @property
    def point_cls(self) -> Type[_hints.Point]:
        return self._point_cls

    @property
    def point_point_point_incircle_test(self) -> _QuaternaryFunction:
        return self._incircle.point_point_point_test

    @property
    def polygon_cls(self) -> Type[_hints.Polygon]:
        return self._polygon_cls

    @property
    def segment_cls(self) -> Type[_hints.Segment]:
        return self._segment_cls

    def angle_kind(self,
                   vertex: _hints.Point,
                   first_ray_point: _hints.Point,
                   second_ray_point: _hints.Point) -> Kind:
        return _angular.kind(self.dot_product, vertex, first_ray_point,
                             second_ray_point)

    def angle_orientation(self,
                          vertex: _hints.Point,
                          first_ray_point: _hints.Point,
                          second_ray_point: _hints.Point) -> Orientation:
        return _angular.orientation(self.cross_product, vertex,
                                    first_ray_point, second_ray_point)

    def contour_centroid(self,
                         vertices: Sequence[_hints.Point]) -> _hints.Point:
        """
        Constructs centroid of a contour given its vertices.

        Time complexity:
            ``O(len(vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.contour_centroid([Point(0, 0), Point(2, 0), Point(2, 2),
        ...                           Point(0, 2)]) == Point(1, 1)
        True
        """
        return self._centroidal.contour_centroid(self._inverse, self.point_cls,
                                                 vertices)

    def merged_box(self, first_box: _hints.Box, second_box: _hints.Box
                   ) -> _hints.Box:
        return _boxed.merge(self.box_cls, first_box, second_box)

    def multipoint_centroid(self,
                            points: Sequence[_hints.Point]) -> _hints.Point:
        """
        Constructs centroid of a multipoint given its points.

        Time complexity:
            ``O(len(points))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.multipoint_centroid([Point(0, 0), Point(2, 0), Point(2, 2),
        ...                              Point(0, 2)]) == Point(1, 1)
        True
        """
        return self._centroidal.multipoint_centroid(self.point_cls, points)

    def points_convex_hull(self,
                           points: Sequence[_hints.Point]
                           ) -> Sequence[_hints.Point]:
        return _discrete.to_convex_hull(self.angle_orientation, points)

    def segment_contains_point(self,
                               start: _hints.Point,
                               end: _hints.Point,
                               point: _hints.Point) -> bool:
        return _linear.segment_contains_point(self.cross_product, start, end,
                                              point)

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
                              second_end: _hints.Point
                              ) -> SegmentsRelationship:
        return _linear.segments_relationship(self.cross_product, first_start,
                                             first_end, second_start,
                                             second_end)


_context = ContextVar('context',
                      default=Context())


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    assert isinstance(context, Context), ('Expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context.set(context)
