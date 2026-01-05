from hypothesis import given

from ground.base import Context
from ground.hints import Segment
from tests.hints import ScalarT
from tests.utils import (
    reverse_geometry,
    reverse_geometry_coordinates,
    reverse_segment,
    reverse_segment_coordinates,
)

from . import strategies


@given(strategies.contexts_with_segments_and_scalars_pairs)
def test_basic(
    context_with_segment_and_factors: tuple[
        Context[ScalarT], Segment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, segment, factor_x, factor_y = context_with_segment_and_factors

    result = context.scale_segment(segment, factor_x, factor_y)

    assert isinstance(result, (context.multipoint_cls, context.segment_cls))


@given(strategies.contexts_with_segments_and_scalars_pairs)
def test_reversals(
    context_with_segment_and_factors: tuple[
        Context[ScalarT], Segment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, segment, factor_x, factor_y = context_with_segment_and_factors

    result = context.scale_segment(segment, factor_x, factor_y)

    assert reverse_geometry(result) == context.scale_segment(
        reverse_segment(segment), factor_x, factor_y
    )
    assert reverse_geometry_coordinates(result) == context.scale_segment(
        reverse_segment_coordinates(segment), factor_y, factor_x
    )
