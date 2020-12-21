import math as _math
import numbers as _numbers
from contextvars import ContextVar as _ContextVar
from decimal import Decimal as _Decimal
from fractions import Fraction as _Fraction
from typing import Type

from reprit.base import generate_repr as _generate_repr

from . import hints as _hints
from .core.hints import (UnaryCoordinatesFunction as _UnaryFunction,
                         UnaryCoordinatesOperation as _UnaryOperation)


class Context:
    __slots__ = '_coordinate_cls', '_rationalizer', '_square_rooter'

    def __init__(self,
                 *,
                 coordinate_cls: Type[_hints.Coordinate],
                 rationalizer: _UnaryFunction[_Fraction],
                 square_rooter: _UnaryOperation) -> None:
        self._coordinate_cls = coordinate_cls
        self._rationalizer = rationalizer
        self._square_rooter = square_rooter

    __repr__ = _generate_repr(__init__)

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self._coordinate_cls

    @property
    def rationalizer(self) -> _UnaryFunction:
        return self._rationalizer

    @property
    def square_rooter(self) -> _UnaryOperation:
        return self._square_rooter


def _rational_sqrt(value: _numbers.Rational) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator)
                                  .sqrt())


def _real_sqrt(value: _numbers.Real) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator
                                   if isinstance(value, _Fraction)
                                   else _Decimal(value))
                                  .sqrt())


float_context = Context(coordinate_cls=float,
                        rationalizer=lambda x: x,
                        square_rooter=_math.sqrt)
rational_context = Context(coordinate_cls=_numbers.Rational,
                           rationalizer=_Fraction,
                           square_rooter=_rational_sqrt)
real_context = Context(coordinate_cls=_numbers.Real,
                       rationalizer=_Fraction,
                       square_rooter=_real_sqrt)

_context = _ContextVar('context',
                       default=real_context)


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    assert isinstance(context, Context), ('expected "{expected}" instance, '
                                          'but got "{actual}".'
                                          .format(expected=Context,
                                                  actual=context))
    _context.set(context)


def to_coordinate_cls() -> Type[_hints.Coordinate]:
    return get_context().coordinate_cls


def to_rationalizer() -> _UnaryFunction:
    return get_context().rationalizer


def to_square_rooter() -> _UnaryOperation:
    return get_context().square_rooter
