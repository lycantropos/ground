from reprit import serializers
from reprit.base import generate_repr

from ground.core.enums import (Kind,
                               Orientation)
from ground.core.hints import TernaryPointFunction
from .exact import (kind as exact_kind,
                    orientation as exact_orientation)
from .plain import (kind as plain_kind,
                    orientation as plain_orientation)
from .robust import (kind as robust_kind,
                     orientation as robust_orientation)


class Context:
    __slots__ = '_kind', '_orientation'

    def __init__(self,
                 kind: TernaryPointFunction[Kind],
                 orientation: TernaryPointFunction[Orientation]) -> None:
        self._kind, self._orientation = kind, orientation

    __repr__ = generate_repr(__init__,
                             argument_serializer=serializers.complex_,
                             with_module_name=True)

    @property
    def kind(self) -> TernaryPointFunction[Kind]:
        return self._kind

    @property
    def orientation(self) -> TernaryPointFunction[Orientation]:
        return self._orientation


exact_context = Context(kind=exact_kind,
                        orientation=exact_orientation)
plain_context = Context(kind=plain_kind,
                        orientation=plain_orientation)
robust_context = Context(kind=robust_kind,
                         orientation=robust_orientation)
