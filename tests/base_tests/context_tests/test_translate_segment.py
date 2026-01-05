from hypothesis import given

from ground.base import Context
from ground.hints import Segment
from tests.hints import ScalarT
from tests.utils import reverse_segment, reverse_segment_coordinates

from . import strategies


@given(strategies.contexts_with_segments_and_scalars_pairs)
def test_basic(
    context_with_segment_and_steps: tuple[
        Context[ScalarT], Segment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, segment, step_x, step_y = context_with_segment_and_steps

    result = context.translate_segment(segment, step_x, step_y)

    assert isinstance(result, context.segment_cls)


@given(strategies.contexts_with_rational_segments_and_scalars_pairs)
def test_round_trip(
    context_with_segment_and_steps: tuple[
        Context[ScalarT], Segment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, segment, step_x, step_y = context_with_segment_and_steps

    result = context.translate_segment(segment, step_x, step_y)

    assert context.translate_segment(
        result, -step_x, -step_y
    ) == context.translate_segment(segment, context.zero, context.zero)


@given(strategies.contexts_with_segments_and_scalars_pairs)
def test_reversals(
    context_with_segment_and_steps: tuple[
        Context[ScalarT], Segment[ScalarT], ScalarT, ScalarT
    ],
) -> None:
    context, segment, step_x, step_y = context_with_segment_and_steps

    result = context.translate_segment(segment, step_x, step_y)

    assert reverse_segment(result) == context.translate_segment(
        reverse_segment(segment), step_x, step_y
    )
    assert reverse_segment_coordinates(result) == context.translate_segment(
        reverse_segment_coordinates(segment), step_y, step_x
    )
