from typing import (Callable,
                    Sequence,
                    TypeVar)

from ground.hints import (Coordinate,
                          Point)

Range = TypeVar('Range')
Components = Sequence[Coordinate]
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
TernaryPointFunction = Callable[[Point, Point, Point], Range]
UnaryCoordinatesFunction = Callable[[Coordinate], Range]
UnaryCoordinatesOperation = Callable[[Coordinate], Coordinate]
