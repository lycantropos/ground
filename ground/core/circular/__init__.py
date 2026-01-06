from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr

from ground.core.enums import Location
from ground.core.hints import Point, ScalarT

from .plain import point_point_point as plain_point_point_point

PointPointPointLocator: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT], Point[ScalarT], Point[ScalarT], ScalarT],
    Location,
]


class Context(Generic[ScalarT]):
    @property
    def point_point_point_locator(self, /) -> PointPointPointLocator[ScalarT]:
        return self._point_point_point_test

    __slots__ = ('_point_point_point_test',)

    def __init__(
        self, point_point_point_test: PointPointPointLocator[ScalarT], /
    ) -> None:
        self._point_point_point_test = point_point_point_test

    def __repr__(self, /) -> str:
        return _context_repr(self)


_context_repr = generate_repr(
    Context.__init__,
    argument_serializer=serializers.complex_,
    with_module_name=True,
)

plain_context: Context[Any] = Context(plain_point_point_point.test)
