from ._core import hints as _hints

Box = _hints.Box
Contour = _hints.Contour
Empty = _hints.Empty
Mix = _hints.Mix
Multipoint = _hints.Multipoint
Multipolygon = _hints.Multipolygon
Multisegment = _hints.Multisegment
Point = _hints.Point
Polygon = _hints.Polygon
Scalar = _hints.Scalar
Segment = _hints.Segment

assert Box.__module__ == __name__
assert Contour.__module__ == __name__
assert Empty.__module__ == __name__
assert Mix.__module__ == __name__
assert Multipoint.__module__ == __name__
assert Multipolygon.__module__ == __name__
assert Multisegment.__module__ == __name__
assert Point.__module__ == __name__
assert Polygon.__module__ == __name__
assert Scalar.__module__ == __name__
assert Segment.__module__ == __name__

Linear = _hints.Linear[_hints.ScalarT]
Shaped = _hints.Shaped[_hints.ScalarT]
