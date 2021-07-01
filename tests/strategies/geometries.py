from operator import (add,
                      itemgetter)
from typing import (List,
                    Optional,
                    Sequence,
                    Tuple)

from hypothesis import strategies

from ground.base import (Context,
                         Orientation)
from ground.hints import (Box,
                          Contour,
                          Multipoint,
                          Multipolygon,
                          Multisegment,
                          Point,
                          Polygon,
                          Scalar,
                          Segment)
from tests.hints import (PointsPair,
                         PointsQuadruplet,
                         PointsTriplet,
                         Strategy)
from tests.utils import (MAX_SEQUENCE_SIZE,
                         cleave,
                         compose,
                         lift,
                         pack,
                         sub_lists,
                         to_pairs)


def to_boxes(context: Context,
             coordinates: Strategy[Scalar]) -> Strategy[Box]:
    return (to_pairs(strategies.lists(coordinates,
                                      unique=True,
                                      min_size=2,
                                      max_size=2)
                     .map(sorted))
            .map(pack(add))
            .map(pack(context.box_cls)))


def to_points(context: Context,
              coordinates: Strategy[Scalar]) -> Strategy[Point]:
    return strategies.builds(context.point_cls, coordinates, coordinates)


def to_multipoints(context: Context,
                   coordinates: Strategy[Scalar],
                   *,
                   min_size: int = 1,
                   max_size: Optional[int] = None) -> Strategy[Multipoint]:
    return strategies.builds(context.multipoint_cls,
                             to_points_lists(context, coordinates,
                                             max_size=max_size,
                                             min_size=min_size,
                                             unique=True))


def to_multipolygons(context: Context,
                     coordinates: Strategy[Scalar]) -> Strategy[Multipolygon]:
    return (to_polygons_sequences(context, coordinates)
            .map(context.multipolygon_cls))


def to_multisegments(context: Context,
                     coordinates: Strategy[Scalar]) -> Strategy[Multisegment]:
    return (to_segments_sequences(context, coordinates)
            .map(context.multisegment_cls))


def to_points_lists(context: Context,
                    coordinates: Strategy[Scalar],
                    *,
                    min_size: int = 0,
                    max_size: Optional[int] = None,
                    unique: bool = False) -> Strategy[List[Point]]:
    return strategies.lists(to_points(context, coordinates),
                            min_size=min_size,
                            max_size=max_size,
                            unique=unique)


def to_segments(context: Context,
                coordinates: Strategy[Scalar]) -> Strategy[Segment]:
    return (to_segments_endpoints(context, coordinates)
            .map(pack(context.segment_cls)))


def to_segments_endpoints(context: Context,
                          coordinates: Strategy[Scalar]
                          ) -> Strategy[PointsPair]:
    return (strategies.lists(to_points(context, coordinates),
                             unique=True,
                             min_size=2,
                             max_size=2)
            .map(tuple))


def to_convex_contours(context: Context,
                       coordinates: Strategy[Scalar]) -> Strategy[Contour]:
    return strategies.builds(context.contour_cls,
                             to_vertices_sequences(context, coordinates,
                                                   max_size=5))


def to_non_degenerate_convex_hulls(context: Context,
                                   coordinates: Strategy[Scalar],
                                   *,
                                   min_size: int = 3,
                                   max_size: Optional[int] = None
                                   ) -> Strategy[Sequence[Point]]:
    def are_points_non_collinear(points_list: List[Point]) -> bool:
        return any(context.angle_orientation(points_list[index - 2],
                                             points_list[index - 1],
                                             points_list[index])
                   is not Orientation.COLLINEAR
                   for index in range(len(points_list)))

    return (to_points_lists(context, coordinates,
                            min_size=min_size,
                            max_size=max_size)
            .filter(are_points_non_collinear)
            .map(context.points_convex_hull))


to_contours = to_convex_contours
to_vertices_sequences = to_non_degenerate_convex_hulls


def to_borders_and_holes_sequences(context: Context,
                                   coordinates: Strategy[Scalar]
                                   ) -> Strategy[Tuple[Contour,
                                                       Sequence[Contour]]]:
    def to_context_with_border_and_holes(vertices: Sequence[Point]
                                         ) -> Tuple[Contour,
                                                    Sequence[Contour]]:
        return context.contour_cls(vertices), []

    return (to_vertices_sequences(context, coordinates)
            .map(to_context_with_border_and_holes))


def to_polygons_sequences(context: Context,
                          coordinates: Strategy[Scalar]
                          ) -> Strategy[Sequence[Polygon]]:
    return to_polygons(context, coordinates).map(lift)


def to_polygons(context, coordinates):
    return strategies.builds(pack(context.polygon_cls),
                             to_borders_and_holes_sequences(context,
                                                            coordinates))


def to_contours_sequences(context: Context,
                          coordinates: Strategy[Scalar]
                          ) -> Strategy[Sequence[Contour]]:
    return to_contours(context, coordinates).map(lift)


def to_segments_sequences(context: Context,
                          coordinates: Strategy[Scalar]
                          ) -> Strategy[Sequence[Segment]]:
    def to_segments_sequence(convex_hull: Sequence[Point],
                             center_offset: int) -> Sequence[Segment]:
        center_offset %= len(convex_hull)
        center = convex_hull[center_offset]
        edges = [context.segment_cls(convex_hull[end_index - 1], end)
                 for end_index, end in enumerate(convex_hull)]
        radii = ([context.segment_cls(center, convex_hull[index])
                  for index in range(center_offset == len(convex_hull) - 1,
                                     center_offset - 1)]
                 + [context.segment_cls(center, convex_hull[index])
                    for index in range(center_offset + 2,
                                       len(convex_hull))]
                 if center_offset
                 else
                 [context.segment_cls(center, convex_hull[index])
                  for index in range(2, len(convex_hull) - 1)])
        assert not any(radius in edges for radius in radii)
        return edges + radii

    def to_contexts_with_segments_subsets(segments: Sequence[Segment]
                                          ) -> Strategy[Sequence[Segment]]:
        return sub_lists(segments,
                         min_size=2)

    return (strategies.builds(to_segments_sequence,
                              to_non_degenerate_convex_hulls(context,
                                                             coordinates),
                              strategies.integers(0))
            .flatmap(to_contexts_with_segments_subsets)
            .map(itemgetter(slice(MAX_SEQUENCE_SIZE))))


def to_touching_segments_pairs(context: Context,
                               coordinates: Strategy[Scalar]
                               ) -> Strategy[Tuple[Segment, Segment]]:
    segment_factory = pack(context.segment_cls)
    return (to_touching_segments_pairs_endpoints(context, coordinates)
            .map(cleave(compose(segment_factory, itemgetter(0, 1)),
                        compose(segment_factory, itemgetter(2, 3)))))


def to_touching_segments_pairs_endpoints(context: Context,
                                         coordinates: Strategy[Scalar]
                                         ) -> Strategy[PointsQuadruplet]:
    return (to_non_zero_angles(context, coordinates)
            .map(itemgetter(0, 1, 0, 2)))


def to_crossing_segments_pairs(context: Context,
                               coordinates: Strategy[Scalar]
                               ) -> Strategy[Tuple[Segment, Segment]]:
    segment_factory = pack(context.segment_cls)
    return (to_crossing_segments_pairs_endpoints(context, coordinates)
            .map(cleave(compose(segment_factory, itemgetter(0, 1)),
                        compose(segment_factory, itemgetter(2, 3)))))


def to_crossing_segments_pairs_endpoints(context: Context,
                                         coordinates: Strategy[Scalar]
                                         ) -> Strategy[PointsQuadruplet]:
    def to_segments_pairs_endpoints(
            angle_points: PointsTriplet,
            first_scale: int,
            second_scale: int) -> PointsQuadruplet:
        vertex, first_ray_point, second_ray_point = angle_points
        return (to_scaled_segment_end(first_ray_point, vertex, first_scale),
                first_ray_point,
                to_scaled_segment_end(second_ray_point, vertex, second_scale),
                second_ray_point)

    def to_scaled_segment_end(start: Point,
                              end: Point,
                              scale: int) -> Point:
        return context.point_cls(end.x + scale * (end.x - start.x),
                                 end.y + scale * (end.y - start.y))

    scales = strategies.integers(1, 100)
    return strategies.builds(to_segments_pairs_endpoints,
                             to_non_zero_sine_angles(context, coordinates),
                             scales, scales)


def to_non_zero_angles(context: Context,
                       coordinates: Strategy[Scalar]
                       ) -> Strategy[PointsTriplet]:
    def is_non_zero_angle(angle_points: PointsTriplet) -> bool:
        vertex, first_ray_point, second_ray_point = angle_points
        return (second_ray_point < min(vertex, first_ray_point)
                or (context.angle_orientation(vertex, first_ray_point,
                                              second_ray_point)
                    is not Orientation.COLLINEAR))

    return (to_points_lists(context, coordinates,
                            min_size=3,
                            max_size=3,
                            unique=True)
            .map(tuple)
            .filter(is_non_zero_angle))


def to_non_zero_sine_angles(context: Context,
                            coordinates: Strategy[Scalar]
                            ) -> Strategy[PointsTriplet]:
    def is_non_zero_sine_angle(angle_points: PointsTriplet) -> bool:
        vertex, first_ray_point, second_ray_point = angle_points
        return (context.angle_orientation(vertex, first_ray_point,
                                          second_ray_point)
                is not Orientation.COLLINEAR)

    return (to_points_lists(context, coordinates,
                            min_size=3,
                            max_size=3,
                            unique=True)
            .map(tuple)
            .filter(is_non_zero_sine_angle))
