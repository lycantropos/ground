from contextvars import ContextVar as _ContextVar

from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.hints import QuaternaryPointFunction as _QuaternaryPointFunction
from .core.plain.cocircular import determinant as _plain_determinant
from .core.plain.parallelogram import signed_area as _plain_signed_area
from .core.plain.projection import signed_length as _plain_signed_length
from .core.robust.cocircular import determinant as _robust_determinant
from .core.robust.parallelogram import signed_area as _robust_signed_area
from .core.robust.projection import signed_length as _robust_signed_length

_QuaternaryFunction = _QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_cross_producer', '_dot_producer', '_incircle_determiner'

    def __init__(self,
                 cross_producer: _QuaternaryFunction,
                 dot_producer: _QuaternaryFunction,
                 incircle_determiner: _QuaternaryFunction) -> None:
        self._cross_producer = cross_producer
        self._dot_producer = dot_producer
        self._incircle_determiner = incircle_determiner

    __repr__ = _generate_repr(__init__)

    @property
    def cross_producer(self) -> _QuaternaryFunction:
        return self._cross_producer

    @property
    def dot_producer(self) -> _QuaternaryFunction:
        return self._dot_producer

    @property
    def incircle_determiner(self) -> _QuaternaryFunction:
        return self._incircle_determiner


plain_context = Context(cross_producer=_plain_signed_area,
                        dot_producer=_plain_signed_length,
                        incircle_determiner=_plain_determinant)
robust_context = Context(cross_producer=_robust_signed_area,
                         dot_producer=_robust_signed_length,
                         incircle_determiner=_robust_determinant)

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


def to_incircle_determiner() -> _QuaternaryFunction:
    return get_context().incircle_determiner
