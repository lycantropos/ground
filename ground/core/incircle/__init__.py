from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.core.hints import QuaternaryPointFunction
from .core.plain import point_point_point as _plain_point_point_point
from .core.robust import point_point_point as _robust_point_point_point

PointPointPointTest = QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_point_point_point_test',

    def __init__(self, point_point_point_test: PointPointPointTest) -> None:
        self._point_point_point_test = point_point_point_test

    __repr__ = _generate_repr(__init__)

    @property
    def point_point_point_test(self) -> PointPointPointTest:
        return self._point_point_point_test


plain_context = Context(point_point_point_test=_plain_point_point_point.test)
robust_context = Context(point_point_point_test=_robust_point_point_point.test)
