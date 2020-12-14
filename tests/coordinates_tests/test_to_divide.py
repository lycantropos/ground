from hypothesis import given

from ground.coordinates import (Context,
                                set_context,
                                to_divide)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_divide() is context.divide
