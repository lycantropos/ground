from .hints import ScalarT


def square(value: ScalarT, /) -> ScalarT:
    return value * value


def to_sign(value: ScalarT, zero: ScalarT, /) -> int:
    return 1 if value > zero else (-1 if value != zero else 0)
