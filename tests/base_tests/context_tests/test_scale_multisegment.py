from hypothesis import given

from ground.base import Context
from ground.hints import Multisegment
from tests.hints import ScalarT
from tests.utils import (
    reverse_geometry,
    reverse_geometry_coordinates,
    reverse_multisegment,
    reverse_multisegment_coordinates,
)

from . import strategies


@given(strategies.contexts_with_multisegments_and_scalars_pairs)
def test_basic(
    context_with_multisegment_and_factors: tuple[
        Context[ScalarT], Multisegment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    (context, multisegment, factor_x, factor_y) = (
        context_with_multisegment_and_factors
    )

    result = context.scale_multisegment(multisegment, factor_x, factor_y)

    assert isinstance(
        result,
        (
            context.multipoint_cls,
            context.multisegment_cls,
            context.mix_cls,
            context.segment_cls,
        ),
    )


@given(strategies.contexts_with_multisegments_and_scalars_pairs)
def test_reversals(
    context_with_multisegment_and_factors: tuple[
        Context[ScalarT], Multisegment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    (context, multisegment, factor_x, factor_y) = (
        context_with_multisegment_and_factors
    )

    result = context.scale_multisegment(multisegment, factor_x, factor_y)

    assert reverse_geometry(result) == context.scale_multisegment(
        reverse_multisegment(multisegment), factor_x, factor_y
    )
    assert reverse_geometry_coordinates(result) == context.scale_multisegment(
        reverse_multisegment_coordinates(multisegment), factor_y, factor_x
    )
