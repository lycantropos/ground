from typing import (Sequence,
                    Tuple)

from hypothesis import given

from ground.base import Context
from ground.hints import Polygon
from tests.utils import (is_point,
                         rotate_sequence)
from . import strategies


@given(strategies.contexts_with_polygons_sequences)
def test_basic(context_with_polygons: Tuple[Context, Sequence[Polygon]]
               ) -> None:
    context, holes = context_with_polygons

    result = context.multipolygon_centroid(holes)

    assert is_point(result)


@given(strategies.contexts_with_rational_polygons_sequences)
def test_rotations(context_with_polygons: Tuple[Context, Sequence[Polygon]]
                   ) -> None:
    context, polygons = context_with_polygons

    result = context.multipolygon_centroid(polygons)

    assert all(context.multipolygon_centroid(rotate_sequence(polygons, offset))
               == result
               for offset in range(len(polygons)))
