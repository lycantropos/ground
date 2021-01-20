from typing import (Callable,
                    Sequence,
                    Type)

from reprit.base import generate_repr

from ground.hints import Point
from .exact import (contour as exact_contour,
                    multipoint as exact_multipoint)
from .plain import (contour as plain_contour,
                    multipoint as plain_multipoint)
from .robust import (contour as robust_contour,
                     multipoint as robust_multipoint)

ContourCentroid = MultipointCentroid = Callable[[Type[Point], Sequence[Point]],
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


exact_context = Context(contour_centroid=exact_contour.centroid,
                        multipoint_centroid=exact_multipoint.centroid)
plain_context = Context(contour_centroid=plain_contour.centroid,
                        multipoint_centroid=plain_multipoint.centroid)
robust_context = Context(contour_centroid=robust_contour.centroid,
                         multipoint_centroid=robust_multipoint.centroid)
