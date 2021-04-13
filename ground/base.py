import enum as _enum
from contextvars import ContextVar as _ContextVar
from typing import (Sequence as _Sequence,
                    Type as _Type)

from reprit.base import generate_repr as _generate_repr
from symba.base import sqrt as _sqrt

from . import hints as _hints
from .core import (angular as _angular,
                   boxed as _boxed,
                   centroidal as _centroidal,
                   discrete as _discrete,
                   enums as _enums,
                   geometries as _geometries,
                   incircle as _incircle,
                   linear as _linear,
                   metric as _metric,
                   vector as _vector)
from .core.hints import QuaternaryPointFunction as _QuaternaryPointFunction

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Coordinate]
Kind = _enums.Kind
Orientation = _enums.Orientation
Relation = _enums.Relation


@_enum.unique
class Mode(_enum.IntEnum):
    """Represents possible context modes."""
    EXACT = 0
    PLAIN = 1
    ROBUST = 2


class Context:
    """Represents common language for computational geometry."""
    __slots__ = ('_box_cls', '_centroidal', '_contour_cls', '_incircle',
                 '_linear', '_metric', '_mode', '_multipoint_cls',
                 '_multipolygon_cls', '_multisegment_cls', '_point_cls',
                 '_polygon_cls', '_segment_cls', '_sqrt', '_vector')

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
        self._sqrt = _sqrt
        (self._centroidal, self._incircle, self._linear, self._metric,
         self._vector) = (
            (_centroidal.exact_context, _incircle.exact_context,
             _linear.exact_context, _metric.exact_context,
             _vector.exact_context)
            if mode is Mode.EXACT
            else ((_centroidal.plain_context, _incircle.plain_context,
                   _linear.plain_context, _metric.plain_context,
                   _vector.plain_context)
                  if mode is Mode.PLAIN
                  else (_centroidal.robust_context, _incircle.robust_context,
                        _linear.exact_context, _metric.robust_context,
                        _vector.robust_context)))

    __repr__ = _generate_repr(__init__)

    @property
    def box_cls(self) -> _Type[_hints.Box]:
        """Returns type for boxes."""
        return self._box_cls

    @property
    def box_point_squared_distance(self) -> _metric.BoxPointMetric:
        """
        Returns squared Euclidean distance between box and a point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point = context.box_cls, context.point_cls
        >>> context.box_point_squared_distance(Box(0, 1, 0, 1),
        ...                                    Point(1, 1)) == 0
        True
        >>> context.box_point_squared_distance(Box(0, 1, 0, 1),
        ...                                    Point(2, 1)) == 1
        True
        >>> context.box_point_squared_distance(Box(0, 1, 0, 1),
        ...                                    Point(2, 2)) == 2
        True
        """
        return self._metric.box_point_squared_metric

    @property
    def contour_cls(self) -> _Type[_hints.Contour]:
        """Returns type for contours."""
        return self._contour_cls

    @property
    def cross_product(self) -> _QuaternaryFunction:
        """
        Returns cross product of the segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.cross_product(Point(0, 0), Point(0, 1), Point(0, 0),
        ...                       Point(1, 0)) == -1
        True
        >>> context.cross_product(Point(0, 0), Point(1, 0), Point(0, 0),
        ...                       Point(1, 0)) == 0
        True
        >>> context.cross_product(Point(0, 0), Point(1, 0), Point(0, 0),
        ...                       Point(0, 1)) == 1
        True
        """
        return self._vector.cross_product

    @property
    def dot_product(self) -> _QuaternaryFunction:
        """
        Returns dot product of the segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.dot_product(Point(0, 0), Point(1, 0), Point(0, 0),
        ...                     Point(-1, 0)) == -1
        True
        >>> context.dot_product(Point(0, 0), Point(1, 0), Point(0, 0),
        ...                     Point(0, 1)) == 0
        True
        >>> context.dot_product(Point(0, 0), Point(1, 0), Point(0, 0),
        ...                     Point(1, 0)) == 1
        True
        """
        return self._vector.dot_product

    @property
    def mode(self) -> Mode:
        """Returns mode of the context."""
        return self._mode

    @property
    def multipoint_cls(self) -> _Type[_hints.Multipoint]:
        """Returns type for multipoints."""
        return self._multipoint_cls

    @property
    def multipolygon_cls(self) -> _Type[_hints.Multipolygon]:
        """Returns type for multipolygons."""
        return self._multipolygon_cls

    @property
    def multisegment_cls(self) -> _Type[_hints.Multisegment]:
        """Returns type for multisegments."""
        return self._multisegment_cls

    @property
    def point_cls(self) -> _Type[_hints.Point]:
        """Returns type for points."""
        return self._point_cls

    @property
    def point_point_point_incircle_test(self) -> _QuaternaryFunction:
        """
        Returns result of "incircle test" for point-point-point case.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.point_point_point_incircle_test(Point(0, 0), Point(2, 0),
        ...                                          Point(0, 2), Point(1, 1))
        ...  > 0)
        True
        >>> (context.point_point_point_incircle_test(Point(0, 0), Point(2, 0),
        ...                                          Point(0, 2), Point(2, 2))
        ...  == 0)
        True
        >>> (context.point_point_point_incircle_test(Point(0, 0), Point(2, 0),
        ...                                          Point(0, 2), Point(3, 3))
        ...  < 0)
        True
        """
        return self._incircle.point_point_point_test

    @property
    def points_squared_distance(self) -> _metric.PointPointMetric:
        """
        Returns squared Euclidean distance between two points.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.points_squared_distance(Point(0, 0), Point(0, 0)) == 0
        True
        >>> context.points_squared_distance(Point(0, 0), Point(1, 0)) == 1
        True
        >>> context.points_squared_distance(Point(0, 1), Point(1, 0)) == 2
        True
        """
        return self._metric.point_point_squared_metric

    @property
    def polygon_cls(self) -> _Type[_hints.Polygon]:
        """Returns type for polygons."""
        return self._polygon_cls

    @property
    def segment_cls(self) -> _Type[_hints.Segment]:
        """Returns type for segments."""
        return self._segment_cls

    def angle_kind(self,
                   vertex: _hints.Point,
                   first_ray_point: _hints.Point,
                   second_ray_point: _hints.Point) -> Kind:
        """
        Returns angle kind.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.angle_kind(Point(0, 0), Point(1, 0), Point(-1, 0))
        ...  is Kind.OBTUSE)
        True
        >>> (context.angle_kind(Point(0, 0), Point(1, 0), Point(0, 1))
        ...  is Kind.RIGHT)
        True
        >>> (context.angle_kind(Point(0, 0), Point(1, 0), Point(1, 0))
        ...  is Kind.ACUTE)
        True
        """
        return _angular.kind(self.dot_product, vertex, first_ray_point,
                             second_ray_point)

    def angle_orientation(self,
                          vertex: _hints.Point,
                          first_ray_point: _hints.Point,
                          second_ray_point: _hints.Point) -> Orientation:
        """
        Returns angle orientation.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.angle_orientation(Point(0, 0), Point(0, 1), Point(1, 0))
        ...  is Orientation.CLOCKWISE)
        True
        >>> (context.angle_orientation(Point(0, 0), Point(1, 0), Point(1, 0))
        ...  is Orientation.COLLINEAR)
        True
        >>> (context.angle_orientation(Point(0, 0), Point(1, 0), Point(0, 1))
        ...  is Orientation.COUNTERCLOCKWISE)
        True
        """
        return _angular.orientation(self.cross_product, vertex,
                                    first_ray_point, second_ray_point)

    def box_segment_squared_distance(self,
                                     box: _hints.Box,
                                     start: _hints.Point,
                                     end: _hints.Point) -> _hints.Coordinate:
        """
        Returns squared Euclidean distance between box and a segment
        given its endpoints.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point = context.box_cls, context.point_cls
        >>> context.box_segment_squared_distance(Box(0, 1, 0, 1), Point(0, 0),
        ...                                      Point(1, 1)) == 0
        True
        >>> context.box_segment_squared_distance(Box(0, 1, 0, 1), Point(2, 0),
        ...                                      Point(2, 1)) == 1
        True
        >>> context.box_segment_squared_distance(Box(0, 1, 0, 1), Point(2, 2),
        ...                                      Point(3, 2)) == 2
        True
        """
        return self._metric.box_segment_squared_metric(
                box, start, end, self.dot_product, self.segments_relation,
                self.point_cls)

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
        return self._centroidal.contour_centroid(self.point_cls, vertices,
                                                 self._sqrt)

    def merged_box(self, first_box: _hints.Box, second_box: _hints.Box
                   ) -> _hints.Box:
        """
        Merges two boxes.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box = context.box_cls
        >>> (context.merged_box(Box(0, 1, 0, 1), Box(1, 2, 1, 2))
        ...  == Box(0, 2, 0, 2))
        True
        """
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

    def multipolygon_centroid(self,
                              polygons: _Sequence[_hints.Polygon]
                              ) -> _hints.Point:
        """
        Constructs centroid of a multipolygon given its polygons.

        Time complexity:
            ``O(len(vertices_count))``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in polygons)``.

        >>> context = get_context()
        >>> Contour, Point, Polygon = (context.contour_cls, context.point_cls,
        ...                            context.polygon_cls)
        >>> (context.multipolygon_centroid(
        ...     [Polygon(Contour([Point(0, 0), Point(1, 0), Point(1, 1),
        ...                       Point(0, 1)]), []),
        ...      Polygon(Contour([Point(1, 1), Point(2, 1), Point(2, 2),
        ...                       Point(1, 2)]), [])])
        ...  == Point(1, 1))
        True
        """
        return self._centroidal.multipolygon_centroid(self.point_cls, polygons)

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
        return _discrete.to_convex_hull(points, self.angle_orientation)

    def polygon_centroid(self,
                         border: _hints.Contour,
                         holes: _Sequence[_hints.Contour]) -> _hints.Point:
        """
        Constructs centroid of a polygon given its border & holes.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(border.vertices)\
 + sum(len(hole.vertices) for hole in holes)``.

        >>> context = get_context()
        >>> Contour, Point = context.contour_cls, context.point_cls
        >>> (context.polygon_centroid(Contour([Point(0, 0), Point(4, 0),
        ...                                    Point(4, 4), Point(0, 4)]),
        ...                           [Contour([Point(1, 1), Point(1, 3),
        ...                                     Point(3, 3), Point(3, 1)])])
        ...  == Point(2, 2))
        True
        """
        return self._centroidal.polygon_centroid(self.point_cls, border, holes)

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
        return self._linear.containment_checker(start, end, point,
                                                self.cross_product)

    def segment_point_squared_distance(self,
                                       start: _hints.Point,
                                       end: _hints.Point,
                                       point: _hints.Point
                                       ) -> _hints.Coordinate:
        """
        Returns squared Euclidean distance between segment given its endpoints
        and a point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.segment_point_squared_distance(Point(0, 0), Point(1, 0),
        ...                                        Point(0, 0)) == 0
        True
        >>> context.segment_point_squared_distance(Point(0, 0), Point(1, 0),
        ...                                        Point(0, 1)) == 1
        True
        >>> context.segment_point_squared_distance(Point(0, 0), Point(1, 0),
        ...                                        Point(2, 1)) == 2
        True
        """
        return self._metric.segment_point_squared_metric(start, end, point,
                                                         self.dot_product)

    def segments_intersection(self,
                              first_start: _hints.Point,
                              first_end: _hints.Point,
                              second_start: _hints.Point,
                              second_end: _hints.Point) -> _hints.Point:
        """
        Returns intersection point of two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.segments_intersection(Point(0, 0), Point(2, 0),
        ...                                Point(0, 0), Point(0, 1))
        ...  == Point(0, 0))
        True
        >>> (context.segments_intersection(Point(0, 0), Point(2, 0),
        ...                                Point(1, 0), Point(1, 1))
        ...  == Point(1, 0))
        True
        >>> (context.segments_intersection(Point(0, 0), Point(2, 0),
        ...                                Point(2, 0), Point(3, 0))
        ...  == Point(2, 0))
        True
        """
        return self._linear.intersector(
                first_start, first_end, second_start, second_end,
                self.cross_product, self.point_cls)

    def segments_relation(self,
                          test_start: _hints.Point,
                          test_end: _hints.Point,
                          goal_start: _hints.Point,
                          goal_end: _hints.Point) -> Relation:
        """
        Returns relation between two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(1, 0),
        ...                           Point(2, 0)) is Relation.DISJOINT
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(0, 0),
        ...                           Point(2, 0)) is Relation.TOUCH
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(2, 0),
        ...                           Point(0, 2)) is Relation.CROSS
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(0, 0),
        ...                           Point(1, 1)) is Relation.COMPOSITE
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(0, 0),
        ...                           Point(2, 2)) is Relation.EQUAL
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(0, 0),
        ...                           Point(3, 3)) is Relation.COMPONENT
        True
        >>> context.segments_relation(Point(0, 0), Point(2, 2), Point(1, 1),
        ...                           Point(3, 3)) is Relation.OVERLAP
        True
        """
        return self._linear.relater(test_start, test_end, goal_start, goal_end,
                                    self.cross_product)

    def segments_squared_distance(self,
                                  first_start: _hints.Point,
                                  first_end: _hints.Point,
                                  second_start: _hints.Point,
                                  second_end: _hints.Point
                                  ) -> _hints.Coordinate:
        """
        Returns squared Euclidean distance between two segments
        given their endpoints.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.segments_squared_distance(Point(0, 0), Point(1, 0),
        ...                                   Point(0, 0), Point(0, 1)) == 0
        True
        >>> context.segments_squared_distance(Point(0, 0), Point(1, 0),
        ...                                   Point(0, 1), Point(1, 1)) == 1
        True
        >>> context.segments_squared_distance(Point(0, 0), Point(1, 0),
        ...                                   Point(2, 1), Point(2, 2)) == 2
        True
        """
        return self._metric.segment_segment_squared_metric(
                first_start, first_end, second_start, second_end,
                self.dot_product, self.segments_relation)


_context = _ContextVar('context',
                       default=Context())


def get_context() -> Context:
    """Returns current context."""
    return _context.get()


def set_context(context: Context) -> None:
    """Sets current context."""
    assert isinstance(context, Context), ('Expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context.set(context)
