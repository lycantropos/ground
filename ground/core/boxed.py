from collections.abc import Iterable

from .hints import Box, Contour, Point, Polygon, ScalarT, Segment


def from_contour(
    contour: Contour[ScalarT], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    return from_points(contour.vertices, box_cls)


def from_contours(
    contours: Iterable[Contour[ScalarT]], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    iterator = iter(contours)
    contour = next(iterator)
    min_x, max_x, min_y, max_y = _from_points(contour.vertices)
    for contour in iterator:
        (contour_min_x, contour_max_x, contour_min_y, contour_max_y) = (
            _from_points(contour.vertices)
        )
        if max_x < contour_max_x:
            max_x = contour_max_x
        if contour_min_x < min_x:
            min_x = contour_min_x
        if max_y < contour_max_y:
            max_y = contour_max_y
        if contour_min_y < min_y:
            min_y = contour_min_y
    return box_cls(min_x, max_x, min_y, max_y)


def from_points(
    points: Iterable[Point[ScalarT]], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    return box_cls(*_from_points(points))


def from_polygon(
    polygon: Polygon[ScalarT], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    return from_points(polygon.border.vertices, box_cls)


def from_polygons(
    polygons: Iterable[Polygon[ScalarT]], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    return from_contours((polygon.border for polygon in polygons), box_cls)


def from_segment(
    segment: Segment[ScalarT], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    return box_cls(*_from_segment(segment))


def from_segments(
    segments: Iterable[Segment[ScalarT]], box_cls: type[Box[ScalarT]], /
) -> Box[ScalarT]:
    iterator = iter(segments)
    segment = next(iterator)
    min_x, max_x, min_y, max_y = _from_segment(segment)
    for segment in iterator:
        (segment_min_x, segment_max_x, segment_min_y, segment_max_y) = (
            _from_segment(segment)
        )
        if max_x < segment_max_x:
            max_x = segment_max_x
        if segment_min_x < min_x:
            min_x = segment_min_x
        if max_y < segment_max_y:
            max_y = segment_max_y
        if segment_min_y < min_y:
            min_y = segment_min_y
    return box_cls(min_x, max_x, min_y, max_y)


def _from_points(
    points: Iterable[Point[ScalarT]], /
) -> tuple[ScalarT, ScalarT, ScalarT, ScalarT]:
    iterator = iter(points)
    point = next(iterator)
    max_x = min_x = point.x
    max_y = min_y = point.y
    for point in iterator:
        if max_x < point.x:
            max_x = point.x
        elif point.x < min_x:
            min_x = point.x
        if max_y < point.y:
            max_y = point.y
        elif point.y < min_y:
            min_y = point.y
    return min_x, max_x, min_y, max_y


def _from_segment(
    segment: Segment[ScalarT], /
) -> tuple[ScalarT, ScalarT, ScalarT, ScalarT]:
    start, end = segment.start, segment.end
    max_x, min_x = (end.x, start.x) if start.x < end.x else (start.x, end.x)
    max_y, min_y = (end.y, start.y) if start.y < end.y else (start.y, end.y)
    return min_x, max_x, min_y, max_y
