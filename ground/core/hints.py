from typing import (Callable,
                    Sequence,
                    TypeVar)

from ground.hints import (Coordinate,
                          Point)

Expansion = Sequence[Coordinate]
Domain = TypeVar('Domain')
Range = TypeVar('Range')
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
TernaryPointFunction = Callable[[Point, Point, Point], Range]
