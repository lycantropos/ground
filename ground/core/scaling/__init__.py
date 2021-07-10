import sys
from collections import OrderedDict
from itertools import chain
from typing import (Callable,
                    Iterable,
                    Type,
                    Union)

from reprit import serializers
from reprit.base import generate_repr

from ground.core.hints import (Contour,
                               Empty,
                               Mix,
                               Multipoint,
                               Multipolygon,
                               Multisegment,
                               Point,
                               Polygon,
                               Scalar,
                               Segment)
from ground.core.packing import (pack_mix,
                                 pack_points,
                                 pack_segments)
from . import (exact,
               plain,
               robust)

PointScaler = Callable[[Point, Scalar, Scalar, Type[Point]], Point]


class Context:
    @property
    def scale_point(self) -> PointScaler:
        return self._scale_point

    def scale_contour(self,
                      contour: Contour,
                      factor_x: Scalar,
                      factor_y: Scalar,
                      contour_cls: Type[Contour],
                      multipoint_cls: Type[Multipoint],
                      point_cls: Type[Point],
                      segment_cls: Type[Segment]
                      ) -> Union[Contour, Multipoint, Segment]:
        return (self.scale_contour_non_degenerate(contour, factor_x, factor_y,
                                                  contour_cls, point_cls)
                if factor_x and factor_y
                else self.scale_contour_degenerate(contour, factor_x, factor_y,
                                                   multipoint_cls, point_cls,
                                                   segment_cls))

    def scale_contour_non_degenerate(self,
                                     contour: Contour,
                                     factor_x: Scalar,
                                     factor_y: Scalar,
                                     contour_cls: Type[Contour],
                                     point_cls: Type[Point]) -> Contour:
        return contour_cls([self.scale_point(vertex, factor_x, factor_y,
                                             point_cls)
                            for vertex in contour.vertices])

    def scale_contour_degenerate(self,
                                 contour: Contour,
                                 factor_x: Scalar,
                                 factor_y: Scalar,
                                 multipoint_cls: Type[Multipoint],
                                 point_cls: Type[Point],
                                 segment_cls: Type[Segment]
                                 ) -> Union[Multipoint, Segment]:
        return self.scale_vertices_degenerate(contour.vertices, factor_x,
                                              factor_y, multipoint_cls,
                                              point_cls, segment_cls)

    def scale_multipoint(self,
                         multipoint: Multipoint,
                         factor_x: Scalar,
                         factor_y: Scalar,
                         multipoint_cls: Type[Multipoint],
                         point_cls: Type[Point]) -> Multipoint:
        return multipoint_cls(
                [self.scale_point(point, factor_x, factor_y, point_cls)
                 for point in multipoint.points]
                if factor_x and factor_y
                else
                (list(unique_ever_seen(self.scale_point(point, factor_x,
                                                        factor_y, point_cls)
                                       for point in multipoint.points))
                 if factor_x or factor_y
                 else [point_cls(factor_x, factor_y)]))

    def scale_multipolygon(self,
                           multipolygon: Multipolygon,
                           factor_x: Scalar,
                           factor_y: Scalar,
                           contour_cls: Type[Contour],
                           multipoint_cls: Type[Multipoint],
                           multipolygon_cls: Type[Multipolygon],
                           multisegment_cls: Type[Multisegment],
                           point_cls: Type[Point],
                           polygon_cls: Type[Polygon],
                           segment_cls: Type[Segment]
                           ) -> Union[Multipoint, Multipolygon, Multisegment]:
        return (
            multipolygon_cls(
                    [self.scale_polygon_non_degenerate(polygon, factor_x,
                                                       factor_y, contour_cls,
                                                       point_cls, polygon_cls)
                     for polygon in multipolygon.polygons])
            if factor_x and factor_y
            else
            (multisegment_cls([self.scale_polygon_degenerate(
                    polygon, factor_x, factor_y, multipoint_cls, point_cls,
                    segment_cls)
                for polygon in multipolygon.polygons])
             if factor_x or factor_y
             else multipoint_cls([point_cls(factor_x, factor_y)])))

    def scale_multisegment(self,
                           multisegment: Multisegment,
                           factor_x: Scalar,
                           factor_y: Scalar,
                           empty: Empty,
                           mix_cls: Type[Mix],
                           multipoint_cls: Type[Multipoint],
                           multisegment_cls: Type[Multisegment],
                           point_cls: Type[Point],
                           segment_cls: Type[Segment]
                           ) -> Union[Mix, Multipoint, Multisegment, Segment]:
        scaled_points, scaled_segments = [], []
        for segment in multisegment.segments:
            if ((factor_x or not is_segment_horizontal(segment)) and factor_y
                    or factor_x and not is_segment_vertical(segment)):
                scaled_segments.append(self.scale_segment_non_degenerate(
                        segment, factor_x, factor_y, point_cls, segment_cls))
            else:
                scaled_points.append(self.scale_point(segment.start, factor_x,
                                                      factor_y, point_cls))
        return pack_mix(pack_points(list(unique_ever_seen(scaled_points)),
                                    empty, multipoint_cls),
                        pack_segments(scaled_segments, empty,
                                      multisegment_cls),
                        empty, empty, mix_cls)

    def scale_polygon(self,
                      polygon: Polygon,
                      factor_x: Scalar,
                      factor_y: Scalar,
                      contour_cls: Type[Contour],
                      multipoint_cls: Type[Multipoint],
                      point_cls: Type[Point],
                      polygon_cls: Type[Polygon],
                      segment_cls: Type[Segment]
                      ) -> Union[Multipoint, Polygon, Segment]:
        return (self.scale_polygon_non_degenerate(polygon, factor_x, factor_y,
                                                  contour_cls, point_cls,
                                                  polygon_cls)
                if factor_x and factor_y
                else self.scale_polygon_degenerate(polygon, factor_x, factor_y,
                                                   multipoint_cls, point_cls,
                                                   segment_cls))

    def scale_polygon_degenerate(self,
                                 polygon: Polygon,
                                 factor_x: Scalar,
                                 factor_y: Scalar,
                                 multipoint_cls: Type[Multipoint],
                                 point_cls: Type[Point],
                                 segment_cls: Type[Segment]
                                 ) -> Union[Multipoint, Segment]:
        return self.scale_contour_degenerate(polygon.border, factor_x,
                                             factor_y, multipoint_cls,
                                             point_cls, segment_cls)

    def scale_polygon_non_degenerate(self,
                                     polygon: Polygon,
                                     factor_x: Scalar,
                                     factor_y: Scalar,
                                     contour_cls: Type[Contour],
                                     point_cls: Type[Point],
                                     polygon_cls: Type[Polygon]) -> Polygon:
        return polygon_cls(
                self.scale_contour_non_degenerate(polygon.border, factor_x,
                                                  factor_y, contour_cls,
                                                  point_cls),
                [self.scale_contour_non_degenerate(hole, factor_x, factor_y,
                                                   contour_cls, point_cls)
                 for hole in polygon.holes])

    def scale_segment(self,
                      segment: Segment,
                      factor_x: Scalar,
                      factor_y: Scalar,
                      multipoint_cls: Type[Multipoint],
                      point_cls: Type[Point],
                      segment_cls: Type[Segment]
                      ) -> Union[Multipoint, Segment]:
        return (self.scale_segment_non_degenerate(segment, factor_x, factor_y,
                                                  point_cls, segment_cls)
                if ((factor_x or not is_segment_horizontal(segment))
                    and factor_y
                    or factor_x and not is_segment_vertical(segment))
                else multipoint_cls([self.scale_point(segment.start, factor_x,
                                                      factor_y, point_cls)]))

    def scale_segment_non_degenerate(self,
                                     segment: Segment,
                                     factor_x: Scalar,
                                     factor_y: Scalar,
                                     point_cls: Type[Point],
                                     segment_cls: Type[Segment]) -> Segment:
        return segment_cls(self.scale_point(segment.start, factor_x, factor_y,
                                            point_cls),
                           self.scale_point(segment.end, factor_x, factor_y,
                                            point_cls))

    def scale_vertices_degenerate(self,
                                  vertices: Iterable[Point],
                                  factor_x: Scalar,
                                  factor_y: Scalar,
                                  multipoint_cls: Type[Multipoint],
                                  point_cls: Type[Point],
                                  segment_cls: Type[Segment]
                                  ) -> Union[Segment, Multipoint]:
        return (self.scale_vertices_projecting_on_ox(vertices, factor_x,
                                                     factor_y, point_cls,
                                                     segment_cls)
                if factor_x
                else (self.scale_vertices_projecting_on_oy(vertices, factor_x,
                                                           factor_y, point_cls,
                                                           segment_cls)
                      if factor_y
                      else multipoint_cls([point_cls(factor_x, factor_y)])))

    @staticmethod
    def scale_vertices_projecting_on_ox(vertices: Iterable[Point],
                                        factor_x: Scalar,
                                        factor_y: Scalar,
                                        point_cls: Type[Point],
                                        segment_cls: Type[Segment]) -> Segment:
        vertices = iter(vertices)
        min_x = max_x = next(vertices).x
        for vertex in vertices:
            if min_x > vertex.x:
                min_x = vertex.x
            elif max_x < vertex.x:
                max_x = vertex.x
        return segment_cls(point_cls(min_x * factor_x, factor_y),
                           point_cls(max_x * factor_x, factor_y))

    @staticmethod
    def scale_vertices_projecting_on_oy(vertices: Iterable[Point],
                                        factor_x: Scalar,
                                        factor_y: Scalar,
                                        point_cls: Type[Point],
                                        segment_cls: Type[Segment]) -> Segment:
        vertices = iter(vertices)
        min_y = max_y = next(vertices).y
        for vertex in vertices:
            if min_y > vertex.y:
                min_y = vertex.y
            elif max_y < vertex.y:
                max_y = vertex.y
        return segment_cls(point_cls(factor_x, min_y * factor_y),
                           point_cls(factor_x, max_y * factor_y))

    __slots__ = '_scale_point',

    def __init__(self, scale_point: PointScaler) -> None:
        self._scale_point = scale_point

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)


exact_context = Context(exact.scale_point)
plain_context = Context(plain.scale_point)
robust_context = Context(robust.scale_point)


def is_segment_horizontal(segment: Segment) -> bool:
    return segment.start.y == segment.end.y


def is_segment_vertical(segment: Segment) -> bool:
    return segment.start.x == segment.end.x


flatten = chain.from_iterable
unique_ever_seen = (dict.fromkeys
                    if sys.version_info >= (3, 6)
                    else OrderedDict.fromkeys)
