from typing import Type

from .hints import Box


def merge(first_box: Box, second_box: Box, box_cls: Type[Box]) -> Box:
    return box_cls(min(first_box.min_x, second_box.min_x),
                   max(first_box.max_x, second_box.max_x),
                   min(first_box.min_y, second_box.min_y),
                   max(first_box.max_y, second_box.max_y))
