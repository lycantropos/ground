from collections.abc import Callable
from typing import Any, Generic

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import Contour, HasRepr, ScalarFactory, ScalarT

from .plain import region as plain_region

RegionSignedMeasure = Callable[
    [Contour[ScalarT], ScalarFactory[ScalarT]], ScalarT
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def region_signed_area(self, /) -> RegionSignedMeasure[ScalarT]:
        return self._region_signed_area

    _region_signed_area: RegionSignedMeasure[ScalarT]
    __slots__ = ('_region_signed_area',)

    def __new__(
        cls, /, *, region_signed_area: RegionSignedMeasure[ScalarT]
    ) -> Self:
        self = super().__new__(cls)
        self._region_signed_area = region_signed_area
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    region_signed_area=plain_region.signed_area
)
