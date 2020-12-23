from hypothesis import given

from ground.geometrical import (Context,
                                set_context,
                                to_point_cls)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    set_context(context)

    assert to_point_cls() is context.point_cls
