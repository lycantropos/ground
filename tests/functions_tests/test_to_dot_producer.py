from hypothesis import given

from ground.functions import (Context,
                              set_context,
                              to_cross_producer)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_cross_producer() is context.cross_producer
