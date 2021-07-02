import sys
from collections import OrderedDict
from typing import (Callable,
                    Type,
                    Union)

from ground.core.hints import (Empty,
                               Mix,
                               Multipoint,
                               Multisegment,
                               Point,
                               Scalar,
                               Segment)
from ground.core.packing import (pack_mix,
                                 pack_points,
                                 pack_segments)
from . import (exact,
               plain,
               robust)

PointScaler = Callable[[Point, Scalar, Scalar, Type[Point]], Point]

unique_ever_seen = (dict.fromkeys
                    if sys.version_info >= (3, 6)
                    else OrderedDict.fromkeys)


class Context:
    @property
    def scale_point(self) -> PointScaler:
        return self._scale_point

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

    def scale_multisegment(self,
                           multisegment: Multisegment,
                           factor_x: Scalar,
                           factor_y: Scalar,
                           empty: Empty,
                           mix_cls: Type[Mix],
                           multipoint_cls: Type[Multipoint],
                           multisegment_cls: Type[Multisegment],
                           point_cls: Type[Point],
                           segment_cls: Type[Segment]) -> Multisegment:
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

    __slots__ = '_scale_point'

    def __init__(self, scale_point: PointScaler) -> None:
        self._scale_point = scale_point


exact_context = Context(exact.scale_point)
plain_context = Context(plain.scale_point)
robust_context = Context(robust.scale_point)


def is_segment_horizontal(segment: Segment) -> bool:
    return segment.start.y == segment.end.y


def is_segment_vertical(segment: Segment) -> bool:
    return segment.start.x == segment.end.x
