from itertools import permutations
from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Polygon
from tests.utils import (is_box,
                         permute,
                         reverse_box_coordinates,
                         reverse_polygons,
                         reverse_polygons_coordinates)
from . import strategies


@given(strategies.contexts_with_polygons_sequences)
def test_basic(context_with_polygons: Tuple[Context, Sequence[Polygon]]
               ) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert is_box(result)


@given(strategies.contexts_with_polygons_sequences)
def test_reversals(context_with_polygons: Tuple[Context, Sequence[Polygon]]
                   ) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert result == context.polygons_box(reverse_polygons(polygons))
    assert result == reverse_box_coordinates(context.polygons_box(
            reverse_polygons_coordinates(polygons)))


@given(strategies.contexts_with_polygons_sequences)
def test_permutations(context_with_polygons: Tuple[Context, Sequence[Polygon]]
                      ) -> None:
    context, polygons = context_with_polygons

    result = context.polygons_box(polygons)

    assert all(context.polygons_box(permute(polygons, permutation))
               == result
               for permutation in permutations(range(len(polygons))))
