from itertools import permutations
from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Segment
from tests.utils import (is_box,
                         permute,
                         reverse_box_coordinates,
                         reverse_segments,
                         reverse_segments_coordinates)
from . import strategies


@given(strategies.contexts_with_segments_sequences)
def test_basic(context_with_segments: Tuple[Context, Sequence[Segment]]
               ) -> None:
    context, segments = context_with_segments

    result = context.segments_box(segments)

    assert is_box(result)


@given(strategies.contexts_with_segments_sequences)
def test_reversals(context_with_segments: Tuple[Context, Sequence[Segment]]
                   ) -> None:
    context, segments = context_with_segments

    result = context.segments_box(segments)

    assert result == context.segments_box(reverse_segments(segments))
    assert result == reverse_box_coordinates(context.segments_box(
            reverse_segments_coordinates(segments)))


@given(strategies.contexts_with_segments_sequences)
def test_permutations(context_with_segments: Tuple[Context, Sequence[Segment]]
                      ) -> None:
    context, segments = context_with_segments

    result = context.segments_box(segments)

    assert all(context.segments_box(permute(segments, permutation))
               == result
               for permutation in permutations(range(len(segments))))
