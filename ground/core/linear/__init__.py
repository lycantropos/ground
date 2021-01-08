from typing import (Callable,
                    Type)

from reprit.base import generate_repr

from ground.core.enums import Relation
from ground.core.hints import (QuaternaryPointFunction,
                               UnaryCoordinateOperation)
from ground.hints import Point
from .plain import segment as plain_segment
from .robust import segment as robust_segment

Intersector = Callable[[QuaternaryPointFunction, UnaryCoordinateOperation,
                        Type[Point], Point, Point, Point, Point], Point]
ContainmentChecker = Callable[[QuaternaryPointFunction, Point, Point, Point],
                              bool]
Relater = Callable[[QuaternaryPointFunction, Point, Point, Point, Point],
                   Relation]


class Context:
    __slots__ = '_containment_checker', '_intersector', '_relater'

    def __init__(self,
                 *,
                 intersector: Intersector,
                 containment_checker: ContainmentChecker,
                 relater: Relater) -> None:
        self._intersector, self._containment_checker, self._relater = (
            intersector, containment_checker, relater)

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def intersector(self) -> Intersector:
        return self._intersector

    @property
    def containment_checker(self) -> ContainmentChecker:
        return self._containment_checker

    @property
    def relater(self) -> Relater:
        return self._relater


plain_context = Context(intersector=plain_segment.intersect,
                        containment_checker=plain_segment.contains_point,
                        relater=plain_segment.relate)
robust_context = Context(intersector=robust_segment.intersect,
                         containment_checker=robust_segment.contains_point,
                         relater=robust_segment.relate)
