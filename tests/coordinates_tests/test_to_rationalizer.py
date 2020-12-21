from hypothesis import given

from ground.coordinates import (Context,
                                set_context,
                                to_rationalizer)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_rationalizer() is context.rationalizer