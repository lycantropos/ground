from contextvars import ContextVar
from typing import (List,
                    NamedTuple,
                    Type)

from reprit.base import generate_repr as _generate_repr

from . import hints as _hints


class Context:
    __slots__ = ('_point_cls', '_multipoint_cls', '_segment_cls',
                 '_multisegment_cls', '_contour_cls', '_polygon_cls',
                 '_multipolygon_cls')

    def __init__(self,
                 *,
                 point_cls: Type[_hints.Point],
                 multipoint_cls: Type[_hints.Multipoint],
                 segment_cls: Type[_hints.Segment],
                 multisegment_cls: Type[_hints.Multisegment],
                 contour_cls: Type[_hints.Contour],
                 polygon_cls: Type[_hints.Polygon],
                 multipolygon_cls: Type[_hints.Multipolygon]) -> None:
        self._point_cls = point_cls
        self._multipoint_cls = multipoint_cls
        self._segment_cls = segment_cls
        self._contour_cls = contour_cls
        self._multisegment_cls = multisegment_cls
        self._polygon_cls = polygon_cls
        self._multipolygon_cls = multipolygon_cls

    __repr__ = _generate_repr(__init__)

    @property
    def contour_cls(self) -> Type[_hints.Contour]:
        return self._contour_cls

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


_context = ContextVar(
        'context',
        default=Context(
                point_cls=NamedTuple('Point', [('x', _hints.Coordinate),
                                               ('y', _hints.Coordinate)]),
                multipoint_cls=NamedTuple('Multipoint',
                                          [('points', List[_hints.Point])]),
                segment_cls=NamedTuple('Segment', [('start', _hints.Point),
                                                   ('end', _hints.Point)]),
                multisegment_cls=NamedTuple('Multisegment',
                                            [('segments',
                                              List[_hints.Segment])]),
                contour_cls=NamedTuple('Contour',
                                       [('vertices', List[_hints.Point])]),
                polygon_cls=NamedTuple('Polygon',
                                       [('border', _hints.Contour),
                                        ('holes', List[_hints.Contour])]),
                multipolygon_cls=NamedTuple('Multipolygon',
                                            [('polygons',
                                              List[_hints.Polygon])])))


def get_context() -> Context:
    return _context.get()


def set_context(context: Context) -> None:
    _context.set(context)


def to_contour_cls() -> Type[_hints.Contour]:
    return get_context().contour_cls


def to_multipoint_cls() -> Type[_hints.Multipoint]:
    return get_context().multipoint_cls


def to_multipolygon_cls() -> Type[_hints.Multipolygon]:
    return get_context().multipolygon_cls


def to_multisegment_cls() -> Type[_hints.Multisegment]:
    return get_context().multisegment_cls


def to_point_cls() -> Type[_hints.Point]:
    return get_context().point_cls


def to_polygon_cls() -> Type[_hints.Polygon]:
    return get_context().polygon_cls


def to_segment_cls() -> Type[_hints.Segment]:
    return get_context().segment_cls
