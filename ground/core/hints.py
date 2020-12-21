from typing import (Callable,
                    Sequence,
                    TypeVar)

from ground.hints import (Coordinate,
                          Point)

Range = TypeVar('Range')
Components = Sequence[Coordinate]
QuaternaryPointFunction = Callable[[Point, Point, Point, Point], Range]
Rationalizer = Callable[[Coordinate], Coordinate]
TernaryPointFunction = Callable[[Point, Point, Point], Range]
UnaryCoordinatesOperation = Callable[[Coordinate], Coordinate]
