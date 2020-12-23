from contextvars import ContextVar as _ContextVar

from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.hints import QuaternaryPointFunction as _QuaternaryPointFunction
from .core.plain import (cross as _plain_cross,
                         dot as _plain_dot)
from .core.robust import (cross as _robust_cross,
                          dot as _robust_dot)

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_cross_producer', '_dot_producer'

    def __init__(self, cross_producer: _QuaternaryFunction,
                 dot_producer: _QuaternaryFunction) -> None:
        self._cross_producer, self._dot_producer = cross_producer, dot_producer

    __repr__ = _generate_repr(__init__)

    @property
    def cross_producer(self) -> _QuaternaryFunction:
        return self._cross_producer

    @property
    def dot_producer(self) -> _QuaternaryFunction:
        return self._dot_producer


plain_context = Context(cross_producer=_plain_cross.multiply,
                        dot_producer=_plain_dot.multiply)
robust_context = Context(cross_producer=_robust_cross.multiply,
                         dot_producer=_robust_dot.multiply)

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


def to_cross_producer() -> _QuaternaryFunction:
    return get_context().cross_producer


def to_dot_producer() -> _QuaternaryFunction:
    return get_context().dot_producer
