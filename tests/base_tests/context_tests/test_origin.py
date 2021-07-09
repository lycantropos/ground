from hypothesis import given

from ground.base import Context
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    result = context.origin

    assert isinstance(result, context.point_cls)
    assert result.x == result.y == 0
