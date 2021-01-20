import enum as _enum
from contextvars import ContextVar as _ContextVar
from typing import (Sequence as _Sequence,
                    Type as _Type)

from reprit.base import generate_repr as _generate_repr

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
Relation = _enums.Relation


@_enum.unique
class Mode(_enum.IntEnum):
    EXACT = 0
    PLAIN = 1
    ROBUST = 2


class Context:
    __slots__ = ('_box_cls', '_centroidal', '_contour_cls', '_incircle',
                 '_linear', '_mode', '_multipoint_cls', '_multipolygon_cls',
                 '_multisegment_cls', '_point_cls', '_polygon_cls',
                 '_segment_cls', '_vector')

    def __init__(self,
                 *,
                 box_cls: _Type[_hints.Box] = _geometries.Box,
                 contour_cls: _Type[_hints.Contour] = _geometries.Contour,
                 multipoint_cls: _Type[_hints.Multipoint]
                 = _geometries.Multipoint,
                 multipolygon_cls: _Type[_hints.Multipolygon]
                 = _geometries.Multipolygon,
                 multisegment_cls: _Type[_hints.Multisegment]
                 = _geometries.Multisegment,
                 point_cls: _Type[_hints.Point] = _geometries.Point,
                 polygon_cls: _Type[_hints.Polygon] = _geometries.Polygon,
                 segment_cls: _Type[_hints.Segment] = _geometries.Segment,
                 mode: Mode = Mode.EXACT) -> None:
        self._box_cls = box_cls
        self._contour_cls = contour_cls
        self._multipoint_cls = multipoint_cls
        self._multipolygon_cls = multipolygon_cls
        self._multisegment_cls = multisegment_cls
        self._point_cls = point_cls
        self._polygon_cls = polygon_cls
        self._segment_cls = segment_cls
        self._mode = mode
        self._centroidal, self._incircle, self._linear, self._vector = (
            (_centroidal.exact_context, _incircle.exact_context,
             _linear.exact_context, _vector.exact_context)
            if mode is Mode.EXACT
            else ((_centroidal.plain_context, _incircle.plain_context,
                   _linear.plain_context, _vector.plain_context)
                  if mode is Mode.PLAIN
                  else (_centroidal.robust_context, _incircle.robust_context,
                        _linear.exact_context, _vector.robust_context)))

    __repr__ = _generate_repr(__init__)

    @property
    def box_cls(self) -> _Type[_hints.Box]:
        return self._box_cls

    @property
    def contour_cls(self) -> _Type[_hints.Contour]:
        return self._contour_cls

    @property
    def cross_product(self) -> _QuaternaryFunction:
        return self._vector.cross_product

    @property
    def dot_product(self) -> _QuaternaryFunction:
        return self._vector.dot_product

    @property
    def mode(self) -> Mode:
        return self._mode

    @property
    def multipoint_cls(self) -> _Type[_hints.Multipoint]:
        return self._multipoint_cls

    @property
    def multipolygon_cls(self) -> _Type[_hints.Multipolygon]:
        return self._multipolygon_cls

    @property
    def multisegment_cls(self) -> _Type[_hints.Multisegment]:
        return self._multisegment_cls

    @property
    def point_cls(self) -> _Type[_hints.Point]:
        return self._point_cls

    @property
    def point_point_point_incircle_test(self) -> _QuaternaryFunction:
        return self._incircle.point_point_point_test

    @property
    def polygon_cls(self) -> _Type[_hints.Polygon]:
        return self._polygon_cls

    @property
    def segment_cls(self) -> _Type[_hints.Segment]:
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
                         vertices: _Sequence[_hints.Point]) -> _hints.Point:
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
        return self._centroidal.contour_centroid(self.point_cls, vertices)

    def merged_box(self, first_box: _hints.Box, second_box: _hints.Box
                   ) -> _hints.Box:
        return _boxed.merge(self.box_cls, first_box, second_box)

    def multipoint_centroid(self,
                            points: _Sequence[_hints.Point]) -> _hints.Point:
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
                           points: _Sequence[_hints.Point]
                           ) -> _Sequence[_hints.Point]:
        """
        Constructs convex hull of points.

        Time complexity:
            ``O(points_count * log(points_count))``
        Memory complexity:
            ``O(points_count)``
        where ``points_count = len(points)``.

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.points_convex_hull([Point(0, 0), Point(2, 0), Point(2, 2),
        ...                              Point(0, 2)])
        ...  == [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
        True
        """
        return _discrete.to_convex_hull(self.angle_orientation, points)

    def segment_contains_point(self,
                               start: _hints.Point,
                               end: _hints.Point,
                               point: _hints.Point) -> bool:
        """
        Checks if a segment given by its endpoints contains given point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(0, 0))
        True
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(0, 2))
        False
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(1, 0))
        True
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(1, 1))
        False
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(2, 0))
        True
        >>> context.segment_contains_point(Point(0, 0), Point(2, 0),
        ...                                Point(3, 0))
        False
        """
        return self._linear.containment_checker(self.cross_product, start, end,
                                                point)

    def segments_intersection(self,
                              first_start: _hints.Point,
                              first_end: _hints.Point,
                              second_start: _hints.Point,
                              second_end: _hints.Point) -> _hints.Point:
        return self._linear.intersector(
                self.cross_product, self.point_cls, first_start, first_end,
                second_start, second_end)

    def segments_relation(self,
                          test_start: _hints.Point,
                          test_end: _hints.Point,
                          goal_start: _hints.Point,
                          goal_end: _hints.Point) -> Relation:
        return self._linear.relater(self.cross_product, test_start, test_end,
                                    goal_start, goal_end)


_context = _ContextVar('context',
                       default=Context())


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    assert isinstance(context, Context), ('Expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context.set(context)
