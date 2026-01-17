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

PointTranslator: TypeAlias = Callable[
    [Point[ScalarT], ScalarT, ScalarT, type[Point[ScalarT]]], Point[ScalarT]
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def translate_point(self, /) -> PointTranslator[ScalarT]:
        return self._translate_point

    def translate_contour(
        self,
        contour: Contour[ScalarT],
        step_x: ScalarT,
        step_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Contour[ScalarT]:
        return contour_cls(
            [
                self.translate_point(vertex, step_x, step_y, point_cls)
                for vertex in contour.vertices
            ]
        )

    def translate_multipoint(
        self,
        multipoint: Multipoint[ScalarT],
        step_x: ScalarT,
        step_y: ScalarT,
        multipoint_cls: type[Multipoint[ScalarT]],
        point_cls: type[Point[ScalarT]],
        /,
    ) -> Multipoint[ScalarT]:
        return multipoint_cls(
            [
                self.translate_point(point, step_x, step_y, point_cls)
                for point in multipoint.points
            ]
        )

    def translate_multipolygon(
        self,
        multipolygon: Multipolygon[ScalarT],
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
                self.translate_polygon(
                    polygon,
                    step_x,
                    step_y,
                    contour_cls,
                    point_cls,
                    polygon_cls,
                )
                for polygon in multipolygon.polygons
            ]
        )

    def translate_multisegment(
        self,
        multisegment: Multisegment[ScalarT],
        step_x: ScalarT,
        step_y: ScalarT,
        multisegment_cls: type[Multisegment[ScalarT]],
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Multisegment[ScalarT]:
        return multisegment_cls(
            [
                self.translate_segment(
                    segment, step_x, step_y, point_cls, segment_cls
                )
                for segment in multisegment.segments
            ]
        )

    def translate_polygon(
        self,
        polygon: Polygon[ScalarT],
        step_x: ScalarT,
        step_y: ScalarT,
        contour_cls: type[Contour[ScalarT]],
        point_cls: type[Point[ScalarT]],
        polygon_cls: type[Polygon[ScalarT]],
        /,
    ) -> Polygon[ScalarT]:
        return polygon_cls(
            self.translate_contour(
                polygon.border, step_x, step_y, contour_cls, point_cls
            ),
            [
                self.translate_contour(
                    hole, step_x, step_y, contour_cls, point_cls
                )
                for hole in polygon.holes
            ],
        )

    def translate_segment(
        self,
        segment: Segment[ScalarT],
        step_x: ScalarT,
        step_y: ScalarT,
        point_cls: type[Point[ScalarT]],
        segment_cls: type[Segment[ScalarT]],
        /,
    ) -> Segment[ScalarT]:
        return segment_cls(
            self.translate_point(segment.start, step_x, step_y, point_cls),
            self.translate_point(segment.end, step_x, step_y, point_cls),
        )

    _translate_point: PointTranslator[ScalarT]

    __slots__ = ('_translate_point',)

    def __new__(cls, /, *, translate_point: PointTranslator[ScalarT]) -> Self:
        self = super().__new__(cls)
        self._translate_point = translate_point
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(translate_point=plain.translate_point)
