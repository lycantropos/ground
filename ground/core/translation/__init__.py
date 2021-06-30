from typing import (Callable,
                    Type)

from ground.core.hints import (Point,
                               Scalar)
from . import (exact,
               plain,
               robust)

PointTranslator = Callable[[Point, Scalar, Scalar, Type[Point]], Point]


class Context:
    __slots__ = '_translate_point'

    def __init__(self, translate_point: PointTranslator) -> None:
        self._translate_point = translate_point

    @property
    def translate_point(self) -> PointTranslator:
        return self._translate_point


exact_context = Context(exact.translate_point)
plain_context = Context(plain.translate_point)
robust_context = Context(robust.translate_point)