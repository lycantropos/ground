from hypothesis import given

from ground.functions import (Context,
                              set_context,
                              to_incircle_determiner)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_incircle_determiner() is context.incircle_determiner
