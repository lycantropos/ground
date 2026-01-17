from collections.abc import Callable
from typing import Any, Generic, TypeAlias

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import (
    Box,
    HasRepr,
    Point,
    QuaternaryPointFunction,
    ScalarFactory,
    ScalarT,
    Segment,
)

from .plain import (
    box as plain_box,
    point as plain_point,
    segment as plain_segment,
)

BoxPointMetric: TypeAlias = Callable[
    [Box[ScalarT], Point[ScalarT], ScalarFactory[ScalarT]], ScalarT
]
BoxSegmentMetric: TypeAlias = Callable[
    [
        Box[ScalarT],
        Segment[ScalarT],
        QuaternaryPointFunction[ScalarT, ScalarT],
        QuaternaryPointFunction[ScalarT, bool],
        ScalarFactory[ScalarT],
        type[Point[ScalarT]],
    ],
    ScalarT,
]
PointPointMetric: TypeAlias = Callable[
    [Point[ScalarT], Point[ScalarT]], ScalarT
]
SegmentPointMetric: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        QuaternaryPointFunction[ScalarT, ScalarT],
        ScalarFactory[ScalarT],
    ],
    ScalarT,
]
SegmentSegmentMetric: TypeAlias = Callable[
    [
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        Point[ScalarT],
        QuaternaryPointFunction[ScalarT, ScalarT],
        QuaternaryPointFunction[ScalarT, bool],
        ScalarFactory[ScalarT],
    ],
    ScalarT,
]


class Context(HasRepr, Generic[ScalarT]):
    @property
    def box_point_squared_metric(self, /) -> BoxPointMetric[ScalarT]:
        return self._box_point_squared_metric

    @property
    def box_segment_squared_metric(self, /) -> BoxSegmentMetric[ScalarT]:
        return self._box_segment_squared_metric

    @property
    def point_point_squared_metric(self, /) -> PointPointMetric[ScalarT]:
        return self._point_point_squared_metric

    @property
    def segment_point_squared_metric(self, /) -> SegmentPointMetric[ScalarT]:
        return self._segment_point_squared_metric

    @property
    def segment_segment_squared_metric(
        self, /
    ) -> SegmentSegmentMetric[ScalarT]:
        return self._segment_segment_squared_metric

    _box_point_squared_metric: BoxPointMetric[ScalarT]
    _box_segment_squared_metric: BoxSegmentMetric[ScalarT]
    _point_point_squared_metric: PointPointMetric[ScalarT]
    _segment_point_squared_metric: SegmentPointMetric[ScalarT]
    _segment_segment_squared_metric: SegmentSegmentMetric[ScalarT]

    __slots__ = (
        '_box_point_squared_metric',
        '_box_segment_squared_metric',
        '_point_point_squared_metric',
        '_segment_point_squared_metric',
        '_segment_segment_squared_metric',
    )

    def __new__(
        cls,
        /,
        *,
        box_point_squared_metric: BoxPointMetric[ScalarT],
        box_segment_squared_metric: BoxSegmentMetric[ScalarT],
        point_point_squared_metric: PointPointMetric[ScalarT],
        segment_point_squared_metric: SegmentPointMetric[ScalarT],
        segment_segment_squared_metric: SegmentSegmentMetric[ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._box_point_squared_metric = box_point_squared_metric
        self._box_segment_squared_metric = box_segment_squared_metric
        self._point_point_squared_metric = point_point_squared_metric
        self._segment_point_squared_metric = segment_point_squared_metric
        self._segment_segment_squared_metric = segment_segment_squared_metric
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    box_point_squared_metric=plain_box.point_squared_distance,
    box_segment_squared_metric=plain_box.segment_squared_distance,
    point_point_squared_metric=plain_point.point_squared_distance,
    segment_point_squared_metric=plain_segment.point_squared_distance,
    segment_segment_squared_metric=plain_segment.segment_squared_distance,
)
