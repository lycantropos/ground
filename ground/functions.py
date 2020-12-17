from contextvars import ContextVar as _ContextVar

from reprit.base import generate_repr as _generate_repr

from . import hints as _hints
from .core.cocircular import determinant as _determinant
from .core.hints import QuaternaryPointFunction as _QuaternaryPointFunction
from .core.parallelogram import signed_area as _signed_area
from .core.projection import signed_length as _signed_length

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


def _to_plain_cross_product(first_start: _hints.Point,
                            first_end: _hints.Point,
                            second_start: _hints.Point,
                            second_end: _hints.Point) -> _hints.Coordinate:
    return ((first_end.x - first_start.x) * (second_end.y - second_start.y)
            - (first_end.y - first_start.y) * (second_end.x - second_start.x))


def _to_plain_dot_product(first_start: _hints.Point,
                          first_end: _hints.Point,
                          second_start: _hints.Point,
                          second_end: _hints.Point) -> _hints.Coordinate:
    return ((first_end.x - first_start.x) * (second_end.x - second_start.x)
            + (first_end.y - first_start.y) * (second_end.y - second_start.y))


def _to_plain_incircle_determinant(first: _hints.Point,
                                   second: _hints.Point,
                                   third: _hints.Point,
                                   fourth: _hints.Point) -> _hints.Coordinate:
    first_dx, first_dy = first.x - fourth.x, first.y - fourth.y
    second_dx, second_dy = second.x - fourth.x, second.y - fourth.y
    third_dx, third_dy = third.x - fourth.x, third.y - fourth.y
    return ((first_dx * first_dx + first_dy * first_dy)
            * (second_dx * third_dy - second_dy * third_dx)
            - (second_dx * second_dx + second_dy * second_dy)
            * (first_dx * third_dy - first_dy * third_dx)
            + (third_dx * third_dx + third_dy * third_dy)
            * (first_dx * second_dy - first_dy * second_dx))


def _to_robust_cross_product(first_start: _hints.Point,
                             first_end: _hints.Point,
                             second_start: _hints.Point,
                             second_end: _hints.Point) -> _hints.Coordinate:
    return _signed_area(first_start.x, first_start.y, first_end.x, first_end.y,
                        second_start.x, second_start.y, second_end.x,
                        second_end.y)


def _to_robust_dot_product(first_start: _hints.Point,
                           first_end: _hints.Point,
                           second_start: _hints.Point,
                           second_end: _hints.Point) -> _hints.Coordinate:
    return _signed_length(first_start.x, first_start.y, first_end.x,
                          first_end.y, second_start.x, second_start.y,
                          second_end.x, second_end.y)


def _to_robust_incircle_determinant(first: _hints.Point,
                                    second: _hints.Point,
                                    third: _hints.Point,
                                    fourth: _hints.Point) -> _hints.Coordinate:
    return _determinant(first.x, first.y, second.x, second.y, third.x, third.y,
                        fourth.x, fourth.y)


plain_context = Context(cross_producer=_to_plain_cross_product,
                        dot_producer=_to_plain_dot_product,
                        incircle_determiner=_to_plain_incircle_determinant)
robust_context = Context(cross_producer=_to_robust_cross_product,
                         dot_producer=_to_robust_dot_product,
                         incircle_determiner=_to_robust_incircle_determinant)

_context_factory = _ContextVar('context',
                               default=robust_context)


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
