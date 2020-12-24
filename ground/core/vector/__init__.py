from reprit.base import generate_repr

from ground.core.hints import QuaternaryPointFunction
from ground.hints import Coordinate
from .plain import (cross as plain_cross,
                    dot as plain_dot)
from .robust import (cross as robust_cross,
                     dot as robust_dot)

QuaternaryFunction = QuaternaryPointFunction[Coordinate]


class Context:
    __slots__ = '_cross_product', '_dot_product'

    def __init__(self,
                 cross_product: QuaternaryFunction,
                 dot_product: QuaternaryFunction) -> None:
        self._cross_product, self._dot_product = cross_product, dot_product

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def cross_product(self) -> QuaternaryFunction:
        return self._cross_product

    @property
    def dot_product(self) -> QuaternaryFunction:
        return self._dot_product


plain_context = Context(cross_product=plain_cross.multiply,
                        dot_product=plain_dot.multiply)
robust_context = Context(cross_product=robust_cross.multiply,
                         dot_product=robust_dot.multiply)
