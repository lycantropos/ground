import enum as _enum
from contextvars import ContextVar as _ContextVar
from typing import (Optional as _Optional,
                    Sequence as _Sequence,
                    Type as _Type,
                    Union as _Union)

from reprit import serializers as _serializers
from reprit.base import generate_repr as _generate_repr
from symba.base import sqrt as _sqrt

from . import hints as _hints
from .core import (angular as _angular,
                   boxed as _boxed,
                   centroidal as _centroidal,
                   circular as _circular,
                   discrete as _discrete,
                   enums as _enums,
                   geometries as _geometries,
                   measured as _measured,
                   metric as _metric,
                   rotation as _rotation,
                   scaling as _scaling,
                   segment as _segment,
                   translation as _translation,
                   vector as _vector)
from .core.hints import (QuaternaryPointFunction as _QuaternaryPointFunction,
                         SquareRooter as _SquareRooter)

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Scalar]

Location = _enums.Location
Kind = _enums.Kind
Orientation = _enums.Orientation
Relation = _enums.Relation


@_enum.unique
class Mode(_enums.Base):
    """Represents possible context modes."""
    EXACT = 0
    PLAIN = 1
    ROBUST = 2


class Context:
    """Represents common language for computational geometry."""
    __slots__ = ('_angular', '_box_cls', '_centroidal', '_circular',
                 '_contour_cls', '_empty', '_empty_cls', '_measured',
                 '_metric', '_mix_cls', '_mode', '_multipoint_cls',
                 '_multipolygon_cls', '_multisegment_cls', '_origin',
                 '_point_cls', '_polygon_cls', '_rotation', '_scaling',
                 '_segment', '_segment_cls', '_sqrt', '_translation',
                 '_vector')

    def __init__(self,
                 *,
                 box_cls: _Type[_hints.Box] = _geometries.Box,
                 contour_cls: _Type[_hints.Contour] = _geometries.Contour,
                 empty_cls: _Type[_hints.Empty] = _geometries.Empty,
                 mix_cls: _Type[_hints.Mix] = _geometries.Mix,
                 multipoint_cls: _Type[_hints.Multipoint]
                 = _geometries.Multipoint,
                 multipolygon_cls: _Type[_hints.Multipolygon]
                 = _geometries.Multipolygon,
                 multisegment_cls: _Type[_hints.Multisegment]
                 = _geometries.Multisegment,
                 point_cls: _Type[_hints.Point] = _geometries.Point,
                 polygon_cls: _Type[_hints.Polygon] = _geometries.Polygon,
                 segment_cls: _Type[_hints.Segment] = _geometries.Segment,
                 mode: Mode = Mode.EXACT,
                 sqrt: _SquareRooter = _sqrt) -> None:
        self._box_cls = box_cls
        self._contour_cls = contour_cls
        self._empty, self._empty_cls = empty_cls(), empty_cls
        self._mix_cls = mix_cls
        self._multipoint_cls = multipoint_cls
        self._multipolygon_cls = multipolygon_cls
        self._multisegment_cls = multisegment_cls
        self._origin = point_cls(0, 0)
        self._point_cls = point_cls
        self._polygon_cls = polygon_cls
        self._segment_cls = segment_cls
        self._mode = mode
        self._sqrt = sqrt
        (self._angular, self._centroidal, self._circular, self._measured,
         self._metric, self._rotation, self._scaling, self._segment,
         self._translation, self._vector) = (
            (_angular.exact_context, _centroidal.exact_context,
             _circular.exact_context, _measured.exact_context,
             _metric.exact_context, _rotation.exact_context,
             _scaling.exact_context, _segment.exact_context,
             _translation.exact_context, _vector.exact_context)
            if mode is Mode.EXACT
            else ((_angular.plain_context, _centroidal.plain_context,
                   _circular.plain_context, _measured.plain_context,
                   _metric.plain_context, _rotation.plain_context,
                   _scaling.plain_context, _segment.plain_context,
                   _translation.plain_context, _vector.plain_context)
                  if mode is Mode.PLAIN
                  else (_angular.robust_context, _centroidal.robust_context,
                        _circular.robust_context, _measured.robust_context,
                        _metric.robust_context, _rotation.robust_context,
                        _scaling.robust_context, _segment.exact_context,
                        _translation.robust_context, _vector.robust_context)))

    __repr__ = _generate_repr(__init__,
                              argument_serializer=_serializers.complex_,
                              skip_defaults=True)

    @property
    def angle_kind(self) -> _QuaternaryPointFunction[Kind]:
        """
        Returns function for computing angle kind.

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
        return self._angular.kind

    @property
    def angle_orientation(self) -> _QuaternaryPointFunction[Orientation]:
        """
        Returns function for computing angle orientation.

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
        return self._angular.orientation

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
    def empty(self) -> _hints.Empty:
        """Returns an empty geometry."""
        return self._empty

    @property
    def empty_cls(self) -> _Type[_hints.Empty]:
        """Returns type for empty geometries."""
        return self._empty_cls

    @property
    def mix_cls(self) -> _Type[_hints.Mix]:
        """Returns type for mixes."""
        return self._mix_cls

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
    def origin(self) -> _hints.Point:
        """Returns origin."""
        return self._origin

    @property
    def point_cls(self) -> _Type[_hints.Point]:
        """Returns type for points."""
        return self._point_cls

    @property
    def locate_point_in_point_point_point_circle(
            self) -> _circular.PointPointPointLocator:
        """
        Returns location of point in point-point-point circle.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.locate_point_in_point_point_point_circle(
        ...      Point(1, 1), Point(0, 0), Point(2, 0), Point(0, 2))
        ...  is Location.INTERIOR)
        True
        >>> (context.locate_point_in_point_point_point_circle(
        ...      Point(2, 2), Point(0, 0), Point(2, 0), Point(0, 2))
        ...  is Location.BOUNDARY)
        True
        >>> (context.locate_point_in_point_point_point_circle(
        ...      Point(3, 3), Point(0, 0), Point(2, 0), Point(0, 2))
        ...  is Location.EXTERIOR)
        True
        """
        return self._circular.point_point_point_locator

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
    def region_signed_area(self) -> _measured.RegionSignedMeasure:
        """
        Returns signed area of the region given its contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (context.region_signed_area(Contour([Point(0, 0), Point(1, 0),
        ...                                      Point(1, 1), Point(0, 1)]))
        ...  == 1)
        True
        >>> (context.region_signed_area(Contour([Point(0, 0), Point(0, 1),
        ...                                      Point(1, 1), Point(1, 0)]))
        ...  == -1)
        True
        """
        return self._measured.region_signed_area

    @property
    def segment_cls(self) -> _Type[_hints.Segment]:
        """Returns type for segments."""
        return self._segment_cls

    @property
    def sqrt(self) -> _SquareRooter:
        """Returns function for computing square root."""
        return self._sqrt

    def box_segment_squared_distance(self,
                                     box: _hints.Box,
                                     segment: _hints.Segment) -> _hints.Scalar:
        """
        Returns squared Euclidean distance between box and a segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box = context.box_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.box_segment_squared_distance(
        ...     Box(0, 1, 0, 1), Segment(Point(0, 0), Point(1, 1))) == 0
        True
        >>> context.box_segment_squared_distance(
        ...     Box(0, 1, 0, 1), Segment(Point(2, 0), Point(2, 1))) == 1
        True
        >>> context.box_segment_squared_distance(
        ...     Box(0, 1, 0, 1), Segment(Point(2, 2), Point(3, 2))) == 2
        True
        """
        return self._metric.box_segment_squared_metric(
                box, segment, self.dot_product, self._segments_intersect,
                self.point_cls)

    def contour_box(self, contour: _hints.Contour) -> _hints.Box:
        """
        Constructs box from contour.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(contour.vertices)``.

        >>> context = get_context()
        >>> Box, Contour, Point = (context.box_cls, context.contour_cls,
        ...                        context.point_cls)
        >>> (context.contour_box(Contour([Point(0, 0), Point(1, 0),
        ...                               Point(1, 1), Point(0, 1)]))
        ...  == Box(0, 1, 0, 1))
        True
        """
        return _boxed.from_contour(contour, self.box_cls)

    def contour_centroid(self, contour: _hints.Contour) -> _hints.Point:
        """
        Constructs centroid of a contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour, Point = context.contour_cls, context.point_cls
        >>> (context.contour_centroid(Contour([Point(0, 0), Point(2, 0),
        ...                                    Point(2, 2), Point(0, 2)]))
        ...  == Point(1, 1))
        True
        """
        return self._centroidal.contour_centroid(contour, self.point_cls,
                                                 self.sqrt)

    def contour_length(self, contour: _hints.Contour) -> _hints.Scalar:
        """
        Returns Euclidean length of a contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.contour_length(Contour([Point(0, 0), Point(3, 0),
        ...                                 Point(0, 4)])) == 12
        True
        >>> context.contour_length(Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(1, 1), Point(0, 1)])) == 4
        True
        """
        points_squared_distance, sqrt = self.points_squared_distance, self.sqrt
        vertices = contour.vertices
        return sum(sqrt(points_squared_distance(vertices[index - 1],
                                                vertices[index]))
                   for index in range(len(vertices)))

    def contour_segments(self, contour: _hints.Contour
                         ) -> _Sequence[_hints.Segment]:
        """
        Constructs segments of a contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.contour_segments(Contour([Point(0, 0), Point(2, 0),
        ...                                    Point(2, 2), Point(0, 2)]))
        ...  == [Segment(Point(0, 2), Point(0, 0)),
        ...      Segment(Point(0, 0), Point(2, 0)),
        ...      Segment(Point(2, 0), Point(2, 2)),
        ...      Segment(Point(2, 2), Point(0, 2))])
        True
        """
        segment_cls, vertices = self.segment_cls, contour.vertices
        return [segment_cls(vertices[index - 1], vertices[index])
                for index in range(len(vertices))]

    def contours_box(self, contours: _Sequence[_hints.Contour]) -> _hints.Box:
        """
        Constructs box from contours.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = sum(len(contour.vertices)\
 for contour in contours)``.

        >>> context = get_context()
        >>> Box = context.box_cls
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (context.contours_box([Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(1, 1), Point(0, 1)]),
        ...                        Contour([Point(1, 1), Point(2, 1),
        ...                                 Point(2, 2), Point(1, 2)])])
        ...  == Box(0, 2, 0, 2))
        True
        """
        return _boxed.from_contours(contours, self.box_cls)

    def is_region_convex(self, contour: _hints.Contour) -> bool:
        """
        Checks if region (given its contour) is convex.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> context.is_region_convex(Contour([Point(0, 0), Point(3, 0),
        ...                                   Point(1, 1), Point(0, 3)]))
        False
        >>> context.is_region_convex(Contour([Point(0, 0), Point(2, 0),
        ...                                   Point(2, 2), Point(0, 2)]))
        True
        """
        vertices = contour.vertices
        vertices_count = len(vertices)
        if vertices_count == 3:
            return True
        orienteer = self.angle_orientation
        base_orientation = orienteer(vertices[-2], vertices[-1], vertices[0])
        # orientation change means that internal angle is greater than 180°
        return all(orienteer(vertices[index - 1], vertices[index],
                             vertices[index + 1]) is base_orientation
                   for index in range(vertices_count - 1))

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
        return self.box_cls(min(first_box.min_x, second_box.min_x),
                            max(first_box.max_x, second_box.max_x),
                            min(first_box.min_y, second_box.min_y),
                            max(first_box.max_y, second_box.max_y))

    def multipoint_centroid(self, multipoint: _hints.Multipoint
                            ) -> _hints.Point:
        """
        Constructs centroid of a multipoint.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> context.multipoint_centroid(
        ...     Multipoint([Point(0, 0), Point(2, 0), Point(2, 2),
        ...                 Point(0, 2)])) == Point(1, 1)
        True
        """
        return self._centroidal.multipoint_centroid(multipoint, self.point_cls)

    def multipolygon_centroid(self, multipolygon: _hints.Multipolygon
                              ) -> _hints.Point:
        """
        Constructs centroid of a multipolygon.

        Time complexity:
            ``O(len(vertices_count))``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in multipolygon.polygons)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> Multipolygon = context.multipolygon_cls
        >>> (context.multipolygon_centroid(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(1, 1), Point(0, 1)]),
        ...                            []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(2, 2), Point(1, 2)]),
        ...                            [])]))
        ...  == Point(1, 1))
        True
        """
        return self._centroidal.multipolygon_centroid(multipolygon,
                                                      self.point_cls)

    def multisegment_centroid(self, multisegment: _hints.Multisegment
                              ) -> _hints.Point:
        """
        Constructs centroid of a multisegment.

        Time complexity:
            ``O(len(multisegment.segments))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> Multisegment = context.multisegment_cls
        >>> (context.multisegment_centroid(
        ...      Multisegment([Segment(Point(0, 0), Point(2, 0)),
        ...                    Segment(Point(2, 0), Point(2, 2)),
        ...                    Segment(Point(0, 2), Point(2, 2)),
        ...                    Segment(Point(0, 0), Point(0, 2))]))
        ...  == Point(1, 1))
        True
        """
        return self._centroidal.multisegment_centroid(
                multisegment, self.point_cls, self.sqrt)

    def multisegment_length(self, multisegment: _hints.Multisegment
                            ) -> _hints.Scalar:
        """
        Returns Euclidean length of a multisegment.

        Time complexity:
            ``O(len(multisegment.segments))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.multisegment_length(
        ...     Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(0, 1))])) == 2
        True
        >>> context.multisegment_length(
        ...     Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(3, 4))])) == 6
        True
        """
        points_squared_distance, sqrt = self.points_squared_distance, self.sqrt
        return sum(sqrt(points_squared_distance(segment.start, segment.end))
                   for segment in multisegment.segments)

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

    def points_box(self, points: _Sequence[_hints.Point]) -> _hints.Box:
        """
        Constructs box from points.

        Time complexity:
            ``O(len(points))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point = context.box_cls, context.point_cls
        >>> (context.points_box([Point(0, 0), Point(2, 0), Point(2, 2),
        ...                      Point(0, 2)])
        ...  == Box(0, 2, 0, 2))
        True
        """
        return _boxed.from_points(points, self.box_cls)

    def polygon_box(self, polygon: _hints.Polygon) -> _hints.Box:
        """
        Constructs box from polygon.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(polygon.border.vertices)``.

        >>> context = get_context()
        >>> Box, Contour, Point, Polygon = (context.box_cls,
        ...                                 context.contour_cls,
        ...                                 context.point_cls,
        ...                                 context.polygon_cls)
        >>> context.polygon_box(
        ...     Polygon(Contour([Point(0, 0), Point(1, 0), Point(1, 1),
        ...                      Point(0, 1)]), [])) == Box(0, 1, 0, 1)
        True
        """
        return _boxed.from_polygon(polygon, self.box_cls)

    def polygon_centroid(self, polygon: _hints.Polygon) -> _hints.Point:
        """
        Constructs centroid of a polygon.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> context.polygon_centroid(
        ...     Polygon(Contour([Point(0, 0), Point(4, 0), Point(4, 4),
        ...                      Point(0, 4)]),
        ...             [Contour([Point(1, 1), Point(1, 3), Point(3, 3),
        ...                       Point(3, 1)])])) == Point(2, 2)
        True
        """
        return self._centroidal.polygon_centroid(polygon, self.point_cls)

    def polygons_box(self, polygons: _Sequence[_hints.Polygon]) -> _hints.Box:
        """
        Constructs box from polygons.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 for polygon in polygons)``.

        >>> context = get_context()
        >>> Box, Contour, Point, Polygon = (context.box_cls,
        ...                                 context.contour_cls,
        ...                                 context.point_cls,
        ...                                 context.polygon_cls)
        >>> context.polygons_box(
        ...     [Polygon(Contour([Point(0, 0), Point(1, 0), Point(1, 1),
        ...                       Point(0, 1)]), []),
        ...      Polygon(Contour([Point(1, 1), Point(2, 1), Point(2, 2),
        ...                       Point(1, 2)]), [])]) == Box(0, 2, 0, 2)
        True
        """
        return _boxed.from_polygons(polygons, self.box_cls)

    def region_centroid(self, contour: _hints.Contour) -> _hints.Point:
        """
        Constructs centroid of a region given its contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (context.region_centroid(Contour([Point(0, 0), Point(2, 0),
        ...                                   Point(2, 2), Point(0, 2)]))
        ...  == Point(1, 1))
        True
        """
        return self._centroidal.region_centroid(contour, self.point_cls)

    def replace(self,
                *,
                box_cls: _Optional[_Type[_hints.Box]] = None,
                contour_cls: _Optional[_Type[_hints.Contour]] = None,
                empty_cls: _Optional[_Type[_hints.Empty]] = None,
                mix_cls: _Optional[_Type[_hints.Mix]] = None,
                multipoint_cls: _Optional[_Type[_hints.Multipoint]] = None,
                multipolygon_cls: _Optional[_Type[_hints.Multipolygon]] = None,
                multisegment_cls: _Optional[_Type[_hints.Multisegment]] = None,
                point_cls: _Optional[_Type[_hints.Point]] = None,
                polygon_cls: _Optional[_Type[_hints.Polygon]] = None,
                segment_cls: _Optional[_Type[_hints.Segment]] = None,
                mode: _Optional[Mode] = None,
                sqrt: _Optional[_SquareRooter] = None) -> 'Context':
        """
        Constructs context from the original one replacing given parameters.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> robust_context = context.replace(mode=Mode.ROBUST)
        >>> isinstance(robust_context, Context)
        True
        >>> robust_context.mode is Mode.ROBUST
        True
        """
        return Context(box_cls=self.box_cls if box_cls is None else box_cls,
                       contour_cls=(self.contour_cls
                                    if contour_cls is None
                                    else contour_cls),
                       empty_cls=(self.empty_cls
                                  if empty_cls is None
                                  else empty_cls),
                       mix_cls=self.mix_cls if mix_cls is None else mix_cls,
                       multipoint_cls=(self.multipoint_cls
                                       if multipoint_cls is None
                                       else multipoint_cls),
                       multipolygon_cls=(self.multipolygon_cls
                                         if multipolygon_cls is None
                                         else multipolygon_cls),
                       multisegment_cls=(self.multisegment_cls
                                         if multisegment_cls is None
                                         else multisegment_cls),
                       point_cls=(self.point_cls
                                  if point_cls is None
                                  else point_cls),
                       polygon_cls=(self.polygon_cls
                                    if polygon_cls is None
                                    else polygon_cls),
                       segment_cls=(self.segment_cls
                                    if segment_cls is None
                                    else segment_cls),
                       mode=self.mode if mode is None else mode,
                       sqrt=self.sqrt if sqrt is None else sqrt)

    def rotate_contour(self,
                       contour: _hints.Contour,
                       cosine: _hints.Scalar,
                       sine: _hints.Scalar,
                       center: _hints.Point) -> _hints.Contour:
        """
        Returns contour rotated by given angle around given center.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (context.rotate_contour(
        ...      Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 0,
        ...      Point(0, 1))
        ...  == Contour([Point(0, 0), Point(1, 0), Point(0, 1)]))
        True
        >>> (context.rotate_contour(
        ...      Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 1,
        ...      Point(0, 1))
        ...  == Contour([Point(1, 1), Point(1, 2), Point(0, 1)]))
        True
        """
        return self._rotation.rotate_translate_contour(
                contour, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.contour_cls, self.point_cls)

    def rotate_contour_around_origin(self,
                                     contour: _hints.Contour,
                                     cosine: _hints.Scalar,
                                     sine: _hints.Scalar) -> _hints.Contour:
        """
        Returns contour rotated by given angle around origin.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (context.rotate_contour_around_origin(
        ...      Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 0)
        ...  == Contour([Point(0, 0), Point(1, 0), Point(0, 1)]))
        True
        >>> (context.rotate_contour_around_origin(
        ...      Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 1)
        ...  == Contour([Point(0, 0), Point(0, 1), Point(-1, 0)]))
        True
        """
        return self._rotation.rotate_contour_around_origin(
                contour, cosine, sine, self.contour_cls, self.point_cls)

    def rotate_multipoint(self,
                          multipoint: _hints.Multipoint,
                          cosine: _hints.Scalar,
                          sine: _hints.Scalar,
                          center: _hints.Point) -> _hints.Multipoint:
        """
        Returns multipoint rotated by given angle around given center.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (context.rotate_multipoint(Multipoint([Point(0, 0), Point(1, 0)]),
        ...                            1, 0, Point(0, 1))
        ...  == Multipoint([Point(0, 0), Point(1, 0)]))
        True
        >>> (context.rotate_multipoint(Multipoint([Point(0, 0), Point(1, 0)]),
        ...                            0, 1, Point(0, 1))
        ...  == Multipoint([Point(1, 1), Point(1, 2)]))
        True
        """
        return self._rotation.rotate_translate_multipoint(
                multipoint, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.multipoint_cls, self.point_cls)

    def rotate_multipoint_around_origin(self,
                                        multipoint: _hints.Multipoint,
                                        cosine: _hints.Scalar,
                                        sine: _hints.Scalar
                                        ) -> _hints.Multipoint:
        """
        Returns multipoint rotated by given angle around origin.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (context.rotate_multipoint_around_origin(
        ...      Multipoint([Point(0, 0), Point(1, 0)]), 1, 0)
        ...  == Multipoint([Point(0, 0), Point(1, 0)]))
        True
        >>> (context.rotate_multipoint_around_origin(
        ...      Multipoint([Point(0, 0), Point(1, 0)]), 0, 1)
        ...  == Multipoint([Point(0, 0), Point(0, 1)]))
        True
        """
        return self._rotation.rotate_multipoint_around_origin(
                multipoint, cosine, sine, self.multipoint_cls, self.point_cls)

    def rotate_multipolygon(self,
                            multipolygon: _hints.Multipolygon,
                            cosine: _hints.Scalar,
                            sine: _hints.Scalar,
                            center: _hints.Point) -> _hints.Multipolygon:
        """
        Returns multipolygon rotated by given angle around given center.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in multipolygon.polygons)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipolygon = context.multipolygon_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.rotate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), [])]),
        ...      1, 0, Point(0, 1))
        ...  == Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                    Point(0, 1)]), [])]))
        True
        >>> (context.rotate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), [])]),
        ...      0, 1, Point(0, 1))
        ...  == Multipolygon([Polygon(Contour([Point(1, 1), Point(1, 2),
        ...                                    Point(0, 1)]), [])]))
        True
        """
        return self._rotation.rotate_translate_multipolygon(
                multipolygon, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.contour_cls, self.multipolygon_cls, self.point_cls,
                self.polygon_cls)

    def rotate_multipolygon_around_origin(self,
                                          multipolygon: _hints.Multipolygon,
                                          cosine: _hints.Scalar,
                                          sine: _hints.Scalar
                                          ) -> _hints.Multipolygon:
        """
        Returns multipolygon rotated by given angle around origin.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in multipolygon.polygons)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipolygon = context.multipolygon_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.rotate_multipolygon_around_origin(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), [])]),
        ...      1, 0)
        ...  == Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                    Point(0, 1)]), [])]))
        True
        >>> (context.rotate_multipolygon_around_origin(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), [])]),
        ...      0, 1)
        ...  == Multipolygon([Polygon(Contour([Point(0, 0), Point(0, 1),
        ...                                    Point(-1, 0)]), [])]))
        True
        """
        return self._rotation.rotate_multipolygon_around_origin(
                multipolygon, cosine, sine, self.contour_cls,
                self.multipolygon_cls, self.point_cls, self.polygon_cls)

    def rotate_multisegment(self,
                            multisegment: _hints.Multisegment,
                            cosine: _hints.Scalar,
                            sine: _hints.Scalar,
                            center: _hints.Point) -> _hints.Multisegment:
        """
        Returns multisegment rotated by given angle around given center.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.rotate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 0,
        ...      Point(0, 1))
        ...  == Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(0, 1))]))
        True
        >>> (context.rotate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 1,
        ...      Point(0, 1))
        ...  == Multisegment([Segment(Point(1, 1), Point(1,2)),
        ...                   Segment(Point(1, 1), Point(0, 1))]))
        True
        """
        return self._rotation.rotate_translate_multisegment(
                multisegment, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.multisegment_cls, self.point_cls, self.segment_cls)

    def rotate_multisegment_around_origin(self,
                                          multisegment: _hints.Multisegment,
                                          cosine: _hints.Scalar,
                                          sine: _hints.Scalar
                                          ) -> _hints.Multisegment:
        """
        Returns multisegment rotated by given angle around origin.

        Time complexity:
            ``O(len(multisegment.segments))``
        Memory complexity:
            ``O(len(multisegment.segments))``

        >>> context = get_context()
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.rotate_multisegment_around_origin(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 0)
        ...  == Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(0, 1))]))
        True
        >>> (context.rotate_multisegment_around_origin(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 1)
        ...  == Multisegment([Segment(Point(0, 0), Point(0, 1)),
        ...                   Segment(Point(0, 0), Point(-1, 0))]))
        True
        """
        return self._rotation.rotate_multisegment_around_origin(
                multisegment, cosine, sine, self.multisegment_cls,
                self.point_cls, self.segment_cls)

    def rotate_point(self,
                     point: _hints.Point,
                     cosine: _hints.Scalar,
                     sine: _hints.Scalar,
                     center: _hints.Point) -> _hints.Point:
        """
        Returns point rotated by given angle around given center.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.rotate_point(Point(1, 0), 1, 0, Point(0, 1)) == Point(1, 0)
        True
        >>> context.rotate_point(Point(1, 0), 0, 1, Point(0, 1)) == Point(1, 2)
        True
        """
        return self._rotation.rotate_translate_point(
                point, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.point_cls)

    def rotate_point_around_origin(self,
                                   point: _hints.Point,
                                   cosine: _hints.Scalar,
                                   sine: _hints.Scalar) -> _hints.Point:
        """
        Returns point rotated by given angle around origin.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (context.rotate_point_around_origin(Point(1, 0), 1, 0)
        ...  == Point(1, 0))
        True
        >>> (context.rotate_point_around_origin(Point(1, 0), 0, 1)
        ...  == Point(0, 1))
        True
        """
        return self._rotation.rotate_point_around_origin(point, cosine, sine,
                                                         self.point_cls)

    def rotate_polygon(self,
                       polygon: _hints.Polygon,
                       cosine: _hints.Scalar,
                       sine: _hints.Scalar,
                       center: _hints.Point) -> _hints.Polygon:
        """
        Returns polygon rotated by given angle around given center.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.rotate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 0, Point(0, 1))
        ...  == Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []))
        True
        >>> (context.rotate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 1, Point(0, 1))
        ...  == Polygon(Contour([Point(1, 1), Point(1, 2), Point(0, 1)]), []))
        True
        """
        return self._rotation.rotate_translate_polygon(
                polygon, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.contour_cls, self.point_cls, self.polygon_cls)

    def rotate_polygon_around_origin(self,
                                     polygon: _hints.Polygon,
                                     cosine: _hints.Scalar,
                                     sine: _hints.Scalar) -> _hints.Polygon:
        """
        Returns polygon rotated by given angle around origin.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.rotate_polygon_around_origin(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 0)
        ...  == Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []))
        True
        >>> (context.rotate_polygon_around_origin(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 1)
        ...  == Polygon(Contour([Point(0, 0), Point(0, 1), Point(-1, 0)]), []))
        True
        """
        return self._rotation.rotate_polygon_around_origin(
                polygon, cosine, sine, self.contour_cls, self.point_cls,
                self.polygon_cls)

    def rotate_segment(self,
                       segment: _hints.Segment,
                       cosine: _hints.Scalar,
                       sine: _hints.Scalar,
                       center: _hints.Point) -> _hints.Segment:
        """
        Returns segment rotated by given angle around given center.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.rotate_segment(Segment(Point(0, 0), Point(1, 0)), 1, 0,
        ...                         Point(0, 1))
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.rotate_segment(Segment(Point(0, 0), Point(1, 0)), 0, 1,
        ...                         Point(0, 1))
        ...  == Segment(Point(1, 1), Point(1, 2)))
        True
        """
        return self._rotation.rotate_translate_segment(
                segment, cosine, sine,
                *self._rotation.point_to_step(center, cosine, sine),
                self.point_cls, self.segment_cls)

    def rotate_segment_around_origin(self,
                                     segment: _hints.Segment,
                                     cosine: _hints.Scalar,
                                     sine: _hints.Scalar) -> _hints.Segment:
        """
        Returns segment rotated by given angle around origin.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.rotate_segment_around_origin(
        ...      Segment(Point(0, 0), Point(1, 0)), 1, 0)
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.rotate_segment_around_origin(
        ...      Segment(Point(0, 0), Point(1, 0)), 0, 1)
        ...  == Segment(Point(0, 0), Point(0, 1)))
        True
        """
        return self._rotation.rotate_segment_around_origin(
                segment, cosine, sine, self.point_cls, self.segment_cls)

    def scale_contour(self,
                      contour: _hints.Contour,
                      factor_x: _hints.Scalar,
                      factor_y: _hints.Scalar
                      ) -> _Union[_hints.Contour, _hints.Multipoint,
                                  _hints.Segment]:
        """
        Returns contour scaled by given factor.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.scale_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(0, 1)]), 0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(0, 1)]), 1, 0)
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.scale_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(0, 1)]), 0, 1)
        ...  == Segment(Point(0, 0), Point(0, 1)))
        True
        >>> (context.scale_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                 Point(0, 1)]), 1, 1)
        ...  == Contour([Point(0, 0), Point(1, 0), Point(0, 1)]))
        True
        """
        return self._scaling.scale_contour(
                contour, factor_x, factor_y, self.contour_cls,
                self.multipoint_cls, self.point_cls, self.segment_cls)

    def scale_multipoint(self,
                         multipoint: _hints.Multipoint,
                         factor_x: _hints.Scalar,
                         factor_y: _hints.Scalar) -> _hints.Multipoint:
        """
        Returns multipoint scaled by given factor.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (context.scale_multipoint(Multipoint([Point(0, 0), Point(1, 1)]),
        ...                           0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_multipoint(Multipoint([Point(0, 0), Point(1, 1)]),
        ...                           1, 0)
        ...  == Multipoint([Point(0, 0), Point(1, 0)]))
        True
        >>> (context.scale_multipoint(Multipoint([Point(0, 0), Point(1, 1)]),
        ...                           0, 1)
        ...  == Multipoint([Point(0, 0), Point(0, 1)]))
        True
        >>> (context.scale_multipoint(Multipoint([Point(0, 0), Point(1, 1)]),
        ...                           1, 1)
        ...  == Multipoint([Point(0, 0), Point(1, 1)]))
        True
        """
        return self._scaling.scale_multipoint(multipoint, factor_x, factor_y,
                                              self.multipoint_cls,
                                              self.point_cls)

    def scale_multipolygon(self,
                           multipolygon: _hints.Multipolygon,
                           factor_x: _hints.Scalar,
                           factor_y: _hints.Scalar
                           ) -> _Union[_hints.Multipoint, _hints.Multipolygon,
                                       _hints.Multisegment]:
        """
        Returns multipolygon scaled by given factor.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in multipolygon.polygons)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipoint = context.multipoint_cls
        >>> Multipolygon = context.multipolygon_cls
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> Segment = context.segment_cls
        >>> (context.scale_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 1, 0)
        ...  == Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(1, 0), Point(2, 0))]))
        True
        >>> (context.scale_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 0, 1)
        ...  == Multisegment([Segment(Point(0, 0), Point(0, 1)),
        ...                   Segment(Point(0, 1), Point(0, 2))]))
        True
        >>> (context.scale_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 1, 1)
        ...  == Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                    Point(0, 1)]), []),
        ...                   Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                    Point(1, 2)]), [])]))
        True
        """
        return self._scaling.scale_multipolygon(
                multipolygon, factor_x, factor_y, self.contour_cls,
                self.multipoint_cls, self.multipolygon_cls,
                self.multisegment_cls, self.point_cls, self.polygon_cls,
                self.segment_cls)

    def scale_multisegment(self,
                           multisegment: _hints.Multisegment,
                           factor_x: _hints.Scalar,
                           factor_y: _hints.Scalar
                           ) -> _Union[_hints.Mix, _hints.Multipoint,
                                       _hints.Multisegment]:
        """
        Returns multisegment scaled by given factor.

        Time complexity:
            ``O(len(multisegment.segments))``
        Memory complexity:
            ``O(len(multisegment.segments))``

        >>> context = get_context()
        >>> EMPTY = context.empty
        >>> Mix = context.mix_cls
        >>> Multipoint = context.multipoint_cls
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.scale_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 0)
        ...  == Mix(Multipoint([Point(0, 0)]),
        ...         Segment(Point(0, 0), Point(1, 0)), EMPTY))
        True
        >>> (context.scale_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 1)
        ...  == Mix(Multipoint([Point(0, 0)]),
        ...         Segment(Point(0, 0), Point(0, 1)), EMPTY))
        True
        >>> (context.scale_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 1)
        ...  == Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(0, 1))]))
        True
        """
        return self._scaling.scale_multisegment(
                multisegment, factor_x, factor_y, self.empty, self.mix_cls,
                self.multipoint_cls, self.multisegment_cls, self.point_cls,
                self.segment_cls)

    def scale_point(self,
                    point: _hints.Point,
                    factor_x: _hints.Scalar,
                    factor_y: _hints.Scalar) -> _hints.Point:
        """
        Returns point scaled by given factor.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.scale_point(Point(1, 1), 0, 0) == Point(0, 0)
        True
        >>> context.scale_point(Point(1, 1), 1, 0) == Point(1, 0)
        True
        >>> context.scale_point(Point(1, 1), 0, 1) == Point(0, 1)
        True
        >>> context.scale_point(Point(1, 1), 1, 1) == Point(1, 1)
        True
        """
        return self._scaling.scale_point(point, factor_x, factor_y,
                                         self.point_cls)

    def scale_polygon(self,
                      polygon: _hints.Polygon,
                      factor_x: _hints.Scalar,
                      factor_y: _hints.Scalar
                      ) -> _Union[_hints.Multipoint, _hints.Polygon,
                                  _hints.Segment]:
        """
        Returns polygon scaled by given factor.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> Segment = context.segment_cls
        >>> (context.scale_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 0)
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.scale_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 1)
        ...  == Segment(Point(0, 0), Point(0, 1)))
        True
        >>> (context.scale_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 1)
        ...  == Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []))
        True
        """
        return self._scaling.scale_polygon(
                polygon, factor_x, factor_y, self.contour_cls,
                self.multipoint_cls, self.point_cls, self.polygon_cls,
                self.segment_cls)

    def scale_segment(self,
                      segment: _hints.Segment,
                      factor_x: _hints.Scalar,
                      factor_y: _hints.Scalar
                      ) -> _Union[_hints.Multipoint, _hints.Segment]:
        """
        Returns segment scaled by given factor.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 0, 0)
        ...  == Multipoint([Point(0, 0)]))
        True
        >>> (context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 1, 0)
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 0, 1)
        ...  == Segment(Point(0, 0), Point(0, 1)))
        True
        >>> (context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 1, 1)
        ...  == Segment(Point(0, 0), Point(1, 1)))
        True
        """
        return self._scaling.scale_segment(
                segment, factor_x, factor_y, self.multipoint_cls,
                self.point_cls, self.segment_cls)

    def segment_box(self, segment: _hints.Segment) -> _hints.Box:
        """
        Constructs box from segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point, Segment = (context.box_cls, context.point_cls,
        ...                        context.segment_cls)
        >>> (context.segment_box(Segment(Point(0, 1), Point(2, 3)))
        ...  == Box(0, 2, 1, 3))
        True
        """
        return _boxed.from_segment(segment, self.box_cls)

    def segment_centroid(self, segment: _hints.Segment) -> _hints.Point:
        """
        Constructs centroid of a segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point, Segment = context.point_cls, context.segment_cls
        >>> (context.segment_centroid(Segment(Point(0, 1), Point(2, 3)))
        ...  == Point(1, 2))
        True
        """
        return self._centroidal.segment_centroid(segment, self.point_cls)

    def segment_contains_point(self,
                               segment: _hints.Segment,
                               point: _hints.Point) -> bool:
        """
        Checks if a segment contains given point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(0, 0))
        True
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(0, 2))
        False
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(1, 0))
        True
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(1, 1))
        False
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(2, 0))
        True
        >>> context.segment_contains_point(Segment(Point(0, 0), Point(2, 0)),
        ...                                Point(3, 0))
        False
        """
        return self._segment.containment_checker(segment.start, segment.end,
                                                 point, self.angle_orientation)

    def segment_length(self, segment: _hints.Segment) -> _hints.Scalar:
        """
        Returns Euclidean length of a segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.segment_length(Segment(Point(0, 0), Point(1, 0))) == 1
        True
        >>> context.segment_length(Segment(Point(0, 0), Point(0, 1))) == 1
        True
        >>> context.segment_length(Segment(Point(0, 0), Point(3, 4))) == 5
        True
        """
        return self.sqrt(self.points_squared_distance(segment.start,
                                                      segment.end))

    def segment_point_squared_distance(self,
                                       segment: _hints.Segment,
                                       point: _hints.Point) -> _hints.Scalar:
        """
        Returns squared Euclidean distance between segment and a point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.segment_point_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)), Point(0, 0)) == 0
        True
        >>> context.segment_point_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)), Point(0, 1)) == 1
        True
        >>> context.segment_point_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)), Point(2, 1)) == 2
        True
        """
        return self._metric.segment_point_squared_metric(
                segment.start, segment.end, point, self.dot_product)

    def segments_box(self, segments: _Sequence[_hints.Segment]) -> _hints.Box:
        """
        Constructs box from segments.

        Time complexity:
            ``O(len(segments))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point, Segment = (context.box_cls, context.point_cls,
        ...                        context.segment_cls)
        >>> (context.segments_box([Segment(Point(0, 0), Point(1, 1)),
        ...                        Segment(Point(1, 1), Point(2, 2))])
        ...  == Box(0, 2, 0, 2))
        True
        """
        return _boxed.from_segments(segments, self.box_cls)

    def segments_intersection(self,
                              first: _hints.Segment,
                              second: _hints.Segment) -> _hints.Point:
        """
        Returns intersection point of two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.segments_intersection(Segment(Point(0, 0), Point(2, 0)),
        ...                                Segment(Point(0, 0), Point(0, 1)))
        ...  == Point(0, 0))
        True
        >>> (context.segments_intersection(Segment(Point(0, 0), Point(2, 0)),
        ...                                Segment(Point(1, 0), Point(1, 1)))
        ...  == Point(1, 0))
        True
        >>> (context.segments_intersection(Segment(Point(0, 0), Point(2, 0)),
        ...                                Segment(Point(2, 0), Point(3, 0)))
        ...  == Point(2, 0))
        True
        """
        return self._segment.intersector(first.start, first.end, second.start,
                                         second.end, self.point_cls,
                                         self._segment_contains_point)

    def segments_relation(self,
                          test: _hints.Segment,
                          goal: _hints.Segment) -> Relation:
        """
        Returns relation between two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(1, 0), Point(2, 0)))
        ...  is Relation.DISJOINT)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(0, 0), Point(2, 0)))
        ...  is Relation.TOUCH)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(2, 0), Point(0, 2)))
        ...  is Relation.CROSS)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                           Segment(Point(0, 0), Point(1, 1)))
        ...  is Relation.COMPOSITE)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(0, 0), Point(2, 2)))
        ...  is Relation.EQUAL)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(0, 0), Point(3, 3)))
        ...  is Relation.COMPONENT)
        True
        >>> (context.segments_relation(Segment(Point(0, 0), Point(2, 2)),
        ...                            Segment(Point(1, 1), Point(3, 3)))
        ...  is Relation.OVERLAP)
        True
        """
        return self._segment.relater(test.start, test.end, goal.start,
                                     goal.end, self.angle_orientation)

    def segments_squared_distance(self,
                                  first: _hints.Segment,
                                  second: _hints.Segment) -> _hints.Scalar:
        """
        Returns squared Euclidean distance between two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.segments_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)),
        ...     Segment(Point(0, 0), Point(0, 1))) == 0
        True
        >>> context.segments_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)),
        ...     Segment(Point(0, 1), Point(1, 1))) == 1
        True
        >>> context.segments_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)),
        ...     Segment(Point(2, 1), Point(2, 2))) == 2
        True
        """
        return self._metric.segment_segment_squared_metric(
                first.start, first.end, second.start, second.end,
                self.dot_product, self._segments_intersect)

    def translate_contour(self,
                          contour: _hints.Contour,
                          step_x: _hints.Scalar,
                          step_y: _hints.Scalar) -> _hints.Contour:
        """
        Returns contour translated by given step.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.translate_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), 0, 0)
        ...  == Contour([Point(0, 0), Point(1, 0), Point(0, 1)]))
        True
        >>> (context.translate_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), 1, 0)
        ...  == Contour([Point(1, 0), Point(2, 0), Point(1, 1)]))
        True
        >>> (context.translate_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), 0, 1)
        ...  == Contour([Point(0, 1), Point(1, 1), Point(0, 2)]))
        True
        >>> (context.translate_contour(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), 1, 1)
        ...  == Contour([Point(1, 1), Point(2, 1), Point(1, 2)]))
        True
        """
        return self._translation.translate_contour(
                contour, step_x, step_y, self.contour_cls, self.point_cls)

    def translate_multipoint(self,
                             multipoint: _hints.Multipoint,
                             step_x: _hints.Scalar,
                             step_y: _hints.Scalar) -> _hints.Multipoint:
        """
        Returns multipoint translated by given step.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (context.translate_multipoint(Multipoint([Point(0, 0),
        ...                                           Point(1, 0)]), 0, 0)
        ...  == Multipoint([Point(0, 0), Point(1, 0)]))
        True
        >>> (context.translate_multipoint(Multipoint([Point(0, 0),
        ...                                           Point(1, 0)]), 1, 0)
        ...  == Multipoint([Point(1, 0), Point(2, 0)]))
        True
        >>> (context.translate_multipoint(Multipoint([Point(0, 0),
        ...                                           Point(1, 0)]), 0, 1)
        ...  == Multipoint([Point(0, 1), Point(1, 1)]))
        True
        >>> (context.translate_multipoint(Multipoint([Point(0, 0),
        ...                                           Point(1, 0)]), 1, 1)
        ...  == Multipoint([Point(1, 1), Point(2, 1)]))
        True
        """
        return self._translation.translate_multipoint(
                multipoint, step_x, step_y, self.multipoint_cls,
                self.point_cls)

    def translate_multipolygon(self,
                               multipolygon: _hints.Multipolygon,
                               step_x: _hints.Scalar,
                               step_y: _hints.Scalar) -> _hints.Multipolygon:
        """
        Returns multipolygon translated by given step.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = sum(len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)\
 for polygon in multipolygon.polygons)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Multipolygon = context.multipolygon_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.translate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 0, 0)
        ...  == Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                    Point(0, 1)]), []),
        ...                   Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                    Point(1, 2)]), [])]))
        True
        >>> (context.translate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 1, 0)
        ...  == Multipolygon([Polygon(Contour([Point(1, 0), Point(2, 0),
        ...                                    Point(1, 1)]), []),
        ...                   Polygon(Contour([Point(2, 1), Point(3, 1),
        ...                                    Point(2, 2)]), [])]))
        True
        >>> (context.translate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 0, 1)
        ...  == Multipolygon([Polygon(Contour([Point(0, 1), Point(1, 1),
        ...                                    Point(0, 2)]), []),
        ...                   Polygon(Contour([Point(1, 2), Point(2, 2),
        ...                                    Point(1, 3)]), [])]))
        True
        >>> (context.translate_multipolygon(
        ...      Multipolygon([Polygon(Contour([Point(0, 0), Point(1, 0),
        ...                                     Point(0, 1)]), []),
        ...                    Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                     Point(1, 2)]), [])]), 1, 1)
        ...  == Multipolygon([Polygon(Contour([Point(1, 1), Point(2, 1),
        ...                                    Point(1, 2)]), []),
        ...                   Polygon(Contour([Point(2, 2), Point(3, 2),
        ...                                    Point(2, 3)]), [])]))
        True
        """
        return self._translation.translate_multipolygon(
                multipolygon, step_x, step_y, self.contour_cls,
                self.multipolygon_cls, self.point_cls, self.polygon_cls)

    def translate_multisegment(self,
                               multisegment: _hints.Multisegment,
                               step_x: _hints.Scalar,
                               step_y: _hints.Scalar) -> _hints.Multisegment:
        """
        Returns multisegment translated by given step.

        Time complexity:
            ``O(len(multisegment.segments))``
        Memory complexity:
            ``O(len(multisegment.segments))``

        >>> context = get_context()
        >>> Multisegment = context.multisegment_cls
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.translate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 0)
        ...  == Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                   Segment(Point(0, 0), Point(0, 1))]))
        True
        >>> (context.translate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 0)
        ...  == Multisegment([Segment(Point(1, 0), Point(2, 0)),
        ...                   Segment(Point(1, 0), Point(1, 1))]))
        True
        >>> (context.translate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 0, 1)
        ...  == Multisegment([Segment(Point(0, 1), Point(1, 1)),
        ...                   Segment(Point(0, 1), Point(0, 2))]))
        True
        >>> (context.translate_multisegment(
        ...      Multisegment([Segment(Point(0, 0), Point(1, 0)),
        ...                    Segment(Point(0, 0), Point(0, 1))]), 1, 1)
        ...  == Multisegment([Segment(Point(1, 1), Point(2, 1)),
        ...                   Segment(Point(1, 1), Point(1, 2))]))
        True
        """
        return self._translation.translate_multisegment(
                multisegment, step_x, step_y, self.multisegment_cls,
                self.point_cls, self.segment_cls)

    def translate_point(self,
                        point: _hints.Point,
                        step_x: _hints.Scalar,
                        step_y: _hints.Scalar) -> _hints.Point:
        """
        Returns point translated by given step.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.translate_point(Point(0, 0), 0, 0) == Point(0, 0)
        True
        >>> context.translate_point(Point(0, 0), 1, 0) == Point(1, 0)
        True
        >>> context.translate_point(Point(0, 0), 0, 1) == Point(0, 1)
        True
        >>> context.translate_point(Point(0, 0), 1, 1) == Point(1, 1)
        True
        """
        return self._translation.translate_point(point, step_x, step_y,
                                                 self.point_cls)

    def translate_polygon(self,
                          polygon: _hints.Polygon,
                          step_x: _hints.Scalar,
                          step_y: _hints.Scalar) -> _hints.Polygon:
        """
        Returns polygon translated by given step.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(vertices_count)``

        where ``vertices_count = len(polygon.border.vertices)\
 + sum(len(hole.vertices) for hole in polygon.holes)``.

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> Polygon = context.polygon_cls
        >>> (context.translate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 0)
        ...  == Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []))
        True
        >>> (context.translate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 0)
        ...  == Polygon(Contour([Point(1, 0), Point(2, 0), Point(1, 1)]), []))
        True
        >>> (context.translate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      0, 1)
        ...  == Polygon(Contour([Point(0, 1), Point(1, 1), Point(0, 2)]), []))
        True
        >>> (context.translate_polygon(
        ...      Polygon(Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), []),
        ...      1, 1)
        ...  == Polygon(Contour([Point(1, 1), Point(2, 1), Point(1, 2)]), []))
        True
        """
        return self._translation.translate_polygon(
                polygon, step_x, step_y, self.contour_cls, self.point_cls,
                self.polygon_cls)

    def translate_segment(self,
                          segment: _hints.Segment,
                          step_x: _hints.Scalar,
                          step_y: _hints.Scalar) -> _hints.Segment:
        """
        Returns segment translated by given step.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (context.translate_segment(Segment(Point(0, 0), Point(1, 0)), 0, 0)
        ...  == Segment(Point(0, 0), Point(1, 0)))
        True
        >>> (context.translate_segment(Segment(Point(0, 0), Point(1, 0)), 1, 0)
        ...  == Segment(Point(1, 0), Point(2, 0)))
        True
        >>> (context.translate_segment(Segment(Point(0, 0), Point(1, 0)), 0, 1)
        ...  == Segment(Point(0, 1), Point(1, 1)))
        True
        >>> (context.translate_segment(Segment(Point(0, 0), Point(1, 0)), 1, 1)
        ...  == Segment(Point(1, 1), Point(2, 1)))
        True
        """
        return self._translation.translate_segment(
                segment, step_x, step_y, self.point_cls, self.segment_cls)

    def _segment_contains_point(self,
                                start: _hints.Point,
                                end: _hints.Point,
                                point: _hints.Point) -> bool:
        return self._segment.containment_checker(start, end, point,
                                                 self.angle_orientation)

    def _segments_intersect(self,
                            first_start: _hints.Point,
                            first_end: _hints.Point,
                            second_start: _hints.Point,
                            second_end: _hints.Point) -> bool:
        return self._segment.collision_detector(first_start, first_end,
                                                second_start, second_end,
                                                self.angle_orientation)


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
