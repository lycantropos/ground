from typing import Sequence

from reprit.base import generate_repr

from ground import hints
from ground.hints import Coordinate


class Point:
    __slots__ = '_x', '_y'

    def __init__(self, x: Coordinate, y: Coordinate) -> None:
        self._x, self._y = x, y

    __repr__ = generate_repr(__init__)

    @property
    def x(self) -> Coordinate:
        return self._x

    @property
    def y(self) -> Coordinate:
        return self._y


class Multipoint:
    __slots__ = '_points',

    def __init__(self, points: Sequence[hints.Point]) -> None:
        self._points = points

    __repr__ = generate_repr(__init__)

    @property
    def points(self) -> Sequence[hints.Point]:
        return self._points


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


class Multisegment:
    __slots__ = '_segments',

    def __init__(self, segments: Sequence[hints.Segment]) -> None:
        self._segments = segments

    __repr__ = generate_repr(__init__)

    @property
    def segments(self) -> Sequence[hints.Segment]:
        return self._segments


class Contour:
    __slots__ = '_vertices',

    def __init__(self, vertices: Sequence[hints.Polygon]) -> None:
        self._vertices = vertices

    __repr__ = generate_repr(__init__)

    @property
    def vertices(self) -> Sequence[hints.Polygon]:
        return self._vertices


class Multicontour:
    __slots__ = '_contours',

    def __init__(self, contours: Sequence[hints.Contour]) -> None:
        self._contours = contours

    __repr__ = generate_repr(__init__)

    @property
    def contours(self) -> Sequence[hints.Contour]:
        return self._contours


class Polygon:
    __slots__ = '_border', '_holes'

    def __init__(self, border: hints.Contour, holes: Sequence[hints.Contour]
                 ) -> None:
        self._border, self._holes = border, holes

    __repr__ = generate_repr(__init__)

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

    @property
    def polygons(self) -> Sequence[hints.Polygon]:
        return self._polygons
