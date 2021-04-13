from itertools import groupby
from typing import (Iterable,
                    List,
                    Sequence,
                    TypeVar)

from .enums import Orientation
from .hints import (Point,
                    TernaryPointFunction)


def to_convex_hull(points: Sequence[Point],
                   orienteer: TernaryPointFunction[Orientation]
                   ) -> List[Point]:
    points = _to_unique_just_seen(sorted(points))
    lower, upper = (_to_sub_hull(points, orienteer),
                    _to_sub_hull(reversed(points), orienteer))
    return lower[:-1] + upper[:-1] or points


_T = TypeVar('_T')


def _to_unique_just_seen(iterable: Iterable[_T]) -> Sequence[_T]:
    return [key for key, _ in groupby(iterable)]


def _to_sub_hull(points: Iterable[Point],
                 orienteer: TernaryPointFunction[Orientation]) -> List[Point]:
    result = []
    for point in points:
        while len(result) >= 2:
            if (orienteer(result[-2], result[-1], point)
                    is not Orientation.COUNTERCLOCKWISE):
                del result[-1]
            else:
                break
        result.append(point)
    return result
