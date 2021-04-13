from typing import (Callable,
                    Type)

from reprit.base import generate_repr

from ground.core.enums import Relation
from ground.core.hints import (Point,
                               QuaternaryPointFunction)
from .exact import segment as exact_segment
from .plain import segment as plain_segment

ContainmentChecker = Callable[[Point, Point, Point, QuaternaryPointFunction],
                              bool]
Intersector = Callable[[Point, Point, Point, Point, QuaternaryPointFunction,
                        Type[Point]], Point]
Relater = Callable[[Point, Point, Point, Point, QuaternaryPointFunction],
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


exact_context = Context(intersector=exact_segment.intersect,
                        containment_checker=exact_segment.contains_point,
                        relater=exact_segment.relate)
plain_context = Context(intersector=plain_segment.intersect,
                        containment_checker=plain_segment.contains_point,
                        relater=plain_segment.relate)
