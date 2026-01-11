from hypothesis import given

from ground.context import Context
from ground.hints import Multisegment
from tests.hints import ScalarT
from tests.utils import (
    reverse_multisegment,
    reverse_multisegment_coordinates,
    reverse_point_coordinates,
    rotate_multisegment,
)

from . import strategies


@given(strategies.contexts_with_multisegments)
def test_basic(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert isinstance(result, context.point_cls)


@given(strategies.contexts_with_rational_multisegments)
def test_reversals(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert result == context.multisegment_centroid(
        reverse_multisegment(multisegment)
    )
    assert result == reverse_point_coordinates(
        context.multisegment_centroid(
            reverse_multisegment_coordinates(multisegment)
        )
    )


@given(strategies.contexts_with_multisegments, strategies.indices)
def test_rotations(
    context_with_multisegment: tuple[Context[ScalarT], Multisegment[ScalarT]],
    offset: int,
) -> None:
    context, multisegment = context_with_multisegment

    result = context.multisegment_centroid(multisegment)

    assert result == context.multisegment_centroid(
        rotate_multisegment(multisegment, offset)
    )
