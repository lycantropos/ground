from enum import (IntEnum,
                  unique)


class Base(IntEnum):
    def __repr__(self) -> str:
        return type(self).__qualname__ + '.' + self.name


@unique
class Kind(Base):
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
class Location(Base):
    """
    Represents kinds of locations in which point can be relative to geometry.
    """
    #: point lies in the exterior of the geometry
    EXTERIOR = 0
    #: point lies on the boundary of the geometry
    BOUNDARY = 1
    #: point lies in the interior of the geometry
    INTERIOR = 2


@unique
class Orientation(Base):
    """
    Represents kinds of angle orientations.
    """
    #: in the same direction as a clock's hands
    CLOCKWISE = -1
    #: to the top and then to the bottom or vice versa
    COLLINEAR = 0
    #: opposite to clockwise
    COUNTERCLOCKWISE = 1


@unique
class Relation(Base):
    """
    Represents kinds of relations in which geometries can be.
    Order of members assumes that conditions for previous ones do not hold.
    """
    #: intersection is empty
    DISJOINT = 0
    #: intersection is a strict subset of each of the geometries,
    #: has dimension less than at least of one of the geometries
    #: and if we traverse boundary of each of the geometries in any direction
    #: then boundary of the other geometry won't be on one of sides
    #: at each point of boundaries intersection
    TOUCH = 1
    #: intersection is a strict subset of each of the geometries,
    #: has dimension less than at least of one of the geometries
    #: and if we traverse boundary of each of the geometries in any direction
    #: then boundary of the other geometry will be on both sides
    #: at some point of boundaries intersection
    CROSS = 2
    #: intersection is a strict subset of each of the geometries
    #: and has the same dimension as geometries
    OVERLAP = 3
    #: interior of the geometry is a superset of the other
    COVER = 4
    #: boundary of the geometry contains
    #: at least one boundary point of the other, but not all,
    #: interior of the geometry contains other points of the other
    ENCLOSES = 5
    #: geometry is a strict superset of the other
    #: and interior/boundary of the geometry is a superset
    #: of interior/boundary of the other
    COMPOSITE = 6
    #: geometries are equal
    EQUAL = 7
    #: geometry is a strict subset of the other
    #: and interior/boundary of the geometry is a subset
    #: of interior/boundary of the other
    COMPONENT = 8
    #: at least one boundary point of the geometry
    #: lies on the boundary of the other, but not all,
    #: other points of the geometry lie in the interior of the other
    ENCLOSED = 9
    #: geometry is a subset of the interior of the other
    WITHIN = 10

    @property
    def complement(self) -> 'Relation':
        if self is Relation.COVER:
            return Relation.WITHIN
        elif self is Relation.ENCLOSES:
            return Relation.ENCLOSED
        elif self is Relation.COMPOSITE:
            return Relation.COMPONENT
        elif self is Relation.COMPONENT:
            return Relation.COMPOSITE
        elif self is Relation.ENCLOSED:
            return Relation.ENCLOSES
        elif self is Relation.WITHIN:
            return Relation.COVER
        else:
            return self
