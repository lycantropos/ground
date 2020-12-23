from functools import partial as _partial

from ground.hints import TernaryPointFunction as _TernaryPointFunction
from ground.vector import (to_cross_producer as _to_cross_producer,
                           to_dot_producer as _to_dot_producer)
from .core.base import (kind as _kind,
                        orientation as _orientation)
from .core.enums import (Kind,
                         Orientation)

Kind = Kind
Orientation = Orientation


def to_classifier() -> _TernaryPointFunction[Kind]:
    return _partial(_kind, _to_dot_producer())


def to_orienteer() -> _TernaryPointFunction[Orientation]:
    return _partial(_orientation, _to_cross_producer())
