from operator import eq
from typing import (Sequence,
                    TypeVar)

from reprit.base import generate_repr

from . import hints


class Point:
    __slots__ = '_x', '_y'

    def __init__(self, x: hints.Scalar, y: hints.Scalar) -> None:
        self._x, self._y = x, y

    @property
    def x(self) -> hints.Scalar:
        return self._x

    @property
    def y(self) -> hints.Scalar:
        return self._y

    def __eq__(self, other: 'Point') -> bool:
        return (self.x == other.x and self.y == other.y
                if isinstance(other, Point)
                else NotImplemented)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __le__(self, other: 'Point') -> bool:
        return (self.x < other.x or self.x == other.x and self.y <= other.y
                if isinstance(other, Point)
                else NotImplemented)

    def __lt__(self, other: 'Point') -> bool:
        return (self.x < other.x or self.x == other.x and self.y < other.y
                if isinstance(other, Point)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Empty:
    __slots__ = ()

    def __init__(self) -> None:
        pass

    def __eq__(self, other: 'Empty'):
        return isinstance(other, Empty) or NotImplemented

    __repr__ = generate_repr(__init__)


class Multipoint:
    __slots__ = '_points',

    def __init__(self, points: Sequence[hints.Point]) -> None:
        self._points = points

    @property
    def points(self) -> Sequence[hints.Point]:
        return self._points

    def __eq__(self, other: 'Multipoint') -> bool:
        return (are_sequences_equivalent(self.points, other.points)
                if isinstance(other, Multipoint)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Segment:
    __slots__ = '_start', '_end'

    def __init__(self, start: hints.Point, end: hints.Point) -> None:
        self._start, self._end = start, end

    @property
    def start(self) -> hints.Point:
        return self._start

    @property
    def end(self) -> hints.Point:
        return self._end

    def __eq__(self, other: 'Segment') -> bool:
        return (self.start == other.start and self.end == other.end
                or self.start == other.end and self.end == other.start
                if isinstance(other, Segment)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Multisegment:
    __slots__ = '_segments',

    def __init__(self, segments: Sequence[hints.Segment]) -> None:
        self._segments = segments

    @property
    def segments(self) -> Sequence[hints.Segment]:
        return self._segments

    def __eq__(self, other: 'Multisegment') -> bool:
        return (are_sequences_equivalent(self.segments, other.segments)
                if isinstance(other, Multisegment)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Contour:
    __slots__ = '_vertices',

    def __init__(self, vertices: Sequence[hints.Polygon]) -> None:
        self._vertices = vertices

    @property
    def vertices(self) -> Sequence[hints.Polygon]:
        return self._vertices

    def __eq__(self, other: 'Contour') -> bool:
        return (are_sequences_equivalent(self.vertices, other.vertices)
                if isinstance(other, Contour)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Box:
    __slots__ = '_min_x', '_max_x', '_min_y', '_max_y'

    def __init__(self,
                 min_x: hints.Scalar,
                 max_x: hints.Scalar,
                 min_y: hints.Scalar,
                 max_y: hints.Scalar) -> None:
        self._min_x, self._max_x, self._min_y, self._max_y = (min_x, max_x,
                                                              min_y, max_y)

    @property
    def max_x(self) -> hints.Scalar:
        return self._max_x

    @property
    def max_y(self) -> hints.Scalar:
        return self._max_y

    @property
    def min_x(self) -> hints.Scalar:
        return self._min_x

    @property
    def min_y(self) -> hints.Scalar:
        return self._min_y

    def __eq__(self, other: 'Box') -> bool:
        return (self.min_x == other.min_x and self.max_x == other.max_x
                and self.min_y == other.min_y and self.max_y == other.max_y
                if isinstance(other, Box)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Polygon:
    __slots__ = '_border', '_holes'

    def __init__(self, border: hints.Contour, holes: Sequence[hints.Contour]
                 ) -> None:
        self._border, self._holes = border, holes

    @property
    def border(self) -> hints.Contour:
        return self._border

    @property
    def holes(self) -> Sequence[hints.Contour]:
        return self._holes

    def __eq__(self, other: 'Polygon') -> bool:
        return (self.border == other.border
                and are_sequences_equivalent(self.holes, other.holes)
                if isinstance(other, Polygon)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Multipolygon:
    __slots__ = '_polygons',

    def __init__(self, polygons: Sequence[hints.Polygon]) -> None:
        self._polygons = polygons

    @property
    def polygons(self) -> Sequence[hints.Polygon]:
        return self._polygons

    def __eq__(self, other: 'Multipolygon') -> bool:
        return (are_sequences_equivalent(self.polygons, other.polygons)
                if isinstance(other, Multipolygon)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


class Mix:
    __slots__ = '_discrete', '_linear', '_shaped'

    def __init__(self,
                 discrete: hints.Maybe[hints.Multipoint],
                 linear: hints.Maybe[hints.Linear],
                 shaped: hints.Maybe[hints.Shaped]) -> None:
        self._discrete, self._linear, self._shaped = discrete, linear, shaped

    @property
    def discrete(self) -> hints.Maybe[hints.Multipoint]:
        return self._discrete

    @property
    def linear(self) -> hints.Maybe[hints.Linear]:
        return self._linear

    @property
    def shaped(self) -> hints.Maybe[hints.Shaped]:
        return self._shaped

    def __eq__(self, other: 'Mix') -> bool:
        return (self.discrete == other.discrete
                and self.linear == other.linear
                and self.shaped == other.shaped
                if isinstance(other, Mix)
                else NotImplemented)

    __repr__ = generate_repr(__init__)


_T = TypeVar('_T')


def are_sequences_equivalent(left: Sequence[_T], right: Sequence[_T]) -> bool:
    return len(left) == len(right) and all(map(eq, left, right))
