from typing import (Callable,
                    Sequence)

from ground.hints import (Coordinate,
                          Point)

Expansion = Sequence[Coordinate]
BinaryCoordinatesOperation = Callable[[Coordinate, Coordinate], Coordinate]
UnaryOperation = Callable[[Coordinate], Coordinate]
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Coordinate]
