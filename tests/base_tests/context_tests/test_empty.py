from hypothesis import given

from ground.base import Context
from tests.hints import ScalarT

from . import strategies


@given(strategies.contexts)
def test_basic(context: Context[ScalarT]) -> None:
    assert isinstance(context.empty, context.empty_cls)
