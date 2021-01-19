from abc import abstractmethod as _abstractmethod
from numbers import Real as _Real
from typing import (Sequence as _Sequence,
                    TypeVar as _TypeVar)

try:
    from typing import Protocol as _Protocol
except ImportError:
    from typing_extensions import Protocol as _Protocol

Coordinate = _TypeVar('Coordinate',
                      bound=_Real)


class Point(_Protocol[Coordinate]):
    """
    **Point** is a minimal element of the plane
    defined by pair of real numbers (called *point's coordinates*).

    Points considered to be sorted lexicographically,
    with ``x`` coordinate being compared first.
    """

    @_abstractmethod
    def __new__(cls, x: Coordinate, y: Coordinate) -> 'Point':
        """Constructs point given its coordinates."""

    @_abstractmethod
    def __eq__(self, other: 'Point') -> bool:
        """Checks if the point is equal to the other."""

    @_abstractmethod
    def __hash__(self) -> int:
        """Returns hash value of the point."""

    @_abstractmethod
    def __lt__(self, other: 'Point') -> bool:
        """Checks if the point is less than the other."""

    @_abstractmethod
    def __le__(self, other: 'Point') -> bool:
        """Checks if the point is less than or equal to the other."""

    @property
    @_abstractmethod
    def x(self) -> Coordinate:
        """First coordinate of the point."""

    @property
    @_abstractmethod
    def y(self) -> Coordinate:
        """Second coordinate of the point."""


class Box(_Protocol[Coordinate]):
    """
    **Box** is a limited closed region
    defined by axis-aligned rectangular contour.
    """

    @_abstractmethod
    def __new__(cls,
                min_x: Coordinate,
                max_x: Coordinate,
                min_y: Coordinate,
                max_y: Coordinate) -> 'Box':
        """Constructs box given its coordinates limits."""

    @_abstractmethod
    def __eq__(self, other: 'Box') -> bool:
        """Checks if the box is equal to the other."""

    @property
    @_abstractmethod
    def max_x(self) -> Coordinate:
        """Returns maximum ``x``-coordinate of the box."""

    @property
    @_abstractmethod
    def max_y(self) -> Coordinate:
        """Returns maximum ``y``-coordinate of the box."""

    @property
    @_abstractmethod
    def min_x(self) -> Coordinate:
        """Returns minimum ``x``-coordinate of the box."""

    @property
    @_abstractmethod
    def min_y(self) -> Coordinate:
        """Returns minimum ``y``-coordinate of the box."""


class Multipoint(_Protocol[Coordinate]):
    """
    **Multipoint** is a non-empty set of unique points.
    """

    @_abstractmethod
    def __new__(cls, points: _Sequence[Point]) -> 'Multipoint':
        """Constructs multipoint given its points."""

    @_abstractmethod
    def __eq__(self, other: 'Multipoint') -> bool:
        """Checks if the multipoint is equal to the other."""

    @property
    @_abstractmethod
    def points(self) -> _Sequence[Point]:
        """Returns points of the multipoint."""


class Segment(_Protocol[Coordinate]):
    """
    **Segment** (or **line segment**)
    is a limited continuous part of the line containing more than one point
    defined by a pair of unequal points (called *segment's endpoints*).
    """

    @_abstractmethod
    def __new__(cls, start: Point, end: Point) -> 'Segment':
        """Constructs segment given its endpoints."""

    @_abstractmethod
    def __eq__(self, other: 'Segment') -> bool:
        """Checks if the segment is equal to the other."""

    @property
    @_abstractmethod
    def start(self) -> Point:
        """Returns start endpoint of the segment."""

    @property
    @_abstractmethod
    def end(self) -> Point:
        """Returns start endpoint of the segment."""


class Multisegment(_Protocol[Coordinate]):
    """
    **Multisegment**
    is a non-empty set of non-crossing and non-overlapping segments.
    """

    @_abstractmethod
    def __new__(cls, segments: _Sequence[Segment]) -> 'Multisegment':
        """Constructs multisegment given its segments."""

    @_abstractmethod
    def __eq__(self, other: 'Multisegment') -> bool:
        """Checks if the multisegment is equal to the other."""

    @property
    @_abstractmethod
    def segments(self) -> _Sequence[Segment]:
        """Returns segments of the multisegment."""


class Contour(_Protocol[Coordinate]):
    """
    **Contour** is a closed simple polyline defined by a sequence of points
    (called *contour's vertices*).
    """

    @_abstractmethod
    def __new__(cls, vertices: _Sequence[Point]) -> 'Contour':
        """Constructs contour given its vertices."""

    @_abstractmethod
    def __eq__(self, other: 'Contour') -> bool:
        """Checks if the contour is equal to the other."""

    @property
    @_abstractmethod
    def vertices(self) -> _Sequence[Point]:
        """Returns coordinates of the contour."""


class Polygon(_Protocol[Coordinate]):
    """
    **Polygon** is a limited closed region defined by the pair of outer contour
    (called *polygon's border*) and possibly empty sequence of inner contours
    (called *polygon's holes*).
    """

    @_abstractmethod
    def __new__(cls, border: Contour, holes: _Sequence[Contour]) -> 'Polygon':
        """Constructs polygon given its border and holes."""

    @_abstractmethod
    def __eq__(self, other: 'Polygon') -> bool:
        """Checks if the polygon is equal to the other."""

    @property
    @_abstractmethod
    def border(self) -> Contour:
        """Returns border of the polygon."""

    @property
    @_abstractmethod
    def holes(self) -> _Sequence[Contour]:
        """Returns holes of the polygon."""


class Multipolygon(_Protocol[Coordinate]):
    """
    **Multipolygon** is a non-empty set of non-overlapping polygons
    intersecting only in discrete set of points.
    """

    @_abstractmethod
    def __new__(cls, polygons: _Sequence[Polygon]) -> 'Multipolygon':
        """Constructs multipolygon given its polygons."""

    @_abstractmethod
    def __eq__(self, other: 'Multipolygon') -> bool:
        """Checks if the multipolygon is equal to the other."""

    @property
    @_abstractmethod
    def polygons(self) -> _Sequence[Polygon]:
        """Returns polygons of the multipolygon."""
