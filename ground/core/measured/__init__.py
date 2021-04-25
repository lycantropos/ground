from typing import (Callable,
                    Sequence)

from reprit.base import generate_repr

from ground.core.hints import (Coordinate,
                               Point)
from .exact import region as exact_region
from .plain import region as plain_region
from .robust import region as robust_region

SignedRegionMeasure = Callable[[Sequence[Point]], Coordinate]


class Context:
    __slots__ = '_signed_region_measure',

    def __init__(self,
                 *,
                 signed_region_measure: SignedRegionMeasure) -> None:
        self._signed_region_measure = signed_region_measure

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def signed_region_measure(self) -> SignedRegionMeasure:
        return self._signed_region_measure


exact_context = Context(signed_region_measure=exact_region.signed_area)
plain_context = Context(signed_region_measure=plain_region.signed_area)
robust_context = Context(signed_region_measure=robust_region.signed_area)
