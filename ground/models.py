from typing import Type

from reprit.base import generate_repr as _generate_repr

from ground import hints as _hints


class Context:
    __slots__ = ('_contour_cls', '_coordinate_cls', '_multicontour_cls',
                 '_multipoint_cls', '_multipolygon_cls', '_multisegment_cls',
                 '_point_cls', '_polygon_cls', '_segment_cls')

    def __init__(self,
                 *,
                 contour_cls: Type[_hints.Contour],
                 coordinate_cls: Type[_hints.Coordinate],
                 multicontour_cls: Type[_hints.Multicontour],
                 multipoint_cls: Type[_hints.Multipoint],
                 multipolygon_cls: Type[_hints.Multipolygon],
                 multisegment_cls: Type[_hints.Multisegment],
                 point_cls: Type[_hints.Point],
                 polygon_cls: Type[_hints.Polygon],
                 segment_cls: Type[_hints.Segment]) -> None:
        self._contour_cls = contour_cls
        self._coordinate_cls = coordinate_cls
        self._multicontour_cls = multicontour_cls
        self._multipoint_cls = multipoint_cls
        self._multipolygon_cls = multipolygon_cls
        self._multisegment_cls = multisegment_cls
        self._point_cls = point_cls
        self._polygon_cls = polygon_cls
        self._segment_cls = segment_cls

    __repr__ = _generate_repr(__init__)

    @property
    def contour_cls(self) -> Type[_hints.Contour]:
        return self._contour_cls

    @property
    def coordinate_cls(self) -> Type[_hints.Coordinate]:
        return self._coordinate_cls

    @property
    def multicontour_cls(self) -> Type[_hints.Multicontour]:
        return self._multicontour_cls

    @property
    def multipoint_cls(self) -> Type[_hints.Multipoint]:
        return self._multipoint_cls

    @property
    def multipolygon_cls(self) -> Type[_hints.Multipolygon]:
        return self._multipolygon_cls

    @property
    def multisegment_cls(self) -> Type[_hints.Multisegment]:
        return self._multisegment_cls

    @property
    def point_cls(self) -> Type[_hints.Point]:
        return self._point_cls

    @property
    def polygon_cls(self) -> Type[_hints.Polygon]:
        return self._polygon_cls

    @property
    def segment_cls(self) -> Type[_hints.Segment]:
        return self._segment_cls
