from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Sequence
from typing import Any, Final, Protocol, TypeAlias, TypeVar

from typing_extensions import Self

import ground

MODULE_NAME: Final[str] = f'{ground.__name__}.hints'


class HasRepr(Protocol):
    @abstractmethod
    def __repr__(self, /) -> str:
        raise NotImplementedError


class Scalar(Protocol):
    __module__: str = MODULE_NAME
    __slots__ = ()

    def __add__(self, other: Self, /) -> Self: ...
    def __ge__(self, other: Self, /) -> bool: ...
    def __gt__(self, other: Self, /) -> bool: ...
    def __le__(self, other: Self, /) -> bool: ...
    def __lt__(self, other: Self, /) -> bool: ...
    def __mul__(self, other: Self, /) -> Self: ...
    def __neg__(self, /) -> Self: ...
    def __sub__(self, other: Self, /) -> Self: ...
    def __truediv__(self, other: Self, /) -> Self: ...


ScalarT = TypeVar('ScalarT', bound=Scalar)
ScalarFactory: TypeAlias = Callable[[int], ScalarT]
SquareRooter: TypeAlias = Callable[[Any], ScalarT]
ScalarT_co = TypeVar('ScalarT_co', bound=Any, covariant=True)


class Point(Protocol[ScalarT_co]):
    """
    **Point** is a minimal element of the plane
    defined by pair of real numbers (called *point's coordinates*).

    Points considered to be sorted lexicographically,
    with abscissas being compared first.
    """

    @property
    @abstractmethod
    def x(self, /) -> ScalarT_co:
        """Abscissa of the point."""

    @property
    @abstractmethod
    def y(self, /) -> ScalarT_co:
        """Ordinate of the point."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, x: ScalarT_co, y: ScalarT_co, /) -> Self:
        """Constructs point given its coordinates."""

    @abstractmethod
    def __ge__(self, other: Self, /) -> bool:
        """Checks if the point is greater than or equal to the other."""

    @abstractmethod
    def __gt__(self, other: Self, /) -> bool:
        """Checks if the point is greater than the other."""

    @abstractmethod
    def __hash__(self, /) -> int:
        """Returns hash value of the point."""

    @abstractmethod
    def __le__(self, other: Self, /) -> bool:
        """Checks if the point is less than or equal to the other."""

    @abstractmethod
    def __lt__(self, other: Self, /) -> bool:
        """Checks if the point is less than the other."""


Range = TypeVar('Range')
QuaternaryPointFunction: TypeAlias = Callable[
    [
        Point[ScalarT_co],
        Point[ScalarT_co],
        Point[ScalarT_co],
        Point[ScalarT_co],
    ],
    Range,
]
TernaryPointFunction: TypeAlias = Callable[
    [Point[ScalarT_co], Point[ScalarT_co], Point[ScalarT_co]], Range
]


class Box(Protocol[ScalarT_co]):
    """
    **Box** is a limited closed region
    defined by axis-aligned rectangular contour.
    """

    @property
    @abstractmethod
    def max_x(self, /) -> ScalarT_co:
        """Maximum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def max_y(self, /) -> ScalarT_co:
        """Maximum ``y``-coordinate of the box."""

    @property
    @abstractmethod
    def min_x(self, /) -> ScalarT_co:
        """Minimum ``x``-coordinate of the box."""

    @property
    @abstractmethod
    def min_y(self, /) -> ScalarT_co:
        """Minimum ``y``-coordinate of the box."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(
        cls,
        min_x: ScalarT_co,
        max_x: ScalarT_co,
        min_y: ScalarT_co,
        max_y: ScalarT_co,
        /,
    ) -> Self:
        """Constructs box given its coordinates limits."""


class Empty(Protocol[ScalarT_co]):
    """Represents an empty set of points."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, /) -> Self:
        """Constructs empty geometry."""


_T = TypeVar('_T')


class Multipoint(Protocol[ScalarT_co]):
    """
    **Multipoint** is a discrete geometry
    that represents non-empty set of unique points.
    """

    @property
    @abstractmethod
    def points(self, /) -> Sequence[Point[ScalarT_co]]:
        """Points of the multipoint."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, points: Sequence[Point[ScalarT_co]], /) -> Self:
        """Constructs multipoint given its points."""


class Segment(Protocol[ScalarT_co]):
    """
    **Segment** (or **line segment**) is a linear geometry that represents
    a limited continuous part of the line containing more than one point
    defined by a pair of unequal points (called *segment's endpoints*).
    """

    @property
    @abstractmethod
    def start(self, /) -> Point[ScalarT_co]:
        """Start endpoint of the segment."""

    @property
    @abstractmethod
    def end(self, /) -> Point[ScalarT_co]:
        """End endpoint of the segment."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(
        cls, start: Point[ScalarT_co], end: Point[ScalarT_co], /
    ) -> Self:
        """Constructs segment given its endpoints."""


class Multisegment(Protocol[ScalarT_co]):
    """
    **Multisegment** is a linear geometry that represents set of two or more
    non-crossing and non-overlapping segments.
    """

    @property
    @abstractmethod
    def segments(self, /) -> Sequence[Segment[ScalarT_co]]:
        """Segments of the multisegment."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, segments: Sequence[Segment[ScalarT_co]], /) -> Self:
        """Constructs multisegment given its segments."""


class Contour(Protocol[ScalarT_co]):
    """
    **Contour** is a linear geometry that represents closed simple polyline
    defined by a sequence of points (called *contour's vertices*).
    """

    @property
    @abstractmethod
    def vertices(self, /) -> Sequence[Point[ScalarT_co]]:
        """Vertices of the contour."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, vertices: Sequence[Point[ScalarT_co]], /) -> Self:
        """Constructs contour given its vertices."""


class Polygon(Protocol[ScalarT_co]):
    """
    **Polygon** is a shaped geometry that represents limited closed region
    defined by the pair of outer contour (called *polygon's border*)
    and possibly empty sequence of inner contours (called *polygon's holes*).
    """

    @property
    @abstractmethod
    def border(self, /) -> Contour[ScalarT_co]:
        """Border of the polygon."""

    @property
    @abstractmethod
    def holes(self, /) -> Sequence[Contour[ScalarT_co]]:
        """Holes of the polygon."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(
        cls,
        border: Contour[ScalarT_co],
        holes: Sequence[Contour[ScalarT_co]],
        /,
    ) -> Self:
        """Constructs polygon given its border and holes."""


class Multipolygon(Protocol[ScalarT_co]):
    """
    **Multipolygon** is a shaped geometry that represents set of two or more
    non-overlapping polygons intersecting only in discrete set of points.
    """

    @property
    @abstractmethod
    def polygons(self, /) -> Sequence[Polygon[ScalarT_co]]:
        """Polygons of the multipolygon."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(cls, polygons: Sequence[Polygon[ScalarT_co]], /) -> Self:
        """Constructs multipolygon given its polygons."""


Linear: TypeAlias = (
    Segment[ScalarT_co] | Multisegment[ScalarT_co] | Contour[ScalarT_co]
)
Shaped: TypeAlias = Polygon[ScalarT_co] | Multipolygon[ScalarT_co]


class Mix(Protocol[ScalarT_co]):
    """
    **Mix** is a set of two or more non-empty geometries
    with different dimensions.
    """

    @property
    @abstractmethod
    def discrete(self, /) -> Empty[ScalarT_co] | Multipoint[ScalarT_co]:
        """Discrete component of the mix."""

    @property
    @abstractmethod
    def linear(self, /) -> Empty[ScalarT_co] | Linear[ScalarT_co]:
        """Linear component of the mix."""

    @property
    @abstractmethod
    def shaped(self, /) -> Empty[ScalarT_co] | Shaped[ScalarT_co]:
        """Shaped component of the mix."""

    __module__: str = MODULE_NAME
    __slots__ = ()

    @abstractmethod
    def __new__(
        cls,
        discrete: Empty[ScalarT_co] | Multipoint[ScalarT_co],
        linear: Empty[ScalarT_co] | Linear[ScalarT_co],
        shaped: Empty[ScalarT_co] | Shaped[ScalarT_co],
        /,
    ) -> Self:
        """Constructs mix given its components."""
