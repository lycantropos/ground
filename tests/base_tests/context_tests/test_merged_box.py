from typing import Tuple

from hypothesis import given

from ground.base import Context
from ground.hints import Box
from tests.utils import is_box
from . import strategies


@given(strategies.contexts_with_boxes_pairs)
def test_basic(context_with_boxes_pair: Tuple[Context, Tuple[Box, Box]]
               ) -> None:
    context, (first_box, second_box) = context_with_boxes_pair

    result = context.merged_box(first_box, second_box)

    assert is_box(result)


@given(strategies.contexts_with_boxes_triplets)
def test_associativity(context_with_boxes_triplet
                       : Tuple[Context, Tuple[Box, Box, Box]]) -> None:
    context, (first_box, second_box, third_box) = context_with_boxes_triplet

    result = context.merged_box(context.merged_box(first_box, second_box),
                                third_box)

    assert result == context.merged_box(
            first_box, context.merged_box(second_box, third_box))


@given(strategies.contexts_with_boxes_pairs)
def test_commutativity(context_with_boxes_pair: Tuple[Context, Tuple[Box, Box]]
                       ) -> None:
    context, (first_box, second_box) = context_with_boxes_pair

    result = context.merged_box(first_box, second_box)

    assert result == context.merged_box(second_box, first_box)


@given(strategies.contexts_with_boxes)
def test_diagonal(context_with_box: Tuple[Context, Box]) -> None:
    context, box = context_with_box

    result = context.merged_box(box, box)

    assert result == box
