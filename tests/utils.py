from functools import partial
from numbers import (Rational,
                     Real)
from typing import (Callable,
                    Iterable,
                    Sequence,
                    Tuple,
                    Type)

from hypothesis import strategies

from ground.base import (Context,
                         Mode,
                         Orientation,
                         Relation,
                         get_context)
from ground.core.angular import to_sign
from ground.hints import Coordinate
from .hints import (Domain,
                    Permutation,
                    Range,
                    Strategy)

MAX_SEQUENCE_SIZE = 5

ASYMMETRIC_LINEAR_RELATIONS = (Relation.COMPONENT, Relation.COMPOSITE)
SYMMETRIC_LINEAR_RELATIONS = (Relation.CROSS, Relation.DISJOINT,
                              Relation.EQUAL, Relation.OVERLAP, Relation.TOUCH)
LINEAR_RELATIONS = ASYMMETRIC_LINEAR_RELATIONS + SYMMETRIC_LINEAR_RELATIONS

_context = get_context()
Box = _context.box_cls
Contour = _context.contour_cls
Multipoint = _context.multipoint_cls
Point = _context.point_cls
to_sign = to_sign


def apply(function: Callable[..., Range], args: Iterable[Domain]) -> Range:
    return function(*args)


def compose(*functions: Callable[..., Range]) -> Callable[..., Range]:
    *rest_functions, first_function = functions
    reversed_rest_functions = rest_functions[::-1]

    def composed(*args: Domain, **kwargs: Domain) -> Range:
        result = first_function(*args, **kwargs)
        for function in reversed_rest_functions:
            result = function(result)
        return result

    return composed


def combine(*functions: Callable[[Domain], Range]
            ) -> Callable[[Tuple[Domain, ...]], Tuple[Range, ...]]:
    def combined(args: Tuple[Domain, ...]) -> Tuple[Range, ...]:
        return tuple(function(arg) for function, arg in zip(functions, args))

    return combined


def equivalence(left: bool, right: bool) -> bool:
    return left is right


def identity(value: Domain) -> Domain:
    return value


is_box = Box.__instancecheck__


def is_even_permutation(permutation: Permutation) -> bool:
    if len(permutation) == 1:
        return True
    transitions_count = 0
    for index, element in enumerate(permutation):
        for next_element in permutation[index + 1:]:
            if element > next_element:
                transitions_count += 1
    return not (transitions_count % 2)


is_point = Point.__instancecheck__


def pack(function: Callable[..., Range]
         ) -> Callable[[Iterable[Domain]], Range]:
    return partial(apply, function)


def permute(sequence: Sequence[Domain],
            permutation: Permutation) -> Sequence[Domain]:
    return [sequence[index] for index in permutation]


def reverse_point_coordinates(point: Point) -> Point:
    return Point(point.y, point.x)


def rotate_sequence(vertices: Sequence[Point], offset: int) -> Contour:
    return (vertices[offset:] + vertices[:offset]
            if offset
            else vertices)


def to_contour_vertices_orientation(vertices: Sequence[Point],
                                    context: Context) -> Orientation:
    if len(vertices) < 3:
        return Orientation.COLLINEAR
    index = min(range(len(vertices)),
                key=vertices.__getitem__)
    return context.angle_orientation(vertices[index - 1], vertices[index],
                                     vertices[(index + 1) % len(vertices)])


def to_pairs(strategy: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(strategy, strategy)


def to_perpendicular_point(point: Point) -> Point:
    return Point(-point.y, point.x)


def to_quadruplets(strategy: Strategy[Domain]
                   ) -> Strategy[Tuple[Domain, Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(strategy, strategy, strategy)


def context_to_output_coordinate_cls(context: Context) -> Type[Coordinate]:
    return Rational if context.mode is Mode.EXACT else Real
