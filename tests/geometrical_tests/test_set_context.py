from hypothesis import given

from ground.geometrical import (Context,
                                get_context,
                                set_context)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert get_context() is context
