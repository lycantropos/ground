from hypothesis import given

from ground.base import Context
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    assert isinstance(context.empty, context.empty_cls)
