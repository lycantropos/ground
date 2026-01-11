import math
from collections.abc import Callable, Iterable, Sequence
from fractions import Fraction
from functools import partial, singledispatch
from operator import getitem, is_, itemgetter
from types import UnionType
from typing import Any, TypeAlias, TypeVar, overload

from hypothesis import strategies
from symba.base import Expression
from typing_extensions import TypeIs

from ground._core import geometries, primitive
from ground.context import Context
from ground.enums import Location, Orientation, Relation
from ground.hints import (
    Box,
    Contour,
    Empty,
    Mix,
    Multipoint,
    Multipolygon,
    Multisegment,
    Point,
    Polygon,
    Segment,
)

from .hints import Permutation, ScalarT, Strategy

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

MAX_SEQUENCE_SIZE = 5

ASYMMETRIC_LINEAR_RELATIONS = (Relation.COMPONENT, Relation.COMPOSITE)
SYMMETRIC_LINEAR_RELATIONS = (
    Relation.CROSS,
    Relation.DISJOINT,
    Relation.EQUAL,
    Relation.OVERLAP,
    Relation.TOUCH,
)
LINEAR_RELATIONS = ASYMMETRIC_LINEAR_RELATIONS + SYMMETRIC_LINEAR_RELATIONS

to_sign = primitive.to_sign


def to_coordinate_checker(
    context: Context[ScalarT], /
) -> Callable[[Any], TypeIs[ScalarT]]:
    coordinate_cls: type[Any] | UnionType
    if context.coordinate_factory is Fraction:
        coordinate_cls = Fraction | Expression
    else:
        raise TypeError(context)

    def is_coordinate_value(value: Any, /) -> TypeIs[ScalarT]:
        return isinstance(value, coordinate_cls)

    return is_coordinate_value


def apply(function: Callable[..., _T2], args: Iterable[_T1]) -> _T2:
    return function(*args)


@overload
def cleave(
    function_0: Callable[..., _T1], function_1: Callable[..., _T1], /
) -> Callable[..., tuple[_T1, _T1]]: ...


@overload
def cleave(
    *functions: Callable[..., _T1],
) -> Callable[..., tuple[_T1, ...]]: ...


def cleave(*functions: Callable[..., _T1]) -> Callable[..., tuple[_T1, ...]]:
    def cleft(*args: Any, **kwargs: Any) -> tuple[_T1, ...]:
        return tuple(function(*args, **kwargs) for function in functions)

    return cleft


def compose(*functions: Callable[..., _T2]) -> Callable[..., _T2]:
    *rest_functions, first_function = functions
    reversed_rest_functions = rest_functions[::-1]

    def composed(*args: Any, **kwargs: Any) -> _T2:
        result = first_function(*args, **kwargs)
        for function in reversed_rest_functions:
            result = function(result)
        return result

    return composed


def combine(
    *functions: Callable[[_T1], _T2],
) -> Callable[[tuple[_T1, ...]], tuple[_T2, ...]]:
    def combined(args: tuple[_T1, ...]) -> tuple[_T2, ...]:
        return tuple(
            function(arg)
            for function, arg in zip(functions, args, strict=True)
        )

    return combined


equivalence = is_


def identity(value: _T1) -> _T1:
    return value


def lift(value: _T1) -> list[_T1]:
    return [value]


def are_multipoints_equivalent(
    left: Multipoint[ScalarT], right: Multipoint[ScalarT]
) -> bool:
    return frozenset(left.points) == frozenset(right.points)


is_box = Box.__instancecheck__


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


def pack(function: Callable[..., _T2]) -> Callable[[Iterable[Any]], _T2]:
    return partial(apply, function)


def permute(sequence: Sequence[_T1], index: int) -> Sequence[_T1]:
    return [sequence[index] for index in nth_permutation(index, len(sequence))]


AnyGeometry: TypeAlias = (
    Box[ScalarT]
    | Contour[ScalarT]
    | Empty[ScalarT]
    | Mix[ScalarT]
    | Multipoint[ScalarT]
    | Multipolygon[ScalarT]
    | Multisegment[ScalarT]
    | Point[ScalarT]
    | Polygon[ScalarT]
    | Segment[ScalarT]
)


@singledispatch
def reverse_geometry(geometry: AnyGeometry[ScalarT]) -> Any:
    raise TypeError(f'Unsupported geometry type: {type(geometry)!r}.')


@singledispatch
def reverse_geometry_coordinates(geometry: AnyGeometry[ScalarT]) -> Any:
    raise TypeError(f'Unsupported geometry type: {type(geometry)!r}.')


def reverse_box_coordinates(box: Box[ScalarT]) -> Box[ScalarT]:
    return type(box)(box.min_y, box.max_y, box.min_x, box.max_x)


reverse_geometry_coordinates.register(geometries.Box, reverse_box_coordinates)


def reverse_contour_coordinates(contour: Contour[ScalarT]) -> Contour[ScalarT]:
    return type(contour)(
        [reverse_point_coordinates(vertex) for vertex in contour.vertices]
    )


reverse_geometry_coordinates.register(
    geometries.Contour, reverse_contour_coordinates
)


def reverse_contour(contour: Contour[ScalarT]) -> Contour[ScalarT]:
    return type(contour)(reverse_sequence(contour.vertices))


reverse_geometry.register(geometries.Contour, reverse_contour)


def reverse_contours_coordinates(
    contours: Sequence[Contour[ScalarT]],
) -> Sequence[Contour[ScalarT]]:
    return [reverse_contour_coordinates(contour) for contour in contours]


@reverse_geometry.register(geometries.Empty)
@reverse_geometry_coordinates.register(geometries.Empty)
def reverse_empty(empty: Empty[ScalarT]) -> Empty[ScalarT]:
    return empty


@reverse_geometry.register(geometries.Mix)
def reverse_mix(mix: Mix[ScalarT]) -> Mix[ScalarT]:
    return type(mix)(
        reverse_geometry(mix.discrete),
        reverse_geometry(mix.linear),
        reverse_geometry(mix.shaped),
    )


@reverse_geometry_coordinates.register(geometries.Mix)
def reverse_mix_coordinates(mix: Mix[ScalarT]) -> Mix[ScalarT]:
    return type(mix)(
        reverse_geometry_coordinates(mix.discrete),
        reverse_geometry_coordinates(mix.linear),
        reverse_geometry_coordinates(mix.shaped),
    )


@reverse_geometry.register(geometries.Multipoint)
def reverse_multipoint(multipoint: Multipoint[ScalarT]) -> Multipoint[ScalarT]:
    return type(multipoint)(reverse_sequence(multipoint.points))


@reverse_geometry_coordinates.register(geometries.Multipoint)
def reverse_multipoint_coordinates(
    multipoint: Multipoint[ScalarT],
) -> Multipoint[ScalarT]:
    return type(multipoint)(reverse_points_coordinates(multipoint.points))


@reverse_geometry.register(geometries.Multipolygon)
def reverse_multipolygon(
    multipolygon: Multipolygon[ScalarT],
) -> Multipolygon[ScalarT]:
    return type(multipolygon)(reverse_sequence(multipolygon.polygons))


@reverse_geometry_coordinates.register(geometries.Multipolygon)
def reverse_multipolygon_coordinates(
    multipolygon: Multipolygon[ScalarT],
) -> Multipolygon[ScalarT]:
    return type(multipolygon)(
        [
            reverse_polygon_coordinates(polygon)
            for polygon in multipolygon.polygons
        ]
    )


@reverse_geometry.register(geometries.Multisegment)
def reverse_multisegment(
    multisegment: Multisegment[ScalarT],
) -> Multisegment[ScalarT]:
    return type(multisegment)(reverse_sequence(multisegment.segments))


def reverse_multisegment_coordinates(
    multisegment: Multisegment[ScalarT],
) -> Multisegment[ScalarT]:
    return type(multisegment)(
        [
            reverse_segment_coordinates(segment)
            for segment in multisegment.segments
        ]
    )


reverse_geometry_coordinates.register(
    geometries.Multisegment, reverse_multisegment_coordinates
)


def reverse_point_coordinates(point: Point[ScalarT]) -> Point[ScalarT]:
    return type(point)(point.y, point.x)


reverse_geometry_coordinates.register(
    geometries.Point, reverse_point_coordinates
)


def reverse_points_coordinates(
    points: Sequence[Point[ScalarT]],
) -> Sequence[Point[ScalarT]]:
    return [reverse_point_coordinates(point) for point in points]


def reverse_polygon_border(polygon: Polygon[ScalarT]) -> Polygon[ScalarT]:
    return type(polygon)(reverse_contour(polygon.border), polygon.holes)


def reverse_polygon_coordinates(polygon: Polygon[ScalarT]) -> Polygon[ScalarT]:
    return type(polygon)(
        reverse_contour_coordinates(polygon.border),
        [reverse_contour_coordinates(hole) for hole in polygon.holes],
    )


reverse_geometry_coordinates.register(
    geometries.Polygon, reverse_polygon_coordinates
)


def reverse_polygon_holes(polygon: Polygon[ScalarT]) -> Polygon[ScalarT]:
    return type(polygon)(polygon.border, reverse_sequence(polygon.holes))


def reverse_polygons_coordinates(
    polygons: Sequence[Polygon[ScalarT]],
) -> Sequence[Polygon[ScalarT]]:
    return [reverse_polygon_coordinates(polygon) for polygon in polygons]


def reverse_segment_coordinates(segment: Segment[ScalarT]) -> Segment[ScalarT]:
    return type(segment)(
        reverse_point_coordinates(segment.start),
        reverse_point_coordinates(segment.end),
    )


reverse_geometry_coordinates.register(
    geometries.Segment, reverse_segment_coordinates
)


def reverse_segment(segment: Segment[ScalarT]) -> Segment[ScalarT]:
    return type(segment)(segment.end, segment.start)


reverse_geometry.register(geometries.Segment, reverse_segment)


def reverse_segments_endpoints(
    segments: Sequence[Segment[ScalarT]],
) -> Sequence[Segment[ScalarT]]:
    return [reverse_segment(segment) for segment in segments]


def reverse_segments_coordinates(
    segments: Sequence[Segment[ScalarT]],
) -> Sequence[Segment[ScalarT]]:
    return [reverse_segment_coordinates(segment) for segment in segments]


reverse_sequence = itemgetter(slice(None, None, -1))


def rotate_sequence(vertices: Sequence[_T1], offset: int) -> Sequence[_T1]:
    offset = offset % len(vertices) if vertices else 0
    return [*vertices[offset:], *vertices[:offset]] if offset else vertices


def sub_lists(
    sequence: Sequence[_T1], *, min_size: int = 0
) -> Strategy[list[_T1]]:
    return strategies.builds(
        getitem,
        strategies.permutations(sequence),
        slices(min_size=min_size, max_size=max(len(sequence), 1)),
    )


@strategies.composite
def slices(
    draw: Callable[[Strategy[int | None]], int | None],
    *,
    min_size: int = 0,
    max_size: int | None = None,
) -> slice:
    start = draw(
        strategies.none()
        | (
            strategies.integers(0)
            if max_size is None
            else strategies.integers(0, max_size - min_size)
        )
    )
    step = draw(
        strategies.none()
        | (
            strategies.integers(
                1, (max_size - (0 if start is None else start)) // min_size
            )
            if min_size and max_size is not None
            else strategies.integers(1)
        )
    )
    stop = draw(
        strategies.none()
        | strategies.integers(
            (0 if start is None else start)
            + min_size * (1 if step is None else step),
            max_size,
        )
    )
    return slice(start, stop, step)


def to_contour_vertices_orientation(
    vertices: Sequence[Point[ScalarT]], context: Context[ScalarT]
) -> Orientation:
    if len(vertices) < 3:
        return Orientation.COLLINEAR
    index = min(range(len(vertices)), key=vertices.__getitem__)
    return context.angle_orientation(
        vertices[index - 1],
        vertices[index],
        vertices[(index + 1) % len(vertices)],
    )


def to_pairs(strategy: Strategy[_T1]) -> Strategy[tuple[_T1, _T1]]:
    return strategies.tuples(strategy, strategy)


def to_perpendicular_point(point: Point[ScalarT]) -> Point[ScalarT]:
    return type(point)(-point.y, point.x)


def to_quadruplets(
    strategy: Strategy[_T1],
) -> Strategy[tuple[_T1, _T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy, strategy)


def to_triplets(strategy: Strategy[_T1]) -> Strategy[tuple[_T1, _T1, _T1]]:
    return strategies.tuples(strategy, strategy, strategy)


def permute_multipoint(
    multipoint: Multipoint[ScalarT], index: int
) -> Multipoint[ScalarT]:
    return type(multipoint)(permute(multipoint.points, index))


def rotate_contour(contour: Contour[ScalarT], offset: int) -> Contour[ScalarT]:
    return type(contour)(rotate_sequence(contour.vertices, offset))


def rotate_multipolygon(
    multipolygon: Multipolygon[ScalarT], offset: int
) -> Multipolygon[ScalarT]:
    return type(multipolygon)(rotate_sequence(multipolygon.polygons, offset))


def rotate_multisegment(
    multisegment: Multisegment[ScalarT], offset: int
) -> Multisegment[ScalarT]:
    return type(multisegment)(rotate_sequence(multisegment.segments, offset))


def rotate_polygon_border(
    polygon: Polygon[ScalarT], offset: int
) -> Polygon[ScalarT]:
    return type(polygon)(rotate_contour(polygon.border, offset), polygon.holes)


def rotate_polygon_holes(
    polygon: Polygon[ScalarT], offset: int
) -> Polygon[ScalarT]:
    return type(polygon)(
        polygon.border, rotate_sequence(polygon.holes, offset)
    )


_T = TypeVar('_T')


def cleave_in_tuples(
    *functions: Callable[..., Strategy[_T]],
) -> Callable[..., Strategy[tuple[_T, ...]]]:
    cleft = cleave(*functions)

    def to_tuples(*args: Any, **kwargs: Any) -> Strategy[tuple[_T, ...]]:
        return strategies.tuples(*cleft(*args, **kwargs))

    return to_tuples


def to_opposite_location(location: Location) -> Location:
    return Location(1 - (location - 1))
