from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints
from ground.core.hints import QuaternaryPointFunction
from .plain import (cross as _plain_cross,
                    dot as _plain_dot)
from .robust import (cross as _robust_cross,
                     dot as _robust_dot)

QuaternaryFunction = QuaternaryPointFunction[_hints.Coordinate]


class Context:
    __slots__ = '_cross_product', '_dot_product'

    def __init__(self,
                 cross_product: QuaternaryFunction,
                 dot_product: QuaternaryFunction) -> None:
        self._cross_product, self._dot_product = cross_product, dot_product

    __repr__ = _generate_repr(__init__)

    @property
    def cross_product(self) -> QuaternaryFunction:
        return self._cross_product

    @property
    def dot_product(self) -> QuaternaryFunction:
        return self._dot_product


plain_context = Context(cross_product=_plain_cross.multiply,
                        dot_product=_plain_dot.multiply)
robust_context = Context(cross_product=_robust_cross.multiply,
                         dot_product=_robust_dot.multiply)
