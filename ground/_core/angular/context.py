from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.enums import Kind, Orientation
from ground._core.hints import HasRepr, Point, ScalarT

from .plain import kind as plain_kind, orientation as plain_orientation

AngularKindEvaluator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT], Kind
]
AngularOrientationEvaluator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT], Orientation
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def kind(self, /) -> AngularKindEvaluator[ScalarT]:
        return self._kind

    @property
    def orientation(self, /) -> AngularOrientationEvaluator[ScalarT]:
        return self._orientation

    _kind: AngularKindEvaluator[ScalarT]
    _orientation: AngularOrientationEvaluator[ScalarT]

    __slots__ = '_kind', '_orientation'

    def __new__(
        cls,
        /,
        *,
        kind: AngularKindEvaluator[ScalarT],
        orientation: AngularOrientationEvaluator[ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._kind, self._orientation = kind, orientation
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    kind=plain_kind, orientation=plain_orientation
)
