from typing import (Callable,
                    Sequence,
                    Type)

from reprit.base import generate_repr

from ground.core.hints import (Contour,
                               Coordinate,
                               Point,
                               Polygon,
                               Segment)
from .exact import (contour as exact_contour,
                    multipoint as exact_multipoint,
                    multipolygon as exact_multipolygon,
                    multisegment as exact_multisegment,
                    polygon as exact_polygon,
                    region as exact_region)
from .plain import (contour as plain_contour,
                    multipoint as plain_multipoint,
                    multipolygon as plain_multipolygon,
                    multisegment as plain_multisegment,
                    polygon as plain_polygon,
                    region as plain_region)
from .robust import (contour as robust_contour,
                     multipoint as robust_multipoint,
                     multipolygon as robust_multipolygon,
                     multisegment as robust_multisegment,
                     polygon as robust_polygon,
                     region as robust_region)

ContourCentroid = Callable[[Sequence[Point], Type[Point],
                            Callable[[Coordinate], Coordinate]], Point]
MultipointCentroid = RegionCentroid = Callable[[Sequence[Point], Type[Point]],
                                               Point]
MultipolygonCentroid = Callable[[Sequence[Polygon], Type[Point]], Point]
MultisegmentCentroid = Callable[[Sequence[Segment], Type[Point],
                                 Callable[[Coordinate], Coordinate]], Point]
PolygonCentroid = Callable[[Contour, Sequence[Contour], Type[Point]], Point]


class Context:
    __slots__ = ('_contour_centroid', '_multipoint_centroid',
                 '_multipolygon_centroid', '_multisegment_centroid',
                 '_polygon_centroid', '_region_centroid')

    def __init__(self,
                 contour_centroid: ContourCentroid,
                 multipoint_centroid: MultipointCentroid,
                 multipolygon_centroid: MultipolygonCentroid,
                 multisegment_centroid: MultisegmentCentroid,
                 polygon_centroid: PolygonCentroid,
                 region_centroid: RegionCentroid) -> None:
        self._contour_centroid = contour_centroid
        self._multipoint_centroid = multipoint_centroid
        self._multipolygon_centroid = multipolygon_centroid
        self._multisegment_centroid = multisegment_centroid
        self._polygon_centroid = polygon_centroid
        self._region_centroid = region_centroid

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
    def multisegment_centroid(self) -> MultisegmentCentroid:
        return self._multisegment_centroid

    @property
    def polygon_centroid(self) -> PolygonCentroid:
        return self._polygon_centroid

    @property
    def region_centroid(self) -> RegionCentroid:
        return self._region_centroid


exact_context = Context(contour_centroid=exact_contour.centroid,
                        multipoint_centroid=exact_multipoint.centroid,
                        multipolygon_centroid=exact_multipolygon.centroid,
                        multisegment_centroid=exact_multisegment.centroid,
                        polygon_centroid=exact_polygon.centroid,
                        region_centroid=exact_region.centroid)
plain_context = Context(contour_centroid=plain_contour.centroid,
                        multipoint_centroid=plain_multipoint.centroid,
                        multipolygon_centroid=plain_multipolygon.centroid,
                        multisegment_centroid=plain_multisegment.centroid,
                        polygon_centroid=plain_polygon.centroid,
                        region_centroid=plain_region.centroid)
robust_context = Context(contour_centroid=robust_contour.centroid,
                         multipoint_centroid=robust_multipoint.centroid,
                         multipolygon_centroid=robust_multipolygon.centroid,
                         multisegment_centroid=robust_multisegment.centroid,
                         polygon_centroid=robust_polygon.centroid,
                         region_centroid=robust_region.centroid)
