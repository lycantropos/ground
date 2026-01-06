from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr

from ground.core.enums import Kind, Orientation
from ground.core.hints import (
    Point,
    ScalarT,
    TernaryPointFunction as TernaryPointFunction,
)

from .plain import kind as plain_kind, orientation as plain_orientation

AngularKindEvaluator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT], Kind
]
AngularOrientationEvaluator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT], Orientation
]


class Context(Generic[ScalarT]):
    @property
    def kind(self, /) -> AngularKindEvaluator[ScalarT]:
        return self._kind

    @property
    def orientation(self, /) -> AngularOrientationEvaluator[ScalarT]:
        return self._orientation

    __slots__ = '_kind', '_orientation'

    def __init__(
        self,
        /,
        *,
        kind: AngularKindEvaluator[ScalarT],
        orientation: AngularOrientationEvaluator[ScalarT],
    ) -> None:
        self._kind, self._orientation = kind, orientation

    def __repr__(self, /) -> str:
        return _context_repr(self)


_context_repr = generate_repr(
    Context.__init__,
    argument_serializer=serializers.complex_,
    with_module_name=True,
)

plain_context: Context[Any] = Context(
    kind=plain_kind, orientation=plain_orientation
)
