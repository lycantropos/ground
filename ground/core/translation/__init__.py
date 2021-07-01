from typing import (Callable,
                    Type)

from ground.core.hints import (Multisegment,
                               Point,
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

    __slots__ = '_translate_point'

    def __init__(self, translate_point: PointTranslator) -> None:
        self._translate_point = translate_point


exact_context = Context(exact.translate_point)
plain_context = Context(plain.translate_point)
robust_context = Context(robust.translate_point)
