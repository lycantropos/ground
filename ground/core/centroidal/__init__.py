from typing import (Callable,
                    Type)

from reprit.base import generate_repr

from ground.core.hints import UnaryCoordinateOperation
from ground.hints import (Contour,
                          Multipoint,
                          Point)
from .plain import (contour as plain_contour,
                    multipoint as plain_multipoint)
from .robust import (contour as robust_contour,
                     multipoint as robust_multipoint)

MultipointCentroid = Callable[[Type[Point], Multipoint], Point]
ContourCentroid = Callable[[UnaryCoordinateOperation, Type[Point], Contour],
                           Point]


class Context:
    __slots__ = '_contour_centroid', '_multipoint_centroid'

    def __init__(self,
                 contour_centroid: ContourCentroid,
                 multipoint_centroid: MultipointCentroid) -> None:
        self._contour_centroid = contour_centroid
        self._multipoint_centroid = multipoint_centroid

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def contour_centroid(self) -> ContourCentroid:
        return self._contour_centroid

    @property
    def multipoint_centroid(self) -> MultipointCentroid:
        return self._multipoint_centroid


plain_context = Context(contour_centroid=plain_contour.centroid,
                        multipoint_centroid=plain_multipoint.centroid)
robust_context = Context(contour_centroid=robust_contour.centroid,
                         multipoint_centroid=robust_multipoint.centroid)
