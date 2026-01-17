from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import (
    Contour,
    HasRepr,
    Multipoint,
    Multipolygon,
    Multisegment,
    Point,
    Polygon,
    ScalarT,
    Segment,
)

from . import plain

PointRotatorAroundOrigin: TypeAlias = Callable[
    [Point[ScalarT], ScalarT, ScalarT, type[Point[ScalarT]]], Point[ScalarT]
]
PointTranslatingRotator: TypeAlias = Callable[
    [Point[ScalarT], ScalarT, ScalarT, ScalarT, ScalarT, type[Point[ScalarT]]],
    Point[ScalarT],
]
PointToStep: TypeAlias = Callable[
    [Point[ScalarT], ScalarT, ScalarT], tuple[ScalarT, ScalarT]
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def point_to_step(self, /) -> PointToStep[ScalarT]:
        return self._point_to_step

    @property
    def rotate_point_around_origin(
        self, /
    ) -> PointRotatorAroundOrigin[ScalarT]:
        return self._rotate_point_around_origin

    @property
    def rotate_translate_point(self, /) -> PointTranslatingRotator[ScalarT]:
        return self._rotate_translate_point

    def rotate_contour_around_origin(
        self,
        contour: Contour[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Contour[ScalarT]:
        return contour_cls(
            [
                self.rotate_point_around_origin(point, cosine, sine, point_cls)
                for point in contour.vertices
            ]
        )

    def rotate_multipoint_around_origin(
        self,
        multipoint: Multipoint[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Multipoint[ScalarT]:
        return multipoint_cls(
            [
                self.rotate_point_around_origin(point, cosine, sine, point_cls)
                for point in multipoint.points
            ]
        )

    def rotate_multipolygon_around_origin(
        self,
        multipolygon: Multipolygon[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        multipolygon_cls: type[Multipolygon[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Multipolygon[ScalarT]:
        return multipolygon_cls(
            [
                self.rotate_polygon_around_origin(
                    polygon, cosine, sine, contour_cls, point_cls, polygon_cls
                )
                for polygon in multipolygon.polygons
            ]
        )

    def rotate_multisegment_around_origin(
        self,
        multisegment: Multisegment[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        multisegment_cls: type[Multisegment[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multisegment[ScalarT]:
        return multisegment_cls(
            [
                self.rotate_segment_around_origin(
                    segment, cosine, sine, point_cls, segment_cls
                )
                for segment in multisegment.segments
            ]
        )

    def rotate_polygon_around_origin(
        self,
        polygon: Polygon[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Polygon[ScalarT]:
        return polygon_cls(
            self.rotate_contour_around_origin(
                polygon.border, cosine, sine, contour_cls, point_cls
            ),
            [
                self.rotate_contour_around_origin(
                    hole, cosine, sine, contour_cls, point_cls
                )
                for hole in polygon.holes
            ],
        )

    def rotate_segment_around_origin(
        self,
        segment: Segment[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        return segment_cls(
            self.rotate_point_around_origin(
                segment.start, cosine, sine, point_cls
            ),
            self.rotate_point_around_origin(
                segment.end, cosine, sine, point_cls
            ),
        )

    def rotate_translate_contour(
        self,
        contour: Contour[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Contour[ScalarT]:
        return contour_cls(
            [
                self.rotate_translate_point(
                    point, cosine, sine, step_x, step_y, point_cls
                )
                for point in contour.vertices
            ]
        )

    def rotate_translate_multipoint(
        self,
        multipoint: Multipoint[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Multipoint[ScalarT]:
        return multipoint_cls(
            [
                self.rotate_translate_point(
                    point, cosine, sine, step_x, step_y, point_cls
                )
                for point in multipoint.points
            ]
        )

    def rotate_translate_multipolygon(
        self,
        multipolygon: Multipolygon[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        multipolygon_cls: type[Multipolygon[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Multipolygon[ScalarT]:
        return multipolygon_cls(
            [
                self.rotate_translate_polygon(
                    polygon,
                    cosine,
                    sine,
                    step_x,
                    step_y,
                    contour_cls,
                    point_cls,
                    polygon_cls,
                )
                for polygon in multipolygon.polygons
            ]
        )

    def rotate_translate_multisegment(
        self,
        multisegment: Multisegment[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        multisegment_cls: type[Multisegment[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multisegment[ScalarT]:
        return multisegment_cls(
            [
                self.rotate_translate_segment(
                    segment,
                    cosine,
                    sine,
                    step_x,
                    step_y,
                    point_cls,
                    segment_cls,
                )
                for segment in multisegment.segments
            ]
        )

    def rotate_translate_polygon(
        self,
        polygon: Polygon[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Polygon[ScalarT]:
        return polygon_cls(
            self.rotate_translate_contour(
                polygon.border,
                cosine,
                sine,
                step_x,
                step_y,
                contour_cls,
                point_cls,
            ),
            [
                self.rotate_translate_contour(
                    hole, cosine, sine, step_x, step_y, contour_cls, point_cls
                )
                for hole in polygon.holes
            ],
        )

    def rotate_translate_segment(
        self,
        segment: Segment[ScalarT],
        cosine: ScalarT,
        sine: ScalarT,
        step_x: ScalarT,
        step_y: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        return segment_cls(
            self.rotate_translate_point(
                segment.start, cosine, sine, step_x, step_y, point_cls
            ),
            self.rotate_translate_point(
                segment.end, cosine, sine, step_x, step_y, point_cls
            ),
        )

    _point_to_step: PointToStep[ScalarT]
    _rotate_point_around_origin: PointRotatorAroundOrigin[ScalarT]
    _rotate_translate_point: PointTranslatingRotator[ScalarT]

    __slots__ = (
        '_point_to_step',
        '_rotate_point_around_origin',
        '_rotate_translate_point',
    )

    def __new__(
        cls,
        /,
        *,
        point_to_step: PointToStep[ScalarT],
        rotate_point_around_origin: PointRotatorAroundOrigin[ScalarT],
        rotate_translate_point: PointTranslatingRotator[ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._point_to_step = point_to_step
        self._rotate_point_around_origin = rotate_point_around_origin
        self._rotate_translate_point = rotate_translate_point
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    point_to_step=plain.point_to_step,
    rotate_point_around_origin=plain.rotate_point_around_origin,
    rotate_translate_point=plain.rotate_translate_point,
)
