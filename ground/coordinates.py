import math as _math
import numbers as _numbers
import operator as _operator
from contextvars import ContextVar as _ContextVar
from decimal import Decimal as _Decimal
from fractions import Fraction as _Fraction
from typing import Type

from reprit.base import generate_repr as _generate_repr

from . import hints as _hints
from .core.hints import (BinaryCoordinatesOperation as _BinaryOperation,
                         UnaryOperation as _UnaryOperation)


class Context:
    __slots__ = '_coordinate_cls', '_divider', '_square_rooter'

    def __init__(self,
                 *,
                 coordinate_cls: Type[_hints.Coordinate],
                 divider: _BinaryOperation,
                 square_rooter: _UnaryOperation) -> None:
        self._coordinate_cls = coordinate_cls
        self._divider = divider
        self._square_rooter = square_rooter

    __repr__ = _generate_repr(__init__)

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self._coordinate_cls

    @property
    def divider(self) -> _BinaryOperation:
        return self._divider

    @property
    def square_rooter(self) -> _UnaryOperation:
        return self._square_rooter


def _rational_sqrt(value: _numbers.Rational) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator)
                                  .sqrt())


def _real_robust_divide(dividend: _numbers.Real,
                        divisor: _numbers.Real) -> _numbers.Real:
    return (_Fraction(dividend, divisor)
            if isinstance(dividend, int) and isinstance(divisor, int)
            else dividend / divisor)


def _real_sqrt(value: _numbers.Real) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator
                                   if isinstance(value, _Fraction)
                                   else _Decimal(value))
                                  .sqrt())


float_context = Context(coordinate_cls=float,
                        divider=_operator.truediv,
                        square_rooter=_math.sqrt)
rational_context = Context(coordinate_cls=_numbers.Rational,
                           divider=_Fraction,
                           square_rooter=_rational_sqrt)
real_context = Context(coordinate_cls=_numbers.Real,
                       divider=_real_robust_divide,
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


def to_divider() -> _BinaryOperation:
    return get_context().divider


def to_square_rooter() -> _UnaryOperation:
    return get_context().square_rooter
