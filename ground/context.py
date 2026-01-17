from __future__ import annotations

import math as _math
from collections.abc import Callable as _Callable, Sequence as _Sequence
from contextvars import ContextVar as _ContextVar
from typing import Any as _Any, Generic as _Generic, final as _final

from reprit import serializers as _serializers
from reprit.base import generate_repr as _generate_repr
from typing_extensions import Self as _Self

from ._core import (
    angular as _angular,
    boxed as _boxed,
    centroidal as _centroidal,
    circular as _circular,
    discrete as _discrete,
    geometries as _geometries,
    measured as _measured,
    metric as _metric,
    rotation as _rotation,
    scaling as _scaling,
    segment as _segment,
    translation as _translation,
    vector as _vector,
)
from ._core.enums import (
    Kind as _Kind,
    Location as _Location,
    Orientation as _Orientation,
    Relation as _Relation,
)
from ._core.hints import (
    HasRepr as _HasRepr,
    QuaternaryPointFunction as _QuaternaryPointFunction,
    ScalarFactory as _ScalarFactory,
    ScalarT as _ScalarT,
    SquareRooter as _SquareRooter,
)
from .hints import (
    Box as _Box,
    Contour as _Contour,
    Empty as _Empty,
    Linear as _Linear,
    Mix as _Mix,
    Multipoint as _Multipoint,
    Multipolygon as _Multipolygon,
    Multisegment as _Multisegment,
    Point as _Point,
    Polygon as _Polygon,
    Segment as _Segment,
    Shaped as _Shaped,
)


@_final
class Context(_HasRepr, _Generic[_ScalarT]):
    """Represents common language for computational geometry."""

    @property
    def box_cls(self, /) -> type[_Box[_ScalarT]]:
        """Returns type of boxes."""
        return self._box_cls

    @property
    def contour_cls(self, /) -> type[_Contour[_ScalarT]]:
        """Returns type of contours."""
        return self._contour_cls

    @property
    def coordinate_factory(self, /) -> _Callable[[int], _ScalarT]:
        """Returns coordinate factory."""
        return self._coordinate_factory

    @property
    def cross_product(self, /) -> _QuaternaryPointFunction[_ScalarT, _ScalarT]:
        """
        Returns cross product of the segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.cross_product(
        ...     Point(0, 0), Point(0, 1), Point(0, 0), Point(1, 0)
        ... ) == -1
        True
        >>> context.cross_product(
        ...     Point(0, 0), Point(1, 0), Point(0, 0), Point(1, 0)
        ... ) == 0
        True
        >>> context.cross_product(
        ...     Point(0, 0), Point(1, 0), Point(0, 0), Point(0, 1)
        ... ) == 1
        True
        """
        return self._vector_context.cross_product

    @property
    def dot_product(self, /) -> _QuaternaryPointFunction[_ScalarT, _ScalarT]:
        """
        Returns dot product of the segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> context.dot_product(
        ...     Point(0, 0), Point(1, 0), Point(0, 0), Point(-1, 0)
        ... ) == -1
        True
        >>> context.dot_product(
        ...     Point(0, 0), Point(1, 0), Point(0, 0), Point(0, 1)
        ... ) == 0
        True
        >>> context.dot_product(
        ...     Point(0, 0), Point(1, 0), Point(0, 0), Point(1, 0)
        ... ) == 1
        True
        """
        return self._vector_context.dot_product

    @property
    def empty(self, /) -> _Empty[_ScalarT]:
        """Returns an empty geometry."""
        return self._empty

    @property
    def empty_cls(self, /) -> type[_Empty[_ScalarT]]:
        """Returns type of empty geometries."""
        return self._empty_cls

    @property
    def mix_cls(self, /) -> type[_Mix[_ScalarT]]:
        """Returns type of mixes."""
        return self._mix_cls

    @property
    def multipoint_cls(self, /) -> type[_Multipoint[_ScalarT]]:
        """Returns type of multipoints."""
        return self._multipoint_cls

    @property
    def multipolygon_cls(self, /) -> type[_Multipolygon[_ScalarT]]:
        """Returns type of multipolygons."""
        return self._multipolygon_cls

    @property
    def multisegment_cls(self, /) -> type[_Multisegment[_ScalarT]]:
        """Returns type of multisegments."""
        return self._multisegment_cls

    @property
    def origin(self, /) -> _Point[_ScalarT]:
        """Returns origin."""
        return self._origin

    @property
    def point_cls(self, /) -> type[_Point[_ScalarT]]:
        """Returns type of points."""
        return self._point_cls

    @property
    def points_squared_distance(self, /) -> _metric.PointPointMetric[_ScalarT]:
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
        return self._metric_context.point_point_squared_metric

    @property
    def polygon_cls(self, /) -> type[_Polygon[_ScalarT]]:
        """Returns type of polygons."""
        return self._polygon_cls

    @property
    def segment_cls(self, /) -> type[_Segment[_ScalarT]]:
        """Returns type of segments."""
        return self._segment_cls

    @property
    def sqrt(self, /) -> _SquareRooter[_ScalarT]:
        """Returns function for computing square root."""
        return self._sqrt

    @property
    def zero(self, /) -> _ScalarT:
        """Returns zero."""
        return self._zero

    def angle_kind(
        self,
        vertex: _Point[_ScalarT],
        first_ray_point: _Point[_ScalarT],
        second_ray_point: _Point[_ScalarT],
        /,
    ) -> _Kind:
        """
        Returns function for computing angle kind.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> from ground.enums import Kind
        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (
        ...     context.angle_kind(Point(0, 0), Point(1, 0), Point(-1, 0))
        ...     is Kind.OBTUSE
        ... )
        True
        >>> (
        ...     context.angle_kind(Point(0, 0), Point(1, 0), Point(0, 1))
        ...     is Kind.RIGHT
        ... )
        True
        >>> (
        ...     context.angle_kind(Point(0, 0), Point(1, 0), Point(1, 0))
        ...     is Kind.ACUTE
        ... )
        True
        """
        return self._angular_context.kind(
            vertex, first_ray_point, second_ray_point, self._zero
        )

    def angle_orientation(
        self,
        vertex: _Point[_ScalarT],
        first_ray_point: _Point[_ScalarT],
        second_ray_point: _Point[_ScalarT],
        /,
    ) -> _Orientation:
        """
        Returns function for computing angle orientation.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> from ground.enums import Orientation
        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (
        ...     context.angle_orientation(
        ...         Point(0, 0), Point(0, 1), Point(1, 0)
        ...     )
        ...     is Orientation.CLOCKWISE
        ... )
        True
        >>> (
        ...     context.angle_orientation(
        ...         Point(0, 0), Point(1, 0), Point(1, 0)
        ...     )
        ...     is Orientation.COLLINEAR
        ... )
        True
        >>> (
        ...     context.angle_orientation(
        ...         Point(0, 0), Point(1, 0), Point(0, 1)
        ...     )
        ...     is Orientation.COUNTERCLOCKWISE
        ... )
        True
        """
        return self._angular_context.orientation(
            vertex, first_ray_point, second_ray_point, self._zero
        )

    def box_point_squared_distance(
        self, box: _Box[_ScalarT], point: _Point[_ScalarT], /
    ) -> _ScalarT:
        """
        Returns squared Euclidean distance between box and a point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point = context.box_cls, context.point_cls
        >>> context.box_point_squared_distance(
        ...     Box(0, 1, 0, 1), Point(1, 1)
        ... ) == 0
        True
        >>> context.box_point_squared_distance(
        ...     Box(0, 1, 0, 1), Point(2, 1)
        ... ) == 1
        True
        >>> context.box_point_squared_distance(
        ...     Box(0, 1, 0, 1), Point(2, 2)
        ... ) == 2
        True
        """
        return self._metric_context.box_point_squared_metric(
            box, point, self._coordinate_factory
        )

    def box_segment_squared_distance(
        self, box: _Box[_ScalarT], segment: _Segment[_ScalarT], /
    ) -> _ScalarT:
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
        ...     Box(0, 1, 0, 1), Segment(Point(0, 0), Point(1, 1))
        ... ) == 0
        True
        >>> context.box_segment_squared_distance(
        ...     Box(0, 1, 0, 1), Segment(Point(2, 0), Point(2, 1))
        ... ) == 1
        True
        >>> context.box_segment_squared_distance(
        ...     Box(0, 1, 0, 1), Segment(Point(2, 2), Point(3, 2))
        ... ) == 2
        True
        """
        return self._metric_context.box_segment_squared_metric(
            box,
            segment,
            self.dot_product,
            self._segments_intersect,
            self._coordinate_factory,
            self._point_cls,
        )

    def contour_box(self, contour: _Contour[_ScalarT], /) -> _Box[_ScalarT]:
        """
        Constructs box from contour.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(contour.vertices)``.

        >>> context = get_context()
        >>> Box, Contour, Point = (
        ...     context.box_cls,
        ...     context.contour_cls,
        ...     context.point_cls,
        ... )
        >>> (
        ...     context.contour_box(
        ...         Contour(
        ...             [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        ...         )
        ...     )
        ...     == Box(0, 1, 0, 1)
        ... )
        True
        """
        return _boxed.from_contour(contour, self._box_cls)

    def contour_centroid(
        self, contour: _Contour[_ScalarT], /
    ) -> _Point[_ScalarT]:
        """
        Constructs centroid of a contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour, Point = context.contour_cls, context.point_cls
        >>> (
        ...     context.contour_centroid(
        ...         Contour(
        ...             [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...         )
        ...     )
        ...     == Point(1, 1)
        ... )
        True
        """
        return self._centroidal_context.contour_centroid(
            contour, self._coordinate_factory, self._point_cls, self._sqrt
        )

    def contour_length(self, contour: _Contour[_ScalarT], /) -> _ScalarT:
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
        >>> context.contour_length(
        ...     Contour([Point(0, 0), Point(3, 0), Point(0, 4)])
        ... ) == 12
        True
        >>> context.contour_length(
        ...     Contour([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
        ... ) == 4
        True
        """
        points_squared_distance, sqrt = (
            self.points_squared_distance,
            self._sqrt,
        )
        vertices = contour.vertices
        return sum(
            (
                sqrt(
                    points_squared_distance(
                        vertices[index - 1], vertices[index]
                    )
                )
                for index in range(len(vertices))
            ),
            self._zero,
        )

    def contour_segments(
        self, contour: _Contour[_ScalarT], /
    ) -> _Sequence[_Segment[_ScalarT]]:
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
        >>> (
        ...     context.contour_segments(
        ...         Contour(
        ...             [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...         )
        ...     )
        ...     == [
        ...         Segment(Point(0, 0), Point(2, 0)),
        ...         Segment(Point(2, 0), Point(2, 2)),
        ...         Segment(Point(2, 2), Point(0, 2)),
        ...         Segment(Point(0, 2), Point(0, 0)),
        ...     ]
        ... )
        True
        """
        segment_cls, vertices = self._segment_cls, contour.vertices
        return [
            segment_cls(vertices[index], vertices[index + 1])
            for index in range(len(vertices) - 1)
        ] + [segment_cls(vertices[-1], vertices[0])]

    def contours_box(
        self, contours: _Sequence[_Contour[_ScalarT]], /
    ) -> _Box[_ScalarT]:
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
        return _boxed.from_contours(contours, self._box_cls)

    def is_region_convex(self, contour: _Contour[_ScalarT], /) -> bool:
        """
        Checks if region (given its contour) is convex.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> context.is_region_convex(
        ...     Contour([Point(0, 0), Point(3, 0), Point(1, 1), Point(0, 3)])
        ... )
        False
        >>> context.is_region_convex(
        ...     Contour([Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
        ... )
        True
        """
        vertices = contour.vertices
        vertices_count = len(vertices)
        if vertices_count == 3:
            return True
        orienteer = self.angle_orientation
        base_orientation = orienteer(vertices[-2], vertices[-1], vertices[0])
        # orientation change means that internal angle is greater than 180°
        return all(
            orienteer(
                vertices[index - 1], vertices[index], vertices[index + 1]
            )
            is base_orientation
            for index in range(vertices_count - 1)
        )

    def locate_point_in_point_point_point_circle(
        self,
        point: _Point[_ScalarT],
        first: _Point[_ScalarT],
        second: _Point[_ScalarT],
        third: _Point[_ScalarT],
        /,
    ) -> _Location:
        """
        Returns location of point in point-point-point circle.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> from ground.enums import Location
        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (
        ...     context.locate_point_in_point_point_point_circle(
        ...         Point(1, 1), Point(0, 0), Point(2, 0), Point(0, 2)
        ...     )
        ...     is Location.INTERIOR
        ... )
        True
        >>> (
        ...     context.locate_point_in_point_point_point_circle(
        ...         Point(2, 2), Point(0, 0), Point(2, 0), Point(0, 2)
        ...     )
        ...     is Location.BOUNDARY
        ... )
        True
        >>> (
        ...     context.locate_point_in_point_point_point_circle(
        ...         Point(3, 3), Point(0, 0), Point(2, 0), Point(0, 2)
        ...     )
        ...     is Location.EXTERIOR
        ... )
        True
        """
        return self._circular_context.point_point_point_locator(
            point, first, second, third, self._zero
        )

    def merged_box(
        self, first_box: _Box[_ScalarT], second_box: _Box[_ScalarT], /
    ) -> _Box[_ScalarT]:
        """
        Merges two boxes.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box = context.box_cls
        >>> (
        ...     context.merged_box(Box(0, 1, 0, 1), Box(1, 2, 1, 2))
        ...     == Box(0, 2, 0, 2)
        ... )
        True
        """
        return self._box_cls(
            min(first_box.min_x, second_box.min_x),
            max(first_box.max_x, second_box.max_x),
            min(first_box.min_y, second_box.min_y),
            max(first_box.max_y, second_box.max_y),
        )

    def multipoint_centroid(
        self, multipoint: _Multipoint[_ScalarT], /
    ) -> _Point[_ScalarT]:
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
        ...     Multipoint(
        ...         [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...     )
        ... ) == Point(1, 1)
        True
        """
        return self._centroidal_context.multipoint_centroid(
            multipoint, self._coordinate_factory, self._point_cls
        )

    def multipolygon_centroid(
        self, multipolygon: _Multipolygon[_ScalarT], /
    ) -> _Point[_ScalarT]:
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
        return self._centroidal_context.multipolygon_centroid(
            multipolygon, self._coordinate_factory, self._point_cls
        )

    def multisegment_centroid(
        self, multisegment: _Multisegment[_ScalarT], /
    ) -> _Point[_ScalarT]:
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
        >>> (
        ...     context.multisegment_centroid(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(2, 0)),
        ...                 Segment(Point(2, 0), Point(2, 2)),
        ...                 Segment(Point(0, 2), Point(2, 2)),
        ...                 Segment(Point(0, 0), Point(0, 2)),
        ...             ]
        ...         )
        ...     )
        ...     == Point(1, 1)
        ... )
        True
        """
        return self._centroidal_context.multisegment_centroid(
            multisegment, self._coordinate_factory, self._point_cls, self._sqrt
        )

    def multisegment_length(
        self, multisegment: _Multisegment[_ScalarT], /
    ) -> _ScalarT:
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
        ...     Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...         ]
        ...     )
        ... ) == 2
        True
        >>> context.multisegment_length(
        ...     Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(3, 4)),
        ...         ]
        ...     )
        ... ) == 6
        True
        """
        points_squared_distance, sqrt = (
            self.points_squared_distance,
            self._sqrt,
        )
        return sum(
            (
                sqrt(points_squared_distance(segment.start, segment.end))
                for segment in multisegment.segments
            ),
            self._origin.x,
        )

    def points_convex_hull(
        self, points: _Sequence[_Point[_ScalarT]], /
    ) -> _Sequence[_Point[_ScalarT]]:
        """
        Constructs convex hull of points.

        Time complexity:
            ``O(points_count * log(points_count))``
        Memory complexity:
            ``O(points_count)``

        where ``points_count = len(points)``.

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (
        ...     context.points_convex_hull(
        ...         [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...     )
        ...     == [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ... )
        True
        """
        return _discrete.to_convex_hull(points, self.angle_orientation)

    def points_box(
        self, points: _Sequence[_Point[_ScalarT]], /
    ) -> _Box[_ScalarT]:
        """
        Constructs box from points.

        Time complexity:
            ``O(len(points))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point = context.box_cls, context.point_cls
        >>> (
        ...     context.points_box(
        ...         [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...     )
        ...     == Box(0, 2, 0, 2)
        ... )
        True
        """
        return _boxed.from_points(points, self._box_cls)

    def polygon_box(self, polygon: _Polygon[_ScalarT], /) -> _Box[_ScalarT]:
        """
        Constructs box from polygon.

        Time complexity:
            ``O(vertices_count)``
        Memory complexity:
            ``O(1)``

        where ``vertices_count = len(polygon.border.vertices)``.

        >>> context = get_context()
        >>> Box, Contour, Point, Polygon = (
        ...     context.box_cls,
        ...     context.contour_cls,
        ...     context.point_cls,
        ...     context.polygon_cls,
        ... )
        >>> context.polygon_box(
        ...     Polygon(
        ...         Contour(
        ...             [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        ...         ),
        ...         [],
        ...     )
        ... ) == Box(0, 1, 0, 1)
        True
        """
        return _boxed.from_polygon(polygon, self._box_cls)

    def polygon_centroid(
        self, polygon: _Polygon[_ScalarT], /
    ) -> _Point[_ScalarT]:
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
        return self._centroidal_context.polygon_centroid(
            polygon, self._coordinate_factory, self._point_cls
        )

    def polygons_box(
        self, polygons: _Sequence[_Polygon[_ScalarT]], /
    ) -> _Box[_ScalarT]:
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
        return _boxed.from_polygons(polygons, self._box_cls)

    def region_centroid(
        self, contour: _Contour[_ScalarT], /
    ) -> _Point[_ScalarT]:
        """
        Constructs centroid of a region given its contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.region_centroid(
        ...         Contour(
        ...             [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        ...         )
        ...     )
        ...     == Point(1, 1)
        ... )
        True
        """
        return self._centroidal_context.region_centroid(
            contour, self._coordinate_factory, self._point_cls
        )

    def region_signed_area(self, contour: _Contour[_ScalarT], /) -> _ScalarT:
        """
        Returns signed area of the region given its contour.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.region_signed_area(
        ...         Contour(
        ...             [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        ...         )
        ...     )
        ...     == 1
        ... )
        True
        >>> (
        ...     context.region_signed_area(
        ...         Contour(
        ...             [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        ...         )
        ...     )
        ...     == -1
        ... )
        True
        """
        return self._measured_context.region_signed_area(
            contour, self._coordinate_factory
        )

    def replace(
        self,
        /,
        *,
        box_cls: type[_Box[_ScalarT]] | None = None,
        contour_cls: type[_Contour[_ScalarT]] | None = None,
        coordinate_factory: _ScalarFactory[_ScalarT] | None = None,
        empty_cls: type[_Empty[_ScalarT]] | None = None,
        mix_cls: type[_Mix[_ScalarT]] | None = None,
        multipoint_cls: type[_Multipoint[_ScalarT]] | None = None,
        multipolygon_cls: type[_Multipolygon[_ScalarT]] | None = None,
        multisegment_cls: type[_Multisegment[_ScalarT]] | None = None,
        point_cls: type[_Point[_ScalarT]] | None = None,
        polygon_cls: type[_Polygon[_ScalarT]] | None = None,
        segment_cls: type[_Segment[_ScalarT]] | None = None,
        sqrt: _SquareRooter[_ScalarT] | None = None,
    ) -> Context[_ScalarT]:
        """
        Constructs context from the original one replacing given parameters.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> from fractions import Fraction
        >>> fraction_context = context.replace(coordinate_factory=Fraction)
        >>> isinstance(fraction_context, Context)
        True
        >>> fraction_context.coordinate_factory is Fraction
        True
        """
        return Context(
            box_cls=self._box_cls if box_cls is None else box_cls,
            contour_cls=(
                self._contour_cls if contour_cls is None else contour_cls
            ),
            coordinate_factory=(
                self._coordinate_factory
                if coordinate_factory is None
                else coordinate_factory
            ),
            empty_cls=(self._empty_cls if empty_cls is None else empty_cls),
            mix_cls=self._mix_cls if mix_cls is None else mix_cls,
            multipoint_cls=(
                self._multipoint_cls
                if multipoint_cls is None
                else multipoint_cls
            ),
            multipolygon_cls=(
                self._multipolygon_cls
                if multipolygon_cls is None
                else multipolygon_cls
            ),
            multisegment_cls=(
                self._multisegment_cls
                if multisegment_cls is None
                else multisegment_cls
            ),
            point_cls=(self._point_cls if point_cls is None else point_cls),
            polygon_cls=(
                self._polygon_cls if polygon_cls is None else polygon_cls
            ),
            segment_cls=(
                self._segment_cls if segment_cls is None else segment_cls
            ),
            sqrt=self._sqrt if sqrt is None else sqrt,
        )

    def rotate_contour(
        self,
        contour: _Contour[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Contour[_ScalarT]:
        """
        Returns contour rotated by given angle around given center.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.rotate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]),
        ...         1,
        ...         0,
        ...         Point(0, 1),
        ...     )
        ...     == Contour([Point(0, 0), Point(1, 0), Point(0, 1)])
        ... )
        True
        >>> (
        ...     context.rotate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]),
        ...         0,
        ...         1,
        ...         Point(0, 1),
        ...     )
        ...     == Contour([Point(1, 1), Point(1, 2), Point(0, 1)])
        ... )
        True
        """
        return self._rotation_context.rotate_translate_contour(
            contour,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._contour_cls,
            self._point_cls,
        )

    def rotate_contour_around_origin(
        self, contour: _Contour[_ScalarT], cosine: _ScalarT, sine: _ScalarT, /
    ) -> _Contour[_ScalarT]:
        """
        Returns contour rotated by given angle around origin.

        Time complexity:
            ``O(len(contour.vertices))``
        Memory complexity:
            ``O(len(contour.vertices))``

        >>> context = get_context()
        >>> Contour = context.contour_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.rotate_contour_around_origin(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 0
        ...     )
        ...     == Contour([Point(0, 0), Point(1, 0), Point(0, 1)])
        ... )
        True
        >>> (
        ...     context.rotate_contour_around_origin(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 1
        ...     )
        ...     == Contour([Point(0, 0), Point(0, 1), Point(-1, 0)])
        ... )
        True
        """
        return self._rotation_context.rotate_contour_around_origin(
            contour, cosine, sine, self._contour_cls, self._point_cls
        )

    def rotate_multipoint(
        self,
        multipoint: _Multipoint[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Multipoint[_ScalarT]:
        """
        Returns multipoint rotated by given angle around given center.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.rotate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 1, 0, Point(0, 1)
        ...     )
        ...     == Multipoint([Point(0, 0), Point(1, 0)])
        ... )
        True
        >>> (
        ...     context.rotate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 0, 1, Point(0, 1)
        ...     )
        ...     == Multipoint([Point(1, 1), Point(1, 2)])
        ... )
        True
        """
        return self._rotation_context.rotate_translate_multipoint(
            multipoint,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._multipoint_cls,
            self._point_cls,
        )

    def rotate_multipoint_around_origin(
        self,
        multipoint: _Multipoint[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        /,
    ) -> _Multipoint[_ScalarT]:
        """
        Returns multipoint rotated by given angle around origin.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.rotate_multipoint_around_origin(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 1, 0
        ...     )
        ...     == Multipoint([Point(0, 0), Point(1, 0)])
        ... )
        True
        >>> (
        ...     context.rotate_multipoint_around_origin(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 0, 1
        ...     )
        ...     == Multipoint([Point(0, 0), Point(0, 1)])
        ... )
        True
        """
        return self._rotation_context.rotate_multipoint_around_origin(
            multipoint, cosine, sine, self._multipoint_cls, self._point_cls
        )

    def rotate_multipolygon(
        self,
        multipolygon: _Multipolygon[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Multipolygon[_ScalarT]:
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
        return self._rotation_context.rotate_translate_multipolygon(
            multipolygon,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._contour_cls,
            self._multipolygon_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def rotate_multipolygon_around_origin(
        self,
        multipolygon: _Multipolygon[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        /,
    ) -> _Multipolygon[_ScalarT]:
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
        return self._rotation_context.rotate_multipolygon_around_origin(
            multipolygon,
            cosine,
            sine,
            self._contour_cls,
            self._multipolygon_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def rotate_multisegment(
        self,
        multisegment: _Multisegment[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Multisegment[_ScalarT]:
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
        >>> (
        ...     context.rotate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         0,
        ...         Point(0, 1),
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...         ]
        ...     )
        ... )
        True
        >>> (
        ...     context.rotate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         1,
        ...         Point(0, 1),
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(1, 1), Point(1, 2)),
        ...             Segment(Point(1, 1), Point(0, 1)),
        ...         ]
        ...     )
        ... )
        True
        """
        return self._rotation_context.rotate_translate_multisegment(
            multisegment,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._multisegment_cls,
            self._point_cls,
            self._segment_cls,
        )

    def rotate_multisegment_around_origin(
        self,
        multisegment: _Multisegment[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        /,
    ) -> _Multisegment[_ScalarT]:
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
        >>> (
        ...     context.rotate_multisegment_around_origin(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         0,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...         ]
        ...     )
        ... )
        True
        >>> (
        ...     context.rotate_multisegment_around_origin(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         1,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...             Segment(Point(0, 0), Point(-1, 0)),
        ...         ]
        ...     )
        ... )
        True
        """
        return self._rotation_context.rotate_multisegment_around_origin(
            multisegment,
            cosine,
            sine,
            self._multisegment_cls,
            self._point_cls,
            self._segment_cls,
        )

    def rotate_point(
        self,
        point: _Point[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Point[_ScalarT]:
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
        return self._rotation_context.rotate_translate_point(
            point,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._point_cls,
        )

    def rotate_point_around_origin(
        self, point: _Point[_ScalarT], cosine: _ScalarT, sine: _ScalarT, /
    ) -> _Point[_ScalarT]:
        """
        Returns point rotated by given angle around origin.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> (
        ...     context.rotate_point_around_origin(Point(1, 0), 1, 0)
        ...     == Point(1, 0)
        ... )
        True
        >>> (
        ...     context.rotate_point_around_origin(Point(1, 0), 0, 1)
        ...     == Point(0, 1)
        ... )
        True
        """
        return self._rotation_context.rotate_point_around_origin(
            point, cosine, sine, self._point_cls
        )

    def rotate_polygon(
        self,
        polygon: _Polygon[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Polygon[_ScalarT]:
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
        return self._rotation_context.rotate_translate_polygon(
            polygon,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._contour_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def rotate_polygon_around_origin(
        self, polygon: _Polygon[_ScalarT], cosine: _ScalarT, sine: _ScalarT, /
    ) -> _Polygon[_ScalarT]:
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
        return self._rotation_context.rotate_polygon_around_origin(
            polygon,
            cosine,
            sine,
            self._contour_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def rotate_segment(
        self,
        segment: _Segment[_ScalarT],
        cosine: _ScalarT,
        sine: _ScalarT,
        center: _Point[_ScalarT],
        /,
    ) -> _Segment[_ScalarT]:
        """
        Returns segment rotated by given angle around given center.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (
        ...     context.rotate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 1, 0, Point(0, 1)
        ...     )
        ...     == Segment(Point(0, 0), Point(1, 0))
        ... )
        True
        >>> (
        ...     context.rotate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 0, 1, Point(0, 1)
        ...     )
        ...     == Segment(Point(1, 1), Point(1, 2))
        ... )
        True
        """
        return self._rotation_context.rotate_translate_segment(
            segment,
            cosine,
            sine,
            *self._rotation_context.point_to_step(center, cosine, sine),
            self._point_cls,
            self._segment_cls,
        )

    def rotate_segment_around_origin(
        self, segment: _Segment[_ScalarT], cosine: _ScalarT, sine: _ScalarT, /
    ) -> _Segment[_ScalarT]:
        """
        Returns segment rotated by given angle around origin.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (
        ...     context.rotate_segment_around_origin(
        ...         Segment(Point(0, 0), Point(1, 0)), 1, 0
        ...     )
        ...     == Segment(Point(0, 0), Point(1, 0))
        ... )
        True
        >>> (
        ...     context.rotate_segment_around_origin(
        ...         Segment(Point(0, 0), Point(1, 0)), 0, 1
        ...     )
        ...     == Segment(Point(0, 0), Point(0, 1))
        ... )
        True
        """
        return self._rotation_context.rotate_segment_around_origin(
            segment, cosine, sine, self._point_cls, self._segment_cls
        )

    def scale_contour(
        self,
        contour: _Contour[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> _Contour[_ScalarT] | _Multipoint[_ScalarT] | _Segment[_ScalarT]:
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
        >>> (
        ...     context.scale_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 0
        ...     )
        ...     == Multipoint([Point(0, 0)])
        ... )
        True
        >>> (
        ...     context.scale_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 0
        ...     )
        ...     == Segment(Point(0, 0), Point(1, 0))
        ... )
        True
        >>> (
        ...     context.scale_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 1
        ...     )
        ...     == Segment(Point(0, 0), Point(0, 1))
        ... )
        True
        >>> (
        ...     context.scale_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 1
        ...     )
        ...     == Contour([Point(0, 0), Point(1, 0), Point(0, 1)])
        ... )
        True
        """
        return self._scaling_context.scale_contour(
            contour,
            factor_x,
            factor_y,
            self._contour_cls,
            self._multipoint_cls,
            self._point_cls,
            self._segment_cls,
        )

    def scale_multipoint(
        self,
        multipoint: _Multipoint[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> _Multipoint[_ScalarT]:
        """
        Returns multipoint scaled by given factor.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.scale_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 1)]), 0, 0
        ...     )
        ...     == Multipoint([Point(0, 0)])
        ... )
        True
        >>> (
        ...     context.scale_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 1)]), 1, 0
        ...     )
        ...     == Multipoint([Point(0, 0), Point(1, 0)])
        ... )
        True
        >>> (
        ...     context.scale_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 1)]), 0, 1
        ...     )
        ...     == Multipoint([Point(0, 0), Point(0, 1)])
        ... )
        True
        >>> (
        ...     context.scale_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 1)]), 1, 1
        ...     )
        ...     == Multipoint([Point(0, 0), Point(1, 1)])
        ... )
        True
        """
        return self._scaling_context.scale_multipoint(
            multipoint,
            factor_x,
            factor_y,
            self._multipoint_cls,
            self._point_cls,
        )

    def scale_multipolygon(
        self,
        multipolygon: _Multipolygon[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> (
        _Multipoint[_ScalarT]
        | _Multipolygon[_ScalarT]
        | _Multisegment[_ScalarT]
    ):
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
        return self._scaling_context.scale_multipolygon(
            multipolygon,
            factor_x,
            factor_y,
            self._contour_cls,
            self._multipoint_cls,
            self._multipolygon_cls,
            self._multisegment_cls,
            self._point_cls,
            self._polygon_cls,
            self._segment_cls,
        )

    def scale_multisegment(
        self,
        multisegment: _Multisegment[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> (
        _Empty[_ScalarT]
        | _Linear[_ScalarT]
        | _Mix[_ScalarT]
        | _Multipoint[_ScalarT]
        | _Shaped[_ScalarT]
    ):
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
        >>> (
        ...     context.scale_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         0,
        ...     )
        ...     == Multipoint([Point(0, 0)])
        ... )
        True
        >>> (
        ...     context.scale_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         0,
        ...     )
        ...     == Mix(
        ...         Multipoint([Point(0, 0)]),
        ...         Segment(Point(0, 0), Point(1, 0)),
        ...         EMPTY,
        ...     )
        ... )
        True
        >>> (
        ...     context.scale_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         1,
        ...     )
        ...     == Mix(
        ...         Multipoint([Point(0, 0)]),
        ...         Segment(Point(0, 0), Point(0, 1)),
        ...         EMPTY,
        ...     )
        ... )
        True
        >>> (
        ...     context.scale_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         1,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...         ]
        ...     )
        ... )
        True
        """
        return self._scaling_context.scale_multisegment(
            multisegment,
            factor_x,
            factor_y,
            self._empty,
            self._mix_cls,
            self._multipoint_cls,
            self._multisegment_cls,
            self._point_cls,
            self._segment_cls,
        )

    def scale_point(
        self,
        point: _Point[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> _Point[_ScalarT]:
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
        return self._scaling_context.scale_point(
            point, factor_x, factor_y, self._point_cls
        )

    def scale_polygon(
        self,
        polygon: _Polygon[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> _Multipoint[_ScalarT] | _Polygon[_ScalarT] | _Segment[_ScalarT]:
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
        return self._scaling_context.scale_polygon(
            polygon,
            factor_x,
            factor_y,
            self._contour_cls,
            self._multipoint_cls,
            self._point_cls,
            self._polygon_cls,
            self._segment_cls,
        )

    def scale_segment(
        self,
        segment: _Segment[_ScalarT],
        factor_x: _ScalarT,
        factor_y: _ScalarT,
        /,
    ) -> _Multipoint[_ScalarT] | _Segment[_ScalarT]:
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
        >>> (
        ...     context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 0, 0)
        ...     == Multipoint([Point(0, 0)])
        ... )
        True
        >>> (
        ...     context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 1, 0)
        ...     == Segment(Point(0, 0), Point(1, 0))
        ... )
        True
        >>> (
        ...     context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 0, 1)
        ...     == Segment(Point(0, 0), Point(0, 1))
        ... )
        True
        >>> (
        ...     context.scale_segment(Segment(Point(0, 0), Point(1, 1)), 1, 1)
        ...     == Segment(Point(0, 0), Point(1, 1))
        ... )
        True
        """
        return self._scaling_context.scale_segment(
            segment,
            factor_x,
            factor_y,
            self._multipoint_cls,
            self._point_cls,
            self._segment_cls,
        )

    def segment_box(self, segment: _Segment[_ScalarT], /) -> _Box[_ScalarT]:
        """
        Constructs box from segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point, Segment = (
        ...     context.box_cls,
        ...     context.point_cls,
        ...     context.segment_cls,
        ... )
        >>> (
        ...     context.segment_box(Segment(Point(0, 1), Point(2, 3)))
        ...     == Box(0, 2, 1, 3)
        ... )
        True
        """
        return _boxed.from_segment(segment, self._box_cls)

    def segment_centroid(
        self, segment: _Segment[_ScalarT], /
    ) -> _Point[_ScalarT]:
        """
        Constructs centroid of a segment.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point, Segment = context.point_cls, context.segment_cls
        >>> (
        ...     context.segment_centroid(Segment(Point(0, 1), Point(2, 3)))
        ...     == Point(1, 2)
        ... )
        True
        """
        return self._centroidal_context.segment_centroid(
            segment, self._coordinate_factory, self._point_cls
        )

    def segment_contains_point(
        self, segment: _Segment[_ScalarT], point: _Point[_ScalarT], /
    ) -> bool:
        """
        Checks if a segment contains given point.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(0, 0)
        ... )
        True
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(0, 2)
        ... )
        False
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(1, 0)
        ... )
        True
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(1, 1)
        ... )
        False
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(2, 0)
        ... )
        True
        >>> context.segment_contains_point(
        ...     Segment(Point(0, 0), Point(2, 0)), Point(3, 0)
        ... )
        False
        """
        return self._segment_context.containment_checker(
            segment.start, segment.end, point, self.angle_orientation
        )

    def segment_length(self, segment: _Segment[_ScalarT], /) -> _ScalarT:
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
        return self._sqrt(
            self.points_squared_distance(segment.start, segment.end)
        )

    def segment_point_squared_distance(
        self, segment: _Segment[_ScalarT], point: _Point[_ScalarT], /
    ) -> _ScalarT:
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
        ...     Segment(Point(0, 0), Point(1, 0)), Point(0, 0)
        ... ) == 0
        True
        >>> context.segment_point_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)), Point(0, 1)
        ... ) == 1
        True
        >>> context.segment_point_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)), Point(2, 1)
        ... ) == 2
        True
        """
        return self._metric_context.segment_point_squared_metric(
            segment.start,
            segment.end,
            point,
            self.dot_product,
            self._coordinate_factory,
        )

    def segments_box(
        self, segments: _Sequence[_Segment[_ScalarT]], /
    ) -> _Box[_ScalarT]:
        """
        Constructs box from segments.

        Time complexity:
            ``O(len(segments))``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Box, Point, Segment = (
        ...     context.box_cls,
        ...     context.point_cls,
        ...     context.segment_cls,
        ... )
        >>> (
        ...     context.segments_box(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 1)),
        ...             Segment(Point(1, 1), Point(2, 2)),
        ...         ]
        ...     )
        ...     == Box(0, 2, 0, 2)
        ... )
        True
        """
        return _boxed.from_segments(segments, self._box_cls)

    def segments_intersection(
        self, first: _Segment[_ScalarT], second: _Segment[_ScalarT], /
    ) -> _Point[_ScalarT]:
        """
        Returns intersection point of two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (
        ...     context.segments_intersection(
        ...         Segment(Point(0, 0), Point(2, 0)),
        ...         Segment(Point(0, 0), Point(0, 1)),
        ...     )
        ...     == Point(0, 0)
        ... )
        True
        >>> (
        ...     context.segments_intersection(
        ...         Segment(Point(0, 0), Point(2, 0)),
        ...         Segment(Point(1, 0), Point(1, 1)),
        ...     )
        ...     == Point(1, 0)
        ... )
        True
        >>> (
        ...     context.segments_intersection(
        ...         Segment(Point(0, 0), Point(2, 0)),
        ...         Segment(Point(2, 0), Point(3, 0)),
        ...     )
        ...     == Point(2, 0)
        ... )
        True
        """
        return self._segment_context.intersector(
            first.start,
            first.end,
            second.start,
            second.end,
            self._point_cls,
            self._segment_contains_point,
        )

    def segments_relation(
        self, test: _Segment[_ScalarT], goal: _Segment[_ScalarT], /
    ) -> _Relation:
        """
        Returns relation between two segments.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> from ground.enums import Relation
        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(1, 0), Point(2, 0)),
        ...     )
        ...     is Relation.DISJOINT
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(0, 0), Point(2, 0)),
        ...     )
        ...     is Relation.TOUCH
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(2, 0), Point(0, 2)),
        ...     )
        ...     is Relation.CROSS
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(0, 0), Point(1, 1)),
        ...     )
        ...     is Relation.COMPOSITE
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...     )
        ...     is Relation.EQUAL
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(0, 0), Point(3, 3)),
        ...     )
        ...     is Relation.COMPONENT
        ... )
        True
        >>> (
        ...     context.segments_relation(
        ...         Segment(Point(0, 0), Point(2, 2)),
        ...         Segment(Point(1, 1), Point(3, 3)),
        ...     )
        ...     is Relation.OVERLAP
        ... )
        True
        """
        return self._segment_context.relater(
            test.start, test.end, goal.start, goal.end, self.angle_orientation
        )

    def segments_squared_distance(
        self, first: _Segment[_ScalarT], second: _Segment[_ScalarT], /
    ) -> _ScalarT:
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
        ...     Segment(Point(0, 0), Point(0, 1)),
        ... ) == 0
        True
        >>> context.segments_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)),
        ...     Segment(Point(0, 1), Point(1, 1)),
        ... ) == 1
        True
        >>> context.segments_squared_distance(
        ...     Segment(Point(0, 0), Point(1, 0)),
        ...     Segment(Point(2, 1), Point(2, 2)),
        ... ) == 2
        True
        """
        return self._metric_context.segment_segment_squared_metric(
            first.start,
            first.end,
            second.start,
            second.end,
            self.dot_product,
            self._segments_intersect,
            self._coordinate_factory,
        )

    def translate_contour(
        self,
        contour: _Contour[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Contour[_ScalarT]:
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
        >>> (
        ...     context.translate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 0
        ...     )
        ...     == Contour([Point(0, 0), Point(1, 0), Point(0, 1)])
        ... )
        True
        >>> (
        ...     context.translate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 0
        ...     )
        ...     == Contour([Point(1, 0), Point(2, 0), Point(1, 1)])
        ... )
        True
        >>> (
        ...     context.translate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 0, 1
        ...     )
        ...     == Contour([Point(0, 1), Point(1, 1), Point(0, 2)])
        ... )
        True
        >>> (
        ...     context.translate_contour(
        ...         Contour([Point(0, 0), Point(1, 0), Point(0, 1)]), 1, 1
        ...     )
        ...     == Contour([Point(1, 1), Point(2, 1), Point(1, 2)])
        ... )
        True
        """
        return self._translation_context.translate_contour(
            contour, step_x, step_y, self._contour_cls, self._point_cls
        )

    def translate_multipoint(
        self,
        multipoint: _Multipoint[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Multipoint[_ScalarT]:
        """
        Returns multipoint translated by given step.

        Time complexity:
            ``O(len(multipoint.points))``
        Memory complexity:
            ``O(len(multipoint.points))``

        >>> context = get_context()
        >>> Multipoint = context.multipoint_cls
        >>> Point = context.point_cls
        >>> (
        ...     context.translate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 0, 0
        ...     )
        ...     == Multipoint([Point(0, 0), Point(1, 0)])
        ... )
        True
        >>> (
        ...     context.translate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 1, 0
        ...     )
        ...     == Multipoint([Point(1, 0), Point(2, 0)])
        ... )
        True
        >>> (
        ...     context.translate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 0, 1
        ...     )
        ...     == Multipoint([Point(0, 1), Point(1, 1)])
        ... )
        True
        >>> (
        ...     context.translate_multipoint(
        ...         Multipoint([Point(0, 0), Point(1, 0)]), 1, 1
        ...     )
        ...     == Multipoint([Point(1, 1), Point(2, 1)])
        ... )
        True
        """
        return self._translation_context.translate_multipoint(
            multipoint, step_x, step_y, self._multipoint_cls, self._point_cls
        )

    def translate_multipolygon(
        self,
        multipolygon: _Multipolygon[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Multipolygon[_ScalarT]:
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
        return self._translation_context.translate_multipolygon(
            multipolygon,
            step_x,
            step_y,
            self._contour_cls,
            self._multipolygon_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def translate_multisegment(
        self,
        multisegment: _Multisegment[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Multisegment[_ScalarT]:
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
        >>> (
        ...     context.translate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         0,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 0), Point(1, 0)),
        ...             Segment(Point(0, 0), Point(0, 1)),
        ...         ]
        ...     )
        ... )
        True
        >>> (
        ...     context.translate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         0,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(1, 0), Point(2, 0)),
        ...             Segment(Point(1, 0), Point(1, 1)),
        ...         ]
        ...     )
        ... )
        True
        >>> (
        ...     context.translate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         0,
        ...         1,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(0, 1), Point(1, 1)),
        ...             Segment(Point(0, 1), Point(0, 2)),
        ...         ]
        ...     )
        ... )
        True
        >>> (
        ...     context.translate_multisegment(
        ...         Multisegment(
        ...             [
        ...                 Segment(Point(0, 0), Point(1, 0)),
        ...                 Segment(Point(0, 0), Point(0, 1)),
        ...             ]
        ...         ),
        ...         1,
        ...         1,
        ...     )
        ...     == Multisegment(
        ...         [
        ...             Segment(Point(1, 1), Point(2, 1)),
        ...             Segment(Point(1, 1), Point(1, 2)),
        ...         ]
        ...     )
        ... )
        True
        """
        return self._translation_context.translate_multisegment(
            multisegment,
            step_x,
            step_y,
            self._multisegment_cls,
            self._point_cls,
            self._segment_cls,
        )

    def translate_point(
        self, point: _Point[_ScalarT], step_x: _ScalarT, step_y: _ScalarT, /
    ) -> _Point[_ScalarT]:
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
        return self._translation_context.translate_point(
            point, step_x, step_y, self._point_cls
        )

    def translate_polygon(
        self,
        polygon: _Polygon[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Polygon[_ScalarT]:
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
        return self._translation_context.translate_polygon(
            polygon,
            step_x,
            step_y,
            self._contour_cls,
            self._point_cls,
            self._polygon_cls,
        )

    def translate_segment(
        self,
        segment: _Segment[_ScalarT],
        step_x: _ScalarT,
        step_y: _ScalarT,
        /,
    ) -> _Segment[_ScalarT]:
        """
        Returns segment translated by given step.

        Time complexity:
            ``O(1)``
        Memory complexity:
            ``O(1)``

        >>> context = get_context()
        >>> Point = context.point_cls
        >>> Segment = context.segment_cls
        >>> (
        ...     context.translate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 0, 0
        ...     )
        ...     == Segment(Point(0, 0), Point(1, 0))
        ... )
        True
        >>> (
        ...     context.translate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 1, 0
        ...     )
        ...     == Segment(Point(1, 0), Point(2, 0))
        ... )
        True
        >>> (
        ...     context.translate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 0, 1
        ...     )
        ...     == Segment(Point(0, 1), Point(1, 1))
        ... )
        True
        >>> (
        ...     context.translate_segment(
        ...         Segment(Point(0, 0), Point(1, 0)), 1, 1
        ...     )
        ...     == Segment(Point(1, 1), Point(2, 1))
        ... )
        True
        """
        return self._translation_context.translate_segment(
            segment, step_x, step_y, self._point_cls, self._segment_cls
        )

    _angular_context: _angular.Context[_ScalarT]
    _box_cls: type[_Box[_ScalarT]]
    _centroidal_context: _centroidal.Context[_ScalarT]
    _circular_context: _circular.Context[_ScalarT]
    _contour_cls: type[_Contour[_ScalarT]]
    _coordinate_factory: _ScalarFactory[_ScalarT]
    _empty: _Empty[_ScalarT]
    _empty_cls: type[_Empty[_ScalarT]]
    _measured_context: _measured.Context[_ScalarT]
    _metric_context: _metric.Context[_ScalarT]
    _mix_cls: type[_Mix[_ScalarT]]
    _multipoint_cls: type[_Multipoint[_ScalarT]]
    _multipolygon_cls: type[_Multipolygon[_ScalarT]]
    _multisegment_cls: type[_Multisegment[_ScalarT]]
    _origin: _Point[_ScalarT]
    _point_cls: type[_Point[_ScalarT]]
    _polygon_cls: type[_Polygon[_ScalarT]]
    _rotation_context: _rotation.Context[_ScalarT]
    _scaling_context: _scaling.Context[_ScalarT]
    _segment_cls: type[_Segment[_ScalarT]]
    _segment_context: _segment.Context[_ScalarT]
    _sqrt: _SquareRooter[_ScalarT]
    _translation_context: _translation.Context[_ScalarT]
    _vector_context: _vector.Context[_ScalarT]
    _zero: _ScalarT

    def _segment_contains_point(
        self,
        start: _Point[_ScalarT],
        end: _Point[_ScalarT],
        point: _Point[_ScalarT],
        /,
    ) -> bool:
        return self._segment_context.containment_checker(
            start, end, point, self.angle_orientation
        )

    def _segments_intersect(
        self,
        first_start: _Point[_ScalarT],
        first_end: _Point[_ScalarT],
        second_start: _Point[_ScalarT],
        second_end: _Point[_ScalarT],
        /,
    ) -> bool:
        return self._segment_context.collision_detector(
            first_start,
            first_end,
            second_start,
            second_end,
            self.angle_orientation,
        )

    __slots__ = (
        '_angular_context',
        '_box_cls',
        '_centroidal_context',
        '_circular_context',
        '_contour_cls',
        '_coordinate_factory',
        '_empty',
        '_empty_cls',
        '_measured_context',
        '_metric_context',
        '_mix_cls',
        '_multipoint_cls',
        '_multipolygon_cls',
        '_multisegment_cls',
        '_origin',
        '_point_cls',
        '_polygon_cls',
        '_rotation_context',
        '_scaling_context',
        '_segment_cls',
        '_segment_context',
        '_sqrt',
        '_translation_context',
        '_vector_context',
        '_zero',
    )

    def __new__(
        cls,
        /,
        *,
        box_cls: type[_Box[_ScalarT]] = _geometries.Box,
        contour_cls: type[_Contour[_ScalarT]] = _geometries.Contour,
        coordinate_factory: _Callable[[int], _ScalarT],
        empty_cls: type[_Empty[_ScalarT]] = _geometries.Empty,
        mix_cls: type[_Mix[_ScalarT]] = _geometries.Mix,
        multipoint_cls: type[_Multipoint[_ScalarT]] = _geometries.Multipoint,
        multipolygon_cls: type[
            _Multipolygon[_ScalarT]
        ] = _geometries.Multipolygon,
        multisegment_cls: type[
            _Multisegment[_ScalarT]
        ] = _geometries.Multisegment,
        point_cls: type[_Point[_ScalarT]] = _geometries.Point,
        polygon_cls: type[_Polygon[_ScalarT]] = _geometries.Polygon,
        segment_cls: type[_Segment[_ScalarT]] = _geometries.Segment,
        sqrt: _SquareRooter[_ScalarT],
    ) -> _Self:
        zero = coordinate_factory(0)
        self = super().__new__(cls)
        (
            self._box_cls,
            self._contour_cls,
            self._coordinate_factory,
            self._empty,
            self._empty_cls,
            self._mix_cls,
            self._multipoint_cls,
            self._multipolygon_cls,
            self._multisegment_cls,
            self._origin,
            self._point_cls,
            self._polygon_cls,
            self._segment_cls,
            self._sqrt,
            self._zero,
        ) = (
            box_cls,
            contour_cls,
            coordinate_factory,
            empty_cls(),
            empty_cls,
            mix_cls,
            multipoint_cls,
            multipolygon_cls,
            multisegment_cls,
            point_cls(zero, zero),
            point_cls,
            polygon_cls,
            segment_cls,
            sqrt,
            zero,
        )
        (
            self._angular_context,
            self._centroidal_context,
            self._circular_context,
            self._measured_context,
            self._metric_context,
            self._rotation_context,
            self._scaling_context,
            self._segment_context,
            self._translation_context,
            self._vector_context,
        ) = (
            _angular.plain_context,
            _centroidal.plain_context,
            _circular.plain_context,
            _measured.plain_context,
            _metric.plain_context,
            _rotation.plain_context,
            _scaling.plain_context,
            _segment.plain_context,
            _translation.plain_context,
            _vector.plain_context,
        )
        return self

    def __eq__(self, other: _Any, /) -> _Any:
        return (
            (
                self._box_cls is other._box_cls
                and self._contour_cls is other._contour_cls
                and self._coordinate_factory is other._coordinate_factory
                and self._empty_cls is other._empty_cls
                and self._mix_cls is other._mix_cls
                and self._multipoint_cls is other._multipoint_cls
                and self._multipolygon_cls is other._multipolygon_cls
                and self._multisegment_cls is other._multisegment_cls
                and self._point_cls is other._point_cls
                and self._polygon_cls is other._polygon_cls
                and self._segment_cls is other._segment_cls
                and self._sqrt is other._sqrt
            )
            if isinstance(other, Context)
            else NotImplemented
        )

    __repr__ = _generate_repr(
        __new__, argument_serializer=_serializers.complex_, skip_defaults=True
    )


_context: _ContextVar[Context[_Any]] = _ContextVar(
    'context',
    default=Context(coordinate_factory=float, sqrt=_math.sqrt),  # noqa: B039
)


def get_context() -> Context[_Any]:
    """Returns current context."""
    return _context.get()


def set_context(context: Context[_ScalarT], /) -> None:
    """Sets current context."""
    assert isinstance(context, Context), (
        f'Expected {Context.__qualname__!r} instance, but got {context}.'
    )
    _context.set(context)
