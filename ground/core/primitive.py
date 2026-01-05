from typing import Any

from .hints import ScalarT


def square(value: ScalarT) -> ScalarT:
    return value * value


def to_sign(value: Any) -> int:
    return 1 if value > 0 else (-1 if value else 0)
