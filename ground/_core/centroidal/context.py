from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import (
    Contour,
    HasRepr,
    Multipoint,
    Multipolygon,
    Multisegment,
    Point,
    Polygon,
    ScalarFactory,
    ScalarT,
    Segment,
    SquareRooter,
)

from .plain import (
    contour as plain_contour,
    multipoint as plain_multipoint,
    multipolygon as plain_multipolygon,
    multisegment as plain_multisegment,
    polygon as plain_polygon,
    region as plain_region,
    segment as plain_segment,
)

ContourCentroid: TypeAlias = Callable[
    [
        Contour[ScalarT],
        ScalarFactory[ScalarT],
        type[Point[ScalarT]],
        SquareRooter[ScalarT],
    ],
    Point[ScalarT],
]
MultipointCentroid: TypeAlias = Callable[
    [Multipoint[ScalarT], ScalarFactory[ScalarT], type[Point[ScalarT]]],
    Point[ScalarT],
]
MultipolygonCentroid: TypeAlias = Callable[
    [Multipolygon[ScalarT], ScalarFactory[ScalarT], type[Point[ScalarT]]],
    Point[ScalarT],
]
MultisegmentCentroid: TypeAlias = Callable[
    [
        Multisegment[ScalarT],
        ScalarFactory[ScalarT],
        type[Point[ScalarT]],
        SquareRooter[ScalarT],
    ],
    Point[ScalarT],
]
PolygonCentroid: TypeAlias = Callable[
    [Polygon[ScalarT], ScalarFactory[ScalarT], type[Point[ScalarT]]],
    Point[ScalarT],
]
RegionCentroid: TypeAlias = Callable[
    [Contour[ScalarT], ScalarFactory[ScalarT], type[Point[ScalarT]]],
    Point[ScalarT],
]
SegmentCentroid: TypeAlias = Callable[
    [Segment[ScalarT], ScalarFactory[ScalarT], type[Point[ScalarT]]],
    Point[ScalarT],
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def contour_centroid(self, /) -> ContourCentroid[ScalarT]:
        return self._contour_centroid

    @property
    def multipoint_centroid(self, /) -> MultipointCentroid[ScalarT]:
        return self._multipoint_centroid

    @property
    def multipolygon_centroid(self, /) -> MultipolygonCentroid[ScalarT]:
        return self._multipolygon_centroid

    @property
    def multisegment_centroid(self, /) -> MultisegmentCentroid[ScalarT]:
        return self._multisegment_centroid

    @property
    def polygon_centroid(self, /) -> PolygonCentroid[ScalarT]:
        return self._polygon_centroid

    @property
    def region_centroid(self, /) -> RegionCentroid[ScalarT]:
        return self._region_centroid

    @property
    def segment_centroid(self, /) -> SegmentCentroid[ScalarT]:
        return self._segment_centroid

    _contour_centroid: ContourCentroid[ScalarT]
    _multipoint_centroid: MultipointCentroid[ScalarT]
    _multipolygon_centroid: MultipolygonCentroid[ScalarT]
    _multisegment_centroid: MultisegmentCentroid[ScalarT]
    _polygon_centroid: PolygonCentroid[ScalarT]
    _region_centroid: RegionCentroid[ScalarT]
    _segment_centroid: SegmentCentroid[ScalarT]

    __slots__ = (
        '_contour_centroid',
        '_multipoint_centroid',
        '_multipolygon_centroid',
        '_multisegment_centroid',
        '_polygon_centroid',
        '_region_centroid',
        '_segment_centroid',
    )

    def __new__(
        cls,
        /,
        *,
        contour_centroid: ContourCentroid[ScalarT],
        multipoint_centroid: MultipointCentroid[ScalarT],
        multipolygon_centroid: MultipolygonCentroid[ScalarT],
        multisegment_centroid: MultisegmentCentroid[ScalarT],
        polygon_centroid: PolygonCentroid[ScalarT],
        region_centroid: RegionCentroid[ScalarT],
        segment_centroid: SegmentCentroid[ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._contour_centroid = contour_centroid
        self._multipoint_centroid = multipoint_centroid
        self._multipolygon_centroid = multipolygon_centroid
        self._multisegment_centroid = multisegment_centroid
        self._polygon_centroid = polygon_centroid
        self._region_centroid = region_centroid
        self._segment_centroid = segment_centroid
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    contour_centroid=plain_contour.centroid,
    multipoint_centroid=plain_multipoint.centroid,
    multipolygon_centroid=plain_multipolygon.centroid,
    multisegment_centroid=plain_multisegment.centroid,
    polygon_centroid=plain_polygon.centroid,
    region_centroid=plain_region.centroid,
    segment_centroid=plain_segment.centroid,
)
