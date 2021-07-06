from shewchuk import incircle_test

from ground.core.enums import Location
from ground.core.hints import Point


def test(point: Point,
         first: Point,
         second: Point,
         third: Point) -> Location:
    return Location(1 + incircle_test(point.x, point.y, first.x, first.y,
                                      second.x, second.y, third.x, third.y))
