from hypothesis import given

from ground.base import (Context,
                         get_context,
                         set_context)
from . import strategies


@given(strategies.contexts)
def test_basic(context: Context) -> None:
    result = set_context(context)

    assert result is None


@given(strategies.contexts)
def test_connection_with_get_context(context: Context) -> None:
    set_context(context)

    assert get_context() is context
