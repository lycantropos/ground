from hypothesis import given

from ground.base import Relation
from tests.utils import equivalence
from . import strategies

SYMMETRICAL_RELATIONS = (Relation.CROSS, Relation.DISJOINT, Relation.EQUAL,
                         Relation.OVERLAP, Relation.TOUCH)


@given(strategies.relations)
def test_basic(relation: Relation) -> None:
    result = relation.complement

    assert result in Relation


@given(strategies.relations)
def test_value(relation: Relation) -> None:
    result = relation.complement

    assert equivalence(result is relation, result in SYMMETRICAL_RELATIONS)
