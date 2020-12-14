from hypothesis import given

from ground.geometries import (Context,
                               set_context,
                               to_multisegment_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_multisegment_cls() is context.multisegment_cls
