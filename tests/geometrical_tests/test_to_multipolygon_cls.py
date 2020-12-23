from hypothesis import given

from ground.geometrical import (Context,
                                set_context,
                                to_multipolygon_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_multipolygon_cls() is context.multipolygon_cls
