from hypothesis import given

from ground.geometries import (Context,
                               set_context,
                               to_segment_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_segment_cls() is context.segment_cls
