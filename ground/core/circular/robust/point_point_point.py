from shewchuk import incircle_test

from ground.core.enums import Location
from ground.core.hints import Point


def test(first: Point,
         second: Point,
         third: Point,
         fourth: Point) -> Location:
    return Location(1 + incircle_test(first.x, first.y, second.x, second.y,
                                      third.x, third.y, fourth.x, fourth.y))
