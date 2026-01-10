from ground._core.hints import Contour, ScalarFactory, ScalarT


def signed_area(
    contour: Contour[ScalarT], coordinate_factory: ScalarFactory[ScalarT], /
) -> ScalarT:
    vertices = contour.vertices
    result, vertex = coordinate_factory(0), vertices[-1]
    for next_vertex in vertices:
        result += vertex.x * next_vertex.y - next_vertex.x * vertex.y
        vertex = next_vertex
    return result / coordinate_factory(2)
