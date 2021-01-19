from itertools import groupby
from typing import (Iterable,
                    List,
                    Sequence)

from ground.hints import Point
from .enums import Orientation
from .hints import (Domain,
                    TernaryPointFunction)


def to_convex_hull(orientation: TernaryPointFunction[Orientation],
                   points: Sequence[Point]) -> List[Point]:
    points = _to_unique_just_seen(sorted(points))
    lower, upper = (_to_sub_hull(orientation, points),
                    _to_sub_hull(orientation, reversed(points)))
    return lower[:-1] + upper[:-1] or points


def _to_unique_just_seen(iterable: Iterable[Domain]) -> Sequence[Domain]:
    return [key for key, _ in groupby(iterable)]


def _to_sub_hull(orientation: TernaryPointFunction[Orientation],
                 points: Iterable[Point]) -> List[Point]:
    result = []
    for point in points:
        while len(result) >= 2:
            if (orientation(result[-2], result[-1], point)
                    is not Orientation.COUNTERCLOCKWISE):
                del result[-1]
            else:
                break
        result.append(point)
    return result
