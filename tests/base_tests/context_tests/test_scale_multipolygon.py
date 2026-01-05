from hypothesis import given

from ground.base import Context
from ground.hints import Multipolygon
from tests.hints import ScalarT
from tests.utils import (
    reverse_geometry_coordinates,
    reverse_multipolygon,
    reverse_multipolygon_coordinates,
)

from . import strategies


@given(strategies.contexts_with_multipolygons_and_scalars_pairs)
def test_basic(
    context_with_multipolygon_and_factors: tuple[
        Context[ScalarT], Multipolygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    (context, multipolygon, factor_x, factor_y) = (
        context_with_multipolygon_and_factors
    )

    result = context.scale_multipolygon(multipolygon, factor_x, factor_y)

    assert isinstance(
        result,
        (
            context.multipoint_cls,
            context.multipolygon_cls,
            context.multisegment_cls,
        ),
    )


@given(strategies.contexts_with_multipolygons_and_scalars_pairs)
def test_reversals(
    context_with_multipolygon_and_factors: tuple[
        Context[ScalarT], Multipolygon[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    (context, multipolygon, factor_x, factor_y) = (
        context_with_multipolygon_and_factors
    )

    result = context.scale_multipolygon(multipolygon, factor_x, factor_y)

    assert not isinstance(
        result, context.multipolygon_cls
    ) or reverse_multipolygon(result) == context.scale_multipolygon(
        reverse_multipolygon(multipolygon), factor_x, factor_y
    )
    assert reverse_geometry_coordinates(result) == context.scale_multipolygon(
        reverse_multipolygon_coordinates(multipolygon), factor_y, factor_x
    )
