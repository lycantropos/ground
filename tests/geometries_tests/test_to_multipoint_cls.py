from hypothesis import given

from ground.geometries import (Context,
                               set_context,
                               to_multipoint_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_multipoint_cls() is context.multipoint_cls
