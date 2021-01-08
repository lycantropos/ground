from abc import abstractmethod
from numbers import Real
from typing import (Sequence,
                    TypeVar)

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

Coordinate = TypeVar('Coordinate',
                     bound=Real)


class Point(Protocol[Coordinate]):
    """
    **Point** is a minimal element of the plane
    defined by pair of real numbers (called *point's coordinates*).

    Points considered to be sorted lexicographically,
    with ``x`` coordinate being compared first.
    """

    @abstractmethod
    def __new__(cls, x: Coordinate, y: Coordinate) -> 'Point':
        """Constructs point given its coordinates."""

    @abstractmethod
    def __eq__(self, other: 'Point') -> bool:
        """Checks if the point is equal to the other."""

    @abstractmethod
    def __hash__(self) -> int:
        """Returns hash value of the point."""

    @abstractmethod
    def __lt__(self, other: 'Point') -> bool:
        """Checks if the point is less than the other."""

    @abstractmethod
    def __le__(self, other: 'Point') -> bool:
        """Checks if the point is less than or equal to the other."""

    @property
    @abstractmethod
    def x(self) -> Coordinate:
        """First coordinate of the point."""

    @property
    @abstractmethod
    def y(self) -> Coordinate:
        """Second coordinate of the point."""


class Box(Protocol[Coordinate]):
    """
    **Box** is a limited closed region
    defined by axis-aligned rectangular contour.
    """

    @abstractmethod
    def __new__(cls,
                min_x: Coordinate,
                max_x: Coordinate,
                min_y: Coordinate,
                max_y: Coordinate) -> 'Box':
        """Constructs box given its coordinates limits."""

    @abstractmethod
    def __eq__(self, other: 'Box') -> bool:
        """Checks if the box is equal to the other."""

    @property
    @abstractmethod
    def max_x(self) -> Coordinate:
        """Returns maximum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def max_y(self) -> Coordinate:
        """Returns maximum ``y``-coordinate of the box."""

    @property
    @abstractmethod
    def min_x(self) -> Coordinate:
        """Returns minimum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def min_y(self) -> Coordinate:
        """Returns minimum ``y``-coordinate of the box."""


class Multipoint(Protocol[Coordinate]):
    """
    **Multipoint** is a non-empty set of unique points.
    """

    @abstractmethod
    def __new__(cls, points: Sequence[Point]) -> 'Multipoint':
        """Constructs multipoint given its points."""

    @property
    @abstractmethod
    def points(self) -> Sequence[Point]:
        """Returns points of the multipoint."""


class Segment(Protocol[Coordinate]):
    """
    **Segment** (or **line segment**)
    is a limited continuous part of the line containing more than one point
    defined by a pair of unequal points (called *segment's endpoints*).
    """

    @abstractmethod
    def __new__(cls, start: Point, end: Point) -> 'Segment':
        """Constructs segment given its endpoints."""

    @abstractmethod
    def __eq__(self, other: 'Segment') -> bool:
        """Checks if the segment is equal to the other."""

    @property
    @abstractmethod
    def start(self) -> Point:
        """Returns start endpoint of the segment."""

    @property
    @abstractmethod
    def end(self) -> Point:
        """Returns start endpoint of the segment."""


class Multisegment(Protocol[Coordinate]):
    """
    **Multisegment**
    is a non-empty set of non-crossing and non-overlapping segments.
    """

    @abstractmethod
    def __new__(cls, segments: Sequence[Segment]) -> 'Multisegment':
        """Constructs multisegment given its segments."""

    @property
    @abstractmethod
    def segments(self) -> Sequence[Segment]:
        """Returns segments of the multisegment."""


class Contour(Protocol[Coordinate]):
    """
    **Contour** is a closed simple polyline defined by a sequence of points
    (called *contour's vertices*).
    """

    def __new__(cls, vertices: Sequence[Point]) -> 'Contour':
        """Constructs contour given its vertices."""

    @property
    @abstractmethod
    def vertices(self) -> Sequence[Point]:
        """Returns coordinates of the contour."""


class Polygon(Protocol[Coordinate]):
    """
    **Polygon** is a limited closed region defined by the pair of outer contour
    (called *polygon's border*) and possibly empty sequence of inner contours
    (called *polygon's holes*).
    """

    @abstractmethod
    def __new__(cls, border: Contour, holes: Sequence[Contour]) -> 'Polygon':
        """Constructs polygon given its border and holes."""

    @property
    @abstractmethod
    def border(self) -> Contour:
        """Returns border of the polygon."""

    @property
    @abstractmethod
    def holes(self) -> Sequence[Contour]:
        """Returns holes of the polygon."""


class Multipolygon(Protocol[Coordinate]):
    """
    **Multipolygon** is a non-empty set of non-overlapping polygons
    intersecting only in discrete set of points.
    """

    @abstractmethod
    def __new__(cls, polygons: Sequence[Polygon]) -> 'Multipolygon':
        """Constructs multipolygon given its polygons."""

    @property
    @abstractmethod
    def polygons(self) -> Sequence[Polygon]:
        """Returns polygons of the multipolygon."""
