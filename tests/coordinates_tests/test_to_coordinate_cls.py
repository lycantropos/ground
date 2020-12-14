from hypothesis import given

from ground.coordinates import (Context,
                                set_context,
                                to_coordinate_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_coordinate_cls() is context.coordinate_cls
