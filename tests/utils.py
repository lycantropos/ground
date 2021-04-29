from functools import partial
from numbers import (Rational,
                     Real)
from operator import (getitem,
                      itemgetter)
from typing import (Any,
                    Callable,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Tuple,
                    Type,
                    TypeVar)

import math
from hypothesis import strategies

from ground.base import (Context,
                         Mode,
                         Orientation,
                         Relation)
from ground.core.angular import to_sign
from ground.hints import (Box,
                          Contour,
                          Multipoint,
                          Multipolygon,
                          Multisegment,
                          Point,
                          Polygon,
                          Scalar,
                          Segment)
from .hints import (Permutation,
                    Strategy)

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

MAX_SEQUENCE_SIZE = 5

ASYMMETRIC_LINEAR_RELATIONS = (Relation.COMPONENT, Relation.COMPOSITE)
SYMMETRIC_LINEAR_RELATIONS = (Relation.CROSS, Relation.DISJOINT,
                              Relation.EQUAL, Relation.OVERLAP, Relation.TOUCH)
LINEAR_RELATIONS = ASYMMETRIC_LINEAR_RELATIONS + SYMMETRIC_LINEAR_RELATIONS

to_sign = to_sign


def apply(function: Callable[..., _T2], args: Iterable[_T1]) -> _T2:
    return function(*args)


def cleave(*functions: Callable[..., _T2]
           ) -> Callable[..., Tuple[_T2, ...]]:
    def cleft(*args: Any, **kwargs: Any) -> Tuple[_T2, ...]:
        return tuple(function(*args, **kwargs) for function in functions)

    return cleft


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


def lift(value: _T1) -> List[_T1]:
    return [value]


is_box = Box.__instancecheck__


def is_coordinate(object_: Any) -> bool:
    return isinstance(object_, Scalar.__constraints__)


def is_even_permutation(index: int, size: int) -> bool:
    return ((index % math.factorial(size) - 1) % 4) > 1


is_point = Point.__instancecheck__
is_segment = Segment.__instancecheck__


def nth_permutation(index: int, size: int) -> Permutation:
    permutations_count = math.factorial(size)
    index %= permutations_count
    indices = list(range(size))
    result = []
    for rest_size in range(size, 0, -1):
        permutations_count //= rest_size
        step, index = divmod(index, permutations_count)
        result.append(indices.pop(step))
    return result


def pack(function: Callable[..., _T2]) -> Callable[[Iterable[_T1]], _T2]:
    return partial(apply, function)


def permute(sequence: Sequence[_T1], index: int) -> Sequence[_T1]:
    return [sequence[index] for index in nth_permutation(index, len(sequence))]


def reverse_box_coordinates(box: Box) -> Point:
    return type(box)(box.min_y, box.max_y, box.min_x, box.max_x)


def reverse_contour_coordinates(contour: Contour) -> Contour:
    return type(contour)([reverse_point_coordinates(vertex)
                          for vertex in contour.vertices])


def reverse_contour(contour: Contour) -> Contour:
    return type(contour)(reverse_sequence(contour.vertices))


def reverse_contours_coordinates(contours: Sequence[Contour]
                                 ) -> Sequence[Contour]:
    return [reverse_contour_coordinates(contour) for contour in contours]


def reverse_multipoint(multipoint: Multipoint) -> Multipoint:
    return type(multipoint)(reverse_sequence(multipoint.points))


def reverse_multipolygon(multipolygon: Multipolygon) -> Multipolygon:
    return type(multipolygon)(reverse_sequence(multipolygon.polygons))


def reverse_multipolygon_coordinates(multipolygon: Multipolygon
                                     ) -> Multipolygon:
    return type(multipolygon)([reverse_polygon_coordinates(polygon)
                               for polygon in multipolygon.polygons])


def reverse_multisegment(multisegment: Multisegment) -> Multisegment:
    return type(multisegment)(reverse_sequence(multisegment.segments))


def reverse_multisegment_coordinates(multisegment: Multisegment
                                     ) -> Multisegment:
    return type(multisegment)([reverse_segment_coordinates(segment)
                               for segment in multisegment.segments])


def reverse_point_coordinates(point: Point) -> Point:
    return type(point)(point.y, point.x)


def reverse_points_coordinates(points: Sequence[Point]) -> Sequence[Point]:
    return [reverse_point_coordinates(point) for point in points]


def reverse_polygon_border(polygon: Polygon) -> Polygon:
    return type(polygon)(reverse_contour(polygon.border),
                         polygon.holes)


def reverse_polygon_coordinates(polygon: Polygon) -> Polygon:
    return type(polygon)(reverse_contour_coordinates(polygon.border),
                         [reverse_contour_coordinates(hole)
                          for hole in polygon.holes])


def reverse_polygon_holes(polygon: Polygon) -> Polygon:
    return type(polygon)(polygon.border, reverse_sequence(polygon.holes))


def reverse_polygons_coordinates(polygons: Sequence[Polygon]
                                 ) -> Sequence[Polygon]:
    return [reverse_polygon_coordinates(polygon) for polygon in polygons]


def reverse_segment_coordinates(segment: Segment) -> Segment:
    return type(segment)(reverse_point_coordinates(segment.start),
                         reverse_point_coordinates(segment.end))


def reverse_segment_endpoints(segment: Segment) -> Segment:
    return type(segment)(segment.end, segment.start)


def reverse_segments_endpoints(segments: Sequence[Segment]
                               ) -> Sequence[Segment]:
    return [reverse_segment_endpoints(segment) for segment in segments]


def reverse_segments_coordinates(segments: Sequence[Segment]
                                 ) -> Sequence[Segment]:
    return [reverse_segment_coordinates(segment) for segment in segments]


reverse_sequence = itemgetter(slice(None, None, -1))


def rotate_sequence(vertices: Sequence[_T1], offset: int) -> Sequence[_T1]:
    offset = offset % len(vertices) if vertices else 0
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
    return type(point)(-point.y, point.x)


def to_quadruplets(strategy: Strategy[_T1]
                   ) -> Strategy[Tuple[_T1, _T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[_T1]) -> Strategy[Tuple[_T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy)


def context_to_output_coordinate_cls(context: Context) -> Type[Scalar]:
    return Rational if context.mode is Mode.EXACT else Real


def permute_multipoint(multipoint: Multipoint, index: int) -> Multipoint:
    return type(multipoint)(permute(multipoint.points, index))


def reverse_segment(segment: Segment) -> Segment:
    return type(segment)(segment.end, segment.start)


def rotate_contour(contour: Contour, offset: int) -> Contour:
    return type(contour)(rotate_sequence(contour.vertices, offset))


def rotate_multipolygon(multipolygon: Multipolygon,
                        offset: int) -> Multipolygon:
    return type(multipolygon)(rotate_sequence(multipolygon.polygons, offset))


def rotate_multisegment(multisegment: Multisegment,
                        offset: int) -> Multisegment:
    return type(multisegment)(rotate_sequence(multisegment.multisegment,
                                              offset))


def rotate_polygon_border(polygon: Polygon, offset: int) -> Polygon:
    return type(polygon)(rotate_contour(polygon.border, offset), polygon.holes)


def rotate_polygon_holes(polygon: Polygon, offset: int) -> Polygon:
    return type(polygon)(polygon.border, rotate_sequence(polygon.holes,
                                                         offset))


_T = TypeVar('_T')


def cleave_in_tuples(*functions: Callable[..., Strategy[_T]]
                     ) -> Callable[..., Strategy[Tuple[_T, ...]]]:
    cleft = cleave(*functions)

    def to_tuples(*args: Any, **kwargs: Any) -> Strategy[Tuple[_T, ...]]:
        return strategies.tuples(*cleft(*args, **kwargs))

    return to_tuples
