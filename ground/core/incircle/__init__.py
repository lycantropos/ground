from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.core.hints import QuaternaryPointFunction
from .core.plain import point_point_point as _plain_point_point_point
from .core.robust import point_point_point as _robust_point_point_point

PointPointPointDeterminant = QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_point_point_point_determinant',

    def __init__(self,
                 point_point_point_determinant: PointPointPointDeterminant
                 ) -> None:
        self._point_point_point_determinant = point_point_point_determinant

    __repr__ = _generate_repr(__init__)

    @property
    def point_point_point_determinant(self) -> PointPointPointDeterminant:
        return self._point_point_point_determinant


plain_context = Context(
        point_point_point_determinant=_plain_point_point_point.determine)
robust_context = Context(
        point_point_point_determinant=_robust_point_point_point.determine)
