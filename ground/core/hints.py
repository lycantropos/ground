from abc import abstractmethod
from numbers import Real
from typing import (Callable,
                    Sequence,
                    TypeVar,
                    Union)

from symba.base import Expression

try:
    from typing import (Protocol,
                        runtime_checkable)
except ImportError:
    from typing_extensions import (Protocol,
                                   runtime_checkable)

Scalar = TypeVar('Scalar', Expression, Real)
SquareRooter = Callable[[Scalar], Scalar]


@runtime_checkable
class Point(Protocol[Scalar]):
    """
    **Point** is a minimal element of the plane
    defined by pair of real numbers (called *point's coordinates*).

    Points considered to be sorted lexicographically,
    with abscissas being compared first.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, x: Scalar, y: Scalar) -> 'Point':
        """Constructs point given its coordinates."""

    @property
    @abstractmethod
    def x(self) -> Scalar:
        """Abscissa of the point."""

    @property
    @abstractmethod
    def y(self) -> Scalar:
        """Ordinate of the point."""

    @abstractmethod
    def __eq__(self, other: 'Point') -> bool:
        """Checks if the point is equal to the other."""

    @abstractmethod
    def __ge__(self, other: 'Point') -> bool:
        """Checks if the point is greater than or equal to the other."""

    @abstractmethod
    def __gt__(self, other: 'Point') -> bool:
        """Checks if the point is greater than the other."""

    @abstractmethod
    def __hash__(self) -> int:
        """Returns hash value of the point."""

    @abstractmethod
    def __le__(self, other: 'Point') -> bool:
        """Checks if the point is less than or equal to the other."""

    @abstractmethod
    def __lt__(self, other: 'Point') -> bool:
        """Checks if the point is less than the other."""


Range = TypeVar('Range')
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
TernaryPointFunction = Callable[[Point, Point, Point], Range]


@runtime_checkable
class Box(Protocol[Scalar]):
    """
    **Box** is a limited closed region
    defined by axis-aligned rectangular contour.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls,
                min_x: Scalar,
                max_x: Scalar,
                min_y: Scalar,
                max_y: Scalar) -> 'Box':
        """Constructs box given its coordinates limits."""

    @property
    @abstractmethod
    def max_x(self) -> Scalar:
        """Maximum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def max_y(self) -> Scalar:
        """Maximum ``y``-coordinate of the box."""

    @property
    @abstractmethod
    def min_x(self) -> Scalar:
        """Minimum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def min_y(self) -> Scalar:
        """Minimum ``y``-coordinate of the box."""

    @abstractmethod
    def __eq__(self, other: 'Box') -> bool:
        """Checks if the box is equal to the other."""


@runtime_checkable
class Empty(Protocol):
    """Represents an empty set of points."""
    __slots__ = ()

    @abstractmethod
    def __new__(cls) -> 'Empty':
        """Constructs empty geometry."""

    @abstractmethod
    def __eq__(self, other: 'Empty') -> bool:
        """Checks if the empty geometry is equal to the other."""


_T = TypeVar('_T')
Maybe = Union[Empty, _T]


@runtime_checkable
class Multipoint(Protocol[Scalar]):
    """
    **Multipoint** is a discrete geometry
    that represents non-empty set of unique points.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, points: Sequence[Point]) -> 'Multipoint':
        """Constructs multipoint given its points."""

    @property
    @abstractmethod
    def points(self) -> Sequence[Point]:
        """Points of the multipoint."""

    @abstractmethod
    def __eq__(self, other: 'Multipoint') -> bool:
        """Checks if the multipoint is equal to the other."""


@runtime_checkable
class Segment(Protocol[Scalar]):
    """
    **Segment** (or **line segment**) is a linear geometry that represents
    a limited continuous part of the line containing more than one point
    defined by a pair of unequal points (called *segment's endpoints*).
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, start: Point, end: Point) -> 'Segment':
        """Constructs segment given its endpoints."""

    @property
    @abstractmethod
    def start(self) -> Point:
        """Start endpoint of the segment."""

    @property
    @abstractmethod
    def end(self) -> Point:
        """End endpoint of the segment."""

    @abstractmethod
    def __eq__(self, other: 'Segment') -> bool:
        """Checks if the segment is equal to the other."""


@runtime_checkable
class Multisegment(Protocol[Scalar]):
    """
    **Multisegment** is a linear geometry that represents set of two or more
    non-crossing and non-overlapping segments.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, segments: Sequence[Segment]) -> 'Multisegment':
        """Constructs multisegment given its segments."""

    @property
    @abstractmethod
    def segments(self) -> Sequence[Segment]:
        """Segments of the multisegment."""

    @abstractmethod
    def __eq__(self, other: 'Multisegment') -> bool:
        """Checks if the multisegment is equal to the other."""


@runtime_checkable
class Contour(Protocol[Scalar]):
    """
    **Contour** is a linear geometry that represents closed simple polyline
    defined by a sequence of points (called *contour's vertices*).
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, vertices: Sequence[Point]) -> 'Contour':
        """Constructs contour given its vertices."""

    @property
    @abstractmethod
    def vertices(self) -> Sequence[Point]:
        """Vertices of the contour."""

    @abstractmethod
    def __eq__(self, other: 'Contour') -> bool:
        """Checks if the contour is equal to the other."""


@runtime_checkable
class Polygon(Protocol[Scalar]):
    """
    **Polygon** is a shaped geometry that represents limited closed region
    defined by the pair of outer contour (called *polygon's border*)
    and possibly empty sequence of inner contours (called *polygon's holes*).
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, border: Contour, holes: Sequence[Contour]) -> 'Polygon':
        """Constructs polygon given its border and holes."""

    @property
    @abstractmethod
    def border(self) -> Contour:
        """Border of the polygon."""

    @property
    @abstractmethod
    def holes(self) -> Sequence[Contour]:
        """Holes of the polygon."""

    @abstractmethod
    def __eq__(self, other: 'Polygon') -> bool:
        """Checks if the polygon is equal to the other."""


@runtime_checkable
class Multipolygon(Protocol[Scalar]):
    """
    **Multipolygon** is a shaped geometry that represents set of two or more
    non-overlapping polygons intersecting only in discrete set of points.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls, polygons: Sequence[Polygon]) -> 'Multipolygon':
        """Constructs multipolygon given its polygons."""

    @property
    @abstractmethod
    def polygons(self) -> Sequence[Polygon]:
        """Polygons of the multipolygon."""

    @abstractmethod
    def __eq__(self, other: 'Multipolygon') -> bool:
        """Checks if the multipolygon is equal to the other."""


Linear = Union[Segment, Multisegment, Contour]
Shaped = Union[Polygon, Multipolygon]


@runtime_checkable
class Mix(Protocol[Scalar]):
    """
    **Mix** is a set of two or more non-empty geometries
    with different dimensions.
    """
    __slots__ = ()

    @abstractmethod
    def __new__(cls,
                discrete: Maybe[Multipoint],
                linear: Maybe[Linear],
                shaped: Maybe[Shaped]) -> 'Mix':
        """Constructs mix given its components."""

    @abstractmethod
    def __eq__(self, other: 'Mix') -> bool:
        """Checks if the mix is equal to the other."""

    @property
    @abstractmethod
    def discrete(self) -> Maybe[Multipoint]:
        """Discrete component of the mix."""

    @property
    @abstractmethod
    def linear(self) -> Maybe[Linear]:
        """Linear component of the mix."""

    @property
    @abstractmethod
    def shaped(self) -> Maybe[Shaped]:
        """Shaped component of the mix."""
