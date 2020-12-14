import math as _math
import numbers as _numbers
import operator as _operator
from contextvars import ContextVar as _ContextVar
from decimal import Decimal as _Decimal
from fractions import Fraction as _Fraction
from typing import (Callable,
                    Type)

from reprit.base import generate_repr as _generate_repr

from . import hints as _hints

_BinaryOperation = Callable[[_hints.Coordinate, _hints.Coordinate],
                            _hints.Coordinate]
_UnaryOperation = Callable[[_hints.Coordinate], _hints.Coordinate]


class Context:
    __slots__ = '_coordinate_cls', '_divide', '_sqrt'

    def __init__(self,
                 *,
                 coordinate_cls: Type[_hints.Coordinate],
                 divide: _BinaryOperation,
                 sqrt: _UnaryOperation) -> None:
        self._coordinate_cls = coordinate_cls
        self._divide = divide
        self._sqrt = sqrt

    __repr__ = _generate_repr(__init__)

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self._coordinate_cls

    @property
    def divide(self) -> _BinaryOperation:
        return self._divide

    @property
    def sqrt(self) -> _UnaryOperation:
        return self._sqrt


def _rational_sqrt(value: _numbers.Rational) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator)
                                  .sqrt())


def _real_robust_divide(dividend: _numbers.Real,
                        divisor: _numbers.Real) -> _numbers.Real:
    return (_Fraction(dividend, divisor)
            if isinstance(dividend, int)
            else dividend / divisor)


def _real_sqrt(value: _numbers.Real) -> _Fraction:
    return _Fraction.from_decimal((_Decimal(value.numerator)
                                   / value.denominator
                                   if isinstance(value, _Fraction)
                                   else _Decimal(value))
                                  .sqrt())


float_context = Context(coordinate_cls=float,
                        divide=_operator.truediv,
                        sqrt=_math.sqrt)
rational_context = Context(coordinate_cls=_numbers.Rational,
                           divide=_Fraction,
                           sqrt=_rational_sqrt)
real_context = Context(coordinate_cls=_numbers.Real,
                       divide=_real_robust_divide,
                       sqrt=_real_sqrt)

_context = _ContextVar('context',
                       default=real_context)


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    _context.set(context)


def to_coordinate_cls() -> Type[_hints.Coordinate]:
    return get_context().coordinate_cls


def to_divide() -> _BinaryOperation:
    return get_context().divide


def to_sqrt() -> _UnaryOperation:
    return get_context().sqrt
