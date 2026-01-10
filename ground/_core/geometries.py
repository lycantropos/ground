from collections.abc import Sequence
from operator import eq
from typing import Any, Generic, TypeVar

from reprit.base import generate_repr
from typing_extensions import Self

from . import hints


class Point(Generic[hints.ScalarT]):
    @property
    def x(self, /) -> hints.ScalarT:
        return self._x

    @property
    def y(self, /) -> hints.ScalarT:
        return self._y

    _x: hints.ScalarT
    _y: hints.ScalarT

    __slots__ = '_x', '_y'

    def __new__(cls, x: hints.ScalarT, y: hints.ScalarT, /) -> Self:
        self = super().__new__(cls)
        self._x, self._y = x, y
        return self

    def __ge__(self, other: Self, /) -> bool:
        return (
            self.x > other.x or (self.x == other.x and self.y >= other.y)
            if isinstance(other, Point)
            else NotImplemented
        )

    def __gt__(self, other: Self, /) -> bool:
        return (
            self.x > other.x or (self.x == other.x and self.y > other.y)
            if isinstance(other, Point)
            else NotImplemented
        )

    def __eq__(self, other: Any, /) -> Any:
        return (
            self.x == other.x and self.y == other.y
            if isinstance(other, Point)
            else NotImplemented
        )

    def __hash__(self, /) -> int:
        return hash((self.x, self.y))

    def __le__(self, other: Self, /) -> bool:
        return (
            self.x < other.x or (self.x == other.x and self.y <= other.y)
            if isinstance(other, Point)
            else NotImplemented
        )

    def __lt__(self, other: Self, /) -> bool:
        return (
            self.x < other.x or (self.x == other.x and self.y < other.y)
            if isinstance(other, Point)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _point_repr(self)


_point_repr = generate_repr(Point.__new__)


class Empty(Generic[hints.ScalarT]):
    __slots__ = ()

    def __new__(cls, /) -> Self:
        return super().__new__(cls)

    def __eq__(self, other: Any, /) -> Any:
        return isinstance(other, Empty) or NotImplemented

    def __repr__(self, /) -> str:
        return _empty_repr(self)


_empty_repr = generate_repr(Empty.__new__)


class Multipoint(Generic[hints.ScalarT]):
    @property
    def points(self, /) -> Sequence[hints.Point[hints.ScalarT]]:
        return self._points

    _points: Sequence[hints.Point[hints.ScalarT]]

    __slots__ = ('_points',)

    def __new__(cls, points: Sequence[hints.Point[hints.ScalarT]], /) -> Self:
        self = super().__new__(cls)
        self._points = points
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            are_sequences_equivalent(self._points, other._points)
            if isinstance(other, Multipoint)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _multipoint_repr(self)


_multipoint_repr = generate_repr(Multipoint.__new__)


class Segment(Generic[hints.ScalarT]):
    @property
    def start(self, /) -> hints.Point[hints.ScalarT]:
        return self._start

    @property
    def end(self, /) -> hints.Point[hints.ScalarT]:
        return self._end

    _start: hints.Point[hints.ScalarT]
    _end: hints.Point[hints.ScalarT]

    __slots__ = '_end', '_start'

    def __new__(
        cls,
        start: hints.Point[hints.ScalarT],
        end: hints.Point[hints.ScalarT],
        /,
    ) -> Self:
        self = super().__new__(cls)
        self._start, self._end = start, end
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            (self.start == other.start and self.end == other.end)
            or (self.start == other.end and self.end == other.start)
            if isinstance(other, Segment)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _segment_repr(self)


_segment_repr = generate_repr(Segment.__new__)


class Multisegment(Generic[hints.ScalarT]):
    @property
    def segments(self, /) -> Sequence[hints.Segment[hints.ScalarT]]:
        return self._segments

    _segments: Sequence[hints.Segment[hints.ScalarT]]

    __slots__ = ('_segments',)

    def __new__(
        cls, segments: Sequence[hints.Segment[hints.ScalarT]], /
    ) -> Self:
        self = super().__new__(cls)
        self._segments = segments
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            are_sequences_equivalent(self.segments, other.segments)
            if isinstance(other, Multisegment)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _multisegment_repr(self)


_multisegment_repr = generate_repr(Multisegment.__new__)


class Contour(Generic[hints.ScalarT]):
    @property
    def vertices(self, /) -> Sequence[hints.Point[hints.ScalarT]]:
        return self._vertices

    _vertices: Sequence[hints.Point[hints.ScalarT]]

    __slots__ = ('_vertices',)

    def __new__(
        cls, vertices: Sequence[hints.Point[hints.ScalarT]], /
    ) -> Self:
        self = super().__new__(cls)
        self._vertices = vertices
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            are_sequences_equivalent(self.vertices, other.vertices)
            if isinstance(other, Contour)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _contour_repr(self)


_contour_repr = generate_repr(Contour.__new__)


class Box(Generic[hints.ScalarT]):
    @property
    def max_x(self, /) -> hints.ScalarT:
        return self._max_x

    @property
    def max_y(self, /) -> hints.ScalarT:
        return self._max_y

    @property
    def min_x(self, /) -> hints.ScalarT:
        return self._min_x

    @property
    def min_y(self, /) -> hints.ScalarT:
        return self._min_y

    _min_x: hints.ScalarT
    _max_x: hints.ScalarT
    _min_y: hints.ScalarT
    _max_y: hints.ScalarT

    __slots__ = '_max_x', '_max_y', '_min_x', '_min_y'

    def __new__(
        cls,
        min_x: hints.ScalarT,
        max_x: hints.ScalarT,
        min_y: hints.ScalarT,
        max_y: hints.ScalarT,
        /,
    ) -> Self:
        self = super().__new__(cls)
        self._min_x, self._max_x, self._min_y, self._max_y = (
            min_x,
            max_x,
            min_y,
            max_y,
        )
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            self.min_x == other.min_x
            and self.max_x == other.max_x
            and self.min_y == other.min_y
            and self.max_y == other.max_y
            if isinstance(other, Box)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _box_repr(self)


_box_repr = generate_repr(Box.__new__)


class Polygon(Generic[hints.ScalarT]):
    @property
    def border(self, /) -> hints.Contour[hints.ScalarT]:
        return self._border

    @property
    def holes(self, /) -> Sequence[hints.Contour[hints.ScalarT]]:
        return self._holes

    _border: hints.Contour[hints.ScalarT]
    _holes: Sequence[hints.Contour[hints.ScalarT]]

    __slots__ = '_border', '_holes'

    def __new__(
        cls,
        border: hints.Contour[hints.ScalarT],
        holes: Sequence[hints.Contour[hints.ScalarT]],
        /,
    ) -> Self:
        self = super().__new__(cls)
        self._border, self._holes = border, holes
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            self.border == other.border
            and are_sequences_equivalent(self.holes, other.holes)
            if isinstance(other, Polygon)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _polygon_repr(self)


_polygon_repr = generate_repr(Polygon.__new__)


class Multipolygon(Generic[hints.ScalarT]):
    @property
    def polygons(self, /) -> Sequence[hints.Polygon[hints.ScalarT]]:
        return self._polygons

    _polygons: Sequence[hints.Polygon[hints.ScalarT]]

    __slots__ = ('_polygons',)

    def __new__(cls, polygons: Sequence[hints.Polygon[hints.ScalarT]]) -> Self:
        self = super().__new__(cls)
        self._polygons = polygons
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            are_sequences_equivalent(self.polygons, other.polygons)
            if isinstance(other, Multipolygon)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _multipolygon_repr(self)


_multipolygon_repr = generate_repr(Multipolygon.__new__)


class Mix(Generic[hints.ScalarT]):
    @property
    def discrete(
        self,
    ) -> hints.Empty[hints.ScalarT] | hints.Multipoint[hints.ScalarT]:
        return self._discrete

    @property
    def linear(
        self,
    ) -> hints.Empty[hints.ScalarT] | hints.Linear[hints.ScalarT]:
        return self._linear

    @property
    def shaped(
        self,
    ) -> hints.Empty[hints.ScalarT] | hints.Shaped[hints.ScalarT]:
        return self._shaped

    _discrete: hints.Empty[hints.ScalarT] | hints.Multipoint[hints.ScalarT]
    _linear: hints.Empty[hints.ScalarT] | hints.Linear[hints.ScalarT]
    _shaped: hints.Empty[hints.ScalarT] | hints.Shaped[hints.ScalarT]

    __slots__ = '_discrete', '_linear', '_shaped'

    def __new__(
        cls,
        discrete: hints.Empty[hints.ScalarT] | hints.Multipoint[hints.ScalarT],
        linear: hints.Empty[hints.ScalarT] | hints.Linear[hints.ScalarT],
        shaped: hints.Empty[hints.ScalarT] | hints.Shaped[hints.ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._discrete, self._linear, self._shaped = discrete, linear, shaped
        return self

    def __eq__(self, other: Any, /) -> Any:
        return (
            self.discrete == other.discrete
            and self.linear == other.linear
            and self.shaped == other.shaped
            if isinstance(other, Mix)
            else NotImplemented
        )

    def __repr__(self, /) -> str:
        return _mix_repr(self)


_mix_repr = generate_repr(Mix.__new__)

_T = TypeVar('_T')


def are_sequences_equivalent(
    left: Sequence[_T], right: Sequence[_T], /
) -> bool:
    return len(left) == len(right) and all(map(eq, left, right))
