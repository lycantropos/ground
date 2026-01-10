from collections.abc import Callable
from typing import Any, Generic

from reprit import serializers
from reprit.base import generate_repr

from ground._core.hints import Contour, ScalarFactory, ScalarT

from .plain import region as plain_region

RegionSignedMeasure = Callable[
    [Contour[ScalarT], ScalarFactory[ScalarT]], ScalarT
]


class Context(Generic[ScalarT]):
    @property
    def region_signed_area(self, /) -> RegionSignedMeasure[ScalarT]:
        return self._region_signed_area

    __slots__ = ('_region_signed_area',)

    def __init__(
        self, region_signed_area: RegionSignedMeasure[ScalarT]
    ) -> None:
        self._region_signed_area = region_signed_area

    def __repr__(self, /) -> str:
        return _context_repr(self)


_context_repr = generate_repr(
    Context.__init__,
    argument_serializer=serializers.complex_,
    with_module_name=True,
)

plain_context: Context[Any] = Context(plain_region.signed_area)
