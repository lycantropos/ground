from functools import partial
from numbers import (Rational,
                     Real)
from operator import getitem
from typing import (Any,
                    Callable,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Tuple,
                    Type,
                    TypeVar)

from hypothesis import strategies

from ground.base import (Context,
                         Mode,
                         Orientation,
                         Relation,
                         get_context)
from ground.core.angular import to_sign
from ground.hints import Coordinate
from .hints import (Permutation,
                    Strategy)

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

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
Segment = _context.segment_cls
to_sign = to_sign


def apply(function: Callable[..., _T2], args: Iterable[_T1]) -> _T2:
    return function(*args)


def compose(*functions: Callable[..., _T2]) -> Callable[..., _T2]:
    *rest_functions, first_function = functions
    reversed_rest_functions = rest_functions[::-1]

    def composed(*args: _T1, **kwargs: _T1) -> _T2:
        result = first_function(*args, **kwargs)
        for function in reversed_rest_functions:
            result = function(result)
        return result

    return composed


def combine(*functions: Callable[[_T1], _T2]
            ) -> Callable[[Tuple[_T1, ...]], Tuple[_T2, ...]]:
    def combined(args: Tuple[_T1, ...]) -> Tuple[_T2, ...]:
        return tuple(function(arg) for function, arg in zip(functions, args))

    return combined


def equivalence(left: bool, right: bool) -> bool:
    return left is right


def identity(value: _T1) -> _T1:
    return value


is_box = Box.__instancecheck__


def is_coordinate(object_: Any) -> bool:
    return isinstance(object_, Coordinate.__constraints__)


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


def pack(function: Callable[..., _T2]) -> Callable[[Iterable[_T1]], _T2]:
    return partial(apply, function)


def permute(sequence: Sequence[_T1],
            permutation: Permutation) -> Sequence[_T1]:
    return [sequence[index] for index in permutation]


def reverse_point_coordinates(point: Point) -> Point:
    return Point(point.y, point.x)


def reverse_segment_coordinates(segment: Segment) -> Segment:
    return Segment(reverse_point_coordinates(segment.start),
                   reverse_point_coordinates(segment.end))


def reverse_segments(segments: Sequence[Segment]) -> Sequence[Segment]:
    return segments[::-1]


def reverse_segment_endpoints(segment: Segment) -> Segment:
    return Segment(segment.end, segment.start)


def reverse_segments_endpoints(segments: Sequence[Segment]
                               ) -> Sequence[Segment]:
    return [reverse_segment_endpoints(segment) for segment in segments]


def reverse_segments_coordinates(segments: Sequence[Segment]
                                 ) -> Sequence[Segment]:
    return [reverse_segment_coordinates(segment) for segment in segments]


def rotate_sequence(vertices: Sequence[_T1], offset: int) -> Sequence[_T1]:
    return (vertices[offset:] + vertices[:offset]
            if offset
            else vertices)


def sub_lists(sequence: Sequence[_T1],
              *,
              min_size: int = 0) -> Strategy[List[_T1]]:
    return strategies.builds(getitem,
                             strategies.permutations(sequence),
                             slices(min_size=min_size,
                                    max_size=max(len(sequence), 1)))


@strategies.composite
def slices(draw: Callable[[Strategy[_T1]], _T1],
           *,
           min_size: int = 0,
           max_size: Optional[int] = None) -> Strategy[slice]:
    start = draw(strategies.none()
                 | (strategies.integers(0)
                    if max_size is None
                    else strategies.integers(0, max_size - min_size)))
    step = draw(strategies.none()
                | (strategies.integers(1,
                                       (max_size - (0
                                                    if start is None
                                                    else start)) // min_size)
                   if min_size and max_size is not None
                   else strategies.integers(1)))
    stop = draw(strategies.none()
                | strategies.integers((0 if start is None else start)
                                      + min_size * (1
                                                    if step is None
                                                    else step), max_size))
    return slice(start, stop, step)


def to_contour_vertices_orientation(vertices: Sequence[Point],
                                    context: Context) -> Orientation:
    if len(vertices) < 3:
        return Orientation.COLLINEAR
    index = min(range(len(vertices)),
                key=vertices.__getitem__)
    return context.angle_orientation(vertices[index - 1], vertices[index],
                                     vertices[(index + 1) % len(vertices)])


def to_pairs(strategy: Strategy[_T1]) -> Strategy[Tuple[_T1, _T1]]:
    return strategies.tuples(strategy, strategy)


def to_perpendicular_point(point: Point) -> Point:
    return Point(-point.y, point.x)


def to_quadruplets(strategy: Strategy[_T1]
                   ) -> Strategy[Tuple[_T1, _T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[_T1]) -> Strategy[Tuple[_T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy)


def context_to_output_coordinate_cls(context: Context) -> Type[Coordinate]:
    return Rational if context.mode is Mode.EXACT else Real
