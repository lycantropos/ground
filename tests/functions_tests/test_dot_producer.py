from itertools import (permutations,
                       product)

from hypothesis import given

from ground.core.angular import to_sign
from tests.hints import (DotProducer,
                         PointsPair,
                         PointsQuadruplet)
from tests.utils import (equivalence,
                         is_even_permutation,
                         permute,
                         to_perpendicular_point)
from . import strategies


@given(strategies.dot_producers, strategies.points_quadruplets)
def test_basic(dot_producer: DotProducer,
               points_quadruplet: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruplet

    result = dot_producer(first_start, first_end, second_start, second_end)

    coordinate_cls = type(first_start.x)
    assert isinstance(result, coordinate_cls)


@given(strategies.dot_producers, strategies.points_pairs)
def test_perpendicular_endpoints(dot_producer: DotProducer,
                                 points_pair: PointsPair) -> None:
    first_start, first_end = points_pair

    assert not dot_producer(first_start, first_end,
                            to_perpendicular_point(first_start),
                            to_perpendicular_point(first_end))


@given(strategies.dot_producers, strategies.points_quadruplets)
def test_segments_permutation(dot_producer: DotProducer,
                              points_quadruple: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruple

    result = dot_producer(first_start, first_end, second_start, second_end)

    assert result == dot_producer(second_start, second_end, first_start,
                                  first_end)


@given(strategies.dot_producers, strategies.points_quadruplets)
def test_endpoints_permutations(dot_producer: DotProducer,
                                points_quadruple: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruple

    result = dot_producer(first_start, first_end, second_start, second_end)

    result_sign = to_sign(result)
    first_endpoints = first_start, first_end
    second_endpoints = second_start, second_end
    assert all(to_sign(dot_producer(*permute(first_endpoints,
                                             first_permutation),
                                    *permute(second_endpoints,
                                             second_permutation)))
               == (result_sign
                   if equivalence(is_even_permutation(first_permutation),
                                  is_even_permutation(second_permutation))
                   else -result_sign)
               for first_permutation, second_permutation
               in product(permutations(range(len(first_endpoints))),
                          permutations(range(len(second_endpoints)))))
