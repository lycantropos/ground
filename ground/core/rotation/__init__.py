from typing import (Callable,
                    Tuple,
                    Type)

from reprit.base import generate_repr

from ground.core.hints import (Point,
                               Scalar,
                               Segment)
from . import (exact,
               plain,
               robust)

PointRotatorAroundOrigin = Callable[[Point, Scalar, Scalar, Type[Point]],
                                    Point]
PointTranslatingRotator = Callable[[Point, Scalar, Scalar, Scalar, Scalar,
                                    Type[Point]], Point]
PointStep = Callable[[Point, Scalar, Scalar], Tuple[Scalar, Scalar]]


class Context:
    @property
    def point_to_step(self) -> PointStep:
        return self._point_to_step

    @property
    def rotate_point_around_origin(self) -> PointRotatorAroundOrigin:
        return self._rotate_point_around_origin

    @property
    def rotate_translate_point(self) -> PointTranslatingRotator:
        return self._rotate_translate_point

    def rotate_segment_around_origin(self,
                                     segment: Segment,
                                     cosine: Scalar,
                                     sine: Scalar,
                                     point_cls: Type[Point],
                                     segment_cls: Type[Segment]) -> Segment:
        return segment_cls(self.rotate_point_around_origin(segment.start,
                                                           cosine, sine,
                                                           point_cls),
                           self.rotate_point_around_origin(segment.end,
                                                           cosine, sine,
                                                           point_cls))

    def rotate_translate_segment(self,
                                 segment: Segment,
                                 cosine: Scalar,
                                 sine: Scalar,
                                 step_x: Scalar,
                                 step_y: Scalar,
                                 point_cls: Type[Point],
                                 segment_cls: Type[Segment]) -> Segment:
        return segment_cls(self.rotate_translate_point(segment.start, cosine,
                                                       sine, step_x, step_y,
                                                       point_cls),
                           self.rotate_translate_point(segment.end, cosine,
                                                       sine, step_x, step_y,
                                                       point_cls))

    __slots__ = ('_point_to_step', '_rotate_point_around_origin',
                 '_rotate_translate_point')

    def __init__(self,
                 point_to_step: PointStep,
                 rotate_point_around_origin: PointRotatorAroundOrigin,
                 rotate_translate_point: PointTranslatingRotator) -> None:
        self._point_to_step = point_to_step
        self._rotate_point_around_origin = rotate_point_around_origin
        self._rotate_translate_point = rotate_translate_point

    __repr__ = generate_repr(__init__,
                             with_module_name=True)


exact_context = Context(
        point_to_step=exact.point_to_step,
        rotate_point_around_origin=exact.rotate_point_around_origin,
        rotate_translate_point=exact.rotate_translate_point)
plain_context = Context(
        point_to_step=plain.point_to_step,
        rotate_point_around_origin=plain.rotate_point_around_origin,
        rotate_translate_point=plain.rotate_translate_point)
robust_context = Context(
        point_to_step=robust.point_to_step,
        rotate_point_around_origin=robust.rotate_point_around_origin,
        rotate_translate_point=robust.rotate_translate_point)
