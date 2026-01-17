import sys
from collections import OrderedDict
from collections.abc import Callable, Iterable
from itertools import chain
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import (
    Contour,
    Empty,
    HasRepr,
    Linear,
    Mix,
    Multipoint,
    Multipolygon,
    Multisegment,
    Point,
    Polygon,
    ScalarT,
    Segment,
    Shaped,
)
from ground._core.packing import pack_mix, pack_points, pack_segments

from . import plain

PointScaler: TypeAlias = Callable[
    [Point[ScalarT], ScalarT, ScalarT, type[Point[ScalarT]]], Point[ScalarT]
]


def ensure_segment(
    value: Any, segment_cls: type[Segment[ScalarT]], /
) -> Segment[ScalarT]:
    assert isinstance(value, segment_cls), (value, segment_cls)
    return value


class Context(HasRepr, Generic[ScalarT]):
    @property
    def scale_point(self, /) -> PointScaler[ScalarT]:
        return self._scale_point

    def scale_contour(
        self,
        contour: Contour[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Contour[ScalarT] | Multipoint[ScalarT] | Segment[ScalarT]:
        return (
            self.scale_contour_non_degenerate(
                contour, factor_x, factor_y, contour_cls, point_cls
            )
            if factor_x and factor_y
            else self.scale_contour_degenerate(
                contour,
                factor_x,
                factor_y,
                multipoint_cls,
                point_cls,
                segment_cls,
            )
        )

    def scale_contour_non_degenerate(
        self,
        contour: Contour[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Contour[ScalarT]:
        return contour_cls(
            [
                self.scale_point(vertex, factor_x, factor_y, point_cls)
                for vertex in contour.vertices
            ]
        )

    def scale_contour_degenerate(
        self,
        contour: Contour[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multipoint[ScalarT] | Segment[ScalarT]:
        return self.scale_vertices_degenerate(
            contour.vertices,
            factor_x,
            factor_y,
            multipoint_cls,
            point_cls,
            segment_cls,
        )

    def scale_multipoint(
        self,
        multipoint: Multipoint[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Multipoint[ScalarT]:
        return multipoint_cls(
            [
                self.scale_point(point, factor_x, factor_y, point_cls)
                for point in multipoint.points
            ]
            if factor_x and factor_y
            else (
                list(
                    unique_ever_seen(
                        self.scale_point(point, factor_x, factor_y, point_cls)
                        for point in multipoint.points
                    )
                )
                if factor_x or factor_y
                else [point_cls(factor_x, factor_y)]
            )
        )

    def scale_multipolygon(
        self,
        multipolygon: Multipolygon[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        multipoint_cls: type[Multipoint[ScalarT]],
        multipolygon_cls: type[Multipolygon[ScalarT]],
        multisegment_cls: type[Multisegment[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multipoint[ScalarT] | Multipolygon[ScalarT] | Multisegment[ScalarT]:
        return (
            multipolygon_cls(
                [
                    self.scale_polygon_non_degenerate(
                        polygon,
                        factor_x,
                        factor_y,
                        contour_cls,
                        point_cls,
                        polygon_cls,
                    )
                    for polygon in multipolygon.polygons
                ]
            )
            if factor_x and factor_y
            else (
                multisegment_cls(
                    [
                        ensure_segment(
                            self.scale_polygon_degenerate(
                                polygon,
                                factor_x,
                                factor_y,
                                multipoint_cls,
                                point_cls,
                                segment_cls,
                            ),
                            segment_cls,
                        )
                        for polygon in multipolygon.polygons
                    ]
                )
                if factor_x or factor_y
                else multipoint_cls([point_cls(factor_x, factor_y)])
            )
        )

    def scale_multisegment(
        self,
        multisegment: Multisegment[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        empty: Empty[ScalarT],
        mix_cls: type[Mix[ScalarT]],
        multipoint_cls: type[Multipoint[ScalarT]],
        multisegment_cls: type[Multisegment[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> (
        Empty[ScalarT]
        | Linear[ScalarT]
        | Mix[ScalarT]
        | Multipoint[ScalarT]
        | Shaped[ScalarT]
    ):
        scaled_points, scaled_segments = [], []
        for segment in multisegment.segments:
            if (
                (factor_x or not is_segment_horizontal(segment)) and factor_y
            ) or (factor_x and not is_segment_vertical(segment)):
                scaled_segments.append(
                    self.scale_segment_non_degenerate(
                        segment, factor_x, factor_y, point_cls, segment_cls
                    )
                )
            else:
                scaled_points.append(
                    self.scale_point(
                        segment.start, factor_x, factor_y, point_cls
                    )
                )
        return pack_mix(
            pack_points(
                list(unique_ever_seen(scaled_points)), empty, multipoint_cls
            ),
            pack_segments(scaled_segments, empty, multisegment_cls),
            empty,
            empty,
            mix_cls,
        )

    def scale_polygon(
        self,
        polygon: Polygon[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multipoint[ScalarT] | Polygon[ScalarT] | Segment[ScalarT]:
        return (
            self.scale_polygon_non_degenerate(
                polygon,
                factor_x,
                factor_y,
                contour_cls,
                point_cls,
                polygon_cls,
            )
            if factor_x and factor_y
            else self.scale_polygon_degenerate(
                polygon,
                factor_x,
                factor_y,
                multipoint_cls,
                point_cls,
                segment_cls,
            )
        )

    def scale_polygon_degenerate(
        self,
        polygon: Polygon[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multipoint[ScalarT] | Segment[ScalarT]:
        return self.scale_contour_degenerate(
            polygon.border,
            factor_x,
            factor_y,
            multipoint_cls,
            point_cls,
            segment_cls,
        )

    def scale_polygon_non_degenerate(
        self,
        polygon: Polygon[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Polygon[ScalarT]:
        return polygon_cls(
            self.scale_contour_non_degenerate(
                polygon.border, factor_x, factor_y, contour_cls, point_cls
            ),
            [
                self.scale_contour_non_degenerate(
                    hole, factor_x, factor_y, contour_cls, point_cls
                )
                for hole in polygon.holes
            ],
        )

    def scale_segment(
        self,
        segment: Segment[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multipoint[ScalarT] | Segment[ScalarT]:
        return (
            self.scale_segment_non_degenerate(
                segment, factor_x, factor_y, point_cls, segment_cls
            )
            if (
                ((factor_x or not is_segment_horizontal(segment)) and factor_y)
                or (factor_x and not is_segment_vertical(segment))
            )
            else multipoint_cls(
                [
                    self.scale_point(
                        segment.start, factor_x, factor_y, point_cls
                    )
                ]
            )
        )

    def scale_segment_non_degenerate(
        self,
        segment: Segment[ScalarT],
        factor_x: ScalarT,
        factor_y: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        return segment_cls(
            self.scale_point(segment.start, factor_x, factor_y, point_cls),
            self.scale_point(segment.end, factor_x, factor_y, point_cls),
        )

    def scale_vertices_degenerate(
        self,
        vertices: Iterable[Point[ScalarT]],
        factor_x: ScalarT,
        factor_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT] | Multipoint[ScalarT]:
        return (
            self.scale_vertices_projecting_on_ox(
                vertices, factor_x, factor_y, point_cls, segment_cls
            )
            if factor_x
            else (
                self.scale_vertices_projecting_on_oy(
                    vertices, factor_x, factor_y, point_cls, segment_cls
                )
                if factor_y
                else multipoint_cls([point_cls(factor_x, factor_y)])
            )
        )

    @staticmethod
    def scale_vertices_projecting_on_ox(
        vertices: Iterable[Point[ScalarT]],
        factor_x: ScalarT,
        factor_y: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        vertices = iter(vertices)
        min_x = max_x = next(vertices).x
        for vertex in vertices:
            if min_x > vertex.x:
                min_x = vertex.x
            elif max_x < vertex.x:
                max_x = vertex.x
        return segment_cls(
            point_cls(min_x * factor_x, factor_y),
            point_cls(max_x * factor_x, factor_y),
        )

    @staticmethod
    def scale_vertices_projecting_on_oy(
        vertices: Iterable[Point[ScalarT]],
        factor_x: ScalarT,
        factor_y: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        vertices = iter(vertices)
        min_y = max_y = next(vertices).y
        for vertex in vertices:
            if min_y > vertex.y:
                min_y = vertex.y
            elif max_y < vertex.y:
                max_y = vertex.y
        return segment_cls(
            point_cls(factor_x, min_y * factor_y),
            point_cls(factor_x, max_y * factor_y),
        )

    _scale_point: PointScaler[ScalarT]

    __slots__ = ('_scale_point',)

    def __new__(cls, /, *, scale_point: PointScaler[ScalarT]) -> Self:
        self = super().__new__(cls)
        self._scale_point = scale_point
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(scale_point=plain.scale_point)


def is_segment_horizontal(segment: Segment[ScalarT], /) -> bool:
    result = segment.start.y == segment.end.y
    assert isinstance(result, bool), result
    return result


def is_segment_vertical(segment: Segment[ScalarT], /) -> bool:
    result = segment.start.x == segment.end.x
    assert isinstance(result, bool), result
    return result


flatten = chain.from_iterable
unique_ever_seen = (
    dict.fromkeys if sys.version_info >= (3, 6) else OrderedDict.fromkeys
)
