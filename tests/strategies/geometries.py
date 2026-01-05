from collections.abc import Sequence
from operator import add, itemgetter
from typing import TypeVar

from hypothesis import strategies

from ground.base import Context, Orientation
from ground.hints import (
    Box,
    Contour,
    Multipoint,
    Multipolygon,
    Multisegment,
    Point,
    Polygon,
    Segment,
)
from tests.hints import (
    PointsPair,
    PointsQuadruplet,
    PointsTriplet,
    ScalarT,
    Strategy,
)
from tests.utils import (
    MAX_SEQUENCE_SIZE,
    cleave,
    compose,
    lift,
    pack,
    sub_lists,
    to_pairs,
)


def to_boxes(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Box[ScalarT]]:
    return (
        to_pairs(
            strategies.lists(
                coordinates, unique=True, min_size=2, max_size=2
            ).map(sorted)
        )
        .map(pack(add))
        .map(pack(context.box_cls))
    )


def to_points(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Point[ScalarT]]:
    return strategies.builds(context.point_cls, coordinates, coordinates)


def to_multipoints(
    context: Context[ScalarT],
    coordinates: Strategy[ScalarT],
    *,
    min_size: int = 1,
    max_size: int | None = None,
) -> Strategy[Multipoint[ScalarT]]:
    return strategies.builds(
        context.multipoint_cls,
        to_points_lists(
            context,
            coordinates,
            max_size=max_size,
            min_size=min_size,
            unique=True,
        ),
    )


def to_multipolygons(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Multipolygon[ScalarT]]:
    return to_polygons_sequences(context, coordinates).map(
        context.multipolygon_cls
    )


def to_multisegments(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Multisegment[ScalarT]]:
    return to_segments_sequences(context, coordinates).map(
        context.multisegment_cls
    )


def to_points_lists(
    context: Context[ScalarT],
    coordinates: Strategy[ScalarT],
    *,
    min_size: int = 0,
    max_size: int | None = None,
    unique: bool = False,
) -> Strategy[list[Point[ScalarT]]]:
    return strategies.lists(
        to_points(context, coordinates),
        min_size=min_size,
        max_size=max_size,
        unique=unique,
    )


def to_segments(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Segment[ScalarT]]:
    return to_segments_endpoints(context, coordinates).map(
        pack(context.segment_cls)
    )


def to_segments_endpoints(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[PointsPair[ScalarT]]:
    return strategies.lists(
        to_points(context, coordinates), unique=True, min_size=2, max_size=2
    ).map(ensure_pair)


def to_convex_contours(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Contour[ScalarT]]:
    return strategies.builds(
        context.contour_cls,
        to_vertices_sequences(context, coordinates, max_size=5),
    )


def to_non_degenerate_convex_hulls(
    context: Context[ScalarT],
    coordinates: Strategy[ScalarT],
    *,
    min_size: int = 3,
    max_size: int | None = None,
) -> Strategy[Sequence[Point[ScalarT]]]:
    def are_points_non_collinear(points_list: list[Point[ScalarT]]) -> bool:
        return any(
            context.angle_orientation(
                points_list[index - 2],
                points_list[index - 1],
                points_list[index],
            )
            is not Orientation.COLLINEAR
            for index in range(len(points_list))
        )

    return (
        to_points_lists(
            context, coordinates, min_size=min_size, max_size=max_size
        )
        .filter(are_points_non_collinear)
        .map(context.points_convex_hull)
    )


to_contours = to_convex_contours
to_vertices_sequences = to_non_degenerate_convex_hulls


def to_borders_and_holes_sequences(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[tuple[Contour[ScalarT], Sequence[Contour[ScalarT]]]]:
    def to_context_with_border_and_holes(
        vertices: Sequence[Point[ScalarT]],
    ) -> tuple[Contour[ScalarT], Sequence[Contour[ScalarT]]]:
        return context.contour_cls(vertices), []

    return to_vertices_sequences(context, coordinates).map(
        to_context_with_border_and_holes
    )


def to_polygons_sequences(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Sequence[Polygon[ScalarT]]]:
    return to_polygons(context, coordinates).map(lift)


def to_polygons(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Polygon[ScalarT]]:
    return strategies.builds(
        pack(context.polygon_cls),
        to_borders_and_holes_sequences(context, coordinates),
    )


def to_contours_sequences(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Sequence[Contour[ScalarT]]]:
    return to_contours(context, coordinates).map(lift)


def to_segments_sequences(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[Sequence[Segment[ScalarT]]]:
    def to_segments_sequence(
        convex_hull: Sequence[Point[ScalarT]], center_offset: int
    ) -> Sequence[Segment[ScalarT]]:
        center_offset %= len(convex_hull)
        center = convex_hull[center_offset]
        edges = [
            context.segment_cls(convex_hull[end_index - 1], end)
            for end_index, end in enumerate(convex_hull)
        ]
        radii = (
            [
                context.segment_cls(center, convex_hull[index])
                for index in range(
                    center_offset == len(convex_hull) - 1, center_offset - 1
                )
            ]
            + [
                context.segment_cls(center, convex_hull[index])
                for index in range(center_offset + 2, len(convex_hull))
            ]
            if center_offset
            else [
                context.segment_cls(center, convex_hull[index])
                for index in range(2, len(convex_hull) - 1)
            ]
        )
        assert not any(radius in edges for radius in radii)
        return edges + radii

    def to_contexts_with_segments_subsets(
        segments: Sequence[Segment[ScalarT]],
    ) -> Strategy[Sequence[Segment[ScalarT]]]:
        return sub_lists(segments, min_size=2)

    return (
        strategies.builds(
            to_segments_sequence,
            to_non_degenerate_convex_hulls(context, coordinates),
            strategies.integers(0),
        )
        .flatmap(to_contexts_with_segments_subsets)
        .map(itemgetter(slice(MAX_SEQUENCE_SIZE)))
    )


def to_touching_segments_pairs(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[tuple[Segment[ScalarT], Segment[ScalarT]]]:
    segment_factory = pack(context.segment_cls)
    return to_touching_segments_pairs_endpoints(context, coordinates).map(
        cleave(
            compose(segment_factory, itemgetter(0, 1)),
            compose(segment_factory, itemgetter(2, 3)),
        )
    )


def to_touching_segments_pairs_endpoints(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[PointsQuadruplet[ScalarT]]:
    return to_non_zero_angles(context, coordinates).map(itemgetter(0, 1, 0, 2))


def to_crossing_segments_pairs(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[tuple[Segment[ScalarT], Segment[ScalarT]]]:
    segment_factory = pack(context.segment_cls)
    return to_crossing_segments_pairs_endpoints(context, coordinates).map(
        cleave(
            compose(segment_factory, itemgetter(0, 1)),
            compose(segment_factory, itemgetter(2, 3)),
        )
    )


def to_crossing_segments_pairs_endpoints(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[PointsQuadruplet[ScalarT]]:
    def to_segments_pairs_endpoints(
        angle_points: PointsTriplet[ScalarT],
        first_scale: int,
        second_scale: int,
    ) -> PointsQuadruplet[ScalarT]:
        vertex, first_ray_point, second_ray_point = angle_points
        return (
            to_scaled_segment_end(first_ray_point, vertex, first_scale),
            first_ray_point,
            to_scaled_segment_end(second_ray_point, vertex, second_scale),
            second_ray_point,
        )

    def to_scaled_segment_end(
        start: Point[ScalarT], end: Point[ScalarT], scale: int
    ) -> Point[ScalarT]:
        return context.point_cls(
            end.x + scale * (end.x - start.x),
            end.y + scale * (end.y - start.y),
        )

    scales = strategies.integers(1, 100)
    return strategies.builds(
        to_segments_pairs_endpoints,
        to_non_zero_sine_angles(context, coordinates),
        scales,
        scales,
    )


def to_non_zero_angles(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[PointsTriplet[ScalarT]]:
    def is_non_zero_angle(angle_points: PointsTriplet[ScalarT]) -> bool:
        vertex, first_ray_point, second_ray_point = angle_points
        return second_ray_point < min(vertex, first_ray_point) or (
            context.angle_orientation(
                vertex, first_ray_point, second_ray_point
            )
            is not Orientation.COLLINEAR
        )

    return (
        to_points_lists(
            context, coordinates, min_size=3, max_size=3, unique=True
        )
        .map(ensure_triplet)
        .filter(is_non_zero_angle)
    )


_T = TypeVar('_T')


def ensure_pair(sequence: Sequence[_T], /) -> tuple[_T, _T]:
    first, second = sequence
    return first, second


def ensure_triplet(sequence: Sequence[_T], /) -> tuple[_T, _T, _T]:
    first, second, third = sequence
    return first, second, third


def to_non_zero_sine_angles(
    context: Context[ScalarT], coordinates: Strategy[ScalarT]
) -> Strategy[PointsTriplet[ScalarT]]:
    def is_non_zero_sine_angle(angle_points: PointsTriplet[ScalarT]) -> bool:
        vertex, first_ray_point, second_ray_point = angle_points
        return (
            context.angle_orientation(
                vertex, first_ray_point, second_ray_point
            )
            is not Orientation.COLLINEAR
        )

    return (
        to_points_lists(
            context, coordinates, min_size=3, max_size=3, unique=True
        )
        .map(ensure_triplet)
        .filter(is_non_zero_sine_angle)
    )
