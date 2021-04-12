from typing import (Callable,
                    Sequence,
                    Type)

from reprit.base import generate_repr

from ground.core.hints import (Contour,
                               Coordinate,
                               Point,
                               Polygon)
from .exact import (contour as exact_contour,
                    multipoint as exact_multipoint,
                    multipolygon as exact_multipolygon,
                    polygon as exact_polygon)
from .plain import (contour as plain_contour,
                    multipoint as plain_multipoint,
                    multipolygon as plain_multipolygon,
                    polygon as plain_polygon)
from .robust import (contour as robust_contour,
                     multipoint as robust_multipoint,
                     multipolygon as robust_multipolygon,
                     polygon as robust_polygon)

ContourCentroid = Callable[[Type[Point], Sequence[Point],
                            Callable[[Coordinate], Coordinate]], Point]
MultipointCentroid = Callable[[Type[Point], Sequence[Point]], Point]
MultipolygonCentroid = Callable[[Type[Point], Sequence[Polygon]], Point]
PolygonCentroid = Callable[[Type[Point], Contour, Sequence[Contour]], Point]


class Context:
    __slots__ = ('_contour_centroid', '_multipoint_centroid',
                 '_multipolygon_centroid', '_polygon_centroid')

    def __init__(self,
                 contour_centroid: ContourCentroid,
                 multipoint_centroid: MultipointCentroid,
                 multipolygon_centroid: MultipolygonCentroid,
                 polygon_centroid: PolygonCentroid) -> None:
        self._contour_centroid = contour_centroid
        self._multipoint_centroid = multipoint_centroid
        self._multipolygon_centroid = multipolygon_centroid
        self._polygon_centroid = polygon_centroid

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def contour_centroid(self) -> ContourCentroid:
        return self._contour_centroid

    @property
    def multipoint_centroid(self) -> MultipointCentroid:
        return self._multipoint_centroid

    @property
    def multipolygon_centroid(self) -> MultipolygonCentroid:
        return self._multipolygon_centroid

    @property
    def polygon_centroid(self) -> PolygonCentroid:
        return self._polygon_centroid


exact_context = Context(contour_centroid=exact_contour.centroid,
                        multipoint_centroid=exact_multipoint.centroid,
                        multipolygon_centroid=exact_multipolygon.centroid,
                        polygon_centroid=exact_polygon.centroid)
plain_context = Context(contour_centroid=plain_contour.centroid,
                        multipoint_centroid=plain_multipoint.centroid,
                        multipolygon_centroid=plain_multipolygon.centroid,
                        polygon_centroid=plain_polygon.centroid)
robust_context = Context(contour_centroid=robust_contour.centroid,
                         multipoint_centroid=robust_multipoint.centroid,
                         multipolygon_centroid=robust_multipolygon.centroid,
                         polygon_centroid=robust_polygon.centroid)
