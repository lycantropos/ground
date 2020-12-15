from numbers import Real
from typing import (List,
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

    def __new__(cls, x: Coordinate, y: Coordinate) -> 'Point':
        """Constructs point given its coordinates."""

    def __eq__(self, other: 'Point') -> bool:
        """Checks if the point is equal to the other."""

    def __lt__(self, other: 'Point') -> bool:
        """Checks if the point is less than the other."""

    def __le__(self, other: 'Point') -> bool:
        """Checks if the point is less than or equal to the other."""

    @property
    def x(self) -> Coordinate:
        """First coordinate of the point."""

    @property
    def y(self) -> Coordinate:
        """Second coordinate of the point."""


class Multipoint(Protocol[Coordinate]):
    """
    **Multipoint** is a non-empty set of unique points.
    """

    def __new__(cls, points: List[Point]) -> 'Multipoint':
        """Constructs multipoint given its points."""

    @property
    def points(self) -> List[Point]:
        """Returns points of the multipoint."""


class Segment(Protocol[Coordinate]):
    """
    **Segment** (or **line segment**)
    is a limited continuous part of the line containing more than one point
    defined by a pair of unequal points (called *segment's endpoints*).
    """

    def __new__(cls, start: Point, end: Point) -> 'Segment':
        """Constructs segment given its endpoints."""

    @property
    def start(self) -> Point:
        """Returns start endpoint of the segment."""

    @property
    def end(self) -> Point:
        """Returns start endpoint of the segment."""


class Multisegment(Protocol[Coordinate]):
    """
    **Multisegment**
    is a non-empty set of non-crossing and non-overlapping segments.
    """

    def __new__(cls, segments: List[Segment]) -> 'Multisegment':
        """Constructs multisegment given its segments."""

    @property
    def segments(self) -> List[Segment]:
        """Returns segments of the multisegment."""


class Contour(Protocol[Coordinate]):
    """
    **Contour** is a closed simple polyline defined by a sequence of points
    (called *contour's vertices*).
    """

    @property
    def vertices(self) -> List[Point]:
        """Returns coordinates of the contour."""


class Polygon(Protocol[Coordinate]):
    """
    **Polygon** is a limited closed region defined by the pair of outer contour
    (called *polygon's border*) and possibly empty sequence of inner contours
    (called *polygon's holes*).
    """

    def __new__(cls, border: Contour, holes: List[Contour]) -> 'Polygon':
        """Constructs polygon given its border and holes."""

    @property
    def border(self) -> Contour:
        """Returns border of the polygon."""

    @property
    def holes(self) -> List[Contour]:
        """Returns holes of the polygon."""


class Multipolygon(Protocol[Coordinate]):
    """
    **Multipolygon** is a non-empty set of non-overlapping polygons
    intersecting only in discrete set of points.
    """

    def __new__(cls, polygons: List[Polygon]) -> 'Multipolygon':
        """Constructs multipolygon given its polygons."""

    @property
    def polygons(self) -> List[Polygon]:
        """Returns polygons of the multipolygon."""
