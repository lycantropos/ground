from hypothesis import given

from ground.incircle import (Context,
                             set_context,
                             to_point_point_point_determiner)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert (to_point_point_point_determiner()
            is context.point_point_point_determiner)
