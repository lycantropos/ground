from typing import Callable

from reprit import serializers
from reprit.base import generate_repr

from ground.core.hints import (Contour,
                               Scalar)
from .exact import region as exact_region
from .plain import region as plain_region
from .robust import region as robust_region

RegionSignedMeasure = Callable[[Contour[Scalar]], Scalar]


class Context:
    @property
    def region_signed_area(self) -> RegionSignedMeasure:
        return self._region_signed_area

    __slots__ = '_region_signed_area',

    def __init__(self,
                 region_signed_area: RegionSignedMeasure) -> None:
        self._region_signed_area = region_signed_area

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)


exact_context = Context(exact_region.signed_area)
plain_context = Context(plain_region.signed_area)
robust_context = Context(robust_region.signed_area)
