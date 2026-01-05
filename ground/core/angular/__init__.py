from typing import Any, Generic

from reprit import serializers
from reprit.base import generate_repr

from ground.core.enums import Kind, Orientation
from ground.core.hints import ScalarT, TernaryPointFunction

from .plain import kind as plain_kind, orientation as plain_orientation


class Context(Generic[ScalarT]):
    __slots__ = '_kind', '_orientation'

    def __init__(
        self,
        kind: TernaryPointFunction[ScalarT, Kind],
        orientation: TernaryPointFunction[ScalarT, Orientation],
    ) -> None:
        self._kind, self._orientation = kind, orientation

    def __repr__(self) -> str:
        return _context_repr(self)

    @property
    def kind(self) -> TernaryPointFunction[ScalarT, Kind]:
        return self._kind

    @property
    def orientation(self) -> TernaryPointFunction[ScalarT, Orientation]:
        return self._orientation


_context_repr = generate_repr(
    Context.__init__,
    argument_serializer=serializers.complex_,
    with_module_name=True,
)

plain_context: Context[Any] = Context(
    kind=plain_kind, orientation=plain_orientation
)
