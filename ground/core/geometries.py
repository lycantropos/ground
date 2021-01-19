from operator import eq
from typing import Sequence

from reprit.base import generate_repr

from ground import hints
from .hints import Domain


class Point:
    __slots__ = '_x', '_y'

    def __init__(self, x: hints.Coordinate, y: hints.Coordinate) -> None:
        self._x, self._y = x, y

    __repr__ = generate_repr(__init__)

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

    @property
    def x(self) -> hints.Coordinate:
        return self._x

    @property
    def y(self) -> hints.Coordinate:
        return self._y


class Multipoint:
    __slots__ = '_points',

    def __init__(self, points: Sequence[hints.Point]) -> None:
        self._points = points

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Multipoint') -> bool:
        return are_sequences_equivalent(self.points, other.points)

    @property
    def points(self) -> Sequence[hints.Point]:
        return self._points


class Segment:
    __slots__ = '_start', '_end'

    def __init__(self, start: hints.Point, end: hints.Point) -> None:
        self._start, self._end = start, end

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Segment') -> bool:
        return (self.start == other.start and self.end == other.end
                or self.start == other.end and self.end == other.start
                if isinstance(other, Segment)
                else NotImplemented)

    @property
    def start(self) -> hints.Point:
        return self._start

    @property
    def end(self) -> hints.Point:
        return self._end


class Multisegment:
    __slots__ = '_segments',

    def __init__(self, segments: Sequence[hints.Segment]) -> None:
        self._segments = segments

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Multisegment') -> bool:
        return are_sequences_equivalent(self.segments, other.segments)

    @property
    def segments(self) -> Sequence[hints.Segment]:
        return self._segments


class Contour:
    __slots__ = '_vertices',

    def __init__(self, vertices: Sequence[hints.Polygon]) -> None:
        self._vertices = vertices

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Contour') -> bool:
        return are_sequences_equivalent(self.vertices, other.vertices)

    @property
    def vertices(self) -> Sequence[hints.Polygon]:
        return self._vertices


class Box:
    __slots__ = '_min_x', '_max_x', '_min_y', '_max_y'

    def __init__(self,
                 min_x: hints.Coordinate,
                 max_x: hints.Coordinate,
                 min_y: hints.Coordinate,
                 max_y: hints.Coordinate) -> None:
        self._min_x, self._max_x, self._min_y, self._max_y = (min_x, max_x,
                                                              min_y, max_y)

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Box') -> bool:
        return (self.min_x == other.min_x and self.max_x == other.max_x
                and self.min_y == other.min_y and self.max_y == other.max_y
                if isinstance(other, Box)
                else NotImplemented)

    @property
    def max_x(self) -> hints.Coordinate:
        return self._max_x

    @property
    def max_y(self) -> hints.Coordinate:
        return self._max_y

    @property
    def min_x(self) -> hints.Coordinate:
        return self._min_x

    @property
    def min_y(self) -> hints.Coordinate:
        return self._min_y


class Polygon:
    __slots__ = '_border', '_holes'

    def __init__(self, border: hints.Contour, holes: Sequence[hints.Contour]
                 ) -> None:
        self._border, self._holes = border, holes

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Polygon') -> bool:
        return (self.border == other.border
                and are_sequences_equivalent(self.holes, other.holes))

    @property
    def border(self) -> hints.Contour:
        return self._border

    @property
    def holes(self) -> Sequence[hints.Contour]:
        return self._holes


class Multipolygon:
    __slots__ = '_polygons',

    def __init__(self, polygons: Sequence[hints.Polygon]) -> None:
        self._polygons = polygons

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Multipolygon') -> bool:
        return are_sequences_equivalent(self.polygons, other.polygons)

    @property
    def polygons(self) -> Sequence[hints.Polygon]:
        return self._polygons


def are_sequences_equivalent(left: Sequence[Domain],
                             right: Sequence[Domain]) -> bool:
    return len(left) == len(right) and all(map(eq, left, right))
