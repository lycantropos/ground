from enum import (IntEnum,
                  unique)


@unique
class Kind(IntEnum):
    """
    Represents kinds of angles
    based on their degrees value in range ``[0, 180]``.
    """
    #: ``(90, 180]`` degrees
    OBTUSE = -1
    #: ``90`` degrees
    RIGHT = 0
    #: ``[0, 90)`` degrees
    ACUTE = 1


@unique
class Orientation(IntEnum):
    """
    Represents kinds of angle orientations.
    """
    #: in the same direction as a clock's hands
    CLOCKWISE = -1
    #: to the top and then to the bottom or vice versa
    COLLINEAR = 0
    #: opposite to clockwise
    COUNTERCLOCKWISE = 1
