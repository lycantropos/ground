from typing import Any, Generic

from reprit import serializers
from reprit.base import generate_repr

from ground._core.hints import QuaternaryPointFunction, ScalarT

from .plain import cross as plain_cross, dot as plain_dot


class Context(Generic[ScalarT]):
    @property
    def cross_product(self, /) -> QuaternaryPointFunction[ScalarT, ScalarT]:
        return self._cross_product

    @property
    def dot_product(self, /) -> QuaternaryPointFunction[ScalarT, ScalarT]:
        return self._dot_product

    __slots__ = '_cross_product', '_dot_product'

    def __init__(
        self,
        /,
        *,
        cross_product: QuaternaryPointFunction[ScalarT, ScalarT],
        dot_product: QuaternaryPointFunction[ScalarT, ScalarT],
    ) -> None:
        self._cross_product, self._dot_product = cross_product, dot_product

    def __repr__(self, /) -> str:
        return _context_repr(self)


_context_repr = generate_repr(
    Context.__init__,
    argument_serializer=serializers.complex_,
    with_module_name=True,
)
plain_context: Context[Any] = Context(
    cross_product=plain_cross.multiply, dot_product=plain_dot.multiply
)
