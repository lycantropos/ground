from typing import (Callable,
                    Type)

from ground.core.hints import (Point,
                               Scalar)
from . import (exact,
               plain,
               robust)

PointScaler = Callable[[Point, Scalar, Scalar, Type[Point]], Point]


class Context:
    @property
    def scale_point(self) -> PointScaler:
        return self._scale_point

    __slots__ = '_scale_point'

    def __init__(self, scale_point: PointScaler) -> None:
        self._scale_point = scale_point


exact_context = Context(exact.scale_point)
plain_context = Context(plain.scale_point)
robust_context = Context(robust.scale_point)
