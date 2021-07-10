from typing import (Callable,
                    Type)

from reprit import serializers
from reprit.base import generate_repr

from ground.core.hints import (Contour,
                               Multipoint,
                               Multipolygon,
                               Multisegment,
                               Point,
                               Polygon,
                               Scalar,
                               Segment)
from . import (exact,
               plain,
               robust)

PointTranslator = Callable[[Point, Scalar, Scalar, Type[Point]], Point]


class Context:
    @property
    def translate_point(self) -> PointTranslator:
        return self._translate_point

    def translate_contour(self,
                          contour: Contour,
                          step_x: Scalar,
                          step_y: Scalar,
                          contour_cls: Type[Contour],
                          point_cls: Type[Point]) -> Contour:
        return contour_cls([self.translate_point(vertex, step_x, step_y,
                                                 point_cls)
                            for vertex in contour.vertices])

    def translate_multipoint(self,
                             multipoint: Multipoint,
                             step_x: Scalar,
                             step_y: Scalar,
                             multipoint_cls: Type[Multipoint],
                             point_cls: Type[Point]) -> Multipoint:
        return multipoint_cls([self.translate_point(point, step_x, step_y,
                                                    point_cls)
                               for point in multipoint.points])

    def translate_multipolygon(self,
                               multipolygon: Multipolygon,
                               step_x: Scalar,
                               step_y: Scalar,
                               contour_cls: Type[Contour],
                               multipolygon_cls: Type[Multipolygon],
                               point_cls: Type[Point],
                               polygon_cls: Type[Polygon]) -> Multipolygon:
        return multipolygon_cls(
                [self.translate_polygon(polygon, step_x, step_y, contour_cls,
                                        point_cls, polygon_cls)
                 for polygon in multipolygon.polygons])

    def translate_multisegment(self,
                               multisegment: Multisegment,
                               step_x: Scalar,
                               step_y: Scalar,
                               multisegment_cls: Type[Multisegment],
                               point_cls: Type[Point],
                               segment_cls: Type[Segment]) -> Multisegment:
        return multisegment_cls([self.translate_segment(segment, step_x,
                                                        step_y, point_cls,
                                                        segment_cls)
                                 for segment in multisegment.segments])

    def translate_polygon(self,
                          polygon: Polygon,
                          step_x: Scalar,
                          step_y: Scalar,
                          contour_cls: Type[Contour],
                          point_cls: Type[Point],
                          polygon_cls: Type[Polygon]) -> Polygon:
        return polygon_cls(self.translate_contour(polygon.border, step_x,
                                                  step_y, contour_cls,
                                                  point_cls),
                           [self.translate_contour(hole, step_x, step_y,
                                                   contour_cls, point_cls)
                            for hole in polygon.holes])

    def translate_segment(self,
                          segment: Segment,
                          step_x: Scalar,
                          step_y: Scalar,
                          point_cls: Type[Point],
                          segment_cls: Type[Segment]) -> Segment:
        return segment_cls(self.translate_point(segment.start, step_x, step_y,
                                                point_cls),
                           self.translate_point(segment.end, step_x, step_y,
                                                point_cls))

    __slots__ = '_translate_point',

    def __init__(self, translate_point: PointTranslator) -> None:
        self._translate_point = translate_point

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)


exact_context = Context(exact.translate_point)
plain_context = Context(plain.translate_point)
robust_context = Context(robust.translate_point)
