from typing import (Callable,
                    Sequence,
                    TypeVar)

from ground.hints import (Coordinate,
                          Point)

Expansion = Sequence[Coordinate]
BinaryCoordinatesOperation = Callable[[Coordinate, Coordinate], Coordinate]
UnaryOperation = Callable[[Coordinate], Coordinate]
Range = TypeVar('Range')
TernaryPointFunction = Callable[[Point, Point, Point], Range]
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
