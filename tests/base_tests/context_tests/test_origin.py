from hypothesis import given

from ground.base import Context
from tests.hints import ScalarT

from . import strategies


@given(strategies.contexts)
def test_basic(context: Context[ScalarT]) -> None:
    result = context.origin

    assert isinstance(result, context.point_cls)
    assert result.x == result.y == context.coordinate_factory(0)
