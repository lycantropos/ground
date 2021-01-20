from reprit.base import generate_repr

from ground.core.hints import QuaternaryPointFunction
from ground.hints import Coordinate
from .exact import point_point_point as exact_point_point_point
from .plain import point_point_point as plain_point_point_point
from .robust import point_point_point as robust_point_point_point

PointPointPointTest = QuaternaryPointFunction[Coordinate]


class Context:
    __slots__ = '_point_point_point_test',

    def __init__(self, point_point_point_test: PointPointPointTest) -> None:
        self._point_point_point_test = point_point_point_test

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def point_point_point_test(self) -> PointPointPointTest:
        return self._point_point_point_test


exact_context = Context(point_point_point_test=exact_point_point_point.test)
plain_context = Context(point_point_point_test=plain_point_point_point.test)
robust_context = Context(point_point_point_test=robust_point_point_point.test)
