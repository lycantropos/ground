from typing import (Callable,
                    Sequence,
                    TypeVar)

from ground.hints import (Coordinate,
                          Point)

Expansion = Sequence[Coordinate]
Range = TypeVar('Range')
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
TernaryPointFunction = Callable[[Point, Point, Point], Range]
UnaryCoordinateOperation = Callable[[Coordinate], Coordinate]
