from hypothesis import given

from ground.context import Context, get_context, set_context
from tests.hints import ScalarT

from . import strategies


@given(strategies.contexts)
def test_basic(context: Context[ScalarT]) -> None:
    result = set_context(context)  # type: ignore[func-returns-value]

    assert result is None


@given(strategies.contexts)
def test_connection_with_get_context(context: Context[ScalarT]) -> None:
    set_context(context)

    assert get_context() is context
