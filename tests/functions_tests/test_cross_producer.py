from itertools import (permutations,
                       product)

from hypothesis import given

from ground.core.angular import to_sign
from tests.hints import (CrossProducer,
                         PointsPair,
                         PointsQuadruplet)
from tests.utils import (equivalence,
                         is_even_permutation,
                         permute)
from . import strategies


@given(strategies.cross_producers, strategies.points_quadruplets)
def test_basic(cross_producer: CrossProducer,
               points_quadruplet: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruplet

    result = cross_producer(first_start, first_end, second_start, second_end)

    coordinate_cls = type(first_start.x)
    assert isinstance(result, coordinate_cls)


@given(strategies.cross_producers, strategies.points_pairs)
def test_same_endpoints(cross_producer: CrossProducer,
                        points_pair: PointsPair) -> None:
    first_start, first_end = points_pair

    assert not cross_producer(first_start, first_end, first_start, first_end)


@given(strategies.cross_producers, strategies.points_quadruplets)
def test_segments_permutation(cross_producer: CrossProducer,
                              points_quadruplet: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruplet

    result = cross_producer(first_start, first_end, second_start, second_end)

    assert result == -cross_producer(second_start, second_end, first_start,
                                     first_end)


@given(strategies.cross_producers, strategies.points_quadruplets)
def test_endpoints_permutations(cross_producer: CrossProducer,
                                points_quadruplet: PointsQuadruplet) -> None:
    first_start, first_end, second_start, second_end = points_quadruplet

    result = cross_producer(first_start, first_end, second_start, second_end)

    result_sign = to_sign(result)
    first_endpoints = first_start, first_end
    second_endpoints = second_start, second_end
    assert all(to_sign(cross_producer(*permute(first_endpoints,
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
