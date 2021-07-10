from reprit import serializers
from reprit.base import generate_repr

from ground.core.hints import (QuaternaryPointFunction,
                               Scalar)
from .exact import (cross as exact_cross,
                    dot as exact_dot)
from .plain import (cross as plain_cross,
                    dot as plain_dot)
from .robust import (cross as robust_cross,
                     dot as robust_dot)

QuaternaryFunction = QuaternaryPointFunction[Scalar]


class Context:
    __slots__ = '_cross_product', '_dot_product'

    def __init__(self,
                 cross_product: QuaternaryFunction,
                 dot_product: QuaternaryFunction) -> None:
        self._cross_product, self._dot_product = cross_product, dot_product

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)

    @property
    def cross_product(self) -> QuaternaryFunction:
        return self._cross_product

    @property
    def dot_product(self) -> QuaternaryFunction:
        return self._dot_product


exact_context = Context(cross_product=exact_cross.multiply,
                        dot_product=exact_dot.multiply)
plain_context = Context(cross_product=plain_cross.multiply,
                        dot_product=plain_dot.multiply)
robust_context = Context(cross_product=robust_cross.multiply,
                         dot_product=robust_dot.multiply)
