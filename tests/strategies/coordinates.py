import sys
from decimal import Decimal
from fractions import Fraction

from hypothesis import strategies

from ground.hints import Coordinate
from tests.hints import Strategy

MAX_COORDINATE = 10 ** 10
MIN_COORDINATE = -MAX_COORDINATE


def to_floats(min_value: Coordinate,
              max_value: Coordinate) -> Strategy:
    return (strategies.floats(min_value=min_value,
                              max_value=max_value,
                              allow_nan=False,
                              allow_infinity=False)
            .map(to_digits_count))


def to_digits_count(number: float,
                    *,
                    max_digits_count: int = sys.float_info.dig) -> float:
    decimal = Decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, max(max_digits_count - whole_digits_count, 0))
    return float(str(decimal))


rational_coordinates_strategies_factories = {Fraction: strategies.fractions,
                                             int: strategies.integers}
coordinates_strategies_factories = {
    **rational_coordinates_strategies_factories,
    float: to_floats}
coordinates_types = strategies.sampled_from(
        list(coordinates_strategies_factories.keys()))
coordinates_strategies = strategies.sampled_from(
        [factory(MIN_COORDINATE, MAX_COORDINATE)
         for factory in coordinates_strategies_factories.values()])
coordinates_types_with_strategies = strategies.sampled_from(
        [(type_, factory(MIN_COORDINATE, MAX_COORDINATE))
         for type_, factory in coordinates_strategies_factories.items()])
rational_coordinates_types_with_strategies = strategies.sampled_from(
        [(type_, factory(MIN_COORDINATE, MAX_COORDINATE))
         for type_, factory
         in rational_coordinates_strategies_factories.items()])
