from collections.abc import Sequence

from .hints import (
    Empty,
    Linear,
    Mix,
    Multipoint,
    Multisegment,
    Point,
    ScalarT,
    Segment,
    Shaped,
)


def pack_mix(
    discrete: Empty[ScalarT] | Multipoint[ScalarT],
    linear: Empty[ScalarT] | Linear[ScalarT],
    shaped: Empty[ScalarT] | Shaped[ScalarT],
    empty: Empty[ScalarT],
    mix_cls: type[Mix[ScalarT]],
    /,
) -> (
    Empty[ScalarT]
    | Linear[ScalarT]
    | Mix[ScalarT]
    | Multipoint[ScalarT]
    | Shaped[ScalarT]
):
    return (
        mix_cls(discrete, linear, shaped)
        if (
            (
                (discrete is not empty)
                + (linear is not empty)
                + (shaped is not empty)
            )
            >= 2
        )
        else (
            discrete
            if discrete is not empty
            else (linear if linear is not empty else shaped)
        )
    )


def pack_points(
    points: Sequence[Point[ScalarT]],
    empty: Empty[ScalarT],
    multipoint_cls: type[Multipoint[ScalarT]],
    /,
) -> Empty[ScalarT] | Multipoint[ScalarT]:
    return multipoint_cls(points) if points else empty


def pack_segments(
    segments: Sequence[Segment[ScalarT]],
    empty: Empty[ScalarT],
    multisegment_cls: type[Multisegment[ScalarT]],
    /,
) -> Empty[ScalarT] | Multisegment[ScalarT] | Segment[ScalarT]:
    return (
        (multisegment_cls(segments) if len(segments) > 1 else segments[0])
        if segments
        else empty
    )
