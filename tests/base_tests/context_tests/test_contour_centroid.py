from typing import (Sequence,
                    Tuple)

import pytest
from hypothesis import given

from ground.base import Context
from tests.utils import (IS_PYPY,
                         Point,
                         is_point,
                         rotate_sequence)
from . import strategies

pytestmark = pytest.mark.skipif(IS_PYPY,
                                reason='too slow on PyPy')


@given(strategies.contexts_with_vertices)
def test_basic(context_with_vertices: Tuple[Context, Sequence[Point]]) -> None:
    context, vertices = context_with_vertices

    result = context.contour_centroid(vertices)

    assert is_point(result)


@given(strategies.contexts_with_rational_vertices, strategies.indices)
def test_rotations(context_with_vertices: Tuple[Context, Sequence[Point]],
                   offset: int) -> None:
    context, vertices = context_with_vertices

    result = context.contour_centroid(vertices)

    assert (context.contour_centroid(rotate_sequence(vertices, offset))
            == result)
