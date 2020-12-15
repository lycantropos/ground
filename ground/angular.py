from functools import partial as _partial

from .core import angular as _angular
from .core.hints import TernaryPointFunction as _TernaryPointFunction
from .functions import (to_cross_producer as _to_cross_producer,
                        to_dot_producer as _to_dot_producer)

Kind = _angular.Kind
Orientation = _angular.Orientation


def to_classifier() -> _TernaryPointFunction[Kind]:
    return _partial(_angular.kind, _to_dot_producer())


def to_orienteer() -> _TernaryPointFunction[Orientation]:
    return _partial(_angular.orientation, _to_cross_producer())
