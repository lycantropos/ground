from contextvars import ContextVar as _ContextVar

from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.hints import QuaternaryPointFunction as _QuaternaryPointFunction
from .core.plain import point_point_point as _plain_point_point_point
from .core.robust import point_point_point as _robust_point_point_point

_PointPointPoint = _QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_point_point_point_determiner',

    def __init__(self, point_point_point_determiner: _PointPointPoint) -> None:
        self._point_point_point_determiner = point_point_point_determiner

    __repr__ = _generate_repr(__init__)

    @property
    def point_point_point_determiner(self) -> _PointPointPoint:
        return self._point_point_point_determiner


plain_context = Context(
        point_point_point_determiner=_plain_point_point_point.determine)
robust_context = Context(
        point_point_point_determiner=_robust_point_point_point.determine)

_context_factory = _ContextVar('context',
                               default=plain_context)


def get_context() -> Context:
    return _context_factory.get()


def set_context(context: Context) -> None:
    assert isinstance(context, Context), ('expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context_factory.set(context)


def to_point_point_point_determiner() -> _PointPointPoint:
    return get_context().point_point_point_determiner
