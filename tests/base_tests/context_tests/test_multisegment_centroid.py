from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Segment
from tests.utils import (is_point,
                         reverse_point_coordinates,
                         reverse_sequence,
                         reverse_segments_coordinates,
                         reverse_segments_endpoints,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_segments_sequences)
def test_basic(context_with_segments: Tuple[Context, Sequence[Segment]]
               ) -> None:
    context, segments = context_with_segments

    result = context.multisegment_centroid(segments)

    assert is_point(result)


@given(strategies.contexts_with_rational_segments_sequences)
def test_reversals(context_with_segments: Tuple[Context, Sequence[Segment]]
                   ) -> None:
    context, segments = context_with_segments

    result = context.multisegment_centroid(segments)

    assert result == context.multisegment_centroid(reverse_sequence(segments))
    assert result == context.multisegment_centroid(reverse_segments_endpoints(
            segments))
    assert result == reverse_point_coordinates(context.multisegment_centroid(
            reverse_segments_coordinates(segments)))


@given(strategies.contexts_with_segments_sequences, strategies.indices)
def test_rotations(context_with_segments: Tuple[Context, Sequence[Segment]],
                   offset: int) -> None:
    context, segments = context_with_segments

    result = context.multisegment_centroid(segments)

    assert result == context.multisegment_centroid(rotate_sequence(segments,
                                                                   offset))
