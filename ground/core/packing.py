from typing import (Sequence,
                    Type,
                    Union)

from .hints import (Empty,
                    Linear,
                    Maybe,
                    Mix,
                    Multipoint,
                    Multisegment,
                    Point,
                    Segment,
                    Shaped)


def pack_mix(discrete: Maybe[Multipoint],
             linear: Maybe[Linear],
             shaped: Maybe[Shaped],
             empty: Empty,
             mix_cls: Type[Mix]
             ) -> Union[Empty, Linear, Mix, Multipoint, Shaped]:
    return (mix_cls(discrete, linear, shaped)
            if (((discrete is not empty) + (linear is not empty)
                 + (shaped is not empty)) >= 2)
            else (discrete
                  if discrete is not empty
                  else (linear
                        if linear is not empty
                        else shaped)))


def pack_points(points: Sequence[Point],
                empty: Empty,
                multipoint_cls: Type[Multipoint]) -> Maybe[Multipoint]:
    return multipoint_cls(points) if points else empty


def pack_segments(segments: Sequence[Segment],
                  empty: Empty,
                  multisegment_cls: Type[Multisegment]
                  ) -> Union[Empty, Multisegment, Segment]:
    return ((multisegment_cls(segments)
             if len(segments) > 1
             else segments[0])
            if segments
            else empty)
