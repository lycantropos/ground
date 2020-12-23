from operator import itemgetter
from typing import (Sequence,
                    Tuple)

from hypothesis import strategies

from ground.core.utils import to_sign
from ground.hints import Point
from .hints import (Domain,
                    Permutation,
                    Strategy)

to_sign = to_sign


def equivalence(left: bool, right: bool) -> bool:
    return left is right


def is_even_permutation(permutation: Permutation) -> bool:
    if len(permutation) == 1:
        return True
    transitions_count = 0
    for index, element in enumerate(permutation):
        for next_element in permutation[index + 1:]:
            if element > next_element:
                transitions_count += 1
    return not (transitions_count % 2)


def permute(sequence: Sequence[Domain],
            permutation: Permutation) -> Sequence[Domain]:
    return itemgetter(*permutation)(sequence)


def to_pairs(strategy: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)


def to_perpendicular_point(point: Point) -> Point:
    return type(point)(-point.y, point.x)


def to_quadruplets(strategy: Strategy[Domain]
                   ) -> Strategy[Tuple[Domain, Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy)
