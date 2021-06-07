from cfractions import Fraction

from .hints import Scalar


def robust_divide(dividend: Scalar, divisor: Scalar) -> Scalar:
    return (dividend / Fraction(divisor)
            if isinstance(divisor, int)
            else dividend / divisor)
