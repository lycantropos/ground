from typing import Any, Generic

from reprit import serializers
from reprit.base import generate_repr
from typing_extensions import Self

from ground._core.hints import HasRepr, QuaternaryPointFunction, ScalarT

from .plain import cross as plain_cross, dot as plain_dot


class Context(HasRepr, Generic[ScalarT]):
    @property
    def cross_product(self, /) -> QuaternaryPointFunction[ScalarT, ScalarT]:
        return self._cross_product

    @property
    def dot_product(self, /) -> QuaternaryPointFunction[ScalarT, ScalarT]:
        return self._dot_product

    _cross_product: QuaternaryPointFunction[ScalarT, ScalarT]
    _dot_product: QuaternaryPointFunction[ScalarT, ScalarT]

    __slots__ = '_cross_product', '_dot_product'

    def __new__(
        cls,
        /,
        *,
        cross_product: QuaternaryPointFunction[ScalarT, ScalarT],
        dot_product: QuaternaryPointFunction[ScalarT, ScalarT],
    ) -> Self:
        self = super().__new__(cls)
        self._cross_product, self._dot_product = cross_product, dot_product
        return self

    __repr__ = generate_repr(
        __new__,
        argument_serializer=serializers.complex_,
        with_module_name=True,
    )


plain_context: Context[Any] = Context(
    cross_product=plain_cross.multiply, dot_product=plain_dot.multiply
)
