import sys

from hypothesis import given
from symba.base import sqrt

from ground.context import Context
from tests.hints import ScalarT

from . import strategies


@given(strategies.contexts)
def test_round_trip(context: Context[ScalarT]) -> None:
    result = repr(context)

    assert (
        eval(
            result,
            {
                **sys.modules,
                Context.__qualname__: Context,
                sqrt.__qualname__: context.sqrt,
            },
        )
        == context
    )
