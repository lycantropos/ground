from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.enums import Location
from ground._core.hints import HasRepr, Point, ScalarT

from .plain import point_point_point as plain_point_point_point

PointPointPointLocator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT],
    Location,
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def point_point_point_locator(self, /) -> PointPointPointLocator[ScalarT]:
        return self._point_point_point_test

    _point_point_point_test: PointPointPointLocator[ScalarT]

    __slots__ = ('_point_point_point_test',)

    def __new__(
        cls, /, *, point_point_point_test: PointPointPointLocator[ScalarT]
    ) -> Self:
        self = super().__new__(cls)
        self._point_point_point_test = point_point_point_test
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    point_point_point_test=plain_point_point_point.test
)
